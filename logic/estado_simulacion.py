from datetime import datetime, timedelta, time
from models.clases import *
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

    def tiempo_actual(self):
        # Actualiza la hora y fecha actual en formato legible.
        hora = self.tiempo_actual.strftime("%H:%M:%S")
        fecha = self.tiempo_actual.strftime("%d/%m/%Y")
        return hora, fecha
    
    def avance_de_tiempo(self, segundos=1):
        #avance de tiempo en 1 segundo y si pasa de las 8 pm, actualizar la fecha al dia siguiente
        self.tiempo_actual += timedelta(seconds=segundos)
        
        if self.tiempo_actual.hour >= 20:
            nueva_fecha = self.tiempo_actual.date() + timedelta(days=1)
            self.tiempo_actual = datetime.combine(nueva_fecha, time(7, 0, 0))
        
        return self.tiempo_actual

    def generador_eventos(self):
        # Generador de eventos aleatorios en la simulacion
        #revisar como usar la semilla para generar eventos que se pueda repetir
        eventos = [
            #nombre de eventos con sus caracteristicas(self)
        ]
        evento = random.choice(eventos)
        return evento

    #def __str__(self):
        #hora, fecha = self.actualizar_display()
        #return f"EstadoSimulacion(hora_actual={hora}, fecha={fecha})"
        #Revisar si esto es util