from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:tellmemore@localhost:8889/build-a-blog'
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(999))

    def __init__(self, title, body):
        self.title = title
        self.body = body


def validate_title(title):
    title, title_error = title, ""
    if title == "":
        title_error = "Blog entry must have a title."
    return title, title_error

def validate_body(body):
    body, body_error = body, ""
    if body == "":
        body_error = "Blog entry must have content."
    return body, body_error

@app.route('/', methods=["POST", "GET"])
def index():
    entries = Blog.query.all()
    return render_template('posts.html', page_title="blog", entries = entries)


@app.route('/add-entry', methods=["POST", "GET"])
def add_entry():
    
    if request.method == "POST":
        title_name = request.form['title']
        body_name = request.form['body']
        new_entry = Blog(title_name, body_name)
        db.session.add(new_entry)
        db.session.commit()

    entries = Blog.query.all()
    
    return render_template('add-entry.html', page_title="blog", entries=entries)


@app.route('/validate', methods=["POST", "GET"])
def validate():

    title, title_error = validate_title(request.form["title"])
    body, body_error = validate_body(request.form["body"])
    
    if not title_error and not body_error:
        if request.method == "POST":
            title_name = request.form['title']
            body_name = request.form['body']
            new_entry = Blog(title_name, body_name)
            db.session.add(new_entry)
            db.session.commit()

        return render_template('confirmation.html', page_title = "confirmation")
    else:
        return render_template('add-entry.html', page_title = "blog", title = title, title_error = title_error, body = body, body_error = body_error)


if __name__ == '__main__':
    app.run()