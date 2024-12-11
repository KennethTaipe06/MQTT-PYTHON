from flask import Flask
from flask_restful import Api, Resource
from flasgger import Swagger
import paho.mqtt.client as mqtt

# Crear una instancia de Flask
app = Flask(__name__)

# Crear una instancia de Api para manejar los recursos RESTful
api = Api(app)

# Configurar Swagger para la documentación de la API
swagger = Swagger(app, template_file='swagger.yaml')

# Definir un recurso RESTful
class HelloWorld(Resource):
    def get(self):
        """
        Un endpoint GET simple
        ---
        tags:
          - HelloWorld
        responses:
          200:
            description: Devuelve un mensaje de hello world
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Hello, World!
        """
        return {'message': 'Hello, World!'}

# Añadir el recurso HelloWorld a la API en la ruta '/'
api.add_resource(HelloWorld, '/')

# Función de callback cuando el cliente se conecta al broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Suscribirse a un tema específico
    client.subscribe("test/topic")

# Función de callback cuando se recibe un mensaje en un tema suscrito
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# Crear una instancia del cliente MQTT
client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker MQTT
client.connect("broker.hivemq.com", 1883, 60)

# Ejecutar la aplicación Flask y el cliente MQTT
if __name__ == '__main__':
    # Iniciar el bucle del cliente MQTT en segundo plano
    client.loop_start()
    print("Swagger UI disponible en http://0.0.0.0:5000/apidocs/")
    # Ejecutar la aplicación Flask
    app.run(host='0.0.0.0', port=5000)