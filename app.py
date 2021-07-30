from flask import Flask, request, render_template, redirect, session
import sqlite3
from flask.globals import session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from tempfile import mkdtemp
from functools import wraps




app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods =['GET', 'POST'])
#@login_required
def index():
    """Shows all posts on the wall starting from the most upvoted to the last"""
    #TODO    

    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute("SELECT * FROM posts;")

    posts = [dict(row) for row in cursor.fetchall()]



    return render_template("index.html", posts = posts)

@app.route("/register", methods = ['GET', 'POST'])
def register():
    """Request user to register"""

    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirm =  request.form.get("confirmation")

        if not name:
            message = "You must input a username to register"
            return render_template("apology.html", message=message)

        if not password == confirm:
            message = "Your password and confirm must match"
            return render_template("apology.html", message = message)
        
        db = sqlite3.connect('database.db')
        
        cursor = db.cursor()
        
        cursor.execute("INSERT INTO users (user, hash) VALUES (?, ?);", (name, generate_password_hash(password)))

        db.commit()

        db.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    """Request user to login"""

    if request.method == "POST":
        session.clear()
        name = request.form.get("username")
        password = request.form.get("password")

        db = sqlite3.connect("database.db")
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE user = ?;",(name,))

        login = [dict(row) for row in cursor.fetchall()]

        if name != login[0]['user']:
            message = "You must provide a valid username"
            return render_template("apology.html", message = message)
        
        if not check_password_hash(login[0]['hash'] ,password):
            message = "You must provide a valid password"
            return render_template("apology.html", message = message)
        
        session["user_id"] = login[0]['id']
        
        return redirect("/post")
    try:
        if session["user_id"] != None:
            return redirect('/post')
    except:
        return render_template("login.html")

@app.route("/post", methods = ['GET', 'POST'])
@login_required
def post():
    """Input to post on the wall"""

    if request.method == "POST":
        post = request.form.get("post")

        db = sqlite3.connect("database.db")
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        cursor.execute("INSERT INTO posts (user_id, post, upvote) VALUES (?, ?, 0)", (session["user_id"], post))

        db.commit()
        db.close()

        return redirect('/')

    return render_template("post.html")

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/login")

@app.route("/history")
@login_required
def history():

    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute("SELECT * FROM posts WHERE user_id = ?;", (session["user_id"],))

    posts = [dict(row) for row in cursor.fetchall()]




    return render_template("history.html", posts = posts)

@app.route("/upvote", methods = ['POST'])
@login_required
def upvote():

    post_id = request.form.get("post_id")
    
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute("SELECT * FROM posts WHERE post_id = ?", (post_id, ))

    rows = [dict(row) for row in cursor.fetchall()]

    if rows[0]["upvoted_by"] == None:

        rows[0]["upvoted_by"] = str(session["user_id"])
        
    elif str(session["user_id"]) in list(rows[0]["upvoted_by"].split(',')):
        message = "You already upvoted for this post :)"
        return render_template("apology.html", message = message)
    else:
        rows[0]["upvoted_by"] += "," + str(session["user_id"])
    
        if rows[0]["upvote"] == None:
            rows[0]["upvote"] = 1
        else:
            rows[0]["upvote"] += 1
    
        cursor.execute("UPDATE posts SET upvoted_by = ?, upvote = ? WHERE post_id =?", (rows[0]["upvoted_by"], rows[0]["upvote"], post_id))

        db.commit()

        db.close()

        return redirect("/")







