class Tren:
    """
    Representa un tipo de tren con sus especificaciones de ingeniería.
    """
    def __init__(self, nombre: str, capacidad: int, combustible: str, velocidad_max: int):
        self.nombre = nombre
        self.capacidad = capacidad
        self.combustible = combustible
        self.velocidad_max = velocidad_max
        
    def __str__(self):
        """Retorna una representación legible del objeto."""
        return (f"Tren {self.nombre} | Capacidad: {self.capacidad} pax | "
                f"Combustible: {self.combustible} | Velocidad Máx: {self.velocidad_max} km/h")
        
    def calcular_tiempo_ruta(self, distancia: float) -> float:
        """
        Calcula el tiempo mínimo teórico para recorrer una ruta, 
        asumiendo velocidad constante (Velocidad Máx).
        Retorna el tiempo en horas.
        """
        if self.velocidad_max > 0:
            return distancia / self.velocidad_max
        return float('inf') # Retorna infinito si la velocidad es cero
    
class Pasajero:
    """
    Representa a un pasajero en la simulación. 
    Se le puede añadir lógica como el origen, destino y el tiempo de espera.
    """
    id_counter = 1000 # Contador estático para asignar IDs únicos

    def __init__(self, origen: str, destino: str, tiempo_llegada: dt.datetime):
        # Asigna un ID único y lo incrementa
        self.id = Pasajero.id_counter
        Pasajero.id_counter += 1
        
        self.origen = origen
        self.destino = destino
        self.tiempo_llegada = tiempo_llegada # Cuando llegó a la estación
        self.tiempo_partida = None            # Cuando sube a un tren
        
    def tiempo_espera(self) -> dt.timedelta:
        """Calcula el tiempo que el pasajero esperó si ya partió."""
        if self.tiempo_partida:
            return self.tiempo_partida - self.tiempo_llegada
        return dt.timedelta(seconds=0) # Todavía esperando

# Nota: Necesitas importar 'datetime' si usas el tipo dt.datetime
import datetime as dt

class Estacion:
    """
    Representa una estación de tren, su ubicación y la cola de pasajeros.
    """
    def __init__(self, nombre: str, coordenada_x: int, coordenada_y: int):
        self.nombre = nombre
        self.coordenada_x = coordenada_x
        self.coordenada_y = coordenada_y
        self.pasajeros_esperando = [] # Lista de objetos Pasajero

    def __str__(self):
        return f"Estación {self.nombre} | Ubicación: ({self.coordenada_x}, {self.coordenada_y}) | Esperando: {len(self.pasajeros_esperando)} pax"

    def agregar_pasajero(self, pasajero: Pasajero):
        """Añade un pasajero a la cola de la estación."""
        self.pasajeros_esperando.append(pasajero)

    def despachar_pasajeros(self, destino: str, capacidad_tren: int) -> list[Pasajero]:
        """
        Retorna la lista de pasajeros con destino específico que caben en el tren, 
        y los elimina de la cola de espera.
        """
        pasajeros_a_cargar = []
        pasajeros_restantes = []
        cargados = 0
        
        for p in self.pasajeros_esperando:
            if p.destino == destino and cargados < capacidad_tren:
                pasajeros_a_cargar.append(p)
                cargados += 1
            else:
                pasajeros_restantes.append(p)
                
        self.pasajeros_esperando = pasajeros_restantes
        return pasajeros_a_cargar
    
class Ruta:
    """
    Representa una conexión directa (ruta) entre dos estaciones.
    """
    def __init__(self, origen: str, destino: str, distancia_km: float):
        self.origen = origen       # Nombre de la estación de origen
        self.destino = destino     # Nombre de la estación de destino
        self.distancia_km = distancia_km
        
    def __str__(self):
        return f"Ruta: {self.origen} -> {self.destino} ({self.distancia_km} km)"