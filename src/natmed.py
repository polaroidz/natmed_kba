from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Natmed Knowledge Based Agent API v1.0.0"