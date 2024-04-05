from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL

mysql = MySQL()

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/categorias', methods=['POST'])
def add_categoria():
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data['descripcion']
    imagen_portada = data['imagen_portada']
    
    cur = mysql.connection.cursor()
    
    query_insertion = """
        INSERT INTO Categorias (nombre, descripcion, imagen_portada)
        VALUES (%s, %s, %s)
        """
        
    cur.execute(query_insertion,(nombre, descripcion, imagen_portada))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Categoria añadida correctamente'})

@categorias_bp.route('/categorias', methods=['GET'])
def get_all_categorias():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Categorias")
    data = cur.fetchall()
    cur.close()
    return jsonify({'categorias': data})

@categorias_bp.route('/categorias/<nombre>', methods=['GET'])
def get_categoria(nombre):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Categorias WHERE nombre = %s", (nombre,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify({'categoria': data})
    else:
        return jsonify({"error": "Categoria no encontrada"})

@categorias_bp.route('/categorias/<id>', methods=['PUT'])
def update_categoria(id):
    data = request.get_json()
    nombre = data['nombre']
    descripcion = data['descripcion']
    imagen_portada = data['imagen_portada']
    
    cur = mysql.connection.cursor()
    
    query_update = """
        UPDATE Categorias
        SET nombre = %s, descripcion = %s, imagen_portada = %s
        WHERE id_c = %s
        """
        
    cur.execute(query_update,(nombre, descripcion, imagen_portada, id))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Categoria actualizada correctamente'})

@categorias_bp.route('/categorias/<id>', methods=['DELETE'])
def delete_categoria(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Categorias WHERE id_c = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'result': 'Categoria eliminada correctamente'})
