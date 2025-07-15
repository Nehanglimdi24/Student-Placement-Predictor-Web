from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)

# ✅ Allow CORS from your Netlify frontend
CORS(app, resources={r"/predict": {"origins": "https://stdplacementpredictor.netlify.app"}})

# Load the trained model
model = joblib.load("placement_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = np.array(data["features"]).reshape(1, -1)
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        
        # Confidence is the probability of the predicted class
        confidence = float(probabilities[prediction])
        
        return jsonify({
            "prediction": int(prediction),
            "confidence": round(confidence, 4)  # Rounded for readability
        })
    except Exception as e:
        print("Error during prediction:", str(e))
        return jsonify({"error": "Prediction failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
