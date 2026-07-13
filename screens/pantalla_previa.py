# screens/pantalla_previa.py

import pygame
import config

class PantallaPrevia:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_texto = pygame.font.SysFont(None, 40)
        self.fuente_btn = pygame.font.SysFont(None, 36)
        
        # Botón centrado
        self.btn_comenzar = pygame.Rect(config.ANCHO // 2 - 150, 400, 300, 50)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.btn_comenzar.collidepoint(evento.pos):
                self.gestor.cambiar_a("preguntas")

    def actualizar(self):
        self.esperando_jugador = True

    def dibujar(self, pantalla):
        pantalla.fill(config.NEGRO)

        # Instrucciones
        linea1 = self.fuente_texto.render("Piensa en uno de los participantes.", True, config.BLANCO)
        linea2 = self.fuente_texto.render("No cambies de persona durante el juego.", True, config.NARANJA)

        pantalla.blit(linea1, (config.ANCHO // 2 - linea1.get_width() // 2, 200))
        pantalla.blit(linea2, (config.ANCHO // 2 - linea2.get_width() // 2, 250))

        # Botón Comenzar
        pygame.draw.rect(pantalla, config.BLANCO, self.btn_comenzar)
        texto_btn = self.fuente_btn.render("COMENZAR PARTIDA", True, config.NEGRO)
        pantalla.blit(texto_btn, (self.btn_comenzar.x + 15, self.btn_comenzar.y + 12))