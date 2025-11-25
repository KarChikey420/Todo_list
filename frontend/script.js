const API_URL = "http://127.0.0.1:5000/api"; // Standard Flask URL

// --- State Management ---
let token = localStorage.getItem('token');
let tasks = [];

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    if (token) {
        showApp();
    } else {
        showAuth();
    }
});

// --- Auth Functions ---
function showAuth() {
    document.getElementById('auth-container').classList.remove('hidden');
    document.getElementById('app-container').classList.add('hidden');
}

function showApp() {
    document.getElementById('auth-container').classList.add('hidden');
    document.getElementById('app-container').classList.remove('hidden');
    fetchTasks();
}

async function signup() {
    const user = document.getElementById('auth-username').value;
    const pass = document.getElementById('auth-password').value;
    
    const res = await fetch(`${API_URL}/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, password: pass })
    });
    
    const data = await res.json();
    if (res.status === 201) {
        document.getElementById('auth-message').innerText = "Signup successful! Please login.";
        document.getElementById('auth-message').style.color = "green";
    } else {
        document.getElementById('auth-message').innerText = data.message;
    }
}

async function login() {
    const user = document.getElementById('auth-username').value;
    const pass = document.getElementById('auth-password').value;
    
    const res = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, password: pass })
    });
    
    const data = await res.json();
    if (res.status === 200) {
        token = data.token;
        localStorage.setItem('token', token);
        document.getElementById('auth-message').innerText = "";
        showApp();
    } else {
        document.getElementById('auth-message').innerText = data.message;
    }
}

function logout() {
    localStorage.removeItem('token');
    token = null;
    showAuth();
}

// --- Task Functions ---

async function fetchTasks() {
    try {
        const res = await fetch(`${API_URL}/tasks`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (res.status === 401) { logout(); return; } // Token expired
        
        tasks = await res.json();
        renderTasks();
    } catch (err) {
        console.error("Error fetching tasks:", err);
    }
}

async function addTask() {
    const input = document.getElementById('new-task-input');
    const taskText = input.value.trim();
    
    if (!taskText) return;

    const res = await fetch(`${API_URL}/tasks`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify({ task: taskText })
    });

    if (res.ok) {
        input.value = "";
        fetchTasks(); // Refresh list
    }
}

// Note: Your backend UPDATE endpoint sets done=TRUE only. 
// It does not currently support toggling back to false.
async function completeTask(id) {
    await fetch(`${API_URL}/tasks/${id}`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${token}` }
    });
    fetchTasks();
}

async function deleteTask(id) {
    await fetch(`${API_URL}/tasks/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
    });
    fetchTasks();
}

// Since the backend doesn't have a "Delete All Completed" endpoint,
// we filter them locally and delete them one by one.
async function clearCompleted() {
    const completedTasks = tasks.filter(t => t.done);
    for (let task of completedTasks) {
        await deleteTask(task.id);
    }
}

// --- Rendering ---
function renderTasks() {
    const list = document.getElementById('task-list');
    list.innerHTML = '';

    let activeCount = 0;
    let completedCount = 0;

    tasks.forEach(task => {
        if (task.done) completedCount++;
        else activeCount++;

        const item = document.createElement('div');
        item.className = `task-item ${task.done ? 'completed' : ''}`;
        
        // Custom checkbox logic
        const checkMark = task.done ? '✔' : '';
        
        item.innerHTML = `
            <div class="custom-checkbox" onclick="completeTask(${task.id})">${checkMark}</div>
            <span class="task-text">${task.task}</span>
            <button class="delete-btn" onclick="deleteTask(${task.id})">✕</button>
        `;
        list.appendChild(item);
    });

    // Update stats
    document.getElementById('stats-text').innerText = `${activeCount} active · ${completedCount} completed`;
}