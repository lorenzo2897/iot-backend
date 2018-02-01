import paho.mqtt.client as mqtt

class IotClient:
    
    def __init__(self, ip, port):
        self.client = mqtt.Client()
        self.client.connect(ip, port, 60)
    def __exit__(self, exc_type, exc_value, traceback):
        client.disconnect()
    
    def test(self, topic = 'Debug', message = 'Hello'):
        self.client.publish(topic, message)
    
