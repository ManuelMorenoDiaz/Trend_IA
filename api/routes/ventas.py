from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings
from concurrent.futures import ThreadPoolExecutor

# Suprimir las advertencias
warnings.filterwarnings("ignore")

mysql = MySQL()

ventas_bp = Blueprint('ventas', __name__)

def ajustar_modelo(id_p, ventas):
    ventas_id_p = ventas[ventas['id_p'] == id_p]
    try:
        # Filtrar las ventas para este id_p
        ventas_id_p = ventas[ventas['id_p'] == id_p]

        # Convertir la fecha a datetime y establecerla como índice
        ventas_id_p['fecha'] = pd.to_datetime(ventas_id_p['fecha'])
        ventas_id_p.set_index('fecha', inplace=True)

        # Agrupar por fecha y sumar la cantidad vendida
        ventas_id_p = ventas_id_p.groupby('fecha').sum()

        # Ordenar el DataFrame por fecha
        ventas_id_p.sort_index(inplace=True)

        # Asignar una frecuencia al índice de fecha
        # 'D' significa diaria. Cambia esto si tus datos tienen una frecuencia diferente
        ventas_id_p = ventas_id_p.asfreq('M')

        # Seleccionar la cantidad vendida para el modelado de series temporales
        cantidad_vendida = ventas_id_p['cantidad']

        # Crear el modelo SARIMA
        modelo = SARIMAX(cantidad_vendida, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))

        # Ajustar el modelo a los datos
        modelo_ajustado = modelo.fit(disp=0)

        # Hacer una predicción de ventas para los próximos 60 días
        prediccion = modelo_ajustado.predict(start=len(cantidad_vendida), end=len(cantidad_vendida) + 60)

        # Calcular la pendiente de la línea de regresión de las predicciones de ventas
        regresion = LinearRegression().fit(np.arange(len(prediccion)).reshape(-1, 1), prediccion.values)
        pendiente = regresion.coef_[0]

        # Devolver la pendiente
        return pendiente
    except Exception as e:
        # print(f"Error al ajustar el modelo para el producto {id_p}: {e}")
        return None

@ventas_bp.route('/ventas', methods=['GET'])
def get_all_ventas():
    cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM Ventas")
    cur.execute("SELECT * FROM Ventas")
    data = cur.fetchall()
    cur.close()

    # Convertir los datos a un DataFrame de pandas
    ventas = pd.DataFrame(data, columns=['id_v', 'cantidad', 'fecha', 'id_p'])

    # Obtener todos los id_p únicos
    id_p_unicos = ventas['id_p'].unique()

    with ThreadPoolExecutor() as executor:
        executor.map(ajustar_modelo, id_p_unicos)

    # Crear un diccionario para almacenar las pendientes de las predicciones de ventas
    pendientes = {}

    # Iterar sobre cada id_p único
    for id_p in id_p_unicos:
        pendiente = ajustar_modelo(id_p, ventas)
        if pendiente is not None:
            pendientes[id_p] = pendiente

    # Ordenar los id_p por la pendiente de las predicciones de ventas
    id_p_ordenados = sorted(pendientes, key=pendientes.get, reverse=True)

    # Convertir los id_p a int antes de devolver la respuesta JSON
    id_p_ordenados = [int(id_p) for id_p in id_p_ordenados[:50]]

    # Fetch the information of each product id
    productos_list = []
    for id_p in id_p_ordenados:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_p, nombre, descripcion, marca, precio, imagen_portada, cantidad_stock, calificacion, fecha_lanzamiento, fecha_estimada, ecommerce, historial_precios, id_c FROM Productos WHERE id_p = %s", (id_p,))
        producto = cur.fetchone()
        cur.close()

        if producto is not None:
            producto_dict = {
                'id_p': producto[0],
                'nombre': producto[1],
                'descripcion': producto[2],
                'marca': producto[3],
                'precio': str(producto[4]),
                'imagen_portada': producto[5],
                'cantidad_stock': producto[6],
                'calificacion': str(producto[7]),
                'fecha_lanzamiento': producto[8].strftime('%Y-%m-%d') if producto[8] else None,
                'fecha_estimada': producto[9],
                'ecommerce': producto[10],
                'historial_precios': producto[11],
                'id_c': producto[12]
            }
            productos_list.append(producto_dict)

    return jsonify({'productos': productos_list})

@ventas_bp.route('/ventas/<id>', methods=['GET'])
def get_venta(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Ventas WHERE id_v = %s", (id,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify({'venta': data})
    else:
        return jsonify({"error": "Venta no encontrada"})

@ventas_bp.route('/ventas', methods=['POST'])
def add_venta():
    data = request.get_json()
    cantidad = data['cantidad']
    fecha = datetime.strptime(data['fecha'], "%Y-%m-%d")
    id_p = data['id_p']
    
    cur = mysql.connection.cursor()
    
    query_insertion = """
        INSERT INTO Ventas (cantidad, fecha, id_p)
        VALUES (%s, %s, %s)
        """
        
    cur.execute(query_insertion,(cantidad, fecha, id_p))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Venta añadida correctamente'})


@ventas_bp.route('/ventas/<id>', methods=['PUT'])
def update_venta(id):
    data = request.get_json()
    cantidad = data['cantidad']
    fecha = datetime.strptime(data['fecha'], "%Y-%m-%d")
    id_p = data['id_p']
    
    cur = mysql.connection.cursor()
    
    query_update = """
        UPDATE Ventas
        SET cantidad = %s, fecha = %s, id_p = %s
        WHERE id_v = %s
        """
        
    cur.execute(query_update,(cantidad, fecha, id_p, id))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Venta actualizada correctamente'})

@ventas_bp.route('/ventas/<id>', methods=['DELETE'])
def delete_venta(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Ventas WHERE id_v = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'result': 'Venta eliminada correctamente'})
