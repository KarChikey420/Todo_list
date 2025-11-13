// src/components/AddTask.js
import React, { useState } from "react";
import axios from "../api";

export default function AddTask({ refreshTasks }) {
  const [task, setTask] = useState("");

  const handleAdd = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      await axios.post(
        "/tasks",
        { task },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setTask("");
      refreshTasks();
    } catch (err) {
      alert("Failed to add task");
    }
  };

  return (
    <form onSubmit={handleAdd}>
      <input
        placeholder="New task..."
        value={task}
        onChange={(e) => setTask(e.target.value)}
      />
      <button type="submit">Add</button>
    </form>
  );
}
