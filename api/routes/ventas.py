from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

mysql = MySQL()

ventas_bp = Blueprint('ventas', __name__)

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

@ventas_bp.route('/ventas', methods=['GET'])
def get_all_ventas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Ventas")
    data = cur.fetchall()
    cur.close()
    return jsonify({'ventas': data})

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
