from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import json
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import os
from dateutil.relativedelta import relativedelta


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
        fecha_actual = datetime.now()
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
        tiempo_futuro = np.array(range(len(precios_historicos), len(precios_historicos) + 10)).reshape(-1, 1)
        precio_futuro = modelo.predict(tiempo_futuro)
         # Decide cuántos meses predecir en base a la fecha actual
        if fecha_actual.month < 10:
            # Si estamos antes de octubre, predecir hasta el final del año
            meses_a_predecir = 13 - fecha_actual.month
        else:
            # Si estamos en octubre o después, predecir los próximos 6 meses
            meses_a_predecir = 6
        # Genera las fechas futuras a partir de la fecha actual
        fechas_futuras = [fecha_actual + relativedelta(months=+i) for i in range(meses_a_predecir)]
        # Crear un diccionario con las fechas futuras y los precios futuros correspondientes
        predicciones = {str(fecha.date()): float(precio) for fecha, precio in zip(fechas_futuras, precio_futuro)}
       
        # plt.figure(figsize=(10,5))
        # plt.plot(fechas, precios_historicos, color='blue', label='Precios históricos')
        # plt.plot(fechas_futuras, precio_futuro, color='red', label='Predicción')
        # plt.xlabel('Fecha')
        # plt.ylabel('Precio')
        # plt.title('Precios históricos y predicción futura')
        # plt.legend()
        # plt.show()
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
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data['descripcion']
    marca = data['marca']
    precio = data['precio']
    imagen_portada = data['imagen_portada']
    cantidad_stock = data['cantidad_stock']
    calificacion = data['calificacion']
    fecha_lanzamiento = datetime.strptime(data['fecha_lanzamiento'], "%Y-%m-%d")
    
    cur = mysql.connection.cursor()
    
    query_insertion = """
        INSERT INTO Productos (nombre, descripcion, marca, precio, imagen_portada,
                               cantidad_stock, calificacion, fecha_lanzamiento)
        VALUES (%s, %s, %s, %s, %s, %s,%s,%s)
        """
        
    cur.execute(query_insertion,(nombre,
                                 descripcion,
                                 marca,
                                 precio,
                                 imagen_portada,
                                 cantidad_stock,
                                 calificacion,
                                 fecha_lanzamiento))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Producto añadido correctamente'})

@productos_bp.route('/productos/<id>', methods=['PUT'])
def update_producto(id):
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data['descripcion']
    marca = data['marca']
    precio = data['precio']
    imagen_portada = data['imagen_portada']
    cantidad_stock = data['cantidad_stock']
    calificacion = data['calificacion']
    fecha_lanzamiento = datetime.strptime(data['fecha_lanzamiento'], "%Y-%m-%d")
    
    cur = mysql.connection.cursor()
    
    query_update = """
        UPDATE Productos
        SET nombre = %s, descripcion = %s, marca = %s, precio = %s, imagen_portada = %s,
            cantidad_stock = %s, calificacion = %s, fecha_lanzamiento = %s
        WHERE id_p = %s
        """
        
    cur.execute(query_update,(nombre,
                              descripcion,
                              marca,
                              precio,
                              imagen_portada,
                              cantidad_stock,
                              calificacion,
                              fecha_lanzamiento,
                              id))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Producto actualizado correctamente'})


@productos_bp.route('/productos/<id>', methods=['DELETE'])
def delete_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Productos WHERE id_p = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'result': 'Producto eliminado correctamente'})
