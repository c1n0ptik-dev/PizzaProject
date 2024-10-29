from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/cashier', methods=['GET'])
def main():
    return render_template('cashier.html')


@app.route('/send_data', methods=['POST'])
def send_data():
    pass


if __name__ == "__main__":
    app.debug = True
    app.run()
