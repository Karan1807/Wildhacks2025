import React from "react";
import { useUser } from "../backend/context/context";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const { user } = useUser();
  const navigate = useNavigate();

  console.log("User in Home:", user); // 🔍 this should log user info after login

  const goToPalmScan = () => navigate("/scanPalm");

  if (!user) return <p>Loading user info...</p>;

  return (
    <div>
      <h2>Welcome, {user.name}</h2>
      <p>Balance: ₹{user.balance}</p>
      <button onClick={goToPalmScan}>Receive Money</button>
    </div>
  );
}
