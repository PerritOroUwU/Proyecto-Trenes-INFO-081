"""
Sistema de guardado y carga de datos del simulador de trenes.
Maneja la serialización/deserialización de objetos a formato JSON.
"""

import json
import os
import datetime as dt
from typing import Dict, List, Any, Optional
from pathlib import Path


# Constantes de configuración
SAVE_DIR = "save_data"
DATA_FILENAME = "simulador_datos.json"
BACKUP_FILENAME = "simulador_datos_backup.json"
DATA_FILE_PATH = os.path.join(SAVE_DIR, DATA_FILENAME)
BACKUP_FILE_PATH = os.path.join(SAVE_DIR, BACKUP_FILENAME)


def _asegurar_directorio_guardado():
    """
    Crea el directorio de guardado si no existe.
    
    Returns:
        True si el directorio existe o fue creado, False si hubo error
    """
    try:
        Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error al crear directorio de guardado: {e}")
        return False


def serializar_trenes(trenes_objetos: Dict) -> Dict[str, Dict[str, Any]]:
    """
    Convierte un diccionario de objetos Tren a formato JSON-compatible.
    
    Args:
        trenes_objetos: Diccionario {nombre: objeto_Tren}
        
    Returns:
        Diccionario con datos serializados
    """
    data = {}
    for nombre, tren in trenes_objetos.items():
        try:
            data[nombre] = {
                "capacidad": tren.capacidad,
                "combustible": tren.combustible,
                "velocidad_max": tren.velocidad_max
            }
        except AttributeError as e:
            print(f"Advertencia: Error al serializar tren '{nombre}': {e}")
            continue
    
    return data


def serializar_pasajero(pasajero) -> Dict[str, Any]:
    """
    Convierte un objeto Pasajero a formato JSON-compatible.
    
    Args:
        pasajero: Objeto Pasajero
        
    Returns:
        Diccionario con datos del pasajero
    """
    try:
        data = {
            "id": pasajero.id,
            "origen": pasajero.origen,
            "destino": pasajero.destino,
            "tiempo_llegada": pasajero.tiempo_llegada.isoformat(),
            "tiempo_partida": (
                pasajero.tiempo_partida.isoformat() 
                if pasajero.tiempo_partida else None
            )
        }
        return data
    except Exception as e:
        print(f"Error al serializar pasajero ID {getattr(pasajero, 'id', '?')}: {e}")
        return None


def serializar_estaciones(estaciones_objetos: Dict) -> Dict[str, Dict[str, Any]]:
    """
    Convierte objetos Estacion a formato JSON-compatible.
    Incluye la serialización de pasajeros en espera.
    
    Args:
        estaciones_objetos: Diccionario {nombre: objeto_Estacion}
        
    Returns:
        Diccionario con datos serializados
    """
    data = {}
    for nombre, estacion in estaciones_objetos.items():
        try:
            # Serializar solo los pasajeros válidos
            pasajeros_serializados = []
            for p in estacion.pasajeros_esperando:
                p_data = serializar_pasajero(p)
                if p_data:
                    pasajeros_serializados.append(p_data)
            
            data[nombre] = {
                "coord_x": estacion.coordenada_x,
                "coord_y": estacion.coordenada_y,
                "pasajeros_esperando": pasajeros_serializados
            }
        except AttributeError as e:
            print(f"Advertencia: Error al serializar estación '{nombre}': {e}")
            continue
    
    return data


def serializar_rutas(rutas_objetos: List) -> List[tuple]:
    """
    Convierte una lista de objetos Ruta a formato JSON-compatible.
    
    Args:
        rutas_objetos: Lista de objetos Ruta
        
    Returns:
        Lista de tuplas (origen, destino, distancia)
    """
    rutas_serializadas = []
    
    for ruta in rutas_objetos:
        try:
            # Si es un objeto Ruta
            if hasattr(ruta, 'origen'):
                rutas_serializadas.append((
                    ruta.origen,
                    ruta.destino,
                    ruta.distancia_km
                ))
            # Si ya es una tupla (compatibilidad con formato antiguo)
            elif isinstance(ruta, (list, tuple)) and len(ruta) == 3:
                rutas_serializadas.append(tuple(ruta))
            else:
                print(f"Advertencia: Formato de ruta no reconocido: {ruta}")
        except Exception as e:
            print(f"Error al serializar ruta: {e}")
            continue
    
    return rutas_serializadas


