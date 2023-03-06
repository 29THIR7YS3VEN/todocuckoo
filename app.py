from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db import *

app = Flask(__name__)
db = SQL("sqlite:///main.db")

dbinit()


@app.route("/")
def home():
    if session:
        user = db.execute("SELECT * FROM users WHERE id == :id",
                          id=session["id"]
                          )
        tasks = db.execute(
            "SELECT * FROM tasks WHERE username = :username", username=user[0]["_username"])
        return render_template("dash.html")
    else:
        return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        check = db.execute(
            "SELECT * FROM users WHERE _username == :username", username=username)

        if len(check) > 0:
            flash("That username is taken")
            return redirect("/signup")
        else:
            db.execute("INSERT INTO users (_username, _password) VALUES (:username, :password)",
                       username=username,
                       password=generate_password_hash(password)
                       )
            user = db.execute(
                "SELECT * FROM users WHERE _username = :username", username=username)

            session["id"] = user[0]["id"]
            return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        check = db.execute(
            "SELECT * FROM users WHERE _username == :username", username=username)

        if len(check) > 0:
            if check_password_hash(check[0]["_password"], password) == 0:
                session["id"] = check[0]["id"]
                return redirect("/")
            else:
                flash("Username or password is incorrect")
                return redirect("/login")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        title = request.form.get("title")
        description = request.form.get("description")
        category = request.form.get("category")
        due = request.form.get("due")

        db.execute("INSERT INTO tasks (username, _title, _description, _due, _complete, _type) VALUES (:username, :title, :description, :due, :complete, :type)",
                   username=session["id"],
                   title=title,
                   description=description,
                   due=due,
                   complete=False,
                   type=category
                   )

        flash("Task added successfully.")
        return redirect("/")
