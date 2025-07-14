const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();

// ✅ CORRECT: Allow only your frontend (Netlify) to access the backend
const corsOptions = {
  origin: 'https://stdplacementpredictor.netlify.app',
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type'],
  credentials: true,
};

app.use(cors(corsOptions));
app.options('*', cors(corsOptions));

// ✅ Middleware to parse JSON
app.use(express.json());

// ✅ Prediction route: forwards to your model backend
app.post("/api/predict", async (req, res) => {
  try {
    const { features } = req.body;

    if (!features || !Array.isArray(features)) {
      return res.status(400).json({ error: "Invalid or missing 'features' array." });
    }

    const response = await axios.post("https://student-placement-predictor-web-1-model.onrender.com/predict", {
      features,
    });

    res.json(response.data);
  } catch (err) {
    console.error("Prediction error:", err.message);
    res.status(500).send("Prediction service failed");
  }
});

// ✅ IMPORTANT: Use dynamic port for Render deployment
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}`);
});
