-- Active: 1705803036174@@127.0.0.1@3306@trend_ia
delete from ventas

ALTER TABLE Ventas AUTO_INCREMENT = 1;
DELIMITER //
CREATE PROCEDURE generar_ventas()
BEGIN
  DECLARE v_finished INTEGER DEFAULT 0;
  DECLARE v_id_p INT;
  DECLARE v_fecha_lanzamiento DATE;
  DECLARE num_ventas INT;
  DECLARE j INT;
  DECLARE random_cantidad INT;
  DECLARE random_fecha DATE;

  -- Cursor para iterar sobre todos los productos
  DECLARE product_cursor CURSOR FOR 
    SELECT id_p, fecha_lanzamiento FROM Productos;
    
  -- Manejo de excepciones para el final del cursor
  DECLARE CONTINUE HANDLER 
        FOR NOT FOUND SET v_finished = 1;

  OPEN product_cursor;

  get_product: LOOP
    FETCH product_cursor INTO v_id_p, v_fecha_lanzamiento;
    IF v_finished = 1 THEN 
      LEAVE get_product;
    END IF;

    -- Genera un número aleatorio de ventas entre 50 y 10000 para cada producto
    SET num_ventas = FLOOR(50 + RAND() * 5000);

    SET j = 1;
    WHILE j <= num_ventas DO
      -- Genera una cantidad aleatoria entre 1 y 50
      SET random_cantidad = FLOOR(1 + RAND() * 50);

      -- Genera una fecha aleatoria entre la fecha de lanzamiento del producto y marzo de 2024
      SET random_fecha = v_fecha_lanzamiento + INTERVAL FLOOR(RAND() * TIMESTAMPDIFF(DAY, v_fecha_lanzamiento, '2024-03-31')) DAY;

      -- Inserta la venta en la tabla de Ventas
      INSERT INTO Ventas (cantidad, fecha, id_p) VALUES (random_cantidad, random_fecha, v_id_p);

      SET j = j + 1;
    END WHILE;
              
   END LOOP get_product;
   CLOSE product_cursor;
END //
DELIMITER ;

CALL generar_ventas

