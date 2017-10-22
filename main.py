from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


# flask setup
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '8g753o9raNd0m5tuFf'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2048))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

def title_verify(s):
    if len(s) < 2 or len(s) > 88:
        return False
    return True

def body_verify(s):
    if len(s) < 5 or len(s) > 2020:
        return False
    return True

@app.route('/')
def index():
    userlist = User.query.all()
    for i in userlist:
        print(i)
    return render_template('index.html', userlist=userlist)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()

        if existing_user and password == existing_user.password:
            # successful login
            session['username'] = username
            flash('Logged in')
            return redirect('/')
        else:
            flash('Invalid login details')
            return redirect('/login')

    return render_template('/login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()
        errors = 0
        # TODO signup check
        if len(username) > 20 or len(username) < 3:
            flash('Invalid username length, 3-20')
            errors += 1
        # user exists?
        if existing_user:
            flash('User already exists')
            errors += 1
        # verify pass
        if len(password) < 6 or len(password) > 25:
            flash('Invalid password length, 6-20')
            errors += 1
        if password != verify:
            flash('Passwords do not match')
            errors += 1
        if errors:
            return redirect('/signup')
        else:
            flash('Logged in')
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')

        
    return render_template('/signup.html')

@app.route('/blog')
def blog():
    # show all posts
    blogid = request.args.get('id')
    user = request.args.get('user')
    blogs = [blog for blog in Blog.query.all()]

    if blogid:
        singleblog = Blog.query.filter_by(id=blogid).first()
        return render_template('singleblog.html', blog=singleblog)

    if user:
        userid = User.query.filter_by(username=user).first()
        userblogs = [blog for blog in Blog.query.filter_by(owner_id=userid.id)]
        return render_template('blog.html', blogs=userblogs)

    return render_template('blog.html', blogs=blogs)

@app.route('/add', methods=['POST', 'GET'])
def add():
    if session['username']:
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            # check length of title and body
            if not title_verify(title):
                flash('Invalid Title')
                return redirect('/add')

            if not body_verify(body):
                flash('Invalid Body')
                return redirect('/add')

            owner = User.query.filter_by(username=session['username']).first() 
            db.session.add(Blog(title, body, owner))
            db.session.commit()
            new_blog = Blog.query.filter_by(title=title).first()
            new_blog_id = str(new_blog.id)
            return redirect('/blog?id=' + new_blog_id)
        return render_template('add.html')

@app.route('/logout')
def logout():
    del session['username']
    flash('Logged out')
    return redirect('/')

if __name__ == '__main__':
    app.run()
