from flask import Flask
from MQTTclient import IotClient

app = Flask(__name__)

@app.route('/')
def hello_world():
    commInter = IotClient("127.0.0.1", 1883)
    commInter.test("Debug", "Hello")
    return 'Hello, World!'