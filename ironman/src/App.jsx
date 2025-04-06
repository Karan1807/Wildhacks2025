import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Register from "../components/register";
import Login from "../components/login";
import ScanPalm from "../components/scanPalm";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/scanPalm" element={<ScanPalm />} />
      </Routes>
    </Router>
  );
}

export default App;
