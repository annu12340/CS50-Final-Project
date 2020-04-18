from flask import Flask ,render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if str(request.method) == 'POST':
        email = request.form['email']
        password = request.form['password']
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>Added New User!</h1>'
    else:
        return render_template('login.html')



@app.route('/show')
def show():
    show_user=User.query.all()
    return render_template('show.html', show_user=show_user)


@app.route('/quote')
def quote():
    return render_template('quote.html')



@app.route('/buy')
def buy():
    return render_template('buy.html')


@app.route('/sell')
def sell():
    return render_template('sell.html')


if __name__ == '__main__':
    db.create_all()
    print('after db.create_all()')
    app.run(debug=True)
