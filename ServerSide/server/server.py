from flask import (Flask, jsonify, request, json)
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
	print(request.args)
	data = request.args
	return jsonify({'dogs': 15}), 200