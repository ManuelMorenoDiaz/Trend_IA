from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Importa los blueprints
from routes.usuarios import usuarios_bp
from routes.productos import productos_bp
from routes.categorias import categorias_bp
from routes.carritos import carritos_bp
from routes.presupuestos import presupuestos_bp
from routes.historial_compras import historial_compras_bp
from routes.historial_presupuestos import historial_presupuestos_bp
from routes.carrito_producto import carrito_producto_bp
from routes.ventas import ventas_bp
from routes.presupuestos_productos import presupuesto_productos_bp

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'trend_ia'

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'rodr'

mysql = MySQL(app)
jwt = JWTManager(app)

# Habilita CORS
CORS(app)

# Registra los blueprints
app.register_blueprint(usuarios_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(carritos_bp)
app.register_blueprint(presupuestos_bp)
app.register_blueprint(historial_compras_bp)
app.register_blueprint(historial_presupuestos_bp)
app.register_blueprint(carrito_producto_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(presupuesto_productos_bp)

if __name__ == '__main__':
    app.run(debug=True)
