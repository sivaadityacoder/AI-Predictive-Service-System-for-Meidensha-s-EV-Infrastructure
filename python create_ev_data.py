import pandas as pd
import numpy as np

print("Generating training data for healthy EV chargers...")
num_rows = 5000
data = {
    'voltage_output': np.random.normal(loc=480.0, scale=2.5, size=num_rows),
    'current_draw': np.random.normal(loc=30.0, scale=1.5, size=num_rows),
    'internal_coolant_temp': np.random.normal(loc=70.0, scale=2.0, size=num_rows),
    'coolant_pump_rpm': np.random.normal(loc=1500.0, scale=50, size=num_rows)
}
df = pd.DataFrame(data)
df.to_csv('ev_charger_normal_data.csv', index=False)
print(f"Successfully generated ev_charger_normal_data.csv.")
