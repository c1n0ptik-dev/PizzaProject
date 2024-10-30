from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__, template_folder='templates')


def get_data_from_db():
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Orders")
    rows = cursor.fetchall()

    conn.close()

    return rows


@app.route('/')
def main():
    return render_template('website/index.html')


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if 'start' in request.form:
        start_button = request.form.get('start')
        return redirect("/orders", code=302)

    elif 'ready' in request.form:
        ready_button = request.form.get('ready')
        return redirect("/orders", code=302)

    orders = get_data_from_db()
    return render_template('cashier-kitchen/orders.html', data=orders)


@app.route('/cashier', methods=['GET'])
def cashier():
    return render_template('cashier-kitchen/cashier.html')


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

    return redirect("/cashier", code=302)  # Response for form submission


if __name__ == "__main__":
    app.debug = True
    app.run()
