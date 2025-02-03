USE [IotBD]
GO
/****** Object:  StoredProcedure [dbo].[GenerarLecturasSensor_PR]    Script Date: 2/2/2025 1:06:12 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[GenerarLecturasSensor_PR]
    @TipoSensor NVARCHAR(50),
    @FechaHora DATETIME
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        DECLARE @SensorID INT;
        DECLARE @RandomValue DECIMAL(10,2);
        DECLARE @EsAnomalo BIT = CASE WHEN RAND() < 0.50 THEN 1 ELSE 0 END; -- 15% de probabilidad de anomalía

        SET @SensorID = CASE 
            WHEN @TipoSensor = 'Temperatura' THEN 1
            WHEN @TipoSensor = 'Consumo Eléctrico' THEN 2
            WHEN @TipoSensor = 'Ocupación' THEN 3
            WHEN @TipoSensor = 'Luz Ambiental' THEN 4
            WHEN @TipoSensor = 'Humedad' THEN 5
            ELSE NULL
        END;

        IF @SensorID IS NULL
        BEGIN
            RAISERROR ('Error: Tipo de sensor inválido', 16, 1);
            RETURN;
        END;

        -- Generar valores normales o anómalos
        SET @RandomValue = CASE 
            WHEN @SensorID = 1 THEN 
                CASE WHEN @EsAnomalo = 1 THEN RAND() * 40 + 50 ELSE RAND() * 10 + 20 END -- Temperatura: 20-30°C (Normal), 50-90°C (Anómalo)
            WHEN @SensorID = 2 THEN 
                CASE WHEN @EsAnomalo = 1 THEN RAND() * 500 + 500 ELSE RAND() * 100 + 20 END -- Consumo eléctrico: 20-120 kWh (Normal), 500-1000 kWh (Anómalo)
            WHEN @SensorID = 3 THEN 
                CASE WHEN @EsAnomalo = 1 THEN RAND() * 50 + 20 ELSE RAND() * 10 END -- Ocupación: 0-10 (Normal), 20-60 (Anómalo)
            WHEN @SensorID = 4 THEN 
                CASE WHEN @EsAnomalo = 1 THEN RAND() * 2000 + 3000 ELSE RAND() * 500 + 300 END -- Luz ambiental: 300-800 lux (Normal), 3000-5000 lux (Anómalo)
            WHEN @SensorID = 5 THEN 
                CASE WHEN @EsAnomalo = 1 THEN RAND() * 80 + 100 ELSE RAND() * 40 + 30 END -- Humedad: 30-70% (Normal), 100-180% (Anómalo)
        END;

        INSERT INTO Lecturas_Sensores (ID_Sensor, Fecha_Hora, Valor)
        VALUES (@SensorID, @FechaHora, @RandomValue);
    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000);
        DECLARE @ErrorSeverity INT;
        DECLARE @ErrorState INT;
        DECLARE @ErrorLine INT;
        DECLARE @ErrorProcedure NVARCHAR(200);

        SELECT 
            @ErrorMessage = ERROR_MESSAGE(),
            @ErrorSeverity = ERROR_SEVERITY(),
            @ErrorState = ERROR_STATE(),
            @ErrorLine = ERROR_LINE(),
            @ErrorProcedure = ERROR_PROCEDURE();

        INSERT INTO ErrorLog (ErrorMessage, ErrorSeverity, ErrorState, ErrorLine, ErrorProcedure, Fecha)
        VALUES (@ErrorMessage, @ErrorSeverity, @ErrorState, @ErrorLine, @ErrorProcedure, GETDATE());
    END CATCH
END;
