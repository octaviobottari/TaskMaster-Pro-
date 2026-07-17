# TaskMaster Pro

**Team members:** Octavio Bottari & Victor Andres Chavez Tuchez  
**Group:** 13  
**Scheduled meet time:** Fridays at 5 PM EST (Discord)

---

## About

TaskMaster Pro is a lightweight desktop application designed to help individuals manage their daily tasks efficiently. Whether you're a student juggling assignments, a professional tracking work deadlines, or just someone trying to stay organized, this app provides a clean and intuitive interface to create, organize, and track tasks without unnecessary complexity.

All data is stored locally—no cloud, no accounts, no internet connection required.

---

## Key Features (Completed in Sprint 1)

| Feature | Status | Description |
|---------|--------|-------------|
| **Add Task** | ✅ Done | Create tasks with title, description, due date, priority, and category |
| **Edit Task** | ✅ Done | Modify any task details via double-click or edit button |
| **Delete Task** | ✅ Done | Remove tasks with confirmation prompt |
| **Toggle Status** | ✅ Done | Mark tasks as Pending or Completed |
| **Filter** | ✅ Done | View All, Pending, or Completed tasks |
| **Search** | ✅ Done | Search by title or description (case-insensitive) |
| **Sort** | ✅ Done | Click column headers to sort by Date, Priority, or Category |
| **Statistics** | ✅ Done | Real-time counters: Total, Pending, Completed |
| **Mock Data** | ✅ Done | 3 sample tasks pre-loaded for testing |
| **Data Persistence** | 🔨 In Progress | SQLite integration (Victor's responsibility for Sprint 2) |

---

## Technology Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| **Language** | Python 3.10+ | Easy to learn, fast prototyping, perfect for desktop utilities |
| **GUI Framework** | Tkinter | Built into Python; no external dependencies required |
| **Database** | SQLite3 | Lightweight, serverless, stores all data in a single `.db` file |
| **Version Control** | Git & GitHub | Collaboration, change tracking, assignment submission |

---

## Architecture (MVC-Inspired)

We follow a simple layered architecture to keep concerns separated:
┌─────────────────────────────────────────────────────────────┐
│                      VIEW (Tkinter UI)                     │
│  - Main window, Treeview, forms, buttons, filters          │
│  - Handles user interaction and display                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   CONTROLLER (Business Logic)              │
│  - TaskApp class: manages UI events                        │
│  - Validates input before passing to model                 │
│  - Coordinates between View and Model                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    MODEL (Data Layer)                      │
│  - MockTaskManager (in-memory) OR DBManager (SQLite)       │
│  - Handles CRUD operations, filtering, sorting             │
│  - Implements DatabaseManager interface (contract)         │
└─────────────────────────────────────────────────────────────┘

**Key Design Decision:** The UI depends only on the `DatabaseManager` interface, not on a specific implementation. This allows us to:
- Develop and test the UI with the mock manager (in-memory data)
- Swap in Victor's `DBManager` (SQLite) with zero UI changes
- Keep the code clean, testable, and maintainable

## Project Structure
taskmaster-pro/
│
├── taskmaster_ui.py # Main UI (Tkinter) 
├── mock_manager.py # In-memory mock for testing
├── db_interface.py # Contract for DBManager 
├── db_manager.py # SQLite implementation 
├── test_integration.py # Integration test script
├── requirements.txt # Python dependencies (Tkinter is built-in)
└── README.md 

---

## Development Status

| Sprint | Milestone | Status |
|--------|-----------|--------|
| **Sprint 1** | UI complete with mock data, filters, search, sorting, statistics | ✅ Done |
| **Sprint 2** | SQLite integration, data persistence, CRUD with DB | 🔨 In Progress |
| **Sprint 3** | Edit/delete buttons, toggle status with DB, filter enhancements | 📅 Planned |
| **Sprint 4** | Search, statistics dashboard, polish, bug fixes, demo recording | 📅 Planned |

---

## How to Run the App (Current Version)

1. **Clone the repository:**
   git clone https://github.com/your-repo/taskmaster-pro.git
   cd taskmaster-pro

2. **Run the Application:**
    python taskmaster_ui.py

3. **Expected output:**
    .A window titled "TaskMaster Pro" opens
    .3 sample tasks are pre-loaded
    .All buttons, filters, search, and sorting work immediately
    