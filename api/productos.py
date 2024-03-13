from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import json
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import os

productos_bp = Blueprint('productos', __name__)

mysql = MySQL()

@productos_bp.route('/productos/<id>/predict', methods=['GET'])
def predict_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Productos WHERE id_p = " + str(id))
    data = cur.fetchall()
    cur.close()
    if data:
        producto = data[0]
        precios_historicos_str = producto[-2]
        precios_historicos_dict = json.loads(precios_historicos_str)
        precios_historicos_dict = {v: k for k, v in precios_historicos_dict.items()}
        precios_historicos = np.array([float(precio) for precio in precios_historicos_dict.values()])
        fechas = [datetime.strptime(date, "%Y-%m-%d") for date in precios_historicos_dict.keys()]
        fechas, precios_historicos = zip(*sorted(zip(fechas, precios_historicos)))
        tiempo = np.array(range(len(precios_historicos)))
        tiempo = tiempo.reshape(-1, 1)
        precios_historicos = np.array(precios_historicos).reshape(-1, 1)
        modelo = LinearRegression()
        modelo.fit(tiempo, precios_historicos)
        tiempo_futuro = np.array(range(len(precios_historicos), len(precios_historicos) + 180)).reshape(-1, 1)
        precio_futuro = modelo.predict(tiempo_futuro)
        fechas_futuras = [fechas[-1] + timedelta(days=i) for i in range(180)]
        # Crear un diccionario con las fechas futuras y los precios futuros correspondientes
        predicciones = {str(fecha.date()): float(precio) for fecha, precio in zip(fechas_futuras, precio_futuro)}
       
        plt.figure(figsize=(10,5))
        plt.plot(fechas, precios_historicos, color='blue', label='Precios históricos')
        plt.plot(fechas_futuras, precio_futuro, color='red', label='Predicción')
        plt.xlabel('Fecha')
        plt.ylabel('Precio')
        plt.title('Precios históricos y predicción futura')
        plt.legend()
        plt.show()
        return jsonify({'predicciones': predicciones})

    else:
        return jsonify({"error": "Producto no encontrado"})

def guardar_imagen(ruta, imagen):
    base, extension = os.path.splitext(ruta)
    contador = 1
    while os.path.exists(ruta):
        ruta = f"{base}_{contador}{extension}"
        contador += 1
    imagen.savefig(ruta)
    return ruta
    
@productos_bp.route('/productos', methods=['POST'])
def add_producto():
    # Aquí iría el código para añadir un producto a la base de datos
    # Deberías obtener los datos del producto del cuerpo de la solicitud HTTP
    pass

@productos_bp.route('/productos/<id>', methods=['PUT'])
def update_producto(id):
    # Aquí iría el código para actualizar un producto en la base de datos
    # Deberías obtener los nuevos datos del producto del cuerpo de la solicitud HTTP
    pass

@productos_bp.route('/productos/<id>', methods=['DELETE'])
def delete_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Productos WHERE id_p = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'result': 'Producto eliminado correctamente'})
