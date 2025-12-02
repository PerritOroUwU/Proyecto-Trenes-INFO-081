import json
import os

DATA_FILE = "simulador_datos.json"

def guardar_datos(trenes, estaciones, rutas):
    data = {
        "trenes": trenes,
        "estaciones": estaciones,
        "rutas": rutas
    }
    
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Datos guardados exitosamente en {DATA_FILE}")
        return True
    except IOError as e:
        print(f"Error al guardar los datos: {e}")
        return False

def cargar_datos():
    if not os.path.exists(DATA_FILE):
        print("Archivo de datos no encontrado. Cargando valores por defecto.")
        return {
            "trenes": {},
            "estaciones": {},
            "rutas": []
        }
    
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            print(f"Datos cargados exitosamente desde {DATA_FILE}")
            return data
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error al cargar/decodificar los datos: {e}")
        return {
            "trenes": {},
            "estaciones": {},
            "rutas": []
        }