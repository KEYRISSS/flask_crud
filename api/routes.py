from flask import jsonify
from flask_restful import Resource, fields, marshal_with, reqparse
from . import api, app

# --- Ruta raíz ---
@app.route("/")
def index():
    return jsonify({"message": "Bienvenido a la API de videojuegos"})

# --- Lista de juegos en memoria ---
JUEGOS = []
NEXT_ID = 1

# Campos para serialización
juego_fields = {
    'id': fields.Integer,
    'nombre': fields.String,
    'categoria': fields.String,
    'plataforma': fields.String,
    'precio': fields.Float
}

# Parser para POST/PUT
juego_parser = reqparse.RequestParser()
juego_parser.add_argument('nombre', type=str, required=True, help="Nombre obligatorio")
juego_parser.add_argument('categoria', type=str, required=True)
juego_parser.add_argument('plataforma', type=str, required=True)
juego_parser.add_argument('precio', type=float, required=True)

# --- Recurso JuegoList ---
class JuegoList(Resource):
    @marshal_with(juego_fields)
    def get(self):
        return JUEGOS

    @marshal_with(juego_fields)
    def post(self):
        global NEXT_ID
        args = juego_parser.parse_args()
        juego = {
            'id': NEXT_ID,
            'nombre': args['nombre'],
            'categoria': args['categoria'],
            'plataforma': args['plataforma'],
            'precio': args['precio']
        }
        JUEGOS.append(juego)
        NEXT_ID += 1
        return juego, 201

# --- Recurso JuegoResource ---
class JuegoResource(Resource):
    @marshal_with(juego_fields)
    def get(self, id):
        juego = next((j for j in JUEGOS if j['id'] == id), None)
        if not juego:
            return {"message": "Juego no encontrado"}, 404
        return juego

    @marshal_with(juego_fields)
    def put(self, id):
        args = juego_parser.parse_args()
        juego = next((j for j in JUEGOS if j['id'] == id), None)
        if not juego:
            return {"message": "Juego no encontrado"}, 404
        juego.update({
            'nombre': args['nombre'],
            'categoria': args['categoria'],
            'plataforma': args['plataforma'],
            'precio': args['precio']
        })
        return juego, 200

    def delete(self, id):
        global JUEGOS
        juego = next((j for j in JUEGOS if j['id'] == id), None)
        if not juego:
            return {"message": "Juego no encontrado"}, 404
        JUEGOS = [j for j in JUEGOS if j['id'] != id]
        return '', 204

# --- Registrar recursos ---
api.add_resource(JuegoList, "/api/juegos")
api.add_resource(JuegoResource, "/api/juegos/<int:id>")