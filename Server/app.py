from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder='templates')


def connect_database():
    con = sqlite3.connect("database/database.db")
    cur = con.cursor()
    print("Database has Successfully Connected!")


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

    # Print the data to the console
    print(f"Pizza: {pizza}, Additional Info: {additional_info}, Toppings: {toppings}")

    return "Data received!"  # Response for form submission


if __name__ == "__main__":
    app.debug = True
    app.run()
