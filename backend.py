from flask import Flask, Response, json, request
from flask_mqtt import Mqtt
from time import sleep


app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'silvestri.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

notifications = []

response_await = False
response_data = {}

mqtt = Mqtt(app)


@mqtt.on_connect()
def handle_connect(client, userdata, flasgs, rc):
	mqtt.subscribe('stats')
	mqtt.subscribe('push')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	if message.topic == 'stats':
		global response_await, response_data
		response_data = json.loads(message.payload.decode())
		response_await = False
	elif message.topic == 'push':
		notifications.append(json.loads(message.payload.decode()))


@app.route('/api/get_stats', methods=['POST'])
def api_stats():
	response_await = True
	mqtt.publish('commands', 'stats')
	while response_await:
		sleep(1)
	resp = Response(json.dumps(response_data), status=200, mimetype='application/json')
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
	resp = Response(json.dumps(notifications), status=200, mimetype='application/json')
	return resp


# Test page to check if flask is running
@app.route('/')
def hello_world():
	return 'Hello World!'
