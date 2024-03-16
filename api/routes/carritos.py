from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

mysql = MySQL()

carritos_bp = Blueprint('carritos', __name__)

@carritos_bp.route('/carritos', methods=['POST'])
def add_carrito():
    data = request.get_json()
    fecha_creacion = datetime.strptime(data['fecha_creacion'], "%Y-%m-%d")
    id_u = data['id_u']
    
    cur = mysql.connection.cursor()
    
    query_insertion = """
        INSERT INTO Carritos (fecha_creacion, id_u)
        VALUES (%s, %s)
        """
        
    cur.execute(query_insertion,(fecha_creacion, id_u))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Carrito añadido correctamente'})

@carritos_bp.route('/carritos', methods=['GET'])
def get_all_carritos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Carritos")
    data = cur.fetchall()
    cur.close()
    return jsonify({'carritos': data})

@carritos_bp.route('/carritos/<id>', methods=['GET'])
def get_carrito(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Carritos WHERE id_ca = %s", (id,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify({'carrito': data})
    else:
        return jsonify({"error": "Carrito no encontrado"})

@carritos_bp.route('/carritos/<id>', methods=['PUT'])
def update_carrito(id):
    data = request.get_json()
    fecha_creacion = datetime.strptime(data['fecha_creacion'], "%Y-%m-%d")
    id_u = data['id_u']
    
    cur = mysql.connection.cursor()
    
    query_update = """
        UPDATE Carritos
        SET fecha_creacion = %s, id_u = %s
        WHERE id_ca = %s
        """
        
    cur.execute(query_update,(fecha_creacion, id_u, id))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Carrito actualizado correctamente'})

@carritos_bp.route('/carritos/<id>', methods=['DELETE'])
def delete_carrito(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Carritos WHERE id_ca = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'result': 'Carrito eliminado correctamente'})
