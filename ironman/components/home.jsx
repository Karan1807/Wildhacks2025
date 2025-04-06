import React, { useEffect, useState } from "react";
import { useUser } from "../backend/context/context";
import { useNavigate, useLocation } from "react-router-dom";
import { Link } from "react-router-dom";
import "../styles/home.css";

export default function Home() {
  const { user, setUser } = useUser();
  const [transactions, setTransactions] = useState([]);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (user && user._id) {
      const fetchUser = async () => {
        try {
          const res = await fetch(`http://localhost:3001/get_user/${user._id}`);
          const data = await res.json();
          if (data && data.id) {
            setUser(data); // Update context with fresh data
          }
        } catch (err) {
          console.error("Failed to fetch user:", err);
        }
      };
  
      const fetchTransactions = async () => {
        try {
          const res = await fetch(`http://localhost:3001/get_transactions/${user._id}`);
          const data = await res.json();
          setTransactions(data || []);
        } catch (err) {
          console.error("Failed to fetch transactions:", err);
        }
      };
  
      fetchUser();
      fetchTransactions();
    } else {
      console.warn("User or user._id is undefined:", user);
    }
  }, [location]);
  

  if (!user) {
    return <div className="loading">Loading user info...</div>;
  }

  const walletBalance = user.balance || 0;

  return (
    <div className="stark-wallet-app">
      <div className="stark-wallet-container">
        {/* Navbar */}
        <nav className="stark-navbar">
          <div className="navbar-menu">
            <Link to="/home" className="nav-item">
              DASHBOARD
            </Link>
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
                transactions.map((transaction, index) => {
                  const isCredit = transaction.receiver_id === user._id;
                  const name = isCredit
                    ? transaction.sender_name || "Sender"
                    : transaction.receiver_name || "Receiver";
                  const date = new Date(transaction.timestamp).toLocaleString();

                  return (
                    <div key={index} className="transaction-item">
                      <div className="transaction-icon-container">
                        <div
                          className={`transaction-icon ${
                            isCredit ? "credit" : "debit"
                          }`}
                        >
                          {isCredit ? "↓" : "↑"}
                        </div>
                      </div>
                      <div className="transaction-details">
                        <div className="transaction-name">{name}</div>
                        <div className="transaction-date">{date}</div>
                      </div>
                      <div
                        className={`transaction-amount ${
                          isCredit ? "credit" : "debit"
                        }`}
                      >
                        {isCredit ? "+" : "-"}₹
                        {Math.abs(transaction.amount).toLocaleString("en-IN", {
                          minimumFractionDigits: 2,
                          maximumFractionDigits: 2,
                        })}
                      </div>
                      <div className="transaction-dropdown">▼</div>
                    </div>
                  );
                })
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
