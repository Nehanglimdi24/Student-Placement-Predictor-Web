const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

app.post("/api/predict", async (req, res) => {
  try {
    const response = await axios.post("https://student-placement-predictor-web-1-model.onrender.com/", {
      features: req.body.features,
    });
    res.json(response.data);
  } catch (err) {
    console.error(err);
    res.status(500).send("Prediction service failed");
  }
});

app.listen(4000, () => {
  console.log("Backend running on https://student-placement-predictor-web-1-model.onrender.com/");
});