def _crear_backup(archivo_origen: str, archivo_backup: str) -> bool:
    """
    Crea una copia de seguridad del archivo de datos.
    
    Args:
        archivo_origen: Ruta del archivo a respaldar
        archivo_backup: Ruta donde guardar el backup
        
    Returns:
        True si el backup fue exitoso
    """
    try:
        if os.path.exists(archivo_origen):
            import shutil
            shutil.copy2(archivo_origen, archivo_backup)
            return True
    except Exception as e:
        print(f"Advertencia: No se pudo crear backup: {e}")
    return False


def guardar_datos(
    trenes: Dict,
    estaciones: Dict,
    rutas: List,
    crear_backup: bool = True
) -> bool:
    """
    Guarda todos los datos del simulador en formato JSON.
    
    Args:
        trenes: Diccionario de objetos Tren
        estaciones: Diccionario de objetos Estacion
        rutas: Lista de objetos Ruta
        crear_backup: Si es True, crea un backup antes de guardar
        
    Returns:
        True si el guardado fue exitoso, False en caso contrario
    """
    # Asegurar que existe el directorio
    if not _asegurar_directorio_guardado():
        print(f"Error: No se pudo crear el directorio '{SAVE_DIR}'")
        return False
    
    # Crear backup si se solicita
    if crear_backup:
        _crear_backup(DATA_FILE_PATH, BACKUP_FILE_PATH)
    
    # Serializar los datos
    try:
        data = {
            "version": "1.0",
            "timestamp": dt.datetime.now().isoformat(),
            "trenes": serializar_trenes(trenes),
            "estaciones": serializar_estaciones(estaciones),
            "rutas": serializar_rutas(rutas)
        }
    except Exception as e:
        print(f"Error al serializar los datos: {e}")
        return False
    
    # Guardar en archivo
    try:
        with open(DATA_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"✓ Datos guardados exitosamente en '{DATA_FILE_PATH}'")
        print(f"  - Trenes: {len(trenes)}")
        print(f"  - Estaciones: {len(estaciones)}")
        print(f"  - Rutas: {len(rutas)}")
        return True
        
    except IOError as e:
        print(f"Error de E/S al guardar los datos: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado al guardar los datos: {e}")
        return False


def cargar_datos() -> Dict[str, Any]:
    """
    Carga los datos del simulador desde el archivo JSON.
    Si el archivo no existe o hay error, retorna datos vacíos.
    
    Returns:
        Diccionario con las claves 'trenes', 'estaciones', 'rutas'
    """
    datos_vacios = {
        "trenes": {},
        "estaciones": {},
        "rutas": []
    }
    
    # Verificar si existe el archivo
    if not os.path.exists(DATA_FILE_PATH):
        print(f"Archivo de datos no encontrado en '{DATA_FILE_PATH}'")
        print("Cargando valores por defecto...")
        return datos_vacios
    
    # Intentar cargar el archivo
    try:
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validar estructura básica
        if not isinstance(data, dict):
            print("Error: El archivo de datos no tiene el formato correcto")
            return datos_vacios
        
        # Extraer datos con valores por defecto
        resultado = {
            "trenes": data.get("trenes", {}),
            "estaciones": data.get("estaciones", {}),
            "rutas": data.get("rutas", [])
        }
        
        print(f"✓ Datos cargados exitosamente desde '{DATA_FILE_PATH}'")
        if "timestamp" in data:
            print(f"  - Última modificación: {data['timestamp']}")
        print(f"  - Trenes: {len(resultado['trenes'])}")
        print(f"  - Estaciones: {len(resultado['estaciones'])}")
        print(f"  - Rutas: {len(resultado['rutas'])}")
        
        return resultado
        
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        print("Intentando cargar desde backup...")
        return _cargar_desde_backup()
        
    except IOError as e:
        print(f"Error de E/S al cargar los datos: {e}")
        return datos_vacios
        
    except Exception as e:
        print(f"Error inesperado al cargar los datos: {e}")
        return datos_vacios


def _cargar_desde_backup() -> Dict[str, Any]:
    """
    Intenta cargar datos desde el archivo de backup.
    
    Returns:
        Diccionario con datos o datos vacíos si falla
    """
    datos_vacios = {
        "trenes": {},
        "estaciones": {},
        "rutas": []
    }
    
    if not os.path.exists(BACKUP_FILE_PATH):
        print("No se encontró archivo de backup")
        return datos_vacios
    
    try:
        with open(BACKUP_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✓ Datos cargados desde backup: '{BACKUP_FILE_PATH}'")
        
        return {
            "trenes": data.get("trenes", {}),
            "estaciones": data.get("estaciones", {}),
            "rutas": data.get("rutas", [])
        }
    except Exception as e:
        print(f"Error al cargar backup: {e}")
        return datos_vacios


def exportar_datos(
    trenes: Dict,
    estaciones: Dict,
    rutas: List,
    nombre_archivo: str
) -> bool:
    """
    Exporta los datos a un archivo específico (para exportación manual).
    
    Args:
        trenes: Diccionario de objetos Tren
        estaciones: Diccionario de objetos Estacion
        rutas: Lista de objetos Ruta
        nombre_archivo: Nombre del archivo (con o sin .json)
        
    Returns:
        True si la exportación fue exitosa
    """
    # Asegurar extensión .json
    if not nombre_archivo.endswith('.json'):
        nombre_archivo += '.json'
    
    ruta_exportacion = os.path.join(SAVE_DIR, nombre_archivo)
    
    try:
        if not _asegurar_directorio_guardado():
            return False
        
        data = {
            "version": "1.0",
            "timestamp": dt.datetime.now().isoformat(),
            "trenes": serializar_trenes(trenes),
            "estaciones": serializar_estaciones(estaciones),
            "rutas": serializar_rutas(rutas)
        }
        
        with open(ruta_exportacion, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"✓ Datos exportados a '{ruta_exportacion}'")
        return True
        
    except Exception as e:
        print(f"Error al exportar datos: {e}")
        return False


def listar_guardados_disponibles() -> List[str]:
    """
    Lista todos los archivos de guardado disponibles.
    
    Returns:
        Lista de nombres de archivos .json encontrados
    """
    if not os.path.exists(SAVE_DIR):
        return []
    
    try:
        archivos = [
            f for f in os.listdir(SAVE_DIR)
            if f.endswith('.json')
        ]
        return sorted(archivos)
    except Exception as e:
        print(f"Error al listar guardados: {e}")
        return []


def eliminar_guardado(nombre_archivo: str) -> bool:
    """
    Elimina un archivo de guardado específico.
    
    Args:
        nombre_archivo: Nombre del archivo a eliminar
        
    Returns:
        True si la eliminación fue exitosa
    """
    ruta_archivo = os.path.join(SAVE_DIR, nombre_archivo)
    
    try:
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
            print(f"✓ Archivo '{nombre_archivo}' eliminado")
            return True
        else:
            print(f"El archivo '{nombre_archivo}' no existe")
            return False
    except Exception as e:
        print(f"Error al eliminar archivo: {e}")
        return False


def obtener_info_guardado() -> Optional[Dict[str, Any]]:
    """
    Obtiene información sobre el guardado actual sin cargar todos los datos.
    
    Returns:
        Diccionario con metadatos o None si no existe
    """
    if not os.path.exists(DATA_FILE_PATH):
        return None
    
    try:
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return {
            "version": data.get("version", "desconocida"),
            "timestamp": data.get("timestamp", "desconocido"),
            "num_trenes": len(data.get("trenes", {})),
            "num_estaciones": len(data.get("estaciones", {})),
            "num_rutas": len(data.get("rutas", [])),
            "tamaño_archivo": os.path.getsize(DATA_FILE_PATH)
        }
    except Exception as e:
        print(f"Error al obtener info del guardado: {e}")
        return None