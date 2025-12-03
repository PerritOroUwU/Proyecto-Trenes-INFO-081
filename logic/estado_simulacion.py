from datetime import datetime, timedelta, time
from modelos.clases import *
import random;

class EstadoSimulacion:
    def __init__(self, fecha_inicio_str= "2015-01-01 07:00:00", semilla=random.randint(0, 10000)):
        self.fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M:%S")
        self.fecha_actual = self.fecha_inicio
        random.seed(semilla)

        self.historial_eventos = []
        self.historial_elecciones = []

        #self.trenes =
        #self.estaciones =