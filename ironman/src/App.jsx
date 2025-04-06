import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "../components/register";
import Login from "../components/login";
import ScanPalm from "../components/scanPalm";
import Home from "../components/home";
import { UserProvider } from "../backend/context/context";

function App() {
  return (
    <UserProvider>
      <Router>
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/scanPalm" element={<ScanPalm />} />
          <Route path="/home" element={<Home />} />
        </Routes>
      </Router>
    </UserProvider>
  );
}

export default App;
