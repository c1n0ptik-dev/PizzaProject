from flask import Flask, render_template, request, redirect, jsonify, session
import sqlite3
import time
from time import sleep
import serial
import queue
import threading
from threading import Thread
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='templates')
app.secret_key = '123123'

order_queue = queue.Queue()
order_times = []
ser = None
order_id = 0


def get_next_order_id():
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(order_id) FROM Orders")
    max_order = cursor.fetchone()
    max_order_id = max_order[0] if max_order[0] is not None else 0
    conn.close()
    return max_order_id + 1


def calculate_pickup(pickup_time):
    selected_time_str = pickup_time

    hours, minutes, seconds = map(int, selected_time_str.split(':'))
    selected_timedelta = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    current_time = datetime.now()

    future_pickup_time = current_time + selected_timedelta
    future_pickup_time_str = future_pickup_time.strftime('%H:%M:%S')
    return future_pickup_time_str


def initialize_serial():
    global ser
    if ser is None or not ser.is_open:
        ser = serial.Serial("COM3", baudrate=9600, timeout=1)
        time.sleep(2)
    return ser


def add_order(cook_time):
    order_queue.put(cook_time)
    order_times.append(cook_time)
    print(f"Order added with cook time {cook_time}s. Queue size: {order_queue.qsize()}.")


def process_orders():
    global ser
    ser = initialize_serial()
    total_cook_time = 0

    while True:
        if not order_queue.empty():
            cook_time = order_queue.get()
            total_cook_time += cook_time
            ser.write("RedLight\n".encode())
            print("Sent RedLight command to start cooking.")
            time.sleep(cook_time)
            ser.write("GreenLight\n".encode())
            print("Sent GreenLight command. Order ready.")
            order_times.pop(0)

            if order_queue.empty():
                total_cook_time = 0

        time.sleep(0.5)


def change_color(id):
    sleep(12)
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Orders SET Color = ? WHERE OrderId = ?", ('#acacad', id))
    conn.commit()
    conn.close()


