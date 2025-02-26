import sqlite3

def create_tables():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'staff'))
    )''')
    
    # Menu Items Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS MenuItems (
        item_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        available INTEGER DEFAULT 1,
        ingredient_id INTEGER,
        FOREIGN KEY(ingredient_id) REFERENCES Inventory(ingredient_id)
    )''')
    
    # Orders Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
        order_id INTEGER PRIMARY KEY,
        table_number INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        total_price REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES Users(user_id))
    ''')
    
    # Order Details Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS OrderDetails (
        order_detail_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY(order_id) REFERENCES Orders(order_id),
        FOREIGN KEY(item_id) REFERENCES MenuItems(item_id))
    ''')
    
    # Inventory Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Inventory (
        ingredient_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        quantity REAL NOT NULL,
        reorder_level REAL NOT NULL)
    ''')
    


def fetch_menu_items():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM MenuItems')
    items = cursor.fetchall()
    conn.close()
    
    if items:
        print("Menu Items:")
        for item in items:
            print(item)
    else:
        print("No menu items found.")

if __name__ == "__main__":
    create_tables()
    fetch_menu_items()
