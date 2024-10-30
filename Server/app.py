from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime


app = Flask(__name__, template_folder='templates')

@app.route('/')
def main():
    return render_template('website/index.html')


@app.route('/orders')
def orders():
    return render_template('cashier-kitchen/orders.html')

@app.route('/cashier', methods=['GET'])
def cashier():
    return render_template('cashier-kitchen/cashier.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/send_data', methods=['POST'])
def send_data():
    # Retrieve data from the form
    pizza = request.form.get('pizza')
    additional_info = request.form.get('additional_info')
    toppings = request.form.get('toppings')

    # Current timestamp
    order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert data into the database
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Orders (PizzaType, Description, Toppings, OrderTime)
        VALUES (?, ?, ?, ?)
    ''', (pizza, additional_info, toppings, order_time))
    conn.commit()
    conn.close()

    # Print the data to the console
    print(f"Pizza: {pizza}, Additional Info: {additional_info}, Toppings: {toppings}")

    return redirect("/cashier", code=302) # Response for form submission


if __name__ == "__main__":
    app.debug = True
    app.run()
