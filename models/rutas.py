class rutaa:
    def __init__(self):
        self.rutas = [
            ("Estacion Central", "Rancagua", 80),
            ("Estacion Central", "Chillan", 230),
            ("Rancagua", "Estacion Central", 80),
            ("Rancagua", "Talca", 150),
            ("Talca", "Chillan", 100),
            ("Talca", "Rancagua", 150),
            ("Chillan", "Estacion Central", 230),
            ("Chillan", "Talca" , 100)
        ]

    def obtener_rutas(self):
        return self.rutas

