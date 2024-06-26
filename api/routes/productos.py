from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import json
from datetime import datetime
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import json
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import os
from dateutil.relativedelta import relativedelta
from sklearn.cluster import KMeans

from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error
import numpy as np
import json
from datetime import datetime
import matplotlib.dates as mdates
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
        
        meses = [fecha.month for fecha in fechas]
        años = [fecha.year for fecha in fechas]
        
        datos = np.column_stack((meses, años))
        
        meses_a_predecir = 12
        meses_futuro = [(fecha_actual.month + i) % 12 if (fecha_actual.month + i) % 12 != 0 else 12 for i in range(meses_a_predecir)]
        años_futuro = [fecha_actual.year + (fecha_actual.month + i - 1) // 12 for i in range(meses_a_predecir)]
        
        datos_futuro = np.column_stack((meses_futuro, años_futuro))

        # Ajustar el modelo de Random Forest
        modelo = RandomForestRegressor(random_state=42)
        
        # Definir los hiperparámetros para la búsqueda en cuadrícula
        parametros = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        # Búsqueda en cuadrícula
        grid_search = GridSearchCV(modelo, parametros, cv=5, scoring='neg_mean_squared_error', verbose=1, n_jobs=-1)
        grid_search.fit(datos, np.array(precios_historicos).ravel())
        
        # Mejor modelo
        mejor_modelo = grid_search.best_estimator_
        
        # Validación cruzada
        scores = cross_val_score(mejor_modelo, datos, np.array(precios_historicos).ravel(), cv=5, scoring='neg_mean_squared_error')
        mse_scores = -scores
        print(f"Error Cuadrático Medio (MSE) promedio: {mse_scores.mean()}")

        # Predice los precios futuros
        precio_futuro = mejor_modelo.predict(datos_futuro)

        fechas_futuras = [fecha_actual + relativedelta(months=+i) for i in range(meses_a_predecir)]
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
        return jsonify({"error": "Producto no encontrado"}),404

    
@productos_bp.route('/productos/pre', methods=['POST'])
def get_productos_filtrados():
    data = request.get_json()
    id_c = data['id_c']
    ecommerce = data['ecommerce']
    presupuesto = float(data['presupuesto'])

    # Inicializar la lista de productos recomendados
    productos_recomendados = []

    # Obtener todos los productos que coinciden con el id_c y el ecommerce
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Productos WHERE id_c = %s AND ecommerce = %s", (id_c, ecommerce))
    productos = cur.fetchall()
    cur.close()

   # Convertir los productos a diccionarios
    productos = [dict(zip(['id_p', 'nombre', 'descripcion', 'marca', 'precio', 'imagen_portada', 'cantidad_stock', 'calificacion', 'fecha_lanzamiento', 'fecha_estimada', 'ecommerce', 'historial_precios', 'id_c'], producto)) for producto in productos]

    # Ordenar los productos
    productos = sorted(productos, key=lambda x: (-float(x['calificacion']), -x['cantidad_stock'], x['fecha_estimada'], float(x['precio'])))

    # Recorrer la lista de productos
    for producto in productos:
        # Si el precio del producto es menor o igual al presupuesto
        if float(producto['precio']) <= presupuesto:
            # Añadir el producto a la lista de productos recomendados
            productos_recomendados.append(producto)
            # Restar el precio del producto al presupuesto
            presupuesto -= float(producto['precio'])


    # Devolver la lista de productos recomendados
    return jsonify({'productos': productos_recomendados})


@productos_bp.route('/productos/seg', methods=['GET'])
def get_productosseg():
    id_c = request.args.get('id_c', default=None, type=int)  # Obtenemos el ID de la categoría si está presente
    
    query_base = "SELECT id_p, nombre, descripcion, marca, precio, imagen_portada, cantidad_stock, calificacion, fecha_lanzamiento, fecha_estimada, ecommerce, historial_precios, id_c FROM Productos"
    
    cur = mysql.connection.cursor()
    if id_c is not None:
        # Filtramos los productos por el ID de la categoría
        cur.execute(f"{query_base} WHERE id_c = %s", (id_c,))
    else:
        # Obtenemos todos los productos si no se especificó una categoría
        cur.execute(query_base)
    
    data = cur.fetchall()
    cur.close()

    productos_list = []
    for producto in data:
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

    # Convert the list of dictionaries to a numpy array
    productos_array = np.array([(float(producto['precio']), producto['cantidad_stock'], float(producto['calificacion'])) for producto in productos_list])

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=3, random_state=0).fit(productos_array)

    # Add the cluster labels to the product dictionaries
    for i in range(len(productos_list)):
        productos_list[i]['cluster'] = int(kmeans.labels_[i])

    # Plot the clusters
    plt.scatter([float(producto['precio']) for producto in productos_list], 
                [producto['cantidad_stock'] for producto in productos_list], 
                c=[producto['cluster'] for producto in productos_list])
    plt.xlabel('Precio')
    plt.ylabel('Cantidad en Stock')
    plt.show()

    return jsonify({'productos': productos_list})


def guardar_imagen(ruta, imagen):
    base, extension = os.path.splitext(ruta)
    contador = 1
    while os.path.exists(ruta):
        ruta = f"{base}_{contador}{extension}"
        contador += 1
    imagen.savefig(ruta)
    return ruta




@productos_bp.route('/productos', methods=['GET'])
def get_productos():
    # Obtenemos el nombre de la categoría si está presente
    nombre_categoria = request.args.get('nombre_categoria', default=None, type=str)

    # Se ajusta la consulta para incluir un JOIN con la tabla Categorias y seleccionar nombre_c
    # y filtrar basado en el nombre de la categoría si se proporciona
    query_base = """
    SELECT Productos.id_p, Productos.nombre, Productos.descripcion, Productos.marca, Productos.precio, Productos.imagen_portada, Productos.cantidad_stock, Productos.calificacion, Productos.fecha_lanzamiento, Productos.fecha_estimada, Productos.ecommerce, Productos.historial_precios, Categorias.nombre AS nombre_categoria
    FROM Productos
    JOIN Categorias ON Productos.id_c = Categorias.id_c
    """

    cur = mysql.connection.cursor()
    if nombre_categoria is not None:
        # Filtramos los productos por el nombre de la categoría
        query_base += " WHERE Categorias.nombre = %s"
        cur.execute(query_base, (nombre_categoria,))
    else:
        # Obtenemos todos los productos si no se especificó una categoría por nombre
        cur.execute(query_base)

    data = cur.fetchall()
    cur.close()

    productos_list = []
    for producto in data:
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
            'nombre_categoria': producto[12]
        }
        productos_list.append(producto_dict)

    return jsonify({'productos': productos_list})

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
