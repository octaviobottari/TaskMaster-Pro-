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
| **Data Persistence** | ✅ Done | All tasks automatically saved to SQLite database (Sprint 2) |


## Key Features (Completed in Sprint 2)

| Feature | Status | Description |
|---------|--------|-------------|
| **SQLite Integration** | ✅ Done | Full CRUD operations with SQLite  `task_repository` |
| **Data Persistence** | ✅ Done | Tasks automatically saved to `taskmaster.db` on every change |
| **DB Adapter** | ✅ Done | `DBManager` connects UI repository seamlessly |
| **Integration Testing** | ✅ Done | `test_integration.py` runs app with real database |


## Key Features (Completed in Sprint 3)

| Feature | Status | Description |
|---------|--------|-------------|
| **Category Filter** | ✅ Done | Filter tasks by category (Work, Personal, Study, Urgent, Other) |
| **Priority Filter** | ✅ Done | Filter tasks by priority (High, Medium, Low) |
| **Visual Feedback** | ✅ Done | Color-coded rows: Pending (yellow), Completed (green); priority text colors |
| **UI Layout** | ✅ Done | Improved filter panel with organized rows and clear labels |
| **Enhanced Search** | ✅ Done | Search works combined with all filters |
| **Full Testing** | ✅ Done | Verified all CRUD, filters, search, sorting with SQLite |

### Development Status

| Sprint | Milestone | Status |
|--------|-----------|--------|
| **Sprint 1** | UI complete with mock data, filters, search, sorting, statistics | ✅ Done |
| **Sprint 2** | SQLite integration, data persistence, CRUD with DB | ✅ Done |
| **Sprint 3** | UI enhancements: category/priority filters, visual feedback, layout improvements | ✅ Done |
| **Sprint 4** | Polish, bug fixes, demo recording | 📅 Planned |

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
├── database.py # DB setup and connection
├── task_repository.py # CRUD operations
├── main.py # CLI Test
├── test_database.py # DB test script
├── test_integration.py # Integration test script (UI + DB)
├── requirements.txt # Python dependencies (Tkinter is built-in)
└── README.md 


## How to Run the App (Current Version)

1. **Clone the repository:**
   git clone https://github.com/your-repo/taskmaster-pro.git
   cd taskmaster-pro

2. **Run the Application (with Mock Data - Sprint 1):**
   python taskmaster_ui.py

3. **Run the Application (with SQLite Database - Sprint 2):**
    python test_integration.py

    
We haven't finalized everything yet, but here's the folder/file structure 
we're planning to use to keep things organized:

## Favorite Quotes

> "Success is not final, failure is not fatal: it is the courage to continue that counts." – Winston Churchill

- Added by Victor Chavez
