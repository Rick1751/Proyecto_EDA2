"""
boton.py

Clase chiquita para representar un boton clicable en Pygame. Se usa en
varias pantallas (inicio, preguntas, grafo, resultado) para no repetir una
y otra vez el mismo codigo de "dibujar un rectangulo + detectar el clic".
"""

import pygame
import config


class Boton:
    def __init__(self, rect, texto, color, color_hover, color_texto=config.BLANCO):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.fuente = pygame.font.SysFont(config.NOMBRE_FUENTE, config.TAMANO_BOTON, bold=True)

    def dibujar(self, pantalla):
        # Si el mouse esta encima del boton, lo pintamos con el color
        # "hover" para dar una pequena señal visual al jugador
        mouse_pos = pygame.mouse.get_pos()
        esta_encima = self.rect.collidepoint(mouse_pos)
        color_actual = self.color_hover if esta_encima else self.color

        pygame.draw.rect(pantalla, color_actual, self.rect, border_radius=12)
        pygame.draw.rect(pantalla, config.NEGRO, self.rect, width=2, border_radius=12)

        superficie_texto = self.fuente.render(self.texto, True, self.color_texto)
        rect_texto = superficie_texto.get_rect(center=self.rect.center)
        pantalla.blit(superficie_texto, rect_texto)

    def fue_clickeado(self, evento):
        """Devuelve True si el evento recibido es un clic izquierdo hecho
        dentro del area del boton."""
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(evento.pos)
        return False
