import pickle
import pandas as pd
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model_unzipped', 'rainfall_model.pkl')
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'rainfall in india 1901-2015.csv')

# Globals to store loaded data
model = None
historical_averages = {}

def load_resources():
    global model, historical_averages
    # Load Model
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
            print("Model loaded successfully.")
        else:
            print(f"Warning: Model file not found at {MODEL_PATH}")
    except Exception as e:
        print(f"Error loading model: {e}")

    # Load Dataset and Calculate Averages for Visualization
    try:
        if os.path.exists(DATASET_PATH):
            df = pd.read_csv(DATASET_PATH)
            months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
            # Calculate overall averages for each month
            historical_averages = df[months].mean().round(2).to_dict()
            print("Historical averages calculated.")
        else:
            print(f"Warning: Dataset not found at {DATASET_PATH}")
    except Exception as e:
        print(f"Error calculating stats: {e}")

# Initialize resources
load_resources()

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'dataset_loaded': bool(historical_averages)
    }), 200

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stats')
def get_stats():
    if not historical_averages:
        return jsonify({'error': 'Stats not available'}), 500
    return jsonify(historical_averages)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Prediction model is not loaded on the server.'}), 503

    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        required_months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        required_fields = ['YEAR'] + required_months
        
        # Extract inputs
        input_values = {}
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
            try:
                input_values[field] = float(data[field])
            except ValueError:
                return jsonify({'error': f'Invalid value for {field}. Must be a number.'}), 400
        
        # Calculate derived features in the order required by the model
        # Jan-Feb, Mar-May, Jun-Sep, Oct-Dec
        input_values['Jan-Feb'] = input_values['JAN'] + input_values['FEB']
        input_values['Mar-May'] = input_values['MAR'] + input_values['APR'] + input_values['MAY']
        input_values['Jun-Sep'] = input_values['JUN'] + input_values['JUL'] + input_values['AUG'] + input_values['SEP']
        input_values['Oct-Dec'] = input_values['OCT'] + input_values['NOV'] + input_values['DEC']

        # Ensure correct column order for model
        features_order = ['YEAR', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'Jan-Feb', 'Mar-May', 'Jun-Sep', 'Oct-Dec']
        row = pd.DataFrame([input_values], columns=features_order)

        # Make prediction
        prediction = model.predict(row)[0]
        
        # Determine category based on prediction (example thresholds for Annual rainfall)
        # These are rough estimates; can be tuned
        category = "Normal"
        if prediction < 800: category = "Low"
        elif prediction > 2500: category = "Extreme"
        elif prediction > 1500: category = "High"

        return jsonify({
            'prediction': round(prediction, 2),
            'category': category,
            'status': 'success'
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error during prediction.'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    DEBUG_MODE = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1')

    if DEBUG_MODE:
        app.run(host=host, port=port, debug=True)
    else:
        try:
            from waitress import serve
            print(f"Starting production server on http://{host}:{port}")
            serve(app, host=host, port=port)
        except ImportError:
            print("Waitress not found. Falling back to default server...")
            app.run(host=host, port=port)
