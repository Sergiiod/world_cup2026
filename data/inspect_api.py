import requests
import json

url = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
data = requests.get(url).json()
matches = data["matches"]

print(f"Total matches in JSON: {len(matches)}")

# Count matches with and without scores
with_score    = [m for m in matches if "score" in m]
without_score = [m for m in matches if "score" not in m]
with_winner   = [m for m in matches if "winner" in m.get("team1","").lower() 
                                    or "winner" in m.get("team2","").lower()]

print(f"Matches WITH scores      : {len(with_score)}")
print(f"Matches WITHOUT scores   : {len(without_score)}")
print(f"Matches filtered (winner): {len(with_winner)}")

# Show first scored match structure
if with_score:
    print(f"\nFirst scored match:")
    print(json.dumps(with_score[0], indent=2))

# Show how many scored matches are ALSO being filtered out
filtered_and_scored = [m for m in with_score 
                       if "winner" in m.get("team1","").lower() 
                       or "winner" in m.get("team2","").lower()]
print(f"\nScored matches being wrongly filtered: {len(filtered_and_scored)}")