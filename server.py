from flask import Flask, render_template, request, redirect, session

import csv, codecs
from io import StringIO

app = Flask(__name__)
app.secret_key = "BAD_SECRET_KEY"

@app.route("/")
def hello_world():

    data = session.get("data", {})
    keys = session.get("keys", {})

    return render_template(
        "index.html",
        categories=data.keys(),
        data=data,
        keys=keys
    )

@app.route("/upload", methods=["POST"])
def upload_data():
    session.clear()
    data = request.files["data"]
    data.save("data.csv")

    with open("data.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)

        if "data" not in session:
            session["data"] = {}
        if "keys" not in session:
            session["keys"] = {}

        for key, row in enumerate(reader):
            category = row["Category"]

            if category not in session["data"]:
                session["data"][category] = []

            row['key'] = str(key)

            session["keys"][str(key)] = row
            session["data"][category].append(row)

    return redirect("/")

@app.route("/question/<key>")
def render_question(key):
    entry = session.get("keys")[key]
    # session["keys"].pop(key)
    # session.modified = True
    return render_template("question.html", entry=entry)

@app.route("/complete/<key>", methods=["POST"])
def remove_key(key):
    print("called")
    # session["keys"].pop(key)
    # session.modified = True
    return redirect("/")
