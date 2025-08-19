# setup_db.py
import sqlite3

# Database connection
conn = sqlite3.connect("restaurant.db")
cursor = conn.cursor()

# Enable foreign keys (optional but good practice)
cursor.execute("PRAGMA foreign_keys = ON;")

# Food table
cursor.execute("""
CREATE TABLE IF NOT EXISTS food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
)
""")

# Orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    total_price REAL NOT NULL,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Clear old data (optional)
cursor.execute("DELETE FROM food")

# Sample items
cursor.executemany("""
INSERT INTO food (item_name, category, price) VALUES (?, ?, ?)
""", [
    ("Pizza", "Main Course", 250),
    ("Burger", "Snacks", 120),
    ("Pasta", "Main Course", 200),
    ("Coffee", "Beverage", 80),
    ("Momo", "Snacks", 100),
    ("Salad", "Appetizer", 150),
    ("Ice Cream", "Dessert", 90),
    ("Soft Drink", "Beverage", 50),
    ("Sandwich", "Snacks", 70),
    ("French Fries", "Snacks", 60)
])

conn.commit()
conn.close()

print("Database setup complete ✅")

