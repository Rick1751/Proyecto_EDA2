# screens/pantalla_acerca_de.py

import pygame
import config

class PantallaAcercaDe:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_titulo = pygame.font.SysFont(None, 50)
        self.fuente_texto = pygame.font.SysFont(None, 35)
        self.fuente_btn = pygame.font.SysFont(None, 36)
        
        self.btn_volver = pygame.Rect(50, 500, 150, 45)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.btn_volver.collidepoint(evento.pos):
                self.gestor.cambiar_a("inicio")

    def actualizar(self):
        self.estatica = True

    def dibujar(self, pantalla):
        pantalla.fill(config.NEGRO)

        # Título
        titulo = self.fuente_titulo.render("ACERCA DEL PROYECTO", True, config.NARANJA)
        pantalla.blit(titulo, (config.ANCHO // 2 - titulo.get_width() // 2, 80))

        # Textos informativos
        linea1 = self.fuente_texto.render("Proyecto final de:", True, config.BLANCO)
        linea2 = self.fuente_texto.render("Estructuras de datos y algoritmos", True, config.NARANJA)
        linea3 = self.fuente_texto.render("Estructuras utilizadas:", True, config.BLANCO)
        linea4 = self.fuente_texto.render("- Árbol de decisión", True, config.NARANJA)
        linea5 = self.fuente_texto.render("- Grafo no dirigido", True, config.NARANJA)

        pantalla.blit(linea1, (100, 180))
        pantalla.blit(linea2, (100, 220))
        pantalla.blit(linea3, (100, 290))
        pantalla.blit(linea4, (100, 330))
        pantalla.blit(linea5, (100, 370))

        # Botón Volver
        pygame.draw.rect(pantalla, config.BLANCO, self.btn_volver)
        texto_volver = self.fuente_btn.render("VOLVER", True, config.NEGRO)
        pantalla.blit(texto_volver, (self.btn_volver.x + 25, self.btn_volver.y + 12))