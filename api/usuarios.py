from flask import Blueprint, request
from flask_mysqldb import MySQL

usuarios_bp = Blueprint('usuarios', __name__)

mysql = MySQL()

@usuarios_bp.route('/usuarios', methods=['GET', 'POST', 'PUT', 'DELETE'])
def usuarios():
    # Aquí iría el código para los métodos CRUD de la tabla "usuarios"
    pass
