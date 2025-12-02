import datetime as dt
from collections.abc import Callable
from typing import Any

from ppdc_timed_generator.generadores import GeneradorUniforme


class EstadoDeSimulacion:
    def __init__(
        self,
        id: int,
        hora_inicial: dt.datetime,
    ):
        self.id = id
        self.hora_inicial = hora_inicial

        self.estaciones: dict[int, Estacion] = []
        self.next_id_estaciones: int = 0

    def crear_estacion_dummy(self, nombre: str, poblacion: int = 100_000):
        estacion = Estacion(
            estado_simulacion=self,
            id=self.next_id_estaciones,
            nombre="Ferroviario Valdivia",
            poblacion=poblacion,
            hora_inicio=dt.time(7, 0),
            hora_final=dt.time(20, 0),
        )
        self.next_id_estaciones += 1
        self.estaciones.append(estacion)
        return self.estaciones[-1]


class Cliente:
    def __init__(
        self,
        id: int,
        id_estacion: Any,
        hora_creacion: dt.datetime,
        opciones_estaciones: list = [],
    ):
        self.id = id
        self.id_estacion = id_estacion
        self.nombre = f"Cliente_{id}"
        self.edad = 18 + (id % 50)

        """Para obtener las estaciones posibles, necesitamos que exista un EstadoDeSimulacion
        en algún lugar namescope exterior (por ejemplo, desde __main__).
        Para esto entonces debe utilizarse el mismo nombre de variable
        """
        global g_estado
        self.destino = opciones_estaciones[id % len(opciones_estaciones)]

        self.hora_creacion = hora_creacion
        self.origen = ...
        self.delay = ...  # Cuándo vuelve.


class Estacion:
    def __init__(
        self,
        estado_simulacion: EstadoDeSimulacion,
        id: int,
        nombre: str,
        poblacion: int,
        hora_inicio: dt.time,
        hora_final: dt.time,
    ):
        """El primer argumento forma un vínculo al [EstadoDeSimulacion], lo que nos permitirá
        conocer las estaciones, y otros atributos, desde esta misma clase Estacion."""
        self._estado = estado_simulacion
        self.id = id
        self.nombre = nombre
        self.poblacion = poblacion
        self.generador = GeneradorUniforme(
            poblacion, 123, dt.datetime.now(), hora_inicio, hora_final
        )
        self.clientes: list[Cliente] = []

    def generar_demanda(self, minutos: int, update: bool = True):
        """Para generar_demanda, primero debemos establecer nuestra función para generar al Cliente o Pasajero.
        Recuerda que el generador sólo entregará el [id] y la [fecha_creacion] al cliente.

        En este ejemplo, mi Cliente también necesita el id de su estación (para filtrar su destino),
        por lo tanto creo esta función intermedia [cliente_factory], donde aprovecho
        a pasarle el [self.id], que corresponde con el [id] de la Estación donde el Cliente fue creado.

        También es necesario que le entreguemos las opciones de estaciones disponibles,
        que podemos conseguir teniendo acceso al [EstadoDeSimulacion].
        """

        def cliente_factory(id, fecha_creacion):
            op_estaciones = [e.id for e in self._estado.estaciones]
            op_estaciones.remove(self.id)
            return Cliente(
                id, self.id, fecha_creacion, opciones_estaciones=op_estaciones
            )

        nuevos = self.generador.generar_clientes(
            minutos, cliente_factory, update=update
        )
        self.clientes.extend(nuevos)
        return self.clientes

    def reiniciar(self):
        self.clientes = []
        # TODO: Reiniciar el generador, y actualizar la hora
