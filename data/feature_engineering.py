import pandas as pd
from fetch_data import load_all_matches

def compute_team_stats(df):

    df = df.sort_values('date').reset_index(drop = True)

    team_history = {}

    home_avg_scored    = []
    home_avg_conceded  = []
    home_win_rate      = []
    away_avg_scored    = []
    away_avg_conceded  = []
    away_win_rate      = []

    for _, row in df.iterrows():
        home = row['home_team']
        away = row['away_team']

        home_stats = team_history.get(home, {'scored': [], 'conceded': [], 'wins' : []})
        home_avg_scored.append(
            round(sum(home_stats['scored']) / len(home_stats['scored']), 2)
            if home_stats['scored'] else 0.0
        )
        
        home_avg_conceded.append(
            round(sum(home_stats['conceded']) / len(home_stats['conceded']), 2)
            if home_stats['conceded'] else 0.0
        )

        home_win_rate.append(
            round(sum(home_stats["wins"]) / len(home_stats["wins"]), 2)
            if home_stats["wins"] else 0.0
        )

        away_stats = team_history.get(away, {'scored' : [], 'conceded': [], 'wins': []})

        away_avg_scored.append(
            round(sum(away_stats["scored"]) / len(away_stats["scored"]), 2)
            if away_stats["scored"] else 0.0
        )
        away_avg_conceded.append(
            round(sum(away_stats["conceded"]) / len(away_stats["conceded"]), 2)
            if away_stats["conceded"] else 0.0
        )
        away_win_rate.append(
            round(sum(away_stats["wins"]) / len(away_stats["wins"]), 2)
            if away_stats["wins"] else 0.0
        )

        if home not in team_history:
            team_history[home] = {'scored' : [], 'conceded': [], 'wins': []}
        team_history[home]['scored'].append(row['home_goals'])
        team_history[home]['conceded'].append(row['away_goals'])
        team_history[home]['wins'].append(1 if row['goal_diff'] > 0 else 0)

        if away not in team_history:
            team_history[away] = {'scored' : [], 'conceded': [], 'wins': []}
        team_history[away]['scored'].append(row['away_goals'])
        team_history[away]['conceded'].append(row['home_goals'])
        team_history[away]['wins'].append(1 if row['goal_diff'] < 0 else 0)

    df["home_avg_scored"]   = home_avg_scored
    df["home_avg_conceded"] = home_avg_conceded
    df["home_win_rate"]     = home_win_rate
    df["away_avg_scored"]   = away_avg_scored
    df["away_avg_conceded"] = away_avg_conceded
    df["away_win_rate"]     = away_win_rate
    
    return df

if __name__ == '__main__':
    
    df = load_all_matches()
    df = compute_team_stats(df)
    
    print('\n -- Shape --')
    print('\n -- First 5 Rows --')

    print(df[["home_team", "away_team", "home_avg_scored",
              "away_avg_scored", "home_win_rate", "away_win_rate",
              "goal_diff"]].head())
    
    print('\n -- Feature Stats --')
    print(df[["home_avg_scored", "home_avg_conceded",
              "home_win_rate", "away_avg_scored",
              "away_avg_conceded", "away_win_rate"]].describe())
