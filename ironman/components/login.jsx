import React, { useState } from "react";
import { login } from "../server/api";

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await login(form);
    if (res.error) {
      alert(res.error);
    } else {
      alert("Login successful");
      console.log(res); // Contains role, balance, etc.
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input placeholder="Email" type="email" onChange={e => setForm({ ...form, email: e.target.value })} />
      <input placeholder="Password" type="password" onChange={e => setForm({ ...form, password: e.target.value })} />
      <button type="submit">Login</button>
    </form>
  );
}
