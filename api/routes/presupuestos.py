from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

mysql = MySQL()

presupuestos_bp = Blueprint('presupuestos', __name__)

@presupuestos_bp.route('/presupuestos', methods=['POST'])
def add_presupuesto():
    data = request.get_json()
    titulo = data['titulo']
    monto = data['monto']
    fecha_creacion = datetime.strptime(data['fecha_creacion'], "%Y-%m-%d")
    id_u = data['id_u']
    id_c = data['id_c']
    
    cur = mysql.connection.cursor()
    
    query_insertion = """
        INSERT INTO Presupuestos (titulo, monto, fecha_creacion, id_u, id_c)
        VALUES (%s, %s, %s, %s, %s)
        """
        
    cur.execute(query_insertion,(titulo, monto, fecha_creacion, id_u, id_c))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Presupuesto añadido correctamente'})

@presupuestos_bp.route('/presupuestos', methods=['GET'])
def get_all_presupuestos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Presupuestos")
    data = cur.fetchall()
    cur.close()
    return jsonify({'presupuestos': data})

@presupuestos_bp.route('/presupuestos/<id>', methods=['GET'])
def get_presupuesto(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Presupuestos WHERE id_p = %s", (id,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify({'presupuesto': data})
    else:
        return jsonify({"error": "Presupuesto no encontrado"})

@presupuestos_bp.route('/presupuestos/<id>', methods=['PUT'])
def update_presupuesto(id):
    data = request.get_json()
    titulo = data['titulo']
    monto = data['monto']
    fecha_creacion = datetime.strptime(data['fecha_creacion'], "%Y-%m-%d")
    id_u = data['id_u']
    id_c = data['id_c']
    
    cur = mysql.connection.cursor()
    
    query_update = """
        UPDATE Presupuestos
        SET titulo = %s, monto = %s, fecha_creacion = %s, id_u = %s, id_c = %s
        WHERE id_p = %s
        """
        
    cur.execute(query_update,(titulo, monto, fecha_creacion, id_u, id_c, id))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Presupuesto actualizado correctamente'})

@presupuestos_bp.route('/presupuestos/<id>', methods=['DELETE'])
def delete_presupuesto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Presupuestos WHERE id_p = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'result': 'Presupuesto eliminado correctamente'})