def get_data_from_db(table_name):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
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
        order_id = request.form.get('itemid')
        if start_button == 'pressed':
            change_color_thread = Thread(target=change_color, args=(order_id,))
            change_color_thread.start()
            add_order(10)
            order_thread = threading.Thread(target=process_orders, daemon=True)
            order_thread.start()




    elif 'ready' in request.form:
        ready_button = request.form.get('ready')
        if ready_button == 'pressed':
            orderid = request.form.get('item_id')
            conn = sqlite3.connect('database/database.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Orders WHERE OrderId=?", (orderid,))
            conn.commit()

        return redirect("/orders", code=302)

    orders = get_data_from_db("Orders")
    return render_template('cashier-kitchen/orders.html', data=orders)


@app.route('/cashier', methods=['GET', 'POST'])
def cashier():
    if 'delete' in request.form:
        delete_button = request.form.get('delete')
        if delete_button == 'pressed':
            itemid = request.form.get('item_delete_id')
            conn = sqlite3.connect('database/database.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Orders_basket WHERE Id=?", (itemid,))
            conn.commit()

    items = get_data_from_db("Orders_basket")
    return render_template("cashier-kitchen/cashier.html", data=items)


@app.route('/aboutus')
def aboutus():
    return render_template('website/aboutus.html')


@app.route("/workinghours")
def workinghours():
    return render_template("website/work_hours.html")


@app.route('/menu', methods=['GET'])
def menu():
    return render_template('website/menu.html')


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
            cursor.execute("""DELETE FROM Basket; """)
            conn.commit()
            conn.close()

    items = get_data_from_db("Basket")
    print(items)
    return render_template("website/overview.html", data=items)


def calculate_price(pizza_type, size):
    prices = {
        'Margarita': {'small': 5.00, 'medium': 7.00, 'large': 9.00},
        'Tonno': {'small': 6.00, 'medium': 8.00, 'large': 10.00},
        'Funghi': {'small': 5.50, 'medium': 7.50, 'large': 9.50},
        'Diavola': {'small': 6.50, 'medium': 8.50, 'large': 10.50},
        'Coca-Cola': {'small': 1.50, 'medium': 2.00, 'large': 2.50},
        'Water': {'small': 1.00, 'medium': 1.50, 'large': 2.00},
        'Juice': {'small': 1.50, 'medium': 2.00, 'large': 2.50},
        'Sprite': {'small': 1.50, 'medium': 2.00, 'large': 2.50},
    }
    return prices.get(pizza_type, {}).get(size, 0)


@app.route('/add_to_basket', methods=['POST'])
def add_to_basket():
    data = request.get_json()
    pizzaType = data.get('name')
    img = data.get('image')
    size = data.get('size')
    price = calculate_price(pizzaType, size)

    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    if 'current_order_id' not in session:
        session['current_order_id'] = get_next_order_id()

    current_order_id = session['current_order_id']

    cursor.execute('''INSERT INTO Basket (OrderId, PizzaType, Img, Size, Price)
                      VALUES (?, ?, ?, ?, ?)''',
                   (current_order_id, pizzaType, img, size, price))

    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Item added to basket successfully!'}), 200


@app.route('/basket_data', methods=[''])
def basket_data():
    pizzaType = request.form.get('pizzaType')
    img = request.form.get('img')
    size = request.form.get('size')
    price = request.form.get('price')

    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Basket (OrderId, OrderType, Img, Size, Price)
        VALUES (?, ?, ?, ?, ?)
    ''', (orderId, pizzaType, img, size, price))
    conn.commit()
    conn.close()
    return redirect("/basket", code=302)


@app.route('/checkout_order', methods=['POST'])
def checkout_order():
    selected_time = request.form.get('pickup_time')
    if selected_time == "ASAP":
        time = datetime.now().strftime('%H:%M:%S')
    else:
        time = calculate_pickup(selected_time)

    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Basket")
    basket_items = cursor.fetchall()

    new_order_id = get_next_order_id()

    for item in basket_items:
        pizza_type = item[2]
        description = f"Size: {item[4]}"
        toppings = "No topping"
        time_t = f'Pickup time: {time}'
        cursor.execute(''' 
            INSERT INTO Orders (order_id, PizzaType, Description, Toppings, OrderTime)
            VALUES (?, ?, ?, ?, ?)
        ''', (new_order_id, pizza_type, description, toppings, time_t))

    cursor.execute("DELETE FROM Basket")
    conn.commit()
    conn.close()

    return redirect("/success", code=302)


@app.route("/success")
def success():
    return render_template("website/success.html")


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
    size = request.form.get('size')
    toppings = request.form.get('toppings')
    order_time = datetime.now().strftime('%H:%M:%S')
    price = calculate_price(pizza, size)
    print(price, pizza)
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    new_order_id = 0

    cursor.execute(''' 
        INSERT INTO Orders_basket (OrderId, PizzaType, Description, Toppings, OrderTime, Price, size)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (new_order_id, pizza, additional_info, toppings, order_time, price, size))

    conn.commit()
    conn.close()
    print(f"Pizza: {pizza}, Additional Info: {additional_info}, Toppings: {toppings}")
    return redirect("/cashier", code=302)


@app.route('/cashier_orders', methods=['POST'])
def cashier_orders():
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Orders_basket")
    basket_items = cursor.fetchall()

    new_order_id = get_next_order_id()

    for item in basket_items:
        pizza_type = item[2]
        description = item[3]
        toppings = item[4]
        time_t = item[5]
        cursor.execute(''' 
            INSERT INTO Orders (order_id, PizzaType, Description, Toppings, OrderTime)
            VALUES (?, ?, ?, ?, ?)
        ''', (new_order_id, pizza_type, description, toppings, time_t))
    cursor.execute("DELETE FROM Orders_basket")
    conn.commit()
    conn.close()

    return redirect("/cashier", code=302)


if __name__ == "__main__":
    app.debug = True
    app.run()
