# Importamos las librerias
from flask import Flask, jsonify
import pymongo

# Definimos un servidor flask
app = Flask(__name__)


@app.route('/')  # Definimos las routes
def __init__():
    return "<h1>PRUEBAS PALABRAS</h1>"


def conectarMongo():
    # Levantamos la conexion a mongo
    host = pymongo.MongoClient("mongodb://localhost:27017/")  # Host
    db = host["bdpalabras"]  # BD
    coleccion = db["palabras"]  # Coleccion
    return coleccion


@app.route('/insertar')
def insertarPalabras():
    # Insertamos palabras en la coleccion
    palabras = [
        {"palabra": "lata"},
        {"palabra": "dado"},
        {"palabra": "cafetera"},
        {"palabra": "moto"}
    ]
    conectarMongo().insert_many(palabras)
    return "PALABRAS INSERTADAS"


@app.route('/palabras')
def obtenerPalabras():
    # Devuelve todos los documentos
    palabras = []
    resultado = conectarMongo().find()
    for palabra in resultado:
        palabra.pop('_id')
        palabras.append(palabra)
    return jsonify(palabras)


@app.route('/palabra/<palabra>')
def buscarPalabra(palabra):
    # Buscar una palabra
    busqueda = {"palabra": palabra}
    palabras = []
    resultado = conectarMongo().find(busqueda)
    for palabra in resultado:
        palabra.pop('_id')
        palabras.append(palabra)
    return jsonify(palabras)


@app.route('/buscar/<busqueda>')
def buscarPalabras(busqueda):
    # Buscar palabras con comodines
    palabras = []
    busqueda = {"palabra": {"$gt": busqueda}}
    resultado = conectarMongo().find(busqueda)
    for palabra in resultado:
        palabra.pop('_id')
        palabras.append(palabra)
    return jsonify(palabras)


@app.route('/ordenar/<busqueda>')
def buscarPalabrasOrdenadas(busqueda):
    # Buscando palabras con comodines y ordenando
    palabras = []
    busqueda = {"palabra": {"$gt": busqueda}}
    resultado = conectarMongo().find(busqueda)
    resultado = resultado.sort("palabra", 1)  # ascendente
    resultado = resultado.sort("palabra", -1)  # descendente
    for palabra in resultado:
        palabra.pop('_id')
        palabras.append(palabra)
    return jsonify(palabras)


# Levantamos el servidor flask
if __name__ == "__main__":
    app.run(debug=True)
