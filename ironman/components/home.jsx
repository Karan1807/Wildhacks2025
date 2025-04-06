import React from "react";
import { useUser } from "../backend/context/context";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import "../styles/home.css";

export default function Home() {
  const { user } = useUser();
  const navigate = useNavigate();

  if (!user) {
    return <div className="loading">Loading user info...</div>;
  }

  const walletBalance = user.balance || 0;
  const transactions = user.transactions || []; // Make sure your context provides this

  return (
    <div className="stark-wallet-app">
      <div className="stark-wallet-container">
        {/* Navbar */}
        <nav className="stark-navbar">
          <div className="navbar-brand">
            {/* You can put logo or app name here */}
          </div>

          <div className="navbar-menu">
            <Link to="/home" className={`nav-item`}>
              DASHBOARD
            </Link>
            {/* Add more nav items as needed */}
          </div>
        </nav>

        {/* Main Content */}
        <div className="stark-content">
          <div className="balance-card">
            <div className="balance-section">
              <div className="balance-label">BALANCE</div>
              <div className="balance-amount">
                ₹
                {walletBalance.toLocaleString("en-IN", {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })}
              </div>
            </div>

            <div className="user-section">
              <div className="user-label">WELCOME BACK</div>
              <div className="username">{user.name}</div>
            </div>

            <div className="action-buttons">
              <button
                className="action-button receive"
                onClick={() => navigate("/scanPalm")}
              >
                <span className="icon">↓</span> RECEIVE
              </button>
            </div>
          </div>

          {/* Transactions */}
          <div className="transaction-section">
            <div className="transactions-list">
              {transactions.length > 0 ? (
                transactions.map((transaction, index) => (
                  <div key={index} className="transaction-item">
                    <div className="transaction-icon-container">
                      <div className={`transaction-icon ${transaction.type}`}>
                        {transaction.type === "credit" ? "↓" : "↑"}
                      </div>
                    </div>

                    <div className="transaction-details">
                      <div className="transaction-name">{transaction.name}</div>
                      <div className="transaction-date">{transaction.date}</div>
                    </div>

                    <div className={`transaction-amount ${transaction.type}`}>
                      {transaction.type === "credit" ? "+" : "-"}₹
                      {Math.abs(transaction.amount).toLocaleString("en-IN", {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                      })}
                    </div>

                    <div className="transaction-dropdown">▼</div>
                  </div>
                ))
              ) : (
                <p>No transactions yet.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
