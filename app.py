import sys
import os
import threading
import sqlite3
import webbrowser
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ------------------ PATH FIXES ------------------
def get_resource_path(relative_path):
    """ Get absolute path to resource (index.html inside the exe) """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def get_db_path():
    """ 
    CLEAN FIX: 
    Store the database in the user's hidden AppData folder.
    This keeps the EXE folder clean, but data persists.
    Location: C:/Users/NAME/AppData/Roaming/LeadDork/database.db
    """
    # 1. Get the AppData folder
    app_data = os.getenv('APPDATA')
    
    # 2. Create a specific folder for your app
    app_folder = os.path.join(app_data, 'LeadDork')
    
    # 3. If it doesn't exist, create it
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)
    
    # 4. Return the full path to the db
    return os.path.join(app_folder, "database.db")

INDEX_PATH = get_resource_path("index.html")
DB_PATH = get_db_path()

# ------------------ DATABASE INIT ------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT, keyword TEXT, category TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    c.execute("""CREATE TABLE IF NOT EXISTS saved (
            id INTEGER PRIMARY KEY AUTOINCREMENT, keyword TEXT, category TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    conn.close()

# ------------------ ROUTES ------------------
@app.route("/", methods=["GET"])
def home():
    try:
        with open(INDEX_PATH, "r", encoding="utf8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Error: index.html not found.</h1>"

@app.route("/api/history/add", methods=["POST"])
def api_history_add():
    data = request.json
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO history(keyword, category) VALUES (?, ?)", (data["keyword"], data["category"]))
    return jsonify(status="ok")

@app.route("/api/history/get", methods=["GET"])
def api_history_get():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT id, keyword, category, timestamp FROM history ORDER BY id DESC").fetchall()
    return jsonify(history=[{"id": r[0], "keyword": r[1], "category": r[2], "timestamp": r[3]} for r in rows])

@app.route("/api/history/delete/<int:id>", methods=["DELETE"])
def api_history_delete(id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM history WHERE id=?", (id,))
    return jsonify(status="deleted")

@app.route("/api/saved/add", methods=["POST"])
def api_saved_add():
    data = request.json
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO saved(keyword, category) VALUES (?, ?)", (data["keyword"], data["category"]))
    return jsonify(status="ok")

@app.route("/api/saved/get", methods=["GET"])
def api_saved_get():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT id, keyword, category, timestamp FROM saved ORDER BY id DESC").fetchall()
    return jsonify(saved=[{"id": r[0], "keyword": r[1], "category": r[2], "timestamp": r[3]} for r in rows])

@app.route("/api/saved/delete/<int:id>", methods=["DELETE"])
def api_saved_delete(id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM saved WHERE id=?", (id,))
    return jsonify(status="deleted")

@app.route('/shutdown', methods=['POST'])
def shutdown():
    os._exit(0)

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    init_db()
    threading.Timer(1, open_browser).start()
    app.run(port=5000, debug=False)