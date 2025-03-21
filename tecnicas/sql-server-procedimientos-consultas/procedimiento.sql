CREATE PROCEDURE InsertarEmpleado
    @ID INT,
    @Nombre NVARCHAR(50),
    @Departamento NVARCHAR(50),
    @Salario DECIMAL(10, 2)
AS
BEGIN
    DECLARE @PresupuestoActual DECIMAL(15, 2);
    DECLARE @NuevoPresupuesto DECIMAL(15, 2);
    DECLARE @STATUS_CODE INT;
    DECLARE @STATUS_MESSAGE NVARCHAR(100);

    BEGIN TRY
        -- Presupuesto actual del departamento
        SELECT @PresupuestoActual = Presupuesto
        FROM Departamentos
        WHERE Departamento = @Departamento;

        -- Calcular el nuevo presupuesto
        SET @NuevoPresupuesto = @PresupuestoActual - @Salario;

        -- Verificar si el nuevo presupuesto es válido
        IF @NuevoPresupuesto >= 0
        BEGIN
            -- Insertar el nuevo empleado
            INSERT INTO Empleados (ID, Nombre, Departamento, Salario)
            VALUES (@ID, @Nombre, @Departamento, @Salario);

            -- Actualizar el presupuesto del departamento
            UPDATE Departamentos
            SET Presupuesto = @NuevoPresupuesto
            WHERE Departamento = @Departamento;

            -- Código y mensaje de éxito
            SET @STATUS_CODE = 200;
            SET @STATUS_MESSAGE = 'Empleado insertado correctamente.';
        END
        ELSE
        BEGIN
            -- Código y mensaje de error por presupuesto insuficiente
            SET @STATUS_CODE = 400;
            SET @STATUS_MESSAGE = 'Error: Presupuesto insuficiente para agregar el empleado.';
        END
    END TRY
    BEGIN CATCH
        -- Manejo de excepciones no controladas
        SET @STATUS_CODE = 500;
        SET @STATUS_MESSAGE = 'Error: ' + ERROR_MESSAGE();
    END CATCH

    -- Devolver el código y mensaje de estado
    SELECT @STATUS_CODE AS STATUS_CODE, @STATUS_MESSAGE AS STATUS_MESSAGE;
END