# TodoKit Codebase Guide for AI Agents

## Architecture Overview

**TodoKit** is a full-stack task management application with clear separation:
- **Backend**: Flask + PostgreSQL + JWT authentication
- **Frontend**: React 19 with React Router v7 for client-side routing
- **Communication**: Axios HTTP client with Bearer token auth pattern

### Data Flow
1. Frontend stores JWT token in `localStorage` after login
2. All authenticated requests include `Authorization: Bearer {token}` header
3. Backend validates token via `@token_required` decorator
4. User-scoped data isolation: tasks filtered by `user_id` at DB level

## Backend (Flask + PostgreSQL)

### Key Patterns
- **Entry point**: `backend/app.py` - single file monolith
- **Database initialization**: `initialize_db()` creates `users` and `tasks` tables on startup
- **Connection pooling**: `get_connection()` creates fresh connections per request (not pooled)
- **Authentication**: JWT tokens with 2-hour expiration; passwords hashed with bcrypt

### Critical Flow: Token Validation
The `@token_required` decorator (line ~28) extracts Bearer token from headers, decodes JWT, and injects `current_user` (username) as first argument to protected endpoints. All task operations verify `user_id` matches before CRUD.

### API Endpoints
- `POST /api/signup` - Create user (unique username constraint enforced)
- `POST /api/login` - Return JWT token
- `GET /api/tasks` - List user's tasks (token required)
- `POST /api/tasks` - Create task (token required, auto-assigned to user)
- `PUT /api/tasks/<id>` - Mark task complete (token required)
- `DELETE /api/tasks/<id>` - Delete task (token required)

### Environment Setup
Uses `python-dotenv`. Required variables: `host`, `database`, `user`, `password`, `SECRET_KEY`. See `backend/requirements.txt` for exact dependencies.

## Frontend (React + Router)

### Component Structure
- **App.js**: Router setup with 4 routes (signup, login, tasks, home redirects to login)
- **api.js**: Centralized axios instance configured with `baseURL: "http://127.0.0.1:5000"` via package.json proxy
- **components/signup.js**: New user registration with 6-char minimum password
- **components/login.js**: Stores token to localStorage; redirects to /tasks on success
- **components/TaskList.js**: Main dashboard - fetch tasks, add task form, CRUD actions
- **components/AddTask.js**: Form component (reused child of TaskList)

### Token Management Pattern
- Token retrieved from localStorage for all protected requests
- `TaskList.js` auto-redirects to /login if no token exists
- 401 responses trigger logout and redirect to /login
- No token refresh mechanism; users must re-login after 2-hour expiration

### Styling Convention
Tailwind CSS utility classes - consistent use of `indigo-600` brand color, gray scale (`gray-50` backgrounds, `gray-800` text), and responsive padding/layout.

## Integration Points

### CORS Configuration
Backend has `CORS(app)` enabled for all origins (no restrictions). Frontend proxy configured in `package.json`: `"proxy":"http://127.0.0.1:5000"`. For production, update `api.js` baseURL and restrict CORS in Flask.

### Error Handling
- Frontend: Catches axios errors, displays alert() with `error.response?.data?.message`
- Backend: Returns JSON `{'message': 'description'}` with HTTP status codes (201 created, 400 bad request, 401 unauthorized)

## Development Workflows

### Starting Both Services
```bash
# Terminal 1: Backend
cd backend
python app.py  # Runs on http://localhost:5000

# Terminal 2: Frontend
cd frontend
npm start  # Runs on http://localhost:3000
```

### Testing a Full Flow
1. Signup at `/signup` with unique username
2. Login at `/login` (token stored to localStorage)
3. Add task on `/tasks`
4. Complete task (PUT request)
5. Delete task (DELETE request)
6. Logout clears localStorage and redirects

## Project-Specific Conventions

### No Shared Code
Frontend and backend are completely decoupled. All shared logic (validation, formatting) duplicated in each layer. Backend single file; no service/repository pattern.

### Task ID Handling
- Backend: SERIAL primary key, auto-incremented
- Frontend: Displayed in UI but routes always use path params or body. No internal task state management beyond React component state.

### User Isolation
All task queries hardcoded with `WHERE user_id={current_user_id}`. Backend guarantees no cross-user data leaks at DB level.

## Quick Reference for Common Changes

- **Add new task field**: Update backend schema in `initialize_db()`, add to task insert/select, update frontend `TaskList.js` render
- **Add new route**: Create `@app.route()` decorator in `app.py`, add frontend Route in `App.js`, handle token if protected
- **Styling**: Use existing Tailwind classes from components; maintain indigo/gray palette
- **Debug token issues**: Check browser localStorage in DevTools; backend logs JWT validation in console
