class Cliente:
    def __init__(self, id, fecha):
        self.id = id
        self.fecha = fecha

    def __repr__(self):
        return f"Cliente {self.id} ({self.fecha.strftime('%H:%M')})"

def constructor_cliente(id, fecha):
    return Cliente(id, fecha)
