from flask import Blueprint, request, jsonify, make_response
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

mysql = MySQL()
bcrypt = Bcrypt()
jwt = JWTManager()


usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre = data['nombre']
    correo = data['correo']
    contraseña = bcrypt.generate_password_hash(data['contraseña']).decode('utf-8')
    
    if 'suscripcion' in data:
        suscripcion = data['suscripcion']
    else:
        suscripcion = ' '
    
    cur = mysql.connection.cursor()
    
    query_insertion = """
        INSERT INTO Usuarios (nombre, correo, contraseña, suscripcion)
        VALUES (%s, %s, %s, %s)
        """
        
    cur.execute(query_insertion,(nombre, correo, contraseña, suscripcion))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Usuario registrado correctamente'})

@usuarios_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data['correo']
    contraseña = data['contraseña']
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Usuarios WHERE correo = %s", (correo,))
    user = cur.fetchone()
    cur.close()
    
    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    elif bcrypt.check_password_hash(user[3], contraseña):  # Asume que la contraseña es el cuarto elemento en la tupla
        access_token = create_access_token(identity=correo)
        return jsonify({'message': 'Inicio de sesión exitoso', 'access_token': access_token})
    else:
        return jsonify({"error": "Correo o contraseña incorrectos"})


@usuarios_bp.route('/usuarios', methods=['POST'])
def add_usuario():
    data = request.get_json()
    nombre = data['nombre']
    correo = data['correo']
    contraseña = data['contraseña']
    suscripcion = data['suscripcion']
    
    cur = mysql.connection.cursor()
    
    query_insertion = """
        INSERT INTO Usuarios (nombre, correo, contraseña, suscripcion)
        VALUES (%s, %s, %s, %s)
        """
        
    cur.execute(query_insertion,(nombre, correo, contraseña, suscripcion))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Usuario añadido correctamente'})

@usuarios_bp.route('/usuarios', methods=['GET'])
def get_all_usuarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Usuarios")
    data = cur.fetchall()
    cur.close()
    return jsonify({'usuarios': data})

@usuarios_bp.route('/usuarios/<id>', methods=['GET'])
def get_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Usuarios WHERE id_u = %s", (id,))
    data = cur.fetchone()
    cur.close()
    if data:
        return jsonify({'usuario': data})
    else:
        return jsonify({"error": "Usuario no encontrado"})

@usuarios_bp.route('/usuarios/<id>', methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    nombre = data['nombre']
    correo = data['correo']
    contraseña = data['contraseña']
    suscripcion = data['suscripcion']
    
    cur = mysql.connection.cursor()
    
    query_update = """
        UPDATE Usuarios
        SET nombre = %s, correo = %s, contraseña = %s, suscripcion = %s
        WHERE id_u = %s
        """
        
    cur.execute(query_update,(nombre, correo, contraseña, suscripcion, id))
    
    mysql.connection.commit()
    
    cur.close()
    
    return jsonify({'message': 'Usuario actualizado correctamente'})

@usuarios_bp.route('/usuarios/<id>', methods=['DELETE'])
def delete_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Usuarios WHERE id_u = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'result': 'Usuario eliminado correctamente'})


blacklisted_tokens = set()

@usuarios_bp.route('/logout', methods=['POST'])
def logout():
    # Obtiene el token del usuario desde la solicitud
    token = request.headers.get('Authorization')
    
    if token:
        # Agrega el token a la lista negra
        blacklisted_tokens.add(token)
        
        return jsonify({'message': 'Sesión cerrada correctamente'})
    else:
        return jsonify({'message': 'No se proporcionó un token válido'})

