import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_stats():
    print("Testing /stats...")
    r = requests.get(f"{BASE_URL}/stats")
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("Stats success!")
    else:
        print(f"Stats fail: {r.text}")

def test_predict():
    print("\nTesting /predict...")
    data = {
        "YEAR": 2024,
        "JAN": 15.2, "FEB": 22.4, "MAR": 45.1, "APR": 78.5, "MAY": 120.3,
        "JUN": 350.6, "JUL": 480.2, "AUG": 410.5, "SEP": 290.7,
        "OCT": 130.4, "NOV": 35.6, "DEC": 12.8
    }
    r = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print(f"Prediction result: {r.json()}")
    else:
        print(f"Prediction fail: {r.text}")

if __name__ == "__main__":
    try:
        test_stats()
        test_predict()
    except Exception as e:
        print(f"Error: {e}")
