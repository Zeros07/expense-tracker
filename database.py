import sqlite3
import os
import hashlib

# Database path - use /tmp for serverless environments
DB_PATH = os.environ.get('DATABASE_URL', '/tmp/expenses.db') if os.environ.get('VERCEL') else 'expenses.db'

def init_db():
    """Initialize database and create tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    
    # Create expenses table
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER NOT NULL,
                  type TEXT NOT NULL,
                  category TEXT NOT NULL,
                  amount REAL NOT NULL,
                  description TEXT,
                  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Insert some test users with hashed passwords
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                 ('user1', hash_password('password1')))
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                 ('user2', hash_password('password2')))
    except:
        pass  # Users already exist
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Create new user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        hashed_password = hash_password(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                 (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_username(username):
    """Get user by username"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_expense(user_id, type_, category, amount, description):
    """Add new expense/income"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO expenses (user_id, type, category, amount, description)
                 VALUES (?, ?, ?, ?, ?)''',
              (user_id, type_, category, amount, description))
    conn.commit()
    conn.close()

def get_user_expenses(user_id):
    """Get all expenses for a user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT * FROM expenses 
                 WHERE user_id = ? 
                 ORDER BY date DESC''', (user_id,))
    expenses = c.fetchall()
    conn.close()
    return expenses



def get_expense_by_id(expense_id, user_id):
    """Get single expense by ID for editing"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id))
    expense = c.fetchone()
    conn.close()
    return expense

def update_expense(expense_id, user_id, type_, category, amount, description):
    """Update existing expense"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''UPDATE expenses 
                 SET type = ?, category = ?, amount = ?, description = ?
                 WHERE id = ? AND user_id = ?''',
              (type_, category, amount, description, expense_id, user_id))
    conn.commit()
    conn.close()

def delete_expense(expense_id, user_id):
    """Delete expense"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id))
    conn.commit()
    conn.close()

def get_monthly_summary(user_id, year):
    """Get monthly summary for the year"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    query = '''
    SELECT 
        strftime('%m', date) as month,
        type,
        SUM(amount) as total
    FROM expenses 
    WHERE user_id = ? AND strftime('%Y', date) = ?
    GROUP BY strftime('%m', date), type
    ORDER BY month
    '''
    
    c.execute(query, (user_id, str(year)))
    results = c.fetchall()
    conn.close()
    
    # Process results into monthly data
    monthly_data = {}
    for i in range(1, 13):
        month_key = f"{i:02d}"
        monthly_data[month_key] = {
            'income': 0,
            'expense': 0,
            'balance': 0
        }
    
    for month, type_, total in results:
        if month in monthly_data:
            monthly_data[month][type_] = total
            monthly_data[month]['balance'] = monthly_data[month]['income'] - monthly_data[month]['expense']
    
    return monthly_data

def get_detailed_monthly_data(user_id, year, month=None):
    """Get detailed monthly data with category breakdown"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if month:
        # Get specific month data
        query = '''
        SELECT type, category, amount, description, date
        FROM expenses 
        WHERE user_id = ? AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
        ORDER BY date DESC
        '''
        c.execute(query, (user_id, str(year), f"{month:02d}"))
    else:
        # Get full year data
        query = '''
        SELECT type, category, amount, description, date
        FROM expenses 
        WHERE user_id = ? AND strftime('%Y', date) = ?
        ORDER BY date DESC
        '''
        c.execute(query, (user_id, str(year)))
    
    transactions = c.fetchall()
    conn.close()
    
    # Process data
    income_categories = {}
    expense_categories = {}
    total_income = 0
    total_expense = 0
    
    for type_, category, amount, description, date in transactions:
        if type_ == 'income':
            total_income += amount
            if category not in income_categories:
                income_categories[category] = {'total': 0, 'transactions': []}
            income_categories[category]['total'] += amount
            income_categories[category]['transactions'].append({
                'amount': amount,
                'description': description,
                'date': date
            })
        else:
            total_expense += amount
            if category not in expense_categories:
                expense_categories[category] = {'total': 0, 'transactions': []}
            expense_categories[category]['total'] += amount
            expense_categories[category]['transactions'].append({
                'amount': amount,
                'description': description,
                'date': date
            })
    
    # Calculate percentages
    for category in income_categories:
        income_categories[category]['percentage'] = round((income_categories[category]['total'] / total_income) * 100, 1) if total_income > 0 else 0
    
    for category in expense_categories:
        expense_categories[category]['percentage'] = round((expense_categories[category]['total'] / total_expense) * 100, 1) if total_expense > 0 else 0
    
    return {
        'income_categories': income_categories,
        'expense_categories': expense_categories,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
        'transaction_count': len(transactions)
    }