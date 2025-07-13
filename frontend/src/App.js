import React, { useState } from "react";
import axios from "axios";
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from "jwt-decode";  // ✅ Correct for v4+
import './App.css';


function App() {
  const [features, setFeatures] = useState(["", "", "", "", ""]);
  const [result, setResult] = useState("");
  const [user, setUser] = useState(null);
  const BACKEND_URL = "https://student-placement-predictor-web.onrender.com";
  // Google Login Success Handler
  const handleLogin = async (credentialResponse) => {
  try {
    const token = credentialResponse.credential;
    const decoded = jwtDecode(token);
    console.log("User:", decoded);
    setUser(decoded);

    const response = await fetch(`${BACKEND_URL}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token }),
    });

    const result = await response.json();
    console.log(result);
  } catch (err) {
    console.error("Login error:", err);
  }
};


  // Handle input changes for ML features
  const handleChange = (i, value) => {
    const newFeatures = [...features];
    newFeatures[i] = parseFloat(value);
    setFeatures(newFeatures);
  };

  // Predict placement using backend ML model
  const predict = async () => {
  try {
    const response = await axios.post(`${BACKEND_URL}/api/predict`, {
      features: features,
    });
    setResult(response.data.prediction === 1 ? "Placed" : "Not Placed");
  } catch (err) {
    console.error(err);
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
            <input type="number" onChange={(e) => handleChange(i, e.target.value)} />
          </div>
        ))}
        <button onClick={predict}>Predict</button>
        <div className="result">Result: {result}</div>
      </>
    )}
  </div>
);
}
export default App;
