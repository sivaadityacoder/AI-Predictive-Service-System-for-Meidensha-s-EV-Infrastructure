import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

print("Starting ML model training...")
df = pd.read_csv('ev_charger_normal_data.csv')
features = ['voltage_output', 'current_draw', 'internal_coolant_temp', 'coolant_pump_rpm']
X_train = df[features]

model = IsolationForest(n_estimators=100, contamination='auto', random_state=42)
model.fit(X_train)

joblib.dump(model, 'ev_model.pkl')
print("Model training complete. Saved to ev_model.pkl")
