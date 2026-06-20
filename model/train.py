import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))

from fetch_data import load_all_matches
from feature_engineering import compute_team_stats

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle

df = load_all_matches()
df = compute_team_stats(df)

df["score_diff"]   = df["home_avg_scored"]   - df["away_avg_scored"]
df["concede_diff"] = df["home_avg_conceded"] - df["away_avg_conceded"]
df["winrate_diff"] = df["home_win_rate"]     - df["away_win_rate"]

FEATURES = ["home_avg_scored",
    "home_avg_conceded",
    "home_win_rate",
    "away_avg_scored",
    "away_avg_conceded",
    "away_win_rate",
    "score_diff",
    "concede_diff",
    "winrate_diff"]

TARGET = 'goal_diff'

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

print(f'Training Samples : {len(X_train)}')
print(f'Testing Samples {len(X_test)}')

models = {
    'Linear Regression' : LinearRegression(),
    'Random Forest' : RandomForestRegressor(n_estimators=100, random_state= 42),
    'XGRegressor': XGBRegressor(
                                n_estimators = 200,
                                max_depth=3,
                                learning_rate = 0.05,
                                subsample = 0.8,
                                random_state = 42)
}

results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    results[name] = {'MAE': mae, 'RMSE': rmse, 'R2': r2, 'Model': model}

    print(f'\n-- {name} --')
    print(f'\n MAE : {mae:.3f}')
    print(f'\n RMSE : {rmse:.3f}')
    print(f'\n R2 : {r2:.3f}')

best_name = min(results, key = lambda x: results[x]['MAE'])
best_model = results[best_name]['Model']
print(f'\n ✅ Best model: {best_name}')

rf_model = results['Random Forest']['Model']
importances = pd.Series(rf_model.feature_importances_, index = FEATURES)
importances = importances.sort_values(ascending= False)

print('\n -- Feature Importances (Random Forest) --')
for feat, imp in importances.items():
    bar = "█" * int(imp * 40) 
    print(f"  {feat:<25} {bar} {imp:.3f}")

model_dir = os.path.join(os.path.dirname(__file__))
os.makedirs(model_dir, exist_ok=True)

with open(os.path.join(model_dir, "best_model.pkl"), "wb") as f:
    pickle.dump(best_model, f)

print("\n💾 Model saved to model/best_model.pkl")