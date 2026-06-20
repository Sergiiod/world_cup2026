import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import sys
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

from data.fetch_data import load_all_matches
from data.feature_engineering import compute_team_stats

@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'best_model.pkl')
    with open(model_path, 'rb') as f:
        return pickle.load(f)
    

@st.cache_data
def get_2026_teams():
    url = 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json'
    data = requests.get(url).json()

    teams = set()
    for match in data['matches']:
        t1 = match['team1']
        t2 = match['team2']

        if not t1[0].isdigit() and not t1[-1].isdigit():            
            teams.add(t1)
        if not t2[0].isdigit() and not t2[-1].isdigit():   
            teams.add(t2)

    return sorted(list(teams))

@st.cache_data
def get_team_stats():
    df = load_all_matches()

    home_df = pd.DataFrame({
        "team":     df["home_team"].values,
        "scored":   df["home_goals"].values,
        "conceded": df["away_goals"].values,
    })

    away_df = pd.DataFrame({
        "team":     df["away_team"].values,
        "scored":   df["away_goals"].values,
        "conceded": df["home_goals"].values,
    })

    all_df = pd.concat([home_df, away_df], ignore_index=True)

    all_df["scored"]   = pd.to_numeric(all_df["scored"],   errors="coerce")
    all_df["conceded"] = pd.to_numeric(all_df["conceded"], errors="coerce")

    all_df["win"] = (all_df["scored"] > all_df["conceded"]).astype(int)

    team_test = all_df[all_df['team'] == 'Colombia']
    print(len(team_test))

    stats = all_df.groupby("team").agg(
        avg_scored   = ("scored",   "mean"),
        avg_conceded = ("conceded", "mean"),
        win_rate     = ("win",      "mean"),
    ).round(2)


    return stats.to_dict(orient="index")

def get_features_for_team(team, team_stats):
    if team in team_stats:
        return team_stats[team]
    else:
        all_vals = list(team_stats.values())
        return {
            "avg_scored":   round(pd.Series([t["avg_scored"]   for t in all_vals]).mean(), 2),
            "avg_conceded": round(pd.Series([t["avg_conceded"] for t in all_vals]).mean(), 2),
            "win_rate":     round(pd.Series([t["win_rate"]     for t in all_vals]).mean(), 2),
        }
    

def interpret_result(home_team, away_team, goal_diff):
    if goal_diff > 0.5:
        winner = home_team
        margin = round(abs(goal_diff))
        return f'🏆 **{winner}** wins!', f'by ~ {margin} goal(s)', 'success!'
    elif goal_diff < -0.5:
        winner = away_team
        margin = round(abs(goal_diff))
        return f'🏆 **{winner}** wins!', f'by ~ {margin} goal(s)', 'success!'
    else:
        return f'🤝 **Draw**', 'Very close match predicted!', 'info'

def show_predictor():
    st.title('🤖 Match Result Predcitor')
    st.caption('Predictions based on historical World Cup Data')

    model = load_model()
    teams = get_2026_teams()
    team_stats = get_team_stats()

    st.divider()

    st.subheader('🏟️ Select Teams')
    col1, col_vs, col2 = st.columns(3)

    with col1:
        home_team = st.selectbox('🏠 Home Team', teams, index=teams.index('Brazil') if 'Brazil' in teams else 0)

    with col_vs:
        st.markdown('<br><br>**VS**', unsafe_allow_html= True)

    with col2:
        away_options = [t for t in teams if t != home_team]
        away_team = st.selectbox('✈️ Away Team', away_options, index=away_options.index('Argentina') if 'Argentina' in away_options else 0)

    st.subheader('📊 Team Statistics (Historical)') 
    home_s = get_features_for_team(home_team, team_stats)
    away_s = get_features_for_team(away_team, team_stats)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f'**{home_team}**')
        st.metric('Avg Goals Scored', home_s['avg_scored'])
        st.metric('Avg Goals Conceded', home_s['avg_conceded'])
        st.metric('Win Rate', f'{round(home_s['win_rate']*100)}%')

    with col_b:
        st.markdown(f'**{away_team}**')
        st.metric('Avg Goals Scored', away_s['avg_scored'])
        st.metric('Avg Goals Conceded', away_s['avg_conceded'])
        st.metric('Win Rate', f'{round(away_s['win_rate']*100)}%')

    st.divider()

    if st.button("⚡ Predict Match Result", use_container_width=True):

        features = pd.DataFrame([{
            'home_avg_scored':   home_s['avg_scored'],
            'home_avg_conceded': home_s['avg_conceded'],
            'home_win_rate':     home_s['win_rate'],
            'away_avg_scored':   away_s['avg_scored'],
            'away_avg_conceded': away_s['avg_conceded'],
            'away_win_rate':     away_s['win_rate'],
            'score_diff':        home_s['avg_scored'] - away_s['avg_scored'],
            'concede_diff':      home_s['avg_conceded'] - away_s['avg_conceded'],
            'winrate_diff':      home_s['win_rate'] - away_s['win_rate']
        }])

        goal_diff = model.predict(features)[0]

        label, detail, style = interpret_result(home_team, away_team, goal_diff)

        st.subheader('🎯 Prediction')
        if style == 'Success':
            st.success(f'{label} - {detail}') 
        else:
            st.info(f'{label} - {detail}')

        st.caption(f'Predicted Goal Difference: {goal_diff:.2f} (positive = {home_team} advantage)')