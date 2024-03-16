from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

mysql = MySQL()

historial_presupuestos_bp = Blueprint('historial_presupuestos', __name__)

@historial_presupuestos_bp.route('/historial_presupuestos', methods=['POST'])
def add_historial_presupuesto():
    data = request.get_json()
    fecha_creacion = datetime.strptime(data['fecha_creacion'], "%Y-%m-%d")
    id_p = data['id_p']
    
    cur = mysql.connection.cursor()
    
    query_insertion = """
        INSERT INTO Historial_Presupuestos (fecha_creacion, id_p)
        VALUES (%s, %s)
        """
        
    cur.execute(query_insertion,(fecha_creacion, id_p))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Historial_Presupuesto añadido correctamente'})

@historial_presupuestos_bp.route('/historial_presupuestos', methods=['GET'])
def get_all_historial_presupuestos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Historial_Presupuestos")
    data = cur.fetchall()
    cur.close()
    return jsonify({'historial_presupuestos': data})

@historial_presupuestos_bp.route('/historial_presupuestos/<id>', methods=['GET'])
def get_historial_presupuesto(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Historial_Presupuestos WHERE id_hp = %s", (id,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify({'historial_presupuesto': data})
    else:
        return jsonify({"error": "Historial_Presupuesto no encontrado"})

@historial_presupuestos_bp.route('/historial_presupuestos/<id>', methods=['PUT'])
def update_historial_presupuesto(id):
    data = request.get_json()
    fecha_creacion = datetime.strptime(data['fecha_creacion'], "%Y-%m-%d")
    id_p = data['id_p']
    
    cur = mysql.connection.cursor()
    
    query_update = """
        UPDATE Historial_Presupuestos
        SET fecha_creacion = %s, id_p = %s
        WHERE id_hp = %s
        """
        
    cur.execute(query_update,(fecha_creacion, id_p, id))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Historial_Presupuesto actualizado correctamente'})

@historial_presupuestos_bp.route('/historial_presupuestos/<id>', methods=['DELETE'])
def delete_historial_presupuesto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Historial_Presupuestos WHERE id_hp = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'result': 'Historial_Presupuesto eliminado correctamente'})
