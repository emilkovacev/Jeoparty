from flask import Flask, render_template, request, redirect, session

import csv, codecs
from io import StringIO

app = Flask(__name__)
app.secret_key = "BAD_SECRET_KEY"

@app.route("/")
def hello_world():
    if "data" not in session:
        data = {}
    else:
        data = session["data"]

    print(data)
    return render_template(
        "index.html",
        categories=data.keys(),
        data=data
    )

@app.route("/upload", methods=["POST"])
def upload_data():
    data = request.files["data"]
    data.save("data.csv")

    with open("data.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)

        if "data" not in session:
            session["data"] = {}

        for key, row in enumerate(reader):
            category = row["Category"]
            if category not in session["data"]:
                session["data"][category] = []

            row['key'] = key

            session["data"][category].append(row)

    return redirect("/")

