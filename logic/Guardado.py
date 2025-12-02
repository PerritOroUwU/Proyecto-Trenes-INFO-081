import json
import os

SAVE_DIR = "save_data"
DATA_FILENAME = "simulador_datos.json"
DATA_FILE_PATH = os.path.join(SAVE_DIR, DATA_FILENAME)

def guardar_datos(trenes, estaciones, rutas):
    data = {
        "trenes": trenes,
        "estaciones": estaciones,
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
