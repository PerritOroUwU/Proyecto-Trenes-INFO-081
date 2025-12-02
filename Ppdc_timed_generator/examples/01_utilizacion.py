import datetime as dt

from dummy_classes import EstadoDeSimulacion


def test_crear_y_generar_en_N_minutos(poblacion: int, minutos: int):
    g_estado: EstadoDeSimulacion = EstadoDeSimulacion(
        0, dt.datetime(2025, 1, 1)
    )

    estacion1 = g_estado.crear_estacion_dummy("Ferroviario Valdivia", poblacion)
    # Para probar, necesitamos al menos dos estaciones.
    g_estado.crear_estacion_dummy("Ferroviario BioBio", poblacion)

    res = estacion1.generar_demanda(minutos)
    size = len(res)
    print()
    print(f"Para {poblacion} pasajeros,")
    print(f"{size} clientes en {minutos} minutos.")
    return estacion1


if __name__ == "__main__":
    POBLACION = 100_000

    # Test pequeño:
    estacion = test_crear_y_generar_en_N_minutos(POBLACION, 10)

    # Test para toda la jornada:
    todos_minutos_servicio = (dt.time(20, 0).hour - dt.time(7, 0).hour) * 60
    estacion = test_crear_y_generar_en_N_minutos(
        POBLACION, todos_minutos_servicio
    )

    print("Clientes generados:", len(estacion.clientes))
    res = len(estacion.clientes)
    print("Min permitido:", POBLACION * 0.19)
    print("Max permitido:", POBLACION * 0.21)
    is_valid = POBLACION * 0.19 <= res <= POBLACION * 0.21
    print(["No", "Si"][is_valid], "está dentro del rango.")
    assert is_valid
