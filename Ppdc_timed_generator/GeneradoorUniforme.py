import datetime as dt
from .generador import Generador

class GeneradorUniforme(Generador):
    """Generador con probabilidad uniforme de llegada por minuto."""

    def __init__(self, poblacion: int, probabilidad: float = 0.05, **kwargs):
        super().__init__(poblacion, **kwargs)
        self.probabilidad = probabilidad

    def generar_clientes(self, minutos: int, constructor, update: bool = True):
        clientes = []
        for m in range(minutos):
            if self.rdm.random() < self.probabilidad:
                cliente_id = self.rdm.randint(1, self.poblacion)
                fecha_cliente = self.current_datetime + dt.timedelta(minutes=m)
                clientes.append(constructor(cliente_id, fecha_cliente))

        if update:
            self.current_datetime += dt.timedelta(minutes=minutos)

        return clientes