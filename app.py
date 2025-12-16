from flask import Flask, render_template, request, redirect, session, flash
import database as db
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# Initialize database
db.init_db()


@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    # Get user's expenses
    expenses = db.get_user_expenses(session["user_id"])

    # Calculate totals
    total_income = 0
    total_expense = 0
    
    for exp in expenses:
        if exp[2] == "income":
            total_income += exp[4]
        else:
            total_expense += exp[4] 
    
    balance = total_income - total_expense

    return render_template(
        "dashboard.html",
        username=session["username"],
        expenses=expenses,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = db.get_user_by_username(username)
        if user and user[2] == db.hash_password(password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/")
        else:
            flash("Invalid username or password")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Validation
        if not username or not password:
            flash("Please fill all fields")
        elif password != confirm_password:
            flash("Passwords do not match")
        elif len(username) < 3:
            flash("Username must be at least 3 characters")
        elif len(password) < 4:
            flash("Password must be at least 4 characters")
        else:
            # Create new user
            if db.create_user(username, password):
                flash("Registration successful! Please login.")
                return redirect("/login")
            else:
                flash("Username already exists")

    return render_template("register.html")








@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        type_ = request.form["type"]
        category = request.form["category"]

        amount_str = request.form["amount_raw"]
        amount = float(amount_str) if amount_str else 0

        description = request.form["description"]

        db.add_expense(session["user_id"], type_, category, amount, description)

        # Redirect dengan parameter untuk notifikasi
        if type_ == "income":
            return redirect("/?notification=income_success")
        else:
            return redirect("/?notification=expense_success")

    return render_template("add_expense.html")


@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    if "user_id" not in session:
        return redirect("/login")
    
    expense = db.get_expense_by_id(expense_id, session["user_id"])
    if not expense:
        flash("Transaction not found")
        return redirect("/")
    
    if request.method == "POST":
        type_ = request.form["type"]
        category = request.form["category"]
        amount_str = request.form["amount_raw"]
        amount = float(amount_str) if amount_str else 0
        description = request.form["description"]
        
        db.update_expense(expense_id, session["user_id"], type_, category, amount, description)
        flash("Transaction updated successfully!")
        return redirect("/")
    
    return render_template("edit_expense.html", expense=expense)

@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense_route(expense_id):
    if "user_id" not in session:
        return redirect("/login")
    
    expense = db.get_expense_by_id(expense_id, session["user_id"])
    if expense:
        db.delete_expense(expense_id, session["user_id"])
        flash("Transaction deleted successfully!")
    else:
        flash("Transaction not found")
    
    return redirect("/")

@app.route("/monthly-report")
def monthly_report():
    if "user_id" not in session:
        return redirect("/login")
    
    current_year = datetime.now().year
    year = request.args.get('year', str(current_year))
    monthly_data = db.get_monthly_summary(session["user_id"], year)
    
    # Generate year range (current year + 1 to current year - 5)
    years = list(range(current_year + 1, current_year - 6, -1))
    
    return render_template("monthly_report.html", 
                         monthly_data=monthly_data, 
                         selected_year=year,
                         username=session["username"],
                         years=years)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)