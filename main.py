from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '8g753o9raNd0m5tuFf'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2048))

    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body

@app.route('/blog')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    if 


    return render_template('add.html')

if __name__ == '__main__':
    app.run()
