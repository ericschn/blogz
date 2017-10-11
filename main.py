from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

# flask setup
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '8g753o9raNd0m5tuFf'

# build the class that determines database table layout
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2048))

    def __init__(self, title, body):
        self.title = title
        self.body = body

def title_verify(s):
    if len(s) < 2 or len(s) > 88:
        return False
    return True

def body_verify(s):
    if len(s) < 5 or len(s) > 2020:
        return False
    return True

@app.route('/') # root redirects to the blog page
def root_redirect():
    return redirect('/blog')

@app.route('/blog')
def index():
    blogid = request.args.get('id')
    blogs = [blog for blog in Blog.query.all()]

    if blogid:
        singleblog = Blog.query.filter_by(id=blogid).first()
        return render_template('singleblog.html', singleblog=singleblog)

    return render_template('index.html', blogs=blogs)

@app.route('/add', methods=['POST', 'GET'])
def add():
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
        db.session.add(Blog(title, body))
        db.session.commit()
        new_blog = Blog.query.filter_by(title=title).first()
        new_blog_id = str(new_blog.id)

        return redirect('/blog?id=' + new_blog_id)


    return render_template('add.html')

if __name__ == '__main__':
    app.run()
