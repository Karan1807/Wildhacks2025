// server.js
import express from "express";
import Razorpay from "razorpay";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

const razorpay = new Razorpay({
  key_id: "rzp_test_AbDNAfekvsh8ki",
  key_secret: "Zgw4M4DTbd69QhSCekqGrtUY", // Never expose this on frontend
});

app.post("/create-order", async (req, res) => {
  const options = {
    amount: 50000, // amount in paise = ₹500
    currency: "INR",
    receipt: "receipt#1",
  };

  try {
    const order = await razorpay.orders.create(options);
    res.json(order);
  } catch (err) {
    res.status(500).send("Error creating order");
  }
});

app.listen(3001, () => console.log("Server running on http://localhost:3001"));
