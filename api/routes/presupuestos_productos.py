from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL

mysql = MySQL()

presupuesto_productos_bp = Blueprint('presupuesto_productos', __name__)

@presupuesto_productos_bp.route('/presupuesto_productos', methods=['POST'])
def add_presupuesto_producto():
    data = request.get_json()
    cantidad = data['cantidad']
    id_pre = data['id_pre']
    id_pro = data['id_pro']
    
    cur = mysql.connection.cursor()
    
    query_insertion = """
        INSERT INTO Presupuesto_Productos (cantidad, id_pre, id_pro)
        VALUES (%s, %s, %s)
        """
        
    cur.execute(query_insertion,(cantidad, id_pre, id_pro))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Presupuesto_Producto añadido correctamente'})

@presupuesto_productos_bp.route('/presupuesto_productos', methods=['GET'])
def get_all_presupuesto_productos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Presupuesto_Productos")
    data = cur.fetchall()
    cur.close()
    return jsonify({'presupuesto_productos': data})

@presupuesto_productos_bp.route('/presupuesto_productos/<id>', methods=['GET'])
def get_presupuesto_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Presupuesto_Productos WHERE id_pp = %s", (id,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify({'presupuesto_producto': data})
    else:
        return jsonify({"error": "Presupuesto_Producto no encontrado"})

@presupuesto_productos_bp.route('/presupuesto_productos/<id>', methods=['PUT'])
def update_presupuesto_producto(id):
    data = request.get_json()
    cantidad = data['cantidad']
    id_pre = data['id_pre']
    id_pro = data['id_pro']
    
    cur = mysql.connection.cursor()
    
    query_update = """
        UPDATE Presupuesto_Productos
        SET cantidad = %s, id_pre = %s, id_pro = %s
        WHERE id_pp = %s
        """
        
    cur.execute(query_update,(cantidad, id_pre, id_pro, id))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Presupuesto_Producto actualizado correctamente'})

@presupuesto_productos_bp.route('/presupuesto_productos/<id>', methods=['DELETE'])
def delete_presupuesto_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Presupuesto_Productos WHERE id_pp = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'result': 'Presupuesto_Producto eliminado correctamente'})
