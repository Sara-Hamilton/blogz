from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:letsmingle@localhost:8889/blogz'
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(30))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


def validate_title(title):
    title, title_error = title, ""
    if title == "":
        title_error = "Blog entry must have a title."
    return title, title_error

def validate_body(body):
    body, body_error = body, ""
    if body == "":
        body_error = "Blog entry must have content."
    elif len(body) > 5000:
        body_error = "Blog entry cannot be more than 5000 characters long."
    return body, body_error

@app.route('/blog', methods=["POST", "GET"])
def index():
    entries = Blog.query.all()
    
    if "id" in request.args:
        id = request.args.get('id')
        entry = Blog.query.get(id)
        
        return render_template('entries.html', page_title="blog-post", title = entry.title, body = entry.body)
    
    return render_template('posts.html', page_title="blog", entries = entries)


@app.route('/newpost', methods=["POST", "GET"])
def add_entry():
  
    return render_template('newpost.html', page_title="blog")


@app.route('/validate', methods=["POST", "GET"])
def validate():
    title, title_error = validate_title(request.form["title"])
    body, body_error = validate_body(request.form["body"])
    
    if not title_error and not body_error:
        if request.method == "POST":
            title_name = request.form['title']
            body_name = request.form['body']
            # owner_name = (fill this in)
            new_entry = Blog(title_name, body_name) # add owner_name to this list
            db.session.add(new_entry)
            db.session.commit()
        
        return render_template('entries.html', page_title = "confirmation", title = title, body = body)
    else:
        return render_template('newpost.html', page_title = "blog", title = title, title_error = title_error, body = body, body_error = body_error)


if __name__ == '__main__':
    app.run()