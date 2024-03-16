from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

mysql = MySQL()

historial_compras_bp = Blueprint('historial_compras', __name__)

@historial_compras_bp.route('/historial_compras', methods=['POST'])
def add_historial_compra():
    data = request.get_json()
    fecha_compra = datetime.strptime(data['fecha_compra'], "%Y-%m-%d")
    id_ca = data['id_ca']
    
    cur = mysql.connection.cursor()
    
    query_insertion = """
        INSERT INTO Historial_Compras (fecha_compra, id_ca)
        VALUES (%s, %s)
        """
        
    cur.execute(query_insertion,(fecha_compra, id_ca))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Historial de compra añadido correctamente'})

@historial_compras_bp.route('/historial_compras', methods=['GET'])
def get_all_historial_compras():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Historial_Compras")
    data = cur.fetchall()
    cur.close()
    return jsonify({'historial_compras': data})

@historial_compras_bp.route('/historial_compras/<id>', methods=['GET'])
def get_historial_compra(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Historial_Compras WHERE id_hc = %s", (id,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify({'historial_compra': data})
    else:
        return jsonify({"error": "Historial de compra no encontrado"})

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
