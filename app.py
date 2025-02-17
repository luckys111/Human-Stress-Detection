from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained KNN model
with open('knn_model.pkl', 'rb') as model_file:
    knn_model = pickle.load(model_file)

# Define the home route
@app.route('/')
def home():
    return render_template('index.html')

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the form
        respiration = float(request.form['respiration'])
        snoring = float(request.form['snoring'])
        breath = float(request.form['breath'])
        temperature = float(request.form['temperature'])

        # Prepare the input data as a numpy array
        input_data = np.array([[respiration, snoring, breath, temperature]])

        # Make the prediction
        prediction = knn_model.predict(input_data)

        # Map the predicted class to a readable label and remedies
        stress_levels = {
            0: {
                'label': 'Low stress',
                'remedies': [
                    'Take a short walk in nature.',
                    'Practice deep breathing exercises.',
                    'Listen to calming music.'
                ]
            },
            1: {
                'label': 'Medium stress',
                'remedies': [
                    'Try a 10-minute meditation session.',
                    'Engage in light physical activity like yoga.',
                    'Write down your thoughts in a journal.'
                ]
            },
            2: {
                'label': 'High stress',
                'remedies': [
                    'Seek professional help or counseling.',
                    'Practice mindfulness and relaxation techniques.',
                    'Take a break and spend time with loved ones.'
                ]
            }
        }

        # Get the stress label and remedies for the predicted class
        result = stress_levels.get(prediction[0], {'label': 'Unknown', 'remedies': []})

        # Return the prediction and remedies as JSON
        return jsonify({
            'prediction': result['label'],
            'remedies': result['remedies']
        })

    except ValueError:
        return jsonify({'error': 'Invalid input. Please enter valid numerical values for all features.'})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)