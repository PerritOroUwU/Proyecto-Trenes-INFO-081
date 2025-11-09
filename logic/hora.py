from datetime import datetime, timedelta

class HoraActual:
    def __init__(self):
        self.hora_actual = datetime(2015, 3, 1, 7, 0)
    
    def avanzar_tiempo(self, minutos):
        self.hora_actual += timedelta(minutes=minutos)
    
    def reiniciar(self):
        self.hora_actual = datetime(2015, 3, 1, 7, 0)
    
    def __str__(self):
        return f"Hora actual de la simulación: {self.hora_actual}"