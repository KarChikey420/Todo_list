// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Signup from "./components/Signup";
import Login from "./components/Login";
import TaskList from "./components/TaskList";

function App() {
  return (
    <Router>
      <div style={{ textAlign: "center" }}>
        <nav>
          <Link to="/signup">Signup</Link> | <Link to="/login">Login</Link> |{" "}
          <Link to="/tasks">Tasks</Link>
        </nav>
        <Routes>
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/tasks" element={<TaskList />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
