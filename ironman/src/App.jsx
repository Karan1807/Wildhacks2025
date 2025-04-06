// import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import PaymentGateway from "../pages/paymentGateway";
// import "./App.css";

// function App() {
//   return (
//     <Router>
//       <Routes>
//         <Route path="/payment" element={<PaymentGateway />} />
//       </Routes>
//     </Router>
//   );
// }

// export default App;
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Register from "../components/register";
import Login from "../components/login";

function App() {
  return (
    <Router>
      <nav>
        <Link to="/register">Register</Link> | <Link to="/login">Login</Link>
      </nav>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;
