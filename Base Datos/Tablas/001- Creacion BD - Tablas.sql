create database IotBD

use IotBD

-- Tabla: Sensores
CREATE TABLE Sensores (
    ID_Sensor INT PRIMARY KEY, -- Identificador �nico del sensor
    Tipo NVARCHAR(50), -- Tipo de sensor (Temperatura, Consumo El�ctrico, etc.)
    Ubicacion NVARCHAR(100), -- Ubicaci�n f�sica del sensor
    Fecha_Instalacion DATE, -- Fecha en la que se instal� el sensor
    Estado NVARCHAR(20) -- Estado del sensor (Activo/Inactivo)
);

-- Tabla: Lecturas_Sensores
CREATE TABLE Lecturas_Sensores (
    ID_Lectura INT PRIMARY KEY, -- Identificador �nico de la lectura
    ID_Sensor INT FOREIGN KEY REFERENCES Sensores(ID_Sensor), -- Relaci�n con Sensores
    Fecha_Hora DATETIME, -- Fecha y hora de la lectura
    Valor DECIMAL(10, 2) -- Valor registrado por el sensor
);

-- Tabla: Reglas_Patron
CREATE TABLE Reglas_Patron (
    ID_Regla INT PRIMARY KEY, -- Identificador �nico de la regla
    Nombre NVARCHAR(100), -- Nombre de la regla
    Descripcion NVARCHAR(255), -- Descripci�n de la regla
    Condicion NVARCHAR(255), -- Condici�n de la regla
    Accion NVARCHAR(255), -- Acci�n a ejecutar
    Estado NVARCHAR(20) -- Estado de la regla (Activo/Inactivo)
);

-- Tabla: Patrones_Detectados
CREATE TABLE Patrones_Detectados (
    ID_Patron INT PRIMARY KEY, -- Identificador �nico del patr�n
    ID_Sensor INT FOREIGN KEY REFERENCES Sensores(ID_Sensor), -- Relaci�n con Sensores
    Fecha_Hora DATETIME, -- Fecha y hora en que se detect� el patr�n
    Tipo NVARCHAR(100), -- Tipo de patr�n detectado
    Descripcion NVARCHAR(255), -- Descripci�n del patr�n
    Nivel_Severidad NVARCHAR(20), -- Nivel de severidad del patr�n
    Estado NVARCHAR(20) -- Estado del patr�n
);

-- Tabla: Acciones_Ejecutadas
CREATE TABLE Acciones_Ejecutadas (
    ID_Accion INT PRIMARY KEY, -- Identificador �nico de la acci�n
    ID_Patron INT FOREIGN KEY REFERENCES Patrones_Detectados(ID_Patron), -- Relaci�n con Patrones_Detectados
    Fecha_Hora DATETIME, -- Fecha y hora en que se ejecut� la acci�n
    Accion NVARCHAR(255), -- Detalle de la acci�n realizada
    Estado NVARCHAR(20) -- Estado de la acci�n (Completada/Pendiente)
);

-- Tabla: Modelos_Predictivos
CREATE TABLE Modelos_Predictivos (
    ID_Modelo INT PRIMARY KEY, -- Identificador �nico del modelo
    Nombre NVARCHAR(100), -- Nombre del modelo predictivo
    Descripcion NVARCHAR(255), -- Descripci�n del modelo
    Fecha_Creacion DATE, -- Fecha en que se cre� el modelo
    Estado NVARCHAR(20) -- Estado del modelo (Activo/Inactivo)
);

-- Tabla: Historial_Predicciones
CREATE TABLE Historial_Predicciones (
    ID_Prediccion INT PRIMARY KEY, -- Identificador �nico de la predicci�n
    ID_Modelo INT FOREIGN KEY REFERENCES Modelos_Predictivos(ID_Modelo), -- Relaci�n con Modelos_Predictivos
    Fecha_Hora DATETIME, -- Fecha y hora de la predicci�n
    Valor_Pronosticado DECIMAL(10, 2) -- Valor pronosticado por el modelo
);

-- Tabla: Configuraciones_Sistema
CREATE TABLE Configuraciones_Sistema (
    ID_Configuracion INT PRIMARY KEY, -- Identificador �nico de la configuraci�n
    Parametro NVARCHAR(100), -- Nombre del par�metro de configuraci�n
    Valor NVARCHAR(255) -- Valor del par�metro
);

--Tabla: control de errores

CREATE TABLE [dbo].[ErrorLog](
	[ErrorMessage] [nvarchar](4000) NULL,
	[ErrorSeverity] [int] NULL,
	[ErrorState] [int] NULL,
	[ErrorLine] [int] NULL,
	[ErrorProcedure] [nvarchar](200) NULL,
	[Fecha] [datetime] NULL
)