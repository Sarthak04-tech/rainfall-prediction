import pickle
import pandas as pd

with open('model_unzipped/rainfall_model.pkl', 'rb') as f:
    model = pickle.load(f)

print("Model Type:", type(model))

# Check if it has feature names
if hasattr(model, 'feature_names_in_'):
    print("Features:", model.feature_names_in_)
elif hasattr(model, 'get_booster'):
    # XGBoost specific
    booster = model.get_booster()
    print("XGBoost Features:", booster.feature_names)
else:
    print("Could not directly extract feature names.")
