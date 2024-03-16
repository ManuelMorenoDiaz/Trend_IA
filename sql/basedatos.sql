-- Active: 1705803036174@@127.0.0.1@3306
CREATE DATABASE trend_ia;

use trend_ia;

CREATE TABLE Categorias (
    id_c INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(70),
    descripcion TEXT,
    imagen_portada VARCHAR(255)
);

CREATE TABLE Productos (
    id_p INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    descripcion TEXT,
    marca VARCHAR(100),
    precio DECIMAL(10,2),
    imagen_portada VARCHAR(255),
    cantidad_stock INT,
    calificacion DECIMAL(3,2),
    fecha_lanzamiento DATE,
    fecha_estimada INT,
    ecommerce ENUM('WALMART', 'AMAZON'),
    historial_precios JSON,
    id_c INT,
    FOREIGN KEY (id_c) REFERENCES Categorias(id_c) ON DELETE SET NULL
);

CREATE TABLE Ventas (
    id_v INT PRIMARY KEY AUTO_INCREMENT,
    cantidad INT,
    fecha DATE,
    id_p INT, 
    FOREIGN KEY (id_p) REFERENCES Productos(id_p) ON DELETE CASCADE
);

CREATE TABLE Usuarios (
    id_u INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    suscripcion ENUM('FREE', 'PREMIUM')
);

CREATE TABLE Presupuestos (
    id_pre INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(255) NOT NULL,
    monto DECIMAL(10,2),
    fecha_creacion DATE,
    id_u INT,
    FOREIGN KEY (id_u) REFERENCES Usuarios(id_u) ON DELETE SET NULL,
    id_c INT,
    FOREIGN KEY (id_c) REFERENCES Categorias(id_c) ON DELETE SET NULL
);

CREATE TABLE Presupuesto_Productos (
    id_ppo INT PRIMARY KEY AUTO_INCREMENT,
    cantidad INT NOT NULL,
    id_pre INT,
    FOREIGN KEY (id_pre) REFERENCES Presupuestos(id_pre) ON DELETE CASCADE,
    id_p INT,
    FOREIGN KEY (id_p) REFERENCES Productos(id_p) ON DELETE CASCADE
);

CREATE TABLE Historial_Presupuestos (
    id_hp INT PRIMARY KEY AUTO_INCREMENT,
    fecha_creacion DATE NOT NULL,
    id_pre INT,
    FOREIGN KEY (id_pre) REFERENCES Presupuestos(id_pre) ON DELETE CASCADE
);

CREATE TABLE Carritos (
    id_ca INT PRIMARY KEY AUTO_INCREMENT,
    fecha_creacion DATE,
    id_u INT,
    FOREIGN KEY (id_u) REFERENCES Usuarios(id_u) ON DELETE SET NULL
);

CREATE TABLE Carrito_Producto (
    id_cp INT PRIMARY KEY AUTO_INCREMENT,
    cantidad INT,
    id_p INT,
    FOREIGN KEY (id_p) REFERENCES Productos(id_p) ON DELETE CASCADE,
    id_ca INT,
    FOREIGN KEY (id_ca) REFERENCES Carritos(id_ca) ON DELETE CASCADE
);

CREATE TABLE Historial_Compras (
    id_hc INT PRIMARY KEY AUTO_INCREMENT,
    fecha_compra DATE,
    id_ca INT,
    FOREIGN KEY (id_ca) REFERENCES Carritos(id_ca) ON DELETE CASCADE
);


