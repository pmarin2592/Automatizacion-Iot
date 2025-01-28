--1. Insertar Datos en Sensores

INSERT INTO Sensores (Tipo, Ubicacion, Fecha_Instalacion, Estado)
VALUES 
('Temperatura', 'Sala Principal', '2024-01-01', 'Activo'),
('Consumo Eléctrico', 'Oficina 1', '2024-01-02', 'Activo'),
('Ocupación', 'Pasillo Norte', '2024-01-03', 'Activo'),
('Luz Ambiental', 'Sala de Reuniones', '2024-01-04', 'Activo'),
('Humedad', 'Almacén', '2024-01-05', 'Activo');


--2. Insertar Datos en Reglas_Patron

INSERT INTO Reglas_Patron (Nombre, Descripcion, Condicion, Accion, Estado)
VALUES
('Pico de Consumo', 'Detecta consumo superior a 50 kWh en 1 hora', 'Valor > 50 DURANTE 1 HORA', 'Enviar notificación', 'Activa'),
('Ausencia Prolongada', 'Detecta áreas sin ocupación durante más de 2 horas', 'Ocupación = 0 DURANTE 2 HORAS', 'Apagar luces', 'Activa'),
('Variación Anómala de Temperatura', 'Detecta cambios abruptos de temperatura (>5°C en 10 minutos)', 'ABS(Valor_Anterior - Valor) > 5', 'Enviar alerta', 'Activa');

--3. Insertar Datos en Configuraciones_Sistema

INSERT INTO Configuraciones_Sistema (Parametro, Valor)
VALUES
('Umbral_Consumo', '50'),
('Tiempo_Inactividad', '2 HORAS'),
('Rango_Temperatura', '20-30');

--4. Generar Datos para Lecturas_Sensores
--Este script generará lecturas de sensores para un período de más de un año (por ejemplo, 2024-01-01 al 2025-01-31).

-- Generar lecturas de sensores durante más de un año
DECLARE @StartDate DATE = '2024-01-01';
DECLARE @EndDate DATE = '2025-01-31';
DECLARE @SensorID INT;
DECLARE @CurrentDate DATETIME;
DECLARE @RandomValue DECIMAL(10, 2);

-- Generar datos para cada sensor
SET @SensorID = 1; -- Cambia este valor por cada sensor
WHILE @SensorID <= 5 -- Supongamos que hay 5 sensores
BEGIN
    SET @CurrentDate = @StartDate;
    WHILE @CurrentDate <= @EndDate
    BEGIN
        -- Generar un valor aleatorio basado en el tipo de sensor
        SET @RandomValue = CASE 
            WHEN @SensorID = 1 THEN RAND() * 10 + 20 -- Temperatura: 20°C a 30°C
            WHEN @SensorID = 2 THEN RAND() * 100 + 20 -- Consumo eléctrico: 20 a 120 kWh
            WHEN @SensorID = 3 THEN RAND() * 10 -- Ocupación: 0 a 10 personas
            WHEN @SensorID = 4 THEN RAND() * 500 + 300 -- Luz ambiental: 300 a 800 lux
            WHEN @SensorID = 5 THEN RAND() * 40 + 30 -- Humedad: 30% a 70%
        END;

        -- Insertar la lectura
        INSERT INTO Lecturas_Sensores (ID_Sensor, Fecha_Hora, Valor)
        VALUES (@SensorID, @CurrentDate, @RandomValue);

        -- Incrementar el tiempo (cada 15 minutos)
        SET @CurrentDate = DATEADD(MINUTE, 15, @CurrentDate);
    END;
    SET @SensorID = @SensorID + 1;
END;
