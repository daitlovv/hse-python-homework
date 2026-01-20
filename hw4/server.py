from flask import Flask, jsonify

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
    app.run(debug=True, port=5000)
