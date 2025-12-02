from ppdc_timed_generator.Generador_r import Generador
class GeneradorUniforme(Generador_r):
    def generar_clientes(
        self,
        minutos: int,
        constructor: Callable[[int, dt.datetime], Any],
        update: bool = True,
    ) -> list[Any]:
        clientes = []
        cantidad = int(self.poblacion * minutos / self.minutos_de_funcionamiento())

        for _ in range(cantidad):
            cliente_id = self.rdm.randint(1, self.poblacion)
            fecha = self.current_datetime
            clientes.append(constructor(cliente_id, fecha))

        if update:
            self.current_datetime += dt.timedelta(minutes=minutos)

        return clientes
