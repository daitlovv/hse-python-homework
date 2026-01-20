from flask import Flask, jsonify
from dotenv import dotenv_values

def get_port():
    config = dotenv_values(".env")
    if "PORT" in config:
        return config["PORT"]
    return 5000
    

app = Flask(__name__)


@app.route("/")
def server_info():
    return "My server"


@app.route("/author")
def author():
    author = {
        "name": "Kristina",
        "course": 2,
        "age": 19,
    }
    return jsonify(author)


if __name__ == "__main__":
    app.run(debug=True, port=get_port())
