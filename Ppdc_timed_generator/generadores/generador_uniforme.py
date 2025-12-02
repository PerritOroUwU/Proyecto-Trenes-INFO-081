import datetime as dt
import random
from collections.abc import Callable
from typing import Any

from Ppdc_timed_generator.generador import Generador


class GeneradorUniforme(Generador):
    def generar_clientes(
        self,
        minutos: int,
        constructor: Callable[[int, dt.datetime], Any],
        update: bool = True,
    ):
        if update:
            self.current_datetime += dt.timedelta(minutes=minutos)

        cpm = self.poblacion * 0.2 / self.minutos_de_funcionamiento()
        size = int(minutos * cpm)
        clientes = []
        for _ in range(size):
            val = self.rdm.randint(0, 2_000_000)
            cliente = constructor(val, self.current_datetime)
            clientes.append(cliente)
        return clientes
