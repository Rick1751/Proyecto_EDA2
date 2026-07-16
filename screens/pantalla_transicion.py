# screens/pantalla_transicion.py

import pygame
import config
from ui.estilo import COLOR_ACENTO, COLOR_BORDE, COLOR_SUBTEXTO, COLOR_TEXTO, dibujar_boton, dibujar_fondo_tecnologico, dibujar_panel, centrar_texto

class PantallaTransicion:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_titulo = pygame.font.SysFont("Segoe UI", 46, bold=True)
        self.fuente_texto = pygame.font.SysFont("Segoe UI", 28)
        self.fuente_btn = pygame.font.SysFont("Segoe UI", 26, bold=True)
        
        self.btn_continuar = pygame.Rect(config.ANCHO // 2 - 120, 455, 240, 56)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.btn_continuar.collidepoint(evento.pos):
                self.gestor.cambiar_a("grafo")

    def actualizar(self):
        self.mostrando_aviso = True

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        centrar_texto(pantalla, self.fuente_titulo, "Varios candidatos similares", 74, COLOR_TEXTO)

        panel = pygame.Rect(70, 170, 660, 200)
        dibujar_panel(pantalla, panel, relleno=(12, 42, 68), borde=COLOR_BORDE, radio=16)

        # Textos de alerta
        linea1 = self.fuente_texto.render("El árbol no puede diferenciarlos completamente.", True, COLOR_SUBTEXTO)
        linea2 = self.fuente_texto.render("Activando búsqueda mediante grafo...", True, COLOR_ACENTO)

        pantalla.blit(linea1, (config.ANCHO // 2 - linea1.get_width() // 2, 235))
        pantalla.blit(linea2, (config.ANCHO // 2 - linea2.get_width() // 2, 285))

        # Botón Continuar
        dibujar_boton(pantalla, self.btn_continuar, self.fuente_btn, "CONTINUAR", fondo=(12, 42, 68), borde=COLOR_BORDE)