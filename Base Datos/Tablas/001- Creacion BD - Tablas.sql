create database IotBD

use IotBD

-- Tabla: Sensores
CREATE TABLE Sensores (
    ID_Sensor INT PRIMARY KEY, -- Identificador único del sensor
    Tipo NVARCHAR(50), -- Tipo de sensor (Temperatura, Consumo Eléctrico, etc.)
    Ubicacion NVARCHAR(100), -- Ubicación física del sensor
    Fecha_Instalacion DATE, -- Fecha en la que se instaló el sensor
    Estado NVARCHAR(20) -- Estado del sensor (Activo/Inactivo)
);

-- Tabla: Lecturas_Sensores
CREATE TABLE Lecturas_Sensores (
    ID_Lectura INT PRIMARY KEY, -- Identificador único de la lectura
    ID_Sensor INT FOREIGN KEY REFERENCES Sensores(ID_Sensor), -- Relación con Sensores
    Fecha_Hora DATETIME, -- Fecha y hora de la lectura
    Valor DECIMAL(10, 2) -- Valor registrado por el sensor
);

-- Tabla: Reglas_Patron
CREATE TABLE Reglas_Patron (
    ID_Regla INT PRIMARY KEY, -- Identificador único de la regla
    Nombre NVARCHAR(100), -- Nombre de la regla
    Descripcion NVARCHAR(255), -- Descripción de la regla
    Condicion NVARCHAR(255), -- Condición de la regla
    Accion NVARCHAR(255), -- Acción a ejecutar
    Estado NVARCHAR(20) -- Estado de la regla (Activo/Inactivo)
);

-- Tabla: Patrones_Detectados
CREATE TABLE Patrones_Detectados (
    ID_Patron INT PRIMARY KEY, -- Identificador único del patrón
    ID_Sensor INT FOREIGN KEY REFERENCES Sensores(ID_Sensor), -- Relación con Sensores
    Fecha_Hora DATETIME, -- Fecha y hora en que se detectó el patrón
    Tipo NVARCHAR(100), -- Tipo de patrón detectado
    Descripcion NVARCHAR(255), -- Descripción del patrón
    Nivel_Severidad NVARCHAR(20), -- Nivel de severidad del patrón
    Estado NVARCHAR(20) -- Estado del patrón
);

-- Tabla: Acciones_Ejecutadas
CREATE TABLE Acciones_Ejecutadas (
    ID_Accion INT PRIMARY KEY, -- Identificador único de la acción
    ID_Patron INT FOREIGN KEY REFERENCES Patrones_Detectados(ID_Patron), -- Relación con Patrones_Detectados
    Fecha_Hora DATETIME, -- Fecha y hora en que se ejecutó la acción
    Accion NVARCHAR(255), -- Detalle de la acción realizada
    Estado NVARCHAR(20) -- Estado de la acción (Completada/Pendiente)
);

-- Tabla: Modelos_Predictivos
CREATE TABLE Modelos_Predictivos (
    ID_Modelo INT PRIMARY KEY, -- Identificador único del modelo
    Nombre NVARCHAR(100), -- Nombre del modelo predictivo
    Descripcion NVARCHAR(255), -- Descripción del modelo
    Fecha_Creacion DATE, -- Fecha en que se creó el modelo
    Estado NVARCHAR(20) -- Estado del modelo (Activo/Inactivo)
);

-- Tabla: Historial_Predicciones
CREATE TABLE Historial_Predicciones (
    ID_Prediccion INT PRIMARY KEY, -- Identificador único de la predicción
    ID_Modelo INT FOREIGN KEY REFERENCES Modelos_Predictivos(ID_Modelo), -- Relación con Modelos_Predictivos
    Fecha_Hora DATETIME, -- Fecha y hora de la predicción
    Valor_Pronosticado DECIMAL(10, 2) -- Valor pronosticado por el modelo
);

-- Tabla: Configuraciones_Sistema
CREATE TABLE Configuraciones_Sistema (
    ID_Configuracion INT PRIMARY KEY, -- Identificador único de la configuración
    Parametro NVARCHAR(100), -- Nombre del parámetro de configuración
    Valor NVARCHAR(255) -- Valor del parámetro
);
