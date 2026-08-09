# run_app.py - Ejecuta la aplicación con la base de datos SQLite real
import tkinter as tk
from taskmaster_ui import TaskApp
from db_manager import DBManager
from database import initialize_database

if __name__ == "__main__":
    # Inicializar la base de datos (crea taskmaster.db si no existe)
    initialize_database()
    
    print("🚀 Ejecutando TaskMaster Pro con SQLite (persistencia real)")
    print("📁 Base de datos: taskmaster.db")
    print("=" * 50)
    
    root = tk.Tk()
    app = TaskApp(root, db_manager=DBManager())
    root.mainloop()