from flask import Flask
from flask_restful import Api, Resource
from flasgger import Swagger
import paho.mqtt.client as mqtt

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app, template_file='swagger.yaml')

class HelloWorld(Resource):
    def get(self):
        """
        A simple GET endpoint
        ---
        tags:
          - HelloWorld
        responses:
          200:
            description: Returns a hello world message
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Hello, World!
        """
        return {'message': 'Hello, World!'}

api.add_resource(HelloWorld, '/')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)

if __name__ == '__main__':
    client.loop_start()
    print("Swagger UI disponible en http://0.0.0.0:5000/apidocs/")
    app.run(host='0.0.0.0', port=5000)