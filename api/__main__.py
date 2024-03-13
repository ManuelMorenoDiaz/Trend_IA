from flask import Flask
from usuarios import usuarios_bp
from productos import productos_bp
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'trend_ia'

mysql = MySQL(app)

app.register_blueprint(usuarios_bp)
app.register_blueprint(productos_bp)

if __name__ == '__main__':
    app.run(debug=True)
