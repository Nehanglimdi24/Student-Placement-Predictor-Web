import React, { useState } from "react";
import axios from "axios";
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from "jwt-decode";
import './App.css';

function App() {
  const [features, setFeatures] = useState(["", "", "", "", ""]);
  const [result, setResult] = useState("");
  const [user, setUser] = useState(null);
  const [confidence, setConfidence] = useState(null);

  const MODEL_URL = "https://student-placement-predictor-web-1-model.onrender.com/predict";

  // Handle Google login
  const handleLogin = async (credentialResponse) => {
    try {
      const token = credentialResponse.credential;
      const decoded = jwtDecode(token);
      console.log("User:", decoded);
      setUser(decoded);
    } catch (err) {
      console.error("Login error:", err);
    }
  };

  // Handle input changes
  const handleChange = (i, value) => {
    const newFeatures = [...features];
    newFeatures[i] = parseFloat(value);
    setFeatures(newFeatures);
  };

  // Directly call AI model
  const predict = async () => {
    try {
      const response = await axios.post(MODEL_URL, {
        features: features,
      });

      const prediction = response.data.prediction;
      setConfidence(response.data.confidence);
      setResult(prediction === 1 ? "Placed" : "Not Placed");
    } catch (err) {
      console.error("Prediction error:", err);
      setResult("Error");
    }
  };

  return (
    <div className="container">
      <h1>Placement Prediction App</h1>

      {!user ? (
        <GoogleLogin onSuccess={handleLogin} onError={() => console.log("Login Failed")} />
      ) : (
        <>
          <p>Welcome, <strong>{user.name}</strong></p>

          {["CGPA", "SSC Marks", "HSC Marks", "Aptitude Score", "Work Experience (0/1)"].map((label, i) => (
            <div key={i}>
              <label>{label}</label>
              <input
                type="number"
                onChange={(e) => handleChange(i, e.target.value)}
                value={features[i]}
              />
            </div>
          ))}

          <button onClick={predict}>Predict</button>
          <div className="result">Result: {result} with a confidence {confidence}</div>
        </>
      )}
    </div>
  );
}

export default App;
