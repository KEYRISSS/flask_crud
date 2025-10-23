from flask import Flask
from flask_restful import Api

# Inicializar la app y la API
app = Flask(__name__)
api = Api(app)

# Importar rutas usando importación relativa
from .routes import *
