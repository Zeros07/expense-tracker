import sqlite3

def check_database():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    
    # Cek tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    print("Tables in database:", tables)
    
    # Cek users
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    print("Users:", users)
    
    # Cek expenses
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    print("Expenses:", expenses)
    
    conn.close()

if __name__ == '__main__':
    check_database()