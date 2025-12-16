import sqlite3
from datetime import datetime, timedelta

def add_test_data():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    
    # Data test untuk berbagai tahun/bulan
    test_data = [
        # 2022 data
        (1, 'income', 'Salary', 5000000, 'Gaji bulanan', '2022-01-15 10:00:00'),
        (1, 'expense', 'Food', 500000, 'Makan bulanan', '2022-01-20 12:00:00'),
        (1, 'expense', 'Transport', 300000, 'Bensin', '2022-02-10 08:00:00'),
        
        # 2023 data  
        (1, 'income', 'Salary', 6000000, 'Gaji bulanan', '2023-03-15 10:00:00'),
        (1, 'expense', 'Food', 600000, 'Makan bulanan', '2023-03-20 12:00:00'),
        (1, 'income', 'Bonus', 1000000, 'Bonus tahunan', '2023-12-20 14:00:00'),
        
        # 2024 data (current)
        (1, 'income', 'Salary', 7000000, 'Gaji bulanan', '2024-01-15 10:00:00'),
        (1, 'expense', 'Food', 700000, 'Makan bulanan', '2024-01-20 12:00:00'),
        (1, 'expense', 'Entertainment', 500000, 'Nongkrong', '2024-02-05 20:00:00'),
        (1, 'income', 'Freelance', 2000000, 'Project freelance', '2024-02-10 16:00:00'),
    ]
    
    for data in test_data:
        try:
            c.execute('''INSERT INTO expenses 
                        (user_id, type, category, amount, description, date) 
                        VALUES (?, ?, ?, ?, ?, ?)''', data)
            print(f"Added: {data}")
        except Exception as e:
            print(f"Error adding {data}: {e}")
    
    conn.commit()
    conn.close()
    print("Test data added successfully!")

if __name__ == "__main__":
    add_test_data()