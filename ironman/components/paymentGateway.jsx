import React, { useEffect } from "react";

const PaymentGateway = () => {
  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.async = true;
    document.body.appendChild(script);
  }, []);

  const handlePayment = async () => {
    const res = await fetch("http://localhost:3001/create-order", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });

    const data = await res.json();

    const options = {
      key: "rzp_test_AbDNAfekvsh8ki",
      amount: data.amount,
      currency: data.currency,
      order_id: data.id,
      name: "Test Company",
      description: "Test Transaction",
      handler: function (response) {
        alert("Payment Successful!");
        console.log(response);
      },
      prefill: {
        name: "John Doe",
        email: "john.doe@example.com",
        contact: "9999999999",
      },
      theme: { color: "#F37254" },
    };

    const razor = new window.Razorpay(options);
    razor.open();
  };

  return (
    <div style={{ textAlign: "center", padding: "2rem" }}>
      <h1>Payment Gateway</h1>
      <button onClick={handlePayment}>Pay Now</button>
    </div>
  );
};

export default PaymentGateway;
