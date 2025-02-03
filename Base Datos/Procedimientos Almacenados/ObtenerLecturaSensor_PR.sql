USE [IotBD]
GO
/****** Object:  StoredProcedure [dbo].[ObtenerLecturaSensor_PR]    Script Date: 2/2/2025 6:13:29 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[ObtenerLecturaSensor_PR]
    @id_sensor int       
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
      
		
        
       SELECT ID_Lectura,ID_Sensor,Fecha_Hora, Valor
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
        
        -- Opcional: Loggear el error o insertarlo en una tabla de logs
        INSERT INTO ErrorLog (ErrorMessage, ErrorSeverity, ErrorState, ErrorLine, ErrorProcedure, Fecha)
        VALUES (@ErrorMessage, @ErrorSeverity, @ErrorState, @ErrorLine, @ErrorProcedure, GETDATE());
        
    END CATCH
END;
