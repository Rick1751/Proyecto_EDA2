# screens/pantalla_acerca_de.py

import pygame

from ui.estilo import COLOR_ACENTO, COLOR_BORDE, COLOR_PANEL, COLOR_SUBTEXTO, COLOR_TEXTO, dibujar_boton, dibujar_fondo_tecnologico, dibujar_panel, centrar_texto


class PantallaAcercaDe:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_titulo = pygame.font.SysFont("Segoe UI", 52, bold=True)
        self.fuente_texto = pygame.font.SysFont("Segoe UI", 28)
        self.fuente_btn = pygame.font.SysFont("Segoe UI", 26, bold=True)

        self.btn_volver = pygame.Rect(50, 500, 150, 45)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.btn_volver.collidepoint(evento.pos):
                self.gestor.cambiar_a("inicio")

    def actualizar(self):
        self.estatica = True

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        centrar_texto(pantalla, self.fuente_titulo, "ACERCA DEL PROYECTO", 48, COLOR_TEXTO)

        panel = pygame.Rect(60, 140, 680, 280)
        dibujar_panel(pantalla, panel, relleno=COLOR_PANEL, borde=COLOR_BORDE, radio=16)

        pantalla.blit(self.fuente_texto.render("Proyecto final de:", True, COLOR_SUBTEXTO), (95, 175))
        pantalla.blit(self.fuente_texto.render("Estructuras de datos y algoritmos", True, COLOR_ACENTO), (95, 212))
        pantalla.blit(self.fuente_texto.render("Estructuras utilizadas:", True, COLOR_SUBTEXTO), (95, 275))
        pantalla.blit(self.fuente_texto.render("- Árbol de decisión", True, COLOR_TEXTO), (120, 318))
        pantalla.blit(self.fuente_texto.render("- Grafo no dirigido", True, COLOR_TEXTO), (120, 356))

        dibujar_boton(pantalla, self.btn_volver, self.fuente_btn, "VOLVER", fondo=COLOR_PANEL, borde=COLOR_BORDE)