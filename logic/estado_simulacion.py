from datetime import datetime, timedelta, time
from modelos.clases import *
import random;

class EstadoSimulacion:
    def __init__(self, fecha_inicio_str= "2015-01-01 07:00:00", semilla=random.randint(0, 10000)):
        #inicio en donde si no hay una fecha dada, se inicia en 1 de enero de 2015 a las 7:00 am
        #y poder generar una semilla para poder en un futuro obtener los mismos resultados
        self.fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M:%S")
        self.fecha_actual = self.fecha_inicio 
        # Revisar si es correcto la fecha obtenida
        random.seed(semilla)

        self.historial_eventos = []
        self.historial_elecciones = []

        #self.trenes =
        #self.estaciones =

    def avanzar_tiempo(self, minutos):
        self.fecha_actual += timedelta(minutes=minutos)