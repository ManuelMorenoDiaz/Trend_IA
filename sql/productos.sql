-- Active: 1705803036174@@127.0.0.1@3306@trend_ia

DELETE FROM Productos;
ALTER TABLE Productos AUTO_INCREMENT = 1;
DELIMITER //
CREATE PROCEDURE DatosInsert(categoria INT, precio_min INT, precio_max INT, nombre_pro VARCHAR(255))
BEGIN
  DECLARE i INT DEFAULT 1;
  DECLARE j INT;
  DECLARE random_price INT;
  DECLARE random_stock INT;
  DECLARE random_rating DECIMAL(3,2);
  DECLARE random_date DATE;
  DECLARE random_brand VARCHAR(255);
  DECLARE brands VARCHAR(255);
  DECLARE brand_array TEXT;
  DECLARE price_history VARCHAR(4096) DEFAULT '';
  DECLARE ecommerce VARCHAR(255);
  DECLARE random_estimated INT;
  DECLARE all_dates TEXT;
  DECLARE random_index INT;

  -- Definir marcas para cada categoría
  CASE categoria
    WHEN 1 THEN SET brands = 'Apple, Alienware, Acer, Asus, Dell, Microsoft, Lenovo, HP'; -- Marcas para Computadoras
    WHEN 2 THEN SET brands = 'Samsung, Apple, Xiaomi, Oppo, Vivo, Google, OnePlus, Motorola'; -- Marcas para Telefonos
    WHEN 3 THEN SET brands = 'Bose, Sony, Sennheiser, JBL, Beats by Dre, Apple, Asus, Dell'; -- Marcas para Audifonos
    WHEN 4 THEN SET brands = 'Logitech, Epomaker, Ace and Tate, Nike, Kappa, Copperzeit, Columbia, Lotto'; -- Marcas para Teclados
    WHEN 5 THEN SET brands = 'Spigen, Poetic, Supcase, Ringke, OtterBox, ESR, CASETiFY, Apple'; -- Marcas para Fundas
    WHEN 6 THEN SET brands = 'Ray-Ban, Oakley, Giorgio Armani, Hugo Boss, Chanel, Tom Ford, Adidas, Nike'; -- Marcas para Lentes
    WHEN 7 THEN SET brands = 'Nike, Adidas, Reebok, Puma, Kappa, Copperzeit, Columbia, Lotto'; -- Marcas para Gorras
    WHEN 8 THEN SET brands = 'Samsung, LG, Panasonic, Toshiba, TCL, Hisense, Vizio, Sony'; -- Marcas para Televisiones
    WHEN 9 THEN SET brands = 'Nike, Adidas, Asics, Wilson, Head, Babolat, Yonex, Reebok'; -- Marcas para Tenis
    WHEN 10 THEN SET brands = 'Jarvis, Joss & Main, Realspace, Ebern Designs, Pottery Barn, Ikea, Uplift, Urban Outfitters'; -- Marcas para Escritorios
    WHEN 11 THEN SET brands = 'Flint and Tinder, Relwen, Buck Mason, Fjällräven, Triple F.A.T. Goose, Marmot, Columbia, Canada Goose'; -- Marcas para Chamarras
    WHEN 12 THEN SET brands = 'Bose, JBL, Klipsch, Sonos, Yamaha'; -- Marcas para Bocinas
    WHEN 13 THEN SET brands = 'Apple iPad Air, Samsung Galaxy Tab S9 Ultra, OnePlus Pad, Microsoft Surface Go 3, Amazon Fire Max 11'; -- Marcas para Tabletas
    WHEN 14 THEN SET brands = 'Ushdele Women\'s Plus Size Tops, Amazon Essentials Women\'s Long-Sleeve Woven Blouse, Amazon Essentials Long-Sleeve Blouse, Blooming Jelly Womens Chiffon Blouses, ZC&GF Button Down Shirt Tops'; -- Marcas para Blusas
    WHEN 15 THEN SET brands = 'Levi’s, Bonobos, Uniqlo, Buck Mason, Mavi'; -- Marcas para Pantalones
    ELSE SET brands = 'MarcaG,MarcaH,MarcaI,MarcaJ,MarcaK,MarcaL,MarcaM,MarcaN'; -- Marcas por defecto
  END CASE;

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

    -- Seleccionar una fecha aleatoria de la lista de todas las fechas para la fecha de lanzamiento
    SET random_index = FLOOR(RAND() * JSON_LENGTH(all_dates));
    SET random_date = JSON_UNQUOTE(JSON_EXTRACT(all_dates, CONCAT('$[', random_index, ']')));

    SET j = 1;
    WHILE j <= 100 DO
      -- Seleccionar una fecha aleatoria de la lista de todas las fechas
      SET random_index = FLOOR(RAND() * JSON_LENGTH(all_dates));
      SET random_date = JSON_UNQUOTE(JSON_EXTRACT(all_dates, CONCAT('$[', random_index, ']')));
      SET price_history = CONCAT(price_history, IF(j=1, '', ', '), '"', random_price, '": "', random_date, '"');
      SET random_price = random_price + FLOOR(-100 + RAND() * 200);
      IF random_price < precio_min THEN SET random_price = precio_min; END IF;
      IF random_price > precio_max THEN SET random_price = precio_max; END IF;
      SET j = j + 1;
    END WHILE;

    -- Verificar si se generó un historial de precios
    IF price_history = '' THEN
      SET price_history = CONCAT('"', random_price, '": "', DATE_FORMAT(CURDATE(), '%Y-%m-%d'), '"');
    END IF;

    INSERT INTO Productos ( nombre, descripcion, marca, precio, imagen_portada, cantidad_stock, calificacion, fecha_lanzamiento, fecha_estimada, ecommerce, historial_precios, id_c) 
    VALUES ( CONCAT(nombre_pro, IF(i <= 100, i, i - 100)), 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas quidem alias porro provident consequatur expedita voluptatem, commodi id similique tempora, fugit quo. Dolorum at iusto dolore assumenda natus accusantium provident.', random_brand, random_price,'https://placehold.co/500x400', random_stock , random_rating , random_date , random_estimated , ecommerce, CONCAT('{', price_history, '}'), categoria);
    
    SET price_history = '';
    SET i = i + 1;
  END WHILE;
END //
DELIMITER ;

CALL DatosInsert(1, 3500, 15000, 'Computadora'); -- Computadoras
CALL DatosInsert(2, 2000, 10000, 'Telefono'); -- Telefonos
CALL DatosInsert(3, 200, 4000, 'Audifonos'); -- Audifonos
CALL DatosInsert(4, 300, 5000, 'Teclado'); -- Teclados
CALL DatosInsert(5, 100, 700, 'Funda'); -- Fundas
CALL DatosInsert(6, 200, 2000, 'Lentes'); -- Lentes
CALL DatosInsert(7, 80, 800, 'Gorra'); -- Gorras
CALL DatosInsert(8, 4000, 2000, 'Television'); -- Televisiones
CALL DatosInsert(9, 350, 8000, 'Tenis'); -- Tenis
CALL DatosInsert(10, 2000, 7000, 'Escritorio'); -- Escritorios
CALL DatosInsert(11, 200, 2000, 'Chamarra'); -- Chamarras
CALL DatosInsert(12, 600, 5000, 'Bocina'); -- Bocinas
CALL DatosInsert(13, 2000, 12000, 'Tablet'); -- Tabletas
CALL DatosInsert(14, 100, 1300, 'Blusa'); -- Blusas
CALL DatosInsert(15, 400, 1000, 'Pantalones'); -- Pantalones
