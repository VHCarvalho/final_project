from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods =['GET', 'POST'])
def index():
    """Shows all posts on the wall starting from the most upvoted to the last"""
    #TODO    
    return render_template("index.html")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    """Request user to register"""
    #TODO
    return render_template("register.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    """Request user to login"""
    #TODO
    return render_template("login.html")
@app.route("/dash", methods = ['GET', 'POST'])
def dash():
    """Request user to dash"""
    #TODO
    return render_template("dash.html")