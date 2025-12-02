import datetime as dt
import random
from abc import ABC, abstractmethod  # ABSTRACT
from collections.abc import Callable
from typing import Any


class Generador(ABC):
    """Esta clase Generador es utilizada como una **clase abstracta**.
    Esto quiere decir que está clase está preparada para no usarse directamente,
    sino que ser la clase Base (padre, o ascendente) para alguna otra que herede
    de este Generador.

    En específico, tendremos funciones abstractas, como la función [generar_clientes],
    que no tendrán una implementación en la clase base, y que **deben** ser definidas
    en las clases heredadas.

    Para un ejemplo, observa cómo fue creada la clase GeneradorUniforme
    en ./generadores/generador_uniforme.py .
    """

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
        constructor: Callable[[int, dt.datetime], any],
        update: bool = True,
    ) -> list[Any]:
        """Esta función debe ser implementada para cada ---generador--- que herede de esta clase Generador.
        Que sea abstracta, implica que por defecto no está implementada, sino que la clase heredada debe definir su funcionamiento.

        Parameters
        ----------
        minutos: int
            Cantidad de minutos transcurridos, de los cuales se deberán generar una cantidad de Clientes que sea proporcional.
        constructor: Callable[[int, dt.datetime], any]
            Este constructor debe encargarse de instanciar los Clientes o Pasajeros,
            lo que permite entonces escoger al interior de esa función cuál será la clase, en particular, que será instanciada.
            La función **debe** estar preparada para tres parámetros posicionales (sin nombre, solo orden de aparición):
                - int: que corresponde con el id generado de forma aleatoria.
                - dt.datetime: que es el datetime en el cual fue creado el Cliente.
        update: bool = True
            Un booleando que indica si debemos actualizar [self.current_datetime] con la cantidad de minutos entrante.

        Returns
        -------
        list
            a list of strings representing the header columns
        """
        pass  # o ...
