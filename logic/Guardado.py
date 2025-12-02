import json
import os
import datetime as dt

SAVE_DIR = "save_data"
DATA_FILENAME = "simulador_datos.json"
DATA_FILE_PATH = os.path.join(SAVE_DIR, DATA_FILENAME)

def serializar_trenes(trenes_objetos):
    """Convierte un diccionario de objetos Tren a un diccionario de diccionarios JSON-compatible."""
    data = {}
    for nombre, tren in trenes_objetos.items():
        data[nombre] = {
            "capacidad": tren.capacidad,
            "combustible": tren.combustible,
            "velocidad_max": tren.velocidad_max
        }
    return data

def serializar_pasajero(pasajero):
    """Convierte un objeto Pasajero a un diccionario JSON-compatible."""
    data = {
        "id": pasajero.id,
        "origen": pasajero.origen,
        "destino": pasajero.destino,
        # Convierte el objeto datetime a un string ISO 8601
        "tiempo_llegada": pasajero.tiempo_llegada.isoformat(),
        # Guarda el tiempo de partida solo si existe
        "tiempo_partida": pasajero.tiempo_partida.isoformat() if pasajero.tiempo_partida else None
    }
    return data

def serializar_estaciones(estaciones_objetos):
    """
    Convierte objetos Estacion a un diccionario JSON-compatible, 
    incluyendo la lista serializada de pasajeros.
    """
    data = {}
    for nombre, estacion in estaciones_objetos.items():
        data[nombre] = {
            "coord_x": estacion.coordenada_x,
            "coord_y": estacion.coordenada_y,
            "pasajeros_esperando": [serializar_pasajero(p) for p in estacion.pasajeros_esperando]
        }
    return data

def guardar_datos(trenes, estaciones, rutas):
    data = {
        "trenes": serializar_trenes(trenes),
        "estaciones": serializar_estaciones(estaciones),
        "rutas": rutas
    }
    
    try:
        with open(DATA_FILE_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Datos guardados exitosamente en {DATA_FILE_PATH}")
        return True
    except FileNotFoundError:
        print(f"Error: La carpeta de guardado '{SAVE_DIR}' no existe")
        return False
    except IOError as e:
        print(f"Error al guardar los datos: {e}")
        return False

def cargar_datos():
    if not os.path.exists(DATA_FILE_PATH):
        print("Archivo de datos no encontrado. Cargando valores por defecto.")
        return {
            "trenes": {},
            "estaciones": {},
            "rutas": []
        }
    
    try:
        with open(DATA_FILE_PATH, 'r') as f:
            data = json.load(f)
            print(f"Datos cargados exitosamente desde {DATA_FILE_PATH}")
            return data
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error al cargar/decodificar los datos: {e}")
        return {
            "trenes": {},
            "estaciones": {},
            "rutas": []
        }
