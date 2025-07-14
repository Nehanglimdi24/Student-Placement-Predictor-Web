const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
const corsOptions = {
  origin: 'https://stdplacementpredictor.netlify.app',
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type'],
  credentials: true,
};

app.use(cors(corsOptions));
app.options('*', cors(corsOptions));

app.use(express.json());

app.post("/api/predict", async (req, res) => {
  try {
    const response = await axios.post("https://student-placement-predictor-web-1-model.onrender.com/predict", {
      features: req.body.features,
    });
    res.json(response.data);
  } catch (err) {
    console.error(err);
    res.status(500).send("Prediction service failed");
  }
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}`);
});
