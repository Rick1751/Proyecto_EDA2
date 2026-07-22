# screens/gestor_pantallas.py

import pygame

class GestorPantallas:
    def __init__(self):
        self.pantallas = {}
        self.pantalla_activa = None
        self.nombre_pantalla_activa = None

        # Datos de la transición
        self.transicionando = False
        self.estado_transicion = None
        self.pantalla_destino = None

        # Transparencia del fondo negro
        self.alpha_transicion = 0

        # Velocidad del efecto.
        self.velocidad_transicion = 700

    def registrar_pantalla(self, nombre, pantalla):
        """
        Guarda una pantalla en el diccionario.
        """
        self.pantallas[nombre] = pantalla

    def cambiar_a(self, nombre, inmediato=False):
        """
        Solicita el cambio hacia otra pantalla.
        """

        if nombre not in self.pantallas:
            print(
                f"Advertencia: la pantalla "
                f"'{nombre}' no está registrada."
            )
            return

        # Evitar iniciar otra transición mientras
        # ya se está ejecutando una.
        if self.transicionando:
            return

        # Primera pantalla del programa
        if self.pantalla_activa is None or inmediato:
            self.pantalla_activa = self.pantallas[nombre]
            self.nombre_pantalla_activa = nombre
            self.alpha_transicion = 0
            return

        # Evitar cambiar a la misma pantalla
        if nombre == self.nombre_pantalla_activa:
            return

        # Guardar el destino e iniciar oscurecimiento
        self.pantalla_destino = nombre
        self.transicionando = True
        self.estado_transicion = "oscureciendo"
        self.alpha_transicion = 0

    def obtener_activa(self):
        return self.pantalla_activa

    def esta_transicionando(self):

        return self.transicionando

    def actualizar_transicion(self, delta_tiempo):

        if not self.transicionando:
            return

        cambio_alpha = (
            self.velocidad_transicion
            * delta_tiempo
        )

        # oscurecer la pantalla actual
        if self.estado_transicion == "oscureciendo":
            self.alpha_transicion += cambio_alpha

            if self.alpha_transicion >= 255:
                self.alpha_transicion = 255

                # Cambiar realmente de pantalla
                self.pantalla_activa = self.pantallas[
                    self.pantalla_destino
                ]

                self.nombre_pantalla_activa = (
                    self.pantalla_destino
                )

                # mostrar gradualmente
                self.estado_transicion = "aclarando"

        # retirar la capa negra
        elif self.estado_transicion == "aclarando":
            self.alpha_transicion -= cambio_alpha

            if self.alpha_transicion <= 0:
                self.alpha_transicion = 0
                self.transicionando = False
                self.estado_transicion = None
                self.pantalla_destino = None

    def dibujar_transicion(self, pantalla):
        if not self.transicionando:
            return

        capa_negra = pygame.Surface(
            pantalla.get_size(),
            pygame.SRCALPHA
        )

        capa_negra.fill(
            (
                0,
                0,
                0,
                int(self.alpha_transicion)
            )
        )

        pantalla.blit(
            capa_negra,
            (0, 0)
        )