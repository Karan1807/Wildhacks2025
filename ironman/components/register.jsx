import React, { useState, useRef } from "react";
import { Link } from "react-router-dom";
import "../styles/register.css";

export default function Register() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "user",
  });

  const [scanning, setScanning] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [frames, setFrames] = useState([]);

  const startCamera = async () => {
    try {
      setScanning(true);
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      videoRef.current.play();
    } catch (err) {
      alert("Camera access denied or unavailable.");
    }
  };

  const captureFrames = async () => {
    const context = canvasRef.current.getContext("2d");
    const capturedFrames = [];

    for (let i = 0; i < 10; i++) {
      context.drawImage(videoRef.current, 0, 0, 224, 224);
      const imageData = canvasRef.current.toDataURL("image/jpeg");
      capturedFrames.push(imageData);
      await new Promise((resolve) => setTimeout(resolve, 300));
    }

    setFrames(capturedFrames);
    return capturedFrames;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!scanning) {
      alert("Please start the palm scan first.");
      return;
    }

    const captured = await captureFrames();

    const fullPayload = {
      ...form,
      palm_images: captured,
    };

    const res = await fetch("http://localhost:3001/register_with_palm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(fullPayload),
    });

    const result = await res.json();
    alert(result.message || result.error);
  };

  return (
    <div className="register-container">
      <form className="register-form" onSubmit={handleSubmit}>
        <h2 className="register-title">ArcPay Register</h2>

        <input
          type="text"
          placeholder="Name"
          className="register-input"
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        />
        <input
          type="email"
          placeholder="Email"
          className="register-input"
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="register-input"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
        />
        <select
          className="register-select"
          onChange={(e) => setForm({ ...form, role: e.target.value })}
        >
          <option value="user">User</option>
          <option value="business">Business</option>
        </select>

        <button type="button" onClick={startCamera} className="register-button">
          Start Palm Scan
        </button>

        <video
          ref={videoRef}
          width="300"
          height="225"
          style={{ display: scanning ? "block" : "none", marginTop: "10px" }}
        />
        <canvas
          ref={canvasRef}
          width="224"
          height="224"
          style={{ display: "none" }}
        />

        <button type="submit" className="register-button">
          Register & Upload Palm
        </button>

        {/* Login link */}
        <div className="login-link">
          Already have an account? <Link to="/login">Login</Link>
        </div>
      </form>
    </div>
  );
}
