import sqlite3

def init_db():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 user_id INTEGER PRIMARY KEY,
                 username TEXT,
                 phone TEXT
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS categories (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT UNIQUE
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 category_id INTEGER,
                 price REAL,
                 description TEXT,
                 FOREIGN KEY (category_id) REFERENCES categories(id)
                 )''')
    conn.commit()
    conn.close()

def add_user(user_id: int, username: str, phone: str):
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (user_id, username, phone) VALUES (?, ?, ?)",
              (user_id, username, phone))
    conn.commit()
    conn.close()

def get_user(user_id: int):
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def add_category(name: str) -> bool:
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_categories():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM categories")
    categories = c.fetchall()
    conn.close()
    return categories

def delete_category(category_id: int):
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    conn.commit()
    conn.close()

def update_category(category_id: int, new_name: str) -> bool:
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE categories SET name = ? WHERE id = ?", (new_name, category_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def add_product(name: str, category_id: int, price: float, description: str):
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("INSERT INTO products (name, category_id, price, description) VALUES (?, ?, ?, ?)",
              (name, category_id, price, description))
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("SELECT p.id, p.name, p.price, p.description, c.name FROM products p JOIN categories c ON p.category_id = c.id")
    products = c.fetchall()
    conn.close()
    return products

def search_products(query: str):
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("SELECT p.id, p.name, p.price, p.description, c.name FROM products p JOIN categories c ON p.category_id = c.id WHERE p.name LIKE ?",
              (f"%{query}%",))
    products = c.fetchall()
    conn.close()
    return products

def delete_product(product_id: int):
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def get_product(product_id: int):
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("SELECT id, name, category_id, price, description FROM products WHERE id = ?", (product_id,))
    product = c.fetchone()
    conn.close()
    return product

def update_product(product_id: int, name: str, category_id: int, price: float, description: str):
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("UPDATE products SET name = ?, category_id = ?, price = ?, description = ? WHERE id = ?",
              (name, category_id, price, description, product_id))
    conn.commit()
    conn.close()