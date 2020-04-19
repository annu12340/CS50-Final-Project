from flask import Flask, render_template, request, redirect, session, logging, url_for
from flask_sqlalchemy import SQLAlchemy
from helper import *
import yfinance as yf

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']

        data = User.query.filter_by(email=email, password=password).first()
        print("data is", data)

        if login is not None:
            return redirect(url_for("home"))
        return render_template("login.html")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(email=request.form['email'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


@app.route('/show')
def show():
    show_user = User.query.all()
    return render_template('show.html', show_user=show_user)


@app.route('/quote', methods=['GET', 'POST'])
def quote():
    """Get stock quote."""

    if request.method == "POST":
        print("mehtiod is", request.method)
        if not request.form.get("quote"):
            return apology("no quote provided")

        symbol = request.args.get('symbol', default="AAPL")

        # pull the stock quote
        quote = yf.Ticker(symbol)

        # return the object via the HTTP Response
        return quote.info

        if quote == None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", quote=quote)

    # User reached route via GET (as by clicking a link or via redi)
    else:
        return render_template("quote.html")


@app.route('/buy')
def buy():
    return render_template('buy.html')


@app.route('/sell')
def sell():
    return render_template('sell.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    db.create_all()
    print('after db.create_all()')
    app.run(debug=True)
