from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db

app = Flask(__name__)
CORS(app)

# Create tables
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant TEXT,
        food_type TEXT,
        quantity TEXT,
        pay_delivery TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return "SurplusServe Backend Running"

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, role, phone) VALUES (?, ?, ?)",
        (data["name"], data["role"], data["phone"])
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "User added successfully"})

@app.route("/add_food", methods=["POST"])
def add_food():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO food_donations (restaurant, food_type, quantity, pay_delivery) VALUES (?, ?, ?, ?)",
        (data["restaurant"], data["food_type"], data["quantity"], data["pay_delivery"])
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "Food donation added"})

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/view_food")
def view_food():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_donations")
    data = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in data])
