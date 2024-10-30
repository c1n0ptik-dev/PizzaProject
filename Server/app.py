from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')


@app.route('/')
def main():
    return render_template('website/index.html')

<<<<<<< HEAD
@app.route('/orders')
def orders():
    return render_template('cashier-kitchen/orders.html')

=======
>>>>>>> eebd83a3b9e6398786e6457a1405ad5e4a3f78fd

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
