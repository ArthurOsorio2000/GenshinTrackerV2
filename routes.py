from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Index Page"

@app.route("/holly")
def holly():
    return "<p>Love u Holly!</p>"