from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/commands')
def commands():
    return jsonify(message='')


if __name__ == '__main__':
    app.run()
