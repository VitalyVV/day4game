from flask import (Flask, jsonify)
import json


app = Flask(__name__)

app.config.update(
	SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)

@app.route("/")
def index():
	return "Hell world"

@app.route("/make_action", methods=["GET", "POST"])
def fight():
	return jsonify({'dogs': 15}), 200