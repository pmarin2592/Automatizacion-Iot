USE [IotBD]
GO

/****** 
    Procedimiento almacenado: ObtenerLecturaSensor_PR
    Descripción: Recupera las lecturas más recientes de un sensor específico en la última hora.
    Parámetros:
    - @id_sensor (int): Identificador del sensor cuyas lecturas se desean obtener.
    
    Retorna:
    - ID_Lectura (int): Identificador único de la lectura.
    - ID_Sensor (int): Identificador del sensor asociado a la lectura.
    - Fecha_Hora (datetime): Fecha y hora en que se registró la lectura.
    - Valor (float/int): Valor medido por el sensor.

    Manejo de Errores:
    - Captura errores durante la ejecución y almacena detalles en la tabla ErrorLog.
******/


SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[ObtenerLecturaSensor_PR]
    @id_sensor int       
AS
BEGIN
    -- Evita que se devuelvan mensajes innecesarios en la consulta
    SET NOCOUNT ON;
    BEGIN TRY
      
		 -- Recupera las lecturas del sensor en la última hora, ordenadas de forma descendente
         SELECT 
            ID_Lectura,
            ID_Sensor,
            Fecha_Hora,
            Valor
        FROM [dbo].[Lecturas_Sensores]
        WHERE ID_Sensor = @id_sensor
        AND Fecha_Hora >= DATEADD(MINUTE, -60, (SELECT MAX(Fecha_Hora) 
                                                FROM [dbo].[Lecturas_Sensores] 
                                                WHERE ID_Sensor = @id_sensor))
        ORDER BY Fecha_Hora DESC;

    END TRY
    BEGIN CATCH
         -- Capturar detalles del error
        DECLARE @ErrorMessage NVARCHAR(4000);
        DECLARE @ErrorSeverity INT;
        DECLARE @ErrorState INT;
        DECLARE @ErrorLine INT;
        DECLARE @ErrorProcedure NVARCHAR(200);
        
        -- Obtener detalles del error
        SELECT 
            @ErrorMessage = ERROR_MESSAGE(),
            @ErrorSeverity = ERROR_SEVERITY(),
            @ErrorState = ERROR_STATE(),
            @ErrorLine = ERROR_LINE(),
            @ErrorProcedure = ERROR_PROCEDURE();
        
         -- Registrar el error en la tabla de logs (si existe)
        INSERT INTO ErrorLog (ErrorMessage, ErrorSeverity, ErrorState, ErrorLine, ErrorProcedure, Fecha)
        VALUES (@ErrorMessage, @ErrorSeverity, @ErrorState, @ErrorLine, @ErrorProcedure, GETDATE());
        
    END CATCH
END;
