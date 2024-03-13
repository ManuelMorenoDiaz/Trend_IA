from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'trend_ia'

mysql = MySQL(app)

@app.route('/add', methods=['POST'])
def add():
    # Aquí iría el código para añadir un registro a la base de datos
    pass

@app.route('/update', methods=['PUT'])
def update():
    # Aquí iría el código para actualizar un registro en la base de datos
    pass

@app.route('/delete', methods=['DELETE'])
def delete():
    # Aquí iría el código para eliminar un registro de la base de datos
    pass

@app.route('/get', methods=['GET'])
def get():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    data = cur.fetchall()
    cur.close()
    return {'productos': data}

@app.route('/', methods=['GET'])
def home():
    return "¡Bienvenido a mi API!"

if __name__ == '__main__':
    app.run(debug=True)
