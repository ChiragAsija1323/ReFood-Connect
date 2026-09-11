const express = require("express");
const cors = require("cors");
require("dotenv").config();
const { sequelize } = require("./models");
const authRoutes = require("./routes/authRoutes");
const donationRoutes = require("./routes/donationRoutes");

const app = express();

app.use(cors());
app.use(express.json());

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/donations", donationRoutes);

app.get("/", (req, res) => {
  res.json({
    status: "success",
    message: "ReFood Connect Backend is Running 🚀",
  });
});

const PORT = process.env.PORT || 8000;

sequelize.sync({ force: false }).then(() => {
  console.log("Database synced");
  app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}).catch(err => {
  console.error("Failed to sync database:", err);
});
