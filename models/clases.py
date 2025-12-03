"""
Módulo de clases para el simulador de trenes.
Define las entidades principales: Tren, Estación, Ruta y Pasajero.
"""

import datetime as dt
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field


class Tren:
    """
    Representa un tipo de tren con sus especificaciones técnicas.
    
    Attributes:
        nombre: Identificador único del tipo de tren
        capacidad: Número máximo de pasajeros que puede transportar
        combustible: Tipo de combustible/energía (Diésel, Eléctrico, Híbrido)
        velocidad_max: Velocidad máxima en km/h
    """
    
    def __init__(self, nombre: str, capacidad: int, combustible: str, velocidad_max: int):
        self._validar_parametros(nombre, capacidad, velocidad_max)
        
        self.nombre = nombre
        self.capacidad = capacidad
        self.combustible = combustible
        self.velocidad_max = velocidad_max
        self.pasajeros = []   
    @staticmethod
    def _validar_parametros(nombre: str, capacidad: int, velocidad_max: int):
        """Valida los parámetros de entrada."""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del tren no puede estar vacío")
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")
        if velocidad_max <= 0:
            raise ValueError("La velocidad máxima debe ser mayor a 0")
    
    def __str__(self) -> str:
        """Retorna una representación legible del objeto."""
        return (
            f"Tren {self.nombre} | "
            f"Capacidad: {self.capacidad} pax | "
            f"Combustible: {self.combustible} | "
            f"Velocidad Máx: {self.velocidad_max} km/h"
        )
    
    def __repr__(self) -> str:
        """Retorna una representación técnica del objeto."""
        return (
            f"Tren(nombre='{self.nombre}', capacidad={self.capacidad}, "
            f"combustible='{self.combustible}', velocidad_max={self.velocidad_max})"
        )
    
    def calcular_tiempo_ruta(self, distancia: float) -> float:
        """
        Calcula el tiempo teórico para recorrer una ruta a velocidad constante.
        
        Args:
            distancia: Distancia de la ruta en kilómetros
            
        Returns:
            Tiempo en horas para completar la ruta
        """
        if distancia < 0:
            raise ValueError("La distancia no puede ser negativa")
        
        if self.velocidad_max > 0:
            return distancia / self.velocidad_max
        
        return float('inf')
    
    def calcular_tiempo_ruta_minutos(self, distancia: float) -> float:
        """
        Calcula el tiempo para recorrer una ruta en minutos.
        
        Args:
            distancia: Distancia de la ruta en kilómetros
            
        Returns:
            Tiempo en minutos para completar la ruta
        """
        return self.calcular_tiempo_ruta(distancia) * 60
    
    def consumo_estimado(self, distancia: float, factor_consumo: float = 1.0) -> float:
        """
        Estima el consumo de combustible/energía para una ruta.
        
        Args:
            distancia: Distancia en kilómetros
            factor_consumo: Factor de ajuste según tipo de combustible
            
        Returns:
            Consumo estimado en unidades arbitrarias
        """
        # Fórmula simplificada: capacidad y distancia afectan el consumo
        return (self.capacidad * 0.1 + distancia * 0.5) * factor_consumo
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto a diccionario para serialización."""
        return {
            'nombre': self.nombre,
            'capacidad': self.capacidad,
            'combustible': self.combustible,
            'velocidad_max': self.velocidad_max
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tren':
        """Crea una instancia desde un diccionario."""
        return cls(
            nombre=data['nombre'],
            capacidad=data['capacidad'],
            combustible=data['combustible'],
            velocidad_max=data['velocidad_max']
        )


class Pasajero:
    """
    Representa a un pasajero en la simulación.
    
    Attributes:
        id: Identificador único del pasajero
        origen: Estación de origen
        destino: Estación de destino
        tiempo_llegada: Momento en que llegó a la estación
        tiempo_partida: Momento en que abordó el tren (None si aún espera)
    """
    
    # Contador estático para asignar IDs únicos
    id_counter: int = 1000

    def __init__(self, origen: str, destino: str, tiempo_llegada: dt.datetime):
        self._validar_parametros(origen, destino)
        
        self.id = Pasajero.id_counter
        Pasajero.id_counter += 1
        
        self.origen = origen
        self.destino = destino
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_partida: Optional[dt.datetime] = None
    
    @staticmethod
    def _validar_parametros(origen: str, destino: str):
        """Valida los parámetros de entrada."""
        if not origen or not origen.strip():
            raise ValueError("El origen no puede estar vacío")
        if not destino or not destino.strip():
            raise ValueError("El destino no puede estar vacío")
        if origen == destino:
            raise ValueError("El origen y destino deben ser diferentes")
    
    def __str__(self) -> str:
        """Retorna una representación legible del objeto."""
        estado = "En tránsito" if self.tiempo_partida else "Esperando"
        return f"Pasajero #{self.id} | {self.origen} → {self.destino} | Estado: {estado}"
    
    def __repr__(self) -> str:
        """Retorna una representación técnica del objeto."""
        return (
            f"Pasajero(id={self.id}, origen='{self.origen}', "
            f"destino='{self.destino}', tiempo_llegada={self.tiempo_llegada})"
        )
    
    def registrar_partida(self, tiempo: Optional[dt.datetime] = None):
        """
        Registra el momento en que el pasajero aborda el tren.
        
        Args:
            tiempo: Momento de partida. Si es None, usa el tiempo actual.
        """
        self.tiempo_partida = tiempo or dt.datetime.now()
    
    def tiempo_espera(self) -> dt.timedelta:
        """
        Calcula el tiempo que el pasajero ha esperado o esperó.
        
        Returns:
            Duración de la espera. Si aún no parte, retorna timedelta(0)
        """
        if self.tiempo_partida:
            return self.tiempo_partida - self.tiempo_llegada
        return dt.timedelta(seconds=0)
    
    def tiempo_espera_minutos(self) -> float:
        """
        Calcula el tiempo de espera en minutos.
        
        Returns:
            Tiempo de espera en minutos
        """
        return self.tiempo_espera().total_seconds() / 60
    
    def esta_esperando(self) -> bool:
        """Verifica si el pasajero aún está esperando."""
        return self.tiempo_partida is None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto a diccionario para serialización."""
        return {
            'id': self.id,
            'origen': self.origen,
            'destino': self.destino,
            'tiempo_llegada': self.tiempo_llegada.isoformat(),
            'tiempo_partida': self.tiempo_partida.isoformat() if self.tiempo_partida else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Pasajero':
        """Crea una instancia desde un diccionario."""
        pasajero = cls(
            origen=data['origen'],
            destino=data['destino'],
            tiempo_llegada=dt.datetime.fromisoformat(data['tiempo_llegada'])
        )
        pasajero.id = data['id']
        
        if data.get('tiempo_partida'):
            pasajero.tiempo_partida = dt.datetime.fromisoformat(data['tiempo_partida'])
        
        # Actualizar contador estático si es necesario
        if pasajero.id >= Pasajero.id_counter:
            Pasajero.id_counter = pasajero.id + 1
        
        return pasajero
    
    @classmethod
    def reset_counter(cls, valor: int = 1000):
        """Reinicia el contador de IDs."""
        cls.id_counter = valor


class Estacion:
    """
    Representa una estación de tren con su ubicación y gestión de pasajeros.
    
    Attributes:
        nombre: Nombre identificador de la estación
        coordenada_x: Posición X en el mapa
        coordenada_y: Posición Y en el mapa
        pasajeros_esperando: Lista de pasajeros en la estación
    """
    
    def __init__(self, nombre: str, coordenada_x: int, coordenada_y: int):
        self._validar_parametros(nombre, coordenada_x, coordenada_y)
        
        self.nombre = nombre
        self.coordenada_x = coordenada_x
        self.coordenada_y = coordenada_y
        self.pasajeros_esperando: List[Pasajero] = []
    def agregar_pasajero(self, pasajero):
        self.pasajeros_esperando.append(pasajero)
    
    @staticmethod
    def _validar_parametros(nombre: str, coordenada_x: int, coordenada_y: int):
        """Valida los parámetros de entrada."""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la estación no puede estar vacío")
        if coordenada_x < 0:
            raise ValueError("La coordenada X no puede ser negativa")
        if coordenada_y < 0:
            raise ValueError("La coordenada Y no puede ser negativa")
    
    def __str__(self) -> str:
        """Retorna una representación legible del objeto."""
        return (
            f"Estación {self.nombre} | "
            f"Ubicación: ({self.coordenada_x}, {self.coordenada_y}) | "
            f"Esperando: {len(self.pasajeros_esperando)} pax"
        )
    
    def __repr__(self) -> str:
        """Retorna una representación técnica del objeto."""
        return (
            f"Estacion(nombre='{self.nombre}', "
            f"coordenada_x={self.coordenada_x}, coordenada_y={self.coordenada_y})"
        )
    
    def agregar_pasajero(self, pasajero: Pasajero):
        """
        Añade un pasajero a la cola de la estación.
        
        Args:
            pasajero: Objeto Pasajero a añadir
            
        Raises:
            ValueError: Si el origen del pasajero no coincide con la estación
        """
        if pasajero.origen != self.nombre:
            raise ValueError(
                f"El pasajero tiene origen '{pasajero.origen}' "
                f"pero está en la estación '{self.nombre}'"
            )
        
        self.pasajeros_esperando.append(pasajero)
    
    def agregar_pasajeros(self, pasajeros: List[Pasajero]):
        """Añade múltiples pasajeros a la cola."""
        for pasajero in pasajeros:
            self.agregar_pasajero(pasajero)
    
    def despachar_pasajeros(
        self,
        destino: str,
        capacidad_tren: int,
        tiempo_partida: Optional[dt.datetime] = None
    ) -> List[Pasajero]:
        """
        Despacha pasajeros con destino específico que caben en el tren.
        
        Args:
            destino: Estación de destino
            capacidad_tren: Capacidad disponible en el tren
            tiempo_partida: Momento de partida (None usa tiempo actual)
            
        Returns:
            Lista de pasajeros que abordan el tren
        """
        pasajeros_a_cargar = []
        pasajeros_restantes = []
        cargados = 0
        
        tiempo = tiempo_partida or dt.datetime.now()
        
        for pasajero in self.pasajeros_esperando:
            if pasajero.destino == destino and cargados < capacidad_tren:
                pasajero.registrar_partida(tiempo)
                pasajeros_a_cargar.append(pasajero)
                cargados += 1
            else:
                pasajeros_restantes.append(pasajero)
        
        self.pasajeros_esperando = pasajeros_restantes
        return pasajeros_a_cargar
    
    def contar_pasajeros_destino(self, destino: str) -> int:
        """Cuenta cuántos pasajeros esperan ir a un destino específico."""
        return sum(1 for p in self.pasajeros_esperando if p.destino == destino)
    
    def obtener_destinos_demandados(self) -> Dict[str, int]:
        """
        Retorna un diccionario con los destinos y cantidad de pasajeros.
        
        Returns:
            Dict con formato {destino: cantidad_pasajeros}
        """
        destinos = {}
        for pasajero in self.pasajeros_esperando:
            destinos[pasajero.destino] = destinos.get(pasajero.destino, 0) + 1
        return destinos
    
    def tiempo_espera_promedio(self) -> float:
        """
        Calcula el tiempo de espera promedio de los pasajeros en minutos.
        
        Returns:
            Tiempo promedio en minutos, 0 si no hay pasajeros
        """
        if not self.pasajeros_esperando:
            return 0.0
        
        ahora = dt.datetime.now()
        total_minutos = sum(
            (ahora - p.tiempo_llegada).total_seconds() / 60
            for p in self.pasajeros_esperando
        )
        
        return total_minutos / len(self.pasajeros_esperando)
    
    def limpiar_pasajeros(self):
        """Elimina todos los pasajeros de la estación."""
        self.pasajeros_esperando.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto a diccionario para serialización."""
        return {
            'nombre': self.nombre,
            'coord_x': self.coordenada_x,
            'coord_y': self.coordenada_y,
            'pasajeros_esperando': [p.to_dict() for p in self.pasajeros_esperando]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Estacion':
        """Crea una instancia desde un diccionario."""
        estacion = cls(
            nombre=data['nombre'],
            coordenada_x=data['coord_x'],
            coordenada_y=data['coord_y']
        )
        
        if data.get('pasajeros_esperando'):
            estacion.pasajeros_esperando = [
                Pasajero.from_dict(p_dict)
                for p_dict in data['pasajeros_esperando']
            ]
        
        return estacion


class Ruta:
    """
    Representa una conexión directa entre dos estaciones.
    
    Attributes:
        origen: Nombre de la estación de origen
        destino: Nombre de la estación de destino
        distancia_km: Distancia en kilómetros
    """
    
    def __init__(self, origen: str, destino: str, distancia_km: float):
        self._validar_parametros(origen, destino, distancia_km)
        
        self.origen = origen
        self.destino = destino
        self.distancia_km = distancia_km
    
    @staticmethod
    def _validar_parametros(origen: str, destino: str, distancia_km: float):
        """Valida los parámetros de entrada."""
        if not origen or not origen.strip():
            raise ValueError("El origen no puede estar vacío")
        if not destino or not destino.strip():
            raise ValueError("El destino no puede estar vacío")
        if origen == destino:
            raise ValueError("El origen y destino deben ser diferentes")
        if distancia_km <= 0:
            raise ValueError("La distancia debe ser mayor a 0")
    
    def __str__(self) -> str:
        """Retorna una representación legible del objeto."""
        return f"Ruta: {self.origen} → {self.destino} ({self.distancia_km} km)"
    
    def __repr__(self) -> str:
        """Retorna una representación técnica del objeto."""
        return (
            f"Ruta(origen='{self.origen}', destino='{self.destino}', "
            f"distancia_km={self.distancia_km})"
        )
    
    def __eq__(self, other) -> bool:
        """Compara dos rutas."""
        if not isinstance(other, Ruta):
            return False
        return (
            self.origen == other.origen and
            self.destino == other.destino and
            self.distancia_km == other.distancia_km
        )
    
    def es_ruta_inversa(self, otra_ruta: 'Ruta') -> bool:
        """
        Verifica si otra ruta es la inversa de esta.
        
        Args:
            otra_ruta: Ruta a comparar
            
        Returns:
            True si es la ruta inversa
        """
        return (
            self.origen == otra_ruta.destino and
            self.destino == otra_ruta.origen and
            self.distancia_km == otra_ruta.distancia_km
        )
    
    def calcular_tiempo_viaje(self, velocidad: float) -> float:
        """
        Calcula el tiempo de viaje a una velocidad dada.
        
        Args:
            velocidad: Velocidad en km/h
            
        Returns:
            Tiempo en horas
        """
        if velocidad <= 0:
            raise ValueError("La velocidad debe ser mayor a 0")
        return self.distancia_km / velocidad
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto a diccionario para serialización."""
        return {
            'origen': self.origen,
            'destino': self.destino,
            'distancia_km': self.distancia_km
        }
    
    def to_tuple(self) -> tuple:
        """Convierte el objeto a tupla (compatibilidad con código legacy)."""
        return (self.origen, self.destino, self.distancia_km)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Ruta':
        """Crea una instancia desde un diccionario."""
        return cls(
            origen=data['origen'],
            destino=data['destino'],
            distancia_km=data['distancia_km']
        )
    
    @classmethod
    def from_tuple(cls, data: tuple) -> 'Ruta':
        """Crea una instancia desde una tupla (origen, destino, distancia)."""
        if len(data) != 3:
            raise ValueError("La tupla debe tener exactamente 3 elementos")
        return cls(origen=data[0], destino=data[1], distancia_km=data[2])
class Cliente:
    """guarda datos de os clientes"""
    def __init__(self, id, fecha: dt.datetime):
        self.id = id
        self.fecha = fecha

    def __repr__(self):
        return f"Cliente {self.id} ({self.fecha.strftime('%H:%M')})"


def constructor_cliente(id, fecha):
    return Cliente(id, fecha)