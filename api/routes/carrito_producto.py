from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL

mysql = MySQL()

carrito_producto_bp = Blueprint('carrito_producto', __name__)

@carrito_producto_bp.route('/carrito_producto', methods=['POST'])
def add_carrito_producto():
    data = request.get_json()
    cantidad = data['cantidad']
    id_p = data['id_p']
    id_ca = data['id_ca']
    
    cur = mysql.connection.cursor()
    
    query_insertion = """
        INSERT INTO Carrito_Producto (cantidad, id_p, id_ca)
        VALUES (%s, %s, %s)
        """
        
    cur.execute(query_insertion, (cantidad, id_p, id_ca))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Carrito_Producto añadido correctamente'})

@carrito_producto_bp.route('/carrito_producto', methods=['GET'])
def get_all_carrito_productos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Carrito_Producto")
    data = cur.fetchall()
    cur.close()
    return jsonify({'carrito_productos': data})

@carrito_producto_bp.route('/carrito_producto/<id>', methods=['GET'])
def get_carrito_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Carrito_Producto WHERE id_cp = %s", (id,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify({'carrito_producto': data})
    else:
        return jsonify({"error": "Carrito_Producto no encontrado"})

@carrito_producto_bp.route('/carrito_producto/<id>', methods=['PUT'])
def update_carrito_producto(id):
    data = request.get_json()
    cantidad = data['cantidad']
    id_p = data['id_p']
    id_ca = data['id_ca']
    
    cur = mysql.connection.cursor()
    
    query_update = """
        UPDATE Carrito_Producto
        SET cantidad = %s, id_p = %s, id_ca = %s
        WHERE id_cp = %s
        """
        
    cur.execute(query_update, (cantidad, id_p, id_ca, id))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Carrito_Producto actualizado correctamente'})

@carrito_producto_bp.route('/carrito_producto/<id>', methods=['DELETE'])
def delete_carrito_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Carrito_Producto WHERE id_cp = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'result': 'Carrito_Producto eliminado correctamente'})
