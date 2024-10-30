from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import requests
import time
import serial

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

        if start_button == 'pressed':

            order_number = 1
            command = f"Order{order_number}"
            ser.write((command + "\n").encode())  # Send the command with order number to Arduino

            print(f"Cooking started for Order {order_number}. Waiting for completion...")

            # Wait for response from Arduino
            while True:
                if ser.in_waiting > 0:
                    response = ser.readline().decode().strip()
                    if response == f"Order {order_number} finished":
                        print(f"Order {order_number} is ready! Green LED is now ON.")
                        break
                time.sleep(1)
            start_button = ''

        return redirect("/orders", code=302)

    elif 'ready' in request.form:
        start_button = request.form.get('ready')
        if start_button == 'pressed':
            id = request.form.get('item_id')
            conn = sqlite3.connect('database/database.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Orders WHERE OrderId=?", (id,))
            conn.commit()

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
    order_time = datetime.now().strftime('%H:%M:%S')

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
