import React, { useState } from "react";
import { register } from "../server/api";
import "../styles/register.css"; // Import the CSS file

export default function Register() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "user",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await register(form);
    alert(res.message || res.error);
  };

  return (
    <div className="register-container">
      <form className="register-form" onSubmit={handleSubmit}>
        <h2 className="register-title">Repulser Register</h2>

        <input
          type="text"
          placeholder="Name"
          className="register-input"
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          className="register-input"
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          className="register-input"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        <select
          className="register-select"
          onChange={(e) => setForm({ ...form, role: e.target.value })}
        >
          <option value="user">User</option>
          <option value="business">Business</option>
        </select>
        <button type="submit" className="register-button">
          Register
        </button>
      </form>
    </div>
  );
}
