-- Active: 1705803036174@@127.0.0.1@3306@trend_ia
DELIMITER //
CREATE PROCEDURE gscgaggcsg(categoria INT, precio_min INT, precio_max INT)
BEGIN
  DECLARE i INT DEFAULT 1;
  DECLARE j INT;
  DECLARE random_price INT;
  DECLARE random_stock INT;
  DECLARE random_rating DECIMAL(3,2);
  DECLARE random_date DATE;
  DECLARE random_brand VARCHAR(255);
  DECLARE brands VARCHAR(255) DEFAULT 'MarcaA,MarcaB,MarcaC,MarcaD,MarcaE';
  DECLARE brand_array TEXT;
  DECLARE price_history VARCHAR(4096) DEFAULT '';
  DECLARE ecommerce VARCHAR(255);
  DECLARE random_estimated INT;
  DECLARE all_dates TEXT;
  DECLARE random_index INT;

  SET brand_array = CONCAT('["', REPLACE(brands, ',', '","'), '"]');

  -- Crear una lista de todas las fechas posibles entre 2014 y marzo de 2024
  SET all_dates = '["2014-01-01"';
  SET random_date = '2014-01-01';
  WHILE random_date < '2024-03-31' DO
    SET random_date = DATE_ADD(random_date, INTERVAL 1 DAY);
    SET all_dates = CONCAT(all_dates, ', "', DATE_FORMAT(random_date, '%Y-%m-%d'), '"');
  END WHILE;
  SET all_dates = CONCAT(all_dates, ']');

  WHILE i <= 200 DO
    SET random_price = FLOOR(precio_min + RAND() * (precio_max - precio_min));
    SET random_stock = FLOOR(1 + RAND() * 100);
    SET random_rating = ROUND((2.5 + RAND() * (5 - 2.5)), 2);
    SET random_brand = REPLACE(JSON_UNQUOTE(JSON_EXTRACT(brand_array, CONCAT('$[', FLOOR(RAND() * JSON_LENGTH(brand_array)), ']'))), '"', '');
    SET ecommerce = IF(i <= 100, 'WALMART', 'AMAZON');
    SET random_estimated = FLOOR(1 + RAND() * 7);

    SET j = 1;
    WHILE j <= 100 DO
      -- Seleccionar una fecha aleatoria de la lista de todas las fechas
      SET random_index = FLOOR(RAND() * JSON_LENGTH(all_dates));
      SET random_date = JSON_UNQUOTE(JSON_EXTRACT(all_dates, CONCAT('$[', random_index, ']')));
      -- Eliminar la fecha seleccionada de la lista de todas las fechas
      SET all_dates = JSON_REMOVE(all_dates, CONCAT('$[', random_index, ']'));
      SET price_history = CONCAT(price_history, IF(j=1, '', ', '), '"', random_price, '": "', random_date, '"');
      SET random_price = random_price + FLOOR(-100 + RAND() * 200);
      IF random_price < precio_min THEN SET random_price = precio_min; END IF;
      IF random_price > precio_max THEN SET random_price = precio_max; END IF;
      SET j = j + 1;
    END WHILE;

    INSERT INTO Productos ( nombre, descripcion, marca, precio, imagen_portada, cantidad_stock, calificacion, fecha_lanzamiento, fecha_estimada, ecommerce, historial_precios, id_c) 
    VALUES ( CONCAT('Ropa Modelo ', IF(i <= 100, i, i - 100)), 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas quidem alias porro provident consequatur expedita voluptatem, commodi id similique tempora, fugit quo. Dolorum at iusto dolore assumenda natus accusantium provident.', random_brand, random_price,'https://placehold.co/500x400', random_stock , random_rating , random_date , random_estimated , ecommerce, CONCAT('{', price_history, '}'), categoria);
    
    SET price_history = '';
    SET i = i + 1;
  END WHILE;
END //
DELIMITER ;

CALL gscgaggcsg(1, 500, 600);  -- Ejemplo de cómo llamar al procedimiento con la nueva categoría y rango de precios

DELETE FROM productos;
