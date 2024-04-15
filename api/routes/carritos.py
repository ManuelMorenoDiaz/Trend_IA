from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

mysql = MySQL()

carritos_bp = Blueprint('carritos', __name__)


@carritos_bp.route('/carritos', methods=['POST'])
def add_carrito(id_u=None):
    if request.method == 'POST':
        data = request.get_json()
        id_u = data['id_u']
    elif id_u is None:
        return jsonify({'error': 'No id_u provided'})

    fecha_creacion = datetime.now()

    cur = mysql.connection.cursor()

    query_insertion = """
        INSERT INTO Carritos (fecha_creacion, id_u)
        VALUES (%s, %s)
        """

    cur.execute(query_insertion, (fecha_creacion, id_u))
    mysql.connection.commit()  # Agrega commit aquí

    # Get the last inserted id for the specific user
    query_last_id = """
        SELECT id_ca FROM Carritos WHERE id_u = %s ORDER BY id_ca DESC LIMIT 1
        """
    cur.execute(query_last_id, (id_u,))
    id_ca = cur.fetchone()[0]

    mysql.connection.commit()

    cur.close()

    return jsonify({'message': 'Carrito añadido correctamente', 'id_ca': id_ca})


@carritos_bp.route('/carritos/<idU>', methods=['GET'])
def get_carrito(idU):
    cur = mysql.connection.cursor()

    # Get the last inserted id for the specific user
    query_last_id = """
        SELECT id_ca FROM Carritos WHERE id_u = %s ORDER BY id_ca DESC
        """
    cur.execute(query_last_id, (idU,))

    data = cur.fetchone()

    if data:
        id_ca = data[0]
        return jsonify({'id_ca': id_ca})
    else:
        # If no carrito found for the user, add a new one and get the id
        return add_carrito(idU)

    if data:
        id_ca = data
        return jsonify({'id_ca': id_ca})
    else:
        # If no carrito found for the user, add a new one and get the id
        return add_carrito(idU)


@carritos_bp.route('/carritos', methods=['GET'])
def get_all_carritos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Carritos")
    data = cur.fetchall()
    cur.close()
    return jsonify({'carritos': data})


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

    cur.execute(query_update, (fecha_creacion, id_u, id))

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
