from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})
  # ✅ Enable CORS for all origins

model = joblib.load("placement_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)
    return jsonify({"prediction": int(prediction[0])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
