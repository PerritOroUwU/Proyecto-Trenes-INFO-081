class Tren:
    def __init__(self, nombre: str, capacidad: int):
        self.nombre = nombre
        self.capacidad = capacidad
        self.pasajeros = []

    def embarcar(self, clientes: list):
        espacio = self.capacidad - len(self.pasajeros)
        suben = clientes[:espacio]
        self.pasajeros.extend(suben)
        return clientes[espacio:]

    def __repr__(self):
        return f"{self.nombre} ({len(self.pasajeros)}/{self.capacidad} pasajeros)"
