# MoneyTrack - Personal Finance Tracker

A simple and elegant web application for tracking personal income and expenses built with Flask.

## Features

- 🔐 **User Authentication** - Secure login/register with password hashing
- 💰 **Transaction Management** - Add, edit, and delete income/expense transactions
- 📊 **Dashboard** - Overview of financial summary with recent transactions
- 📈 **Monthly Reports** - Visual charts and trends for monthly financial data
- 📱 **Responsive Design** - Works perfectly on desktop and mobile devices
- 🎨 **Modern UI** - Clean and intuitive interface with smooth animations

## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Add Transaction
![Add Transaction](screenshots/add-transaction.png)

### Monthly Report
![Monthly Report](screenshots/monthly-report.png)

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Fonts**: Inter (Google Fonts)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/moneytrack.git
   cd moneytrack
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

## Usage

### First Time Setup
1. Register a new account or use test accounts:
   - Username: `user1`, Password: `password1`
   - Username: `user2`, Password: `password2`

### Adding Transactions
1. Click "Add New Transaction" on dashboard
2. Select transaction type (Income/Expense)
3. Choose category and enter amount
4. Add description (optional)
5. Submit the form

### Managing Transactions
- **Edit**: Click the edit icon next to any transaction
- **Delete**: Click the trash icon and confirm deletion

### Viewing Reports
- Click "Monthly Report" to see financial trends
- Filter by year to view different periods
- View charts and detailed breakdown

## Project Structure

```
moneytrack/
├── app.py                 # Main Flask application
├── database.py           # Database functions
├── expenses.db           # SQLite database
├── check_db.py          # Database inspection utility
├── templates/           # HTML templates
│   ├── dashboard.html
│   ├── add_expense.html
│   ├── edit_expense.html
│   ├── monthly_report.html
│   ├── login.html
│   └── register.html
└── README.md
```

## Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `password` - Hashed password (SHA-256)

### Expenses Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `type` - Transaction type (income/expense)
- `category` - Transaction category
- `amount` - Transaction amount
- `description` - Optional description
- `date` - Timestamp

## Categories

### Income Categories
- 💼 Salary
- 🎁 Bonus
- 💻 Freelance
- 📈 Investment
- 🎯 Gift
- 💰 Other Income

### Expense Categories
- 🍔 Food & Dining
- 🚗 Transportation
- 🎬 Entertainment
- 📱 Bills & Utilities
- 🛍️ Shopping
- 🏥 Health & Medical
- 📦 Other Expense

## Security Features

- Password hashing using SHA-256
- Session-based authentication
- Input validation and sanitization
- SQL injection prevention

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created with ❤️ by [Your Name]

## Acknowledgments

- Flask framework for the backend
- Chart.js for beautiful charts
- Font Awesome for icons
- Inter font family for typography