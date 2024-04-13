from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

mysql = MySQL()

historial_compras_bp = Blueprint('historial_compras', __name__)

@historial_compras_bp.route('/historial_compras', methods=['POST'])
def add_historial_compra():
    data = request.get_json()
    id_ca = data['id_ca']
    
    # Obteniendo la fecha actual en el momento de la llamada a la función
    fecha_compra = datetime.now()
    
    cur = mysql.connection.cursor()
    
    query_insertion = """
        INSERT INTO Historial_Compras (fecha_compra, id_ca)
        VALUES (%s, %s)
        """
        
    cur.execute(query_insertion,(fecha_compra, id_ca))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Historial de compra añadido correctamente'})


@historial_compras_bp.route('/historial_compras/<idU>', methods=['GET'])
def get_all_historial_compras(idU):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT Carritos.id_ca, Productos.*
        FROM Usuarios
        JOIN Carritos ON Usuarios.id_u = Carritos.id_u
        JOIN Carrito_Producto ON Carritos.id_ca = Carrito_Producto.id_ca
        JOIN Productos ON Carrito_Producto.id_p = Productos.id_p
        JOIN Historial_Compras ON Carritos.id_ca = Historial_Compras.id_ca
        WHERE Usuarios.id_u = %s
    """, (idU,))
    data = cur.fetchall()
    cur.close()

    carritos = {}
    for row in data:
        id_ca = row[0]
        producto = {
            'id_p': row[1],
            'nombre': row[2],
            'descripcion': row[3],
            'marca': row[4],
            'precio': str(row[5]),
            'imagen_portada': row[6],
            'cantidad_stock': row[7],
            'calificacion': str(row[8]),
            'fecha_lanzamiento': row[9].strftime('%Y-%m-%d') if row[9] else None,
            'fecha_estimada': row[10],
            'ecommerce': row[11],
            'historial_precios': row[12],
            'nombre_categoria': row[13]
        }
        if id_ca in carritos:
            carritos[id_ca].append(producto)
        else:
            carritos[id_ca] = [producto]

    return jsonify({'historial_compras': carritos})


@historial_compras_bp.route('/historial_compras/<id>', methods=['PUT'])
def update_historial_compra(id):
    data = request.get_json()
    fecha_compra = datetime.strptime(data['fecha_compra'], "%Y-%m-%d")
    id_ca = data['id_ca']
    
    cur = mysql.connection.cursor()
    
    query_update = """
        UPDATE Historial_Compras
        SET fecha_compra = %s, id_ca = %s
        WHERE id_hc = %s
        """
        
    cur.execute(query_update,(fecha_compra, id_ca, id))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Historial de compra actualizado correctamente'})

@historial_compras_bp.route('/historial_compras/<id>', methods=['DELETE'])
def delete_historial_compra(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Historial_Compras WHERE id_hc = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'result': 'Historial de compra eliminado correctamente'})
