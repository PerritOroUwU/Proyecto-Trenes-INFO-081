from typing import Callable,Any
import random;

class opcion:
    def __init__(self,descripcion:str,efecto: Callable[[Any], Any] = None):
        """
        Inicializa una opción con su descripción y su efecto.
        Args:
            descripcion (str): Descripción de la opción.
            efecto (callable): Función que representa el efecto de la opción.
        """
        self.descripcion = descripcion
        self.efecto = efecto
        
    def ejecutar_efecto(self, estado, nombre_evento: str):
        #guarda la eleccion en el historial
        estado.historial_elecciones.append(self.descripcion)
        estado.historial_eventos.append(nombre_evento)
        return self.efecto(estado)

class Evento:
    def __init__(self,nombre:str, descripcion:str, opcion1:opcion,opcion2:opcion):
        """
        Inicializa un evento con su descripción y opciones.
        
        Args:
            descripcion (str): Descripción del evento.
            opciones (list): Lista de opciones disponibles para el evento.
        """
        self.nombre = nombre
        self.descripcion = descripcion
        self.opcion1 = opcion1
        self.opcion2 = opcion2

     

#Ejemplo de como se podria escribir un evento
def crear_evento_niebla(estado:Callable[[Any], Any] = None)->Evento:
    """
    Escoge un tren al azar y crea un evento de niebla que afecta su velocidad.
    la idea es que ocurra cuando el tren este esperando en una estacion, sino no tiene sentido.
    """
    tren = random.choice(estado.trenes)
    
    efecto_reducir_velocidad= lambda s: (
        setattr(tren, 'velocidad', tren.velocidad * 0.5),
        f"La velocidad del tren {tren.nombre} se ha reducido a {tren.velocidad} km/h debido a la niebla."
    )
    
    #FALTA IMPLEMENTAR EFECTO DE ESPERAR
    efecto_esperar= lambda s: (
        f"El tren {tren.nombre} va a esperar hasta que la niebla se disipe."  
    )
        
    

    descripcion_evento = f"Hay una densa niebla que afecta al tren {tren.nombre}. ¿Qué deseas hacer?"
    opcion1 = opcion(
        descripcion="hacer que el tren vaya a menor velocidad.", 
        efecto=efecto_reducir_velocidad
    )
    opcion2= opcion(
        descripcion="Hacer que el tren espere hasta que la niebla se disipe.",
        efecto=efecto_esperar
    )
    return Evento(
        nombre="Niebla densa",
        descripcion=descripcion_evento,
        opcion1=opcion1,
        opcion2=opcion2
    )
    
        