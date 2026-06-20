import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from data.flags import flag_html

#@st.cache_data(ttl=600)
def fetch_2026_matches():
    url = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
    response = requests.get(url)
    data = response.json()
    matches = []
    for match in data["matches"]:
        has_score = "score" in match
        matches.append({
            "round":       match["round"],
            "date":        pd.to_datetime(match["date"]),
            "home_team":   match["team1"],
            "away_team":   match["team2"],
            "group":       match.get("group", None),
            "ground":      match.get("ground", "TBD"),
            "home_goals":  match["score"]["ft"][0] if has_score else np.zeros,
            "away_goals":  match["score"]["ft"][1] if has_score else np.zeros,
            "played":      has_score,
        })

    df = pd.DataFrame(matches)

    df = df[df['group'].notna()].reset_index(drop=True)
 
    return df
    
def compute_standings(df):
    played = df[df['played']].copy()
    teams = {}

    for _, row in played.iterrows():
        home      = row["home_team"]
        away      = row["away_team"]
        home_gf   = row["home_goals"]
        away_gf   = row["away_goals"]
        for team, scored, conceded in [
            (home, home_gf, away_gf),
            (away, away_gf, home_gf)
        ]:
            if team not in teams:
                teams[team]= {
                    'Team' : team, 'GP': 0, 'W': 0,
                    'D': 0, 'L': 0, 'GF': 0, 'GA': 0,
                    'GD': 0, 'Pts': 0
                }
            
            t = teams[team]
            t['GP'] += 1
            t["GF"] += scored
            t["GA"] += conceded
            t["GD"] += scored - conceded

            if scored > conceded:
                t['W'] += 1; t['Pts'] += 3
            elif scored == conceded:
                t['D'] +=1; t['Pts'] += 1
            else:
                t['L'] +=1
    
    standings = pd.DataFrame(list(teams.values()))
    if standings.empty:
        return standings
    standings = standings.sort_values(['Pts', 'GD', 'GF'], ascending= False).reset_index(drop= True)
    standings.index += 1

    return standings

def show_dashboard():
    st.title("⚽ FIFA World Cup 2026 — Live Dashboard")
    st.caption("Data updated hourly from OpenFootball")
    df = fetch_2026_matches()

    played_df = df[df['played']].copy()
    upcoming_df = df[~df['played']].copy()

    st.subheader('📈 Tournament Overview')
    col1, col2, col3, col4 = st.columns(4)

    total_goals = int(played_df['home_goals'].sum() + played_df['away_goals'].sum()) if not played_df.empty else 0
    avg_goals = round(total_goals / len(played_df), 2) if not played_df.empty else 0

    col1.metric('Matches Played', len(played_df))
    col2.metric('Matches Remaining', len(upcoming_df))
    col3.metric('Total Goals', total_goals)
    col4.metric('Avg Goals/Match', avg_goals)

    st.divider()

    tab1, tab2, tab3 = st.tabs(["🏆 Standings", "📅 Results", "📊 Stats"])

    with tab1:
        st.subheader('Group Standings')

        if played_df.empty:
            st.info('No matches played yet.')
        else:
            groups = sorted(df['group'].unique())
            
            selected_group = st.selectbox('Select a Group', groups)

            group_df = df[df['group'] == selected_group]

            standings = compute_standings(group_df)

            if standings.empty:
                st.info('No matches played yet in this group')

            else:
                standings['Club'] = standings["Team"].apply(
                    lambda t: f'{flag_html(t)}{t}'
                )
                st.markdown(
                    standings[["Club","GP","W","D","L","GF","GA","GD","Pts"]].to_html(escape=False, index=  True),
                    unsafe_allow_html= True
                )

    with tab2:
        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("✅ Results")
            if played_df.empty:
                st.info('No results yet.')
            else:
                for _, row in played_df.sort_values('date', ascending= False).iterrows():
                    st.markdown(
                        f'**{row['home_team']}** {int(row['home_goals'])} - '
                        f'{int(row['away_goals'])} **{row['away_team']}** '
                        f' \n {row['group']} · {row['date'].strftime('%b %d')}' 
                    )
                    st.divider()

        with col_b:
            st.subheader('📅 Upcoming Fixtures')
            if upcoming_df.empty:
                st.info('No upcoming fixtures.')
            else:
                for _, row in upcoming_df.sort_values('date').head(10).iterrows():
                    st.markdown(
                        f'**{row['home_team']}** vs **{row['away_team']}** '
                        f' \n {row['group']} · {row['date'].strftime('%b %d')} · {row['ground']}'
                    )
                    st.divider()

    with tab3:
        if played_df.empty:
            st.info('No stats available yet.')
        else:
            st.subheader('🥅 Goals Scored per Team')
            home_goals = played_df.groupby('home_team')['home_goals'].sum()
            away_goals = played_df.groupby('away_team')['away_goals'].sum()
            total_by_team = (home_goals.add(away_goals, fill_value=0)
                             .sort_values(ascending= True)
                             .reset_index())
            total_by_team.columns = ['Team', 'Goals']

            fig1 = px.bar(
                total_by_team, x= 'Team', y = 'Goals',
                color = 'Goals', color_continuous_scale='Viridis',
                title= 'Total Goals Scored'
            )

            st.plotly_chart(fig1, width='stretch')

            st.subheader('📈 Goals per Match Over Time')
            played_df['total_goals'] = played_df['home_goals'] + played_df['away_goals']

            fig2 = px.line(
                played_df.groupby('date')['total_goals'].sum().reset_index(),
                x= 'date', y= 'total_goals',
                markers= True,
                labels= {'date': 'Date', 'total_goals': 'Total Goals'},
                title = 'Goals per Match Timeline'
            )

            st.plotly_chart(fig2, width= 'stretch')
