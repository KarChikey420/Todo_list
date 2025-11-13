// src/components/TaskList.js
import React, { useEffect, useState } from "react";
import axios from "../api";
import AddTask from "./AddTask";

export default function TaskList() {
  const [tasks, setTasks] = useState([]);

  const fetchTasks = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get("/tasks", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTasks(res.data);
    } catch (err) {
      alert("Failed to fetch tasks");
    }
  };

  const completeTask = async (id) => {
    const token = localStorage.getItem("token");
    await axios.put(`/tasks/${id}`, {}, { headers: { Authorization: `Bearer ${token}` } });
    fetchTasks();
  };

  const deleteTask = async (id) => {
    const token = localStorage.getItem("token");
    await axios.delete(`/tasks/${id}`, { headers: { Authorization: `Bearer ${token}` } });
    fetchTasks();
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "40px" }}>
      <h2>Your Tasks</h2>
      <AddTask refreshTasks={fetchTasks} />
      <ul style={{ listStyle: "none", padding: 0 }}>
        {tasks.map((t) => (
          <li key={t.id}>
            <span style={{ textDecoration: t.done ? "line-through" : "none" }}>
              {t.task}
            </span>
            {!t.done && (
              <button onClick={() => completeTask(t.id)}>Complete</button>
            )}
            <button onClick={() => deleteTask(t.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
