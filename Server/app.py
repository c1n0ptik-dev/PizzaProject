from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import requests
import time
import serial

app = Flask(__name__, template_folder='templates')


def get_data_from_db(table_name):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    conn.close()

    return rows


def arduino():
    ser = serial.Serial("COM3", baudrate=9600, timeout=1)
    time.sleep(2)

    ser.write("StartSequence\n".encode())

    while True:
        if ser.in_waiting > 0:
            response = ser.readline().decode().strip()

            if response == "Sequence finished":
                break

    ser.close()


@app.route('/')
def main():
    return render_template('website/index.html')


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if 'start' in request.form:
        start_button = request.form.get('start')

        if start_button == 'pressed':
            arduino()

        return redirect("/orders", code=302)

    elif 'ready' in request.form:
        start_button = request.form.get('ready')
        if start_button == 'pressed':
            orderid = request.form.get('item_id')
            conn = sqlite3.connect('database/database.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Orders WHERE OrderId=?", (orderid,))
            conn.commit()

        return redirect("/orders", code=302)

    orders = get_data_from_db("Orders")
    return render_template('cashier-kitchen/orders.html', data=orders)


@app.route('/cashier', methods=['GET'])
def cashier():
    return render_template('cashier-kitchen/cashier.html')


@app.route('/aboutus')
def aboutus():
    return render_template('website/aboutus.html')


@app.route('/menu', methods=['GET'])
def menu():
    return render_template('website/overview.html')


@app.route('/basket', methods=['GET', 'POST'])
def basket():
    if 'delete' in request.form:
        delete_button = request.form.get('delete')
        if delete_button == 'pressed':
            itemid = request.form.get('item_delete_id')
            conn = sqlite3.connect('database/database.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Basket WHERE Id=?", (itemid,))
            conn.commit()

    elif 'delete_all' in request.form:
        delete_button = request.form.get('delete_all')
        if delete_button == 'pressed':
            conn = sqlite3.connect('database/database.db')
            cursor = conn.cursor()

            cursor.execute("""DELETE FROM Basket;
            VACUUM; """)

    items = get_data_from_db("Basket")
    print(items)
    return render_template("website/overview.html", data=items)



@app.route('/basket_data', methods=[''])
def basket_data():
    pizzaType = request.form.get('pizzaType')
    img = request.form.get('img')
    size = request.form.get('size')
    price = request.form.get('price')

    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Basket (OrderType, Img, Size, Price)
        VALUES (?, ?, ?, ?)
    ''', (pizzaType, img, size, price))

    conn.commit()
    conn.close()

    return redirect("/basket", code=302)


@app.template_filter('sum_list')
def sum_list(array):
    return sum(array)


@app.template_filter('to_int_list')
def to_int_list(string_list):
    return [float(item) for item in string_list]


@app.route('/send_data', methods=['POST'])
def send_data():
    pizza = request.form.get('pizza')
    additional_info = request.form.get('additional_info')
    toppings = request.form.get('toppings')

    order_time = datetime.now().strftime('%H:%M:%S')

    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO Orders (PizzaType, Description, Toppings, OrderTime)
        VALUES (?, ?, ?, ?)
    ''', (pizza, additional_info, toppings, order_time))

    conn.commit()
    conn.close()

    print(f"Pizza: {pizza}, Additional Info: {additional_info}, Toppings: {toppings}")

    return redirect("/cashier", code=302)


if __name__ == "__main__":
    app.debug = True
    app.run()
