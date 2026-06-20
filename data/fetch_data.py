import requests
import pandas as pd

BASE = "https://raw.githubusercontent.com/openfootball/worldcup.json/master"

URLS = {
    "1930": f"{BASE}/1930/worldcup.json",
    "1934": f"{BASE}/1934/worldcup.json",
    "1938": f"{BASE}/1938/worldcup.json",
    "1950": f"{BASE}/1950/worldcup.json",
    "1954": f"{BASE}/1954/worldcup.json",
    "1958": f"{BASE}/1958/worldcup.json",
    "1962": f"{BASE}/1962/worldcup.json",
    "1966": f"{BASE}/1966/worldcup.json",
    "1970": f"{BASE}/1970/worldcup.json",
    "1974": f"{BASE}/1974/worldcup.json",
    "1978": f"{BASE}/1978/worldcup.json",
    "1982": f"{BASE}/1982/worldcup.json",
    "1986": f"{BASE}/1986/worldcup.json",
    "1990": f"{BASE}/1990/worldcup.json",
    "1994": f"{BASE}/1994/worldcup.json",
    "1998": f"{BASE}/1998/worldcup.json",
    "2002": f"{BASE}/2002/worldcup.json",
    "2006": f"{BASE}/2006/worldcup.json",
    "2010": f"{BASE}/2010/worldcup.json",
    "2014": f"{BASE}/2014/worldcup.json",
    "2018": f"{BASE}/2018/worldcup.json",
    "2022": f"{BASE}/2022/worldcup.json",
    "2026": f"{BASE}/2026/worldcup.json"
}

TEAM_NAME_MAP = {
    "United States":        "USA",
    "Ivory Coast":          "Côte d'Ivoire",
    "West Germany":         "Germany",
    "East Germany":         "Germany",
    "Serbia and Montenegro":"Serbia",
    "Soviet Union":         "Russia",
    "Dutch East Indies":    "Indonesia",
    "Zaire":                "DR Congo",
    "Czechoslovakia":       "Czech Republic",
}

def normalize_team(name):
    return TEAM_NAME_MAP.get(name, name)

def fetch_matches(url):
    response = requests.get(url)
    data = response.json()

    matches = []
    for match in data['matches']:
        
        if 'score' not in match:
            continue

        matches.append({
            'round': match['round'],
            'date': match['date'],
            'home_team': normalize_team(match['team1']),
            'away_team': normalize_team(match['team2']),
            'final_score' : (f'{match['score']['ft'][0]} - {match['score']['ft'][1]}'),
            'home_goals': match['score']['ft'][0],
            'away_goals': match['score']['ft'][1],
            'group': match.get('group', 'a')
        })
    return matches

def load_all_matches():

    all_matches = []

    for year, url in URLS.items():
        print(f'Fetching {year} World Cup data...')
        matches = fetch_matches(url)

        for match in matches:
            match['year'] = int(year)

        all_matches.extend(matches)
        print(f' -> {len(matches)} matches loaded')

    df = pd.DataFrame(all_matches)
    df['date'] = pd.to_datetime(df['date'])
    df['home_goals'] = pd.to_numeric(df['home_goals'], errors= 'coerce')
    df['away_goals'] = pd.to_numeric(df['away_goals'], errors= 'coerce')
    df['goal_diff'] = df['home_goals'] - df['away_goals']
    return df

if __name__ == "__main__":
    df = load_all_matches()

    print('\n -- Shape --')
    print(df.shape)

    print('\n -- First 5 rows --')
    print(df.head(5))

    print('\n -- Data Types --')
    print(df.dtypes)

    print('\n -- Missing Values --')
    print(df.isnull().sum())