# screens/gestor_pantallas.py

class GestorPantallas:
    def __init__(self):
        self.pantallas = {}
        self.pantalla_activa = None

    def registrar_pantalla(self, nombre, pantalla):
        """Guarda la instancia de la pantalla en el diccionario."""
        self.pantallas[nombre] = pantalla

    def cambiar_a(self, nombre):
        """Cambia el estado actual a la pantalla solicitada."""
        if nombre in self.pantallas:
            self.pantalla_activa = self.pantallas[nombre]

    def obtener_activa(self):
        """Devuelve la pantalla que se está mostrando actualmente."""
        return self.pantalla_activa