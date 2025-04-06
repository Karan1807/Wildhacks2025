import React, { useState } from "react";
import { login } from "../server/api";
import "../styles/login.css"; // Import the styles
import { useUser } from "../backend/context/context";
import { useNavigate } from "react-router-dom"; // assuming react-router

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const { setUser } = useUser();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    const res = await login(form);
    if (res.error) {
      alert(res.error);
    } else {
      alert("Login successful");
      console.log(res);
      setUser(res); // { name, email, balance, _id, etc. }
      localStorage.setItem("user", JSON.stringify(res.user));
      navigate("/home"); // go to homepage
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleLogin}>
        <h2 className="login-title">Welcome Back</h2>

        <input
          type="email"
          placeholder="Email"
          className="login-input"
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="login-input"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
        />
        <button type="submit" className="login-button">
          Login
        </button>
      </form>
    </div>
  );
}
