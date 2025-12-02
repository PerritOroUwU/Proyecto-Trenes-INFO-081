import datetime as dt
import random
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

class Generador(ABC):
    def __init__(
        self,
        poblacion: int,
        seed: int = 123,
        fecha_inicial: dt.datetime = dt.datetime(2025, 1, 1),
        hora_apertura: dt.time = dt.time(7, 0),
        hora_cierre: dt.time = dt.time(20, 0),
    ):
        self.poblacion = poblacion
        self.seed = seed
        self.rdm = random.Random(seed)
        self.hora_apertura = hora_apertura
        self.hora_cierre = hora_cierre
        self.current_datetime: dt.datetime = fecha_inicial

    def minutos_de_funcionamiento(self) -> int:
        horas = self.hora_cierre.hour - self.hora_apertura.hour
        return horas * 60

    @abstractmethod
    def generar_clientes(
        self,
        minutos: int,
        constructor: Callable[[int, dt.datetime], Any],
        update: bool = True,
    ) -> list[Any]:
        pass
