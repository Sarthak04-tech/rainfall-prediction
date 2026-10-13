import pandas as pd
import pickle

with open('model_unzipped/rainfall_model.pkl', 'rb') as f:
    model = pickle.load(f)

df = pd.read_csv('dataset/rainfall in india 1901-2015.csv')
features = ['YEAR', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'Jan-Feb', 'Mar-May', 'Jun-Sep', 'Oct-Dec']
row = df.iloc[[0]][features]

pred = model.predict(row)
print('Predicted ANNUAL:', pred)
print('Actual ANNUAL:', df.iloc[0]['ANNUAL'])
