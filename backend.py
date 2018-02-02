from flask import Flask, Response, json, request
from flask_mqtt import Mqtt
import httplib, urllib

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'silvestri.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

notifications = []
json_stats = json.loads("{}")

mqtt = Mqtt(app)

key = 'key=AAAAHLKcF84:APA91bFNR4KXaE5zcTTSSkFRxIoTTYEmIAdRqqAHFeO5-N1Rmb9gOmCKOAYk5Ho9ckOcrbeVx5u09GRB_MbaUsycbk03S2QprA9qaMyUlMqHeEsYkYKuiswHM9otndSt_CgyyI9US3Rl'
headers = {
				"Content-Type": "application/json",
				"Authorization": key
			}

@mqtt.on_connect()
def handle_connect(client, userdata, flasgs, rc):
	mqtt.subscribe('stats')
	mqtt.subscribe('push')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	if message.topic == 'stats':
		global json_stats
		json_stats = json.loads(message.payload.decode())
	elif message.topic == 'push':
		conn = httplib.HTTPSConnection("fcm.googleapis.com:443")
		data = json.dumps({
			"to": "/topics/tea",
			"data": json.loads(message.payload.decode())
			})
		conn.request("POST", "/fcm/send", data, headers)
		response = conn.getresponse()
		print response.status, response.reason
		notifications.append(json.loads(message.payload.decode()))


@app.route('/api/get_stats', methods=['POST'])
def api_stats():
	mqtt.publish('commands', 'stats')
	resp = Response(json.dumps(json_stats), status=200, mimetype='application/json')
	return resp


@app.route('/api/make_tea', methods=['POST'])
def api_make_tea():
	mqtt.publish('commands', 'make_tea')
	resp = Response('{"done": True}', status=200, mimetype='application/json')
	return resp


@app.route('/api/abort', methods=['POST'])
def api_abort():
	mqtt.publish('commands', 'abort')
	resp = Response('{"done": True}', status=200, mimetype='application/json')
	return resp


@app.route('/api/update_settings', methods=['POST'])
def api_update_settings():
	mqtt.publish('set', request.form.get('data'))
	resp = Response('{"done": True}', status=200, mimetype='application/json')
	return resp


@app.route('/api/notifications', methods=['POST'])
def api_notifications():
	global notifications
	resp = Response(json.dumps(notifications), status=200, mimetype='application/json')
	notifications = []
	return resp


# Test page to check if flask is running
@app.route('/')
def hello_world():
	return 'Hello World!'
