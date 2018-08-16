import requests


def send_data(parameters):
	url = 'http://127.0.0.1:5000/make_action'
	try:
		r = requests.post(url=url, params=parameters)
		return r.json()
	except ConnectionError:
		print("Connection error occured, check your network or contact @evgerher")