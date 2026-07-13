# screens/pantalla_transicion.py

import pygame
import config

class PantallaTransicion:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_titulo = pygame.font.SysFont(None, 40)
        self.fuente_texto = pygame.font.SysFont(None, 35)
        self.fuente_btn = pygame.font.SysFont(None, 36)
        
        self.btn_continuar = pygame.Rect(config.ANCHO // 2 - 100, 450, 200, 50)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.btn_continuar.collidepoint(evento.pos):
                self.gestor.cambiar_a("grafo")

    def actualizar(self):
        self.mostrando_aviso = True

    def dibujar(self, pantalla):
        pantalla.fill(config.NEGRO)

        # Textos de alerta
        titulo = self.fuente_titulo.render("¡Varios candidatos similares!", True, config.NARANJA)
        linea1 = self.fuente_texto.render("El árbol no puede diferenciarlos completamente.", True, config.BLANCO)
        linea2 = self.fuente_texto.render("Activando búsqueda mediante grafo...", True, config.BLANCO)

        pantalla.blit(titulo, (config.ANCHO // 2 - titulo.get_width() // 2, 150))
        pantalla.blit(linea1, (config.ANCHO // 2 - linea1.get_width() // 2, 230))
        pantalla.blit(linea2, (config.ANCHO // 2 - linea2.get_width() // 2, 280))

        # Botón Continuar
        pygame.draw.rect(pantalla, config.BLANCO, self.btn_continuar)
        texto_btn = self.fuente_btn.render("CONTINUAR", True, config.NEGRO)
        pantalla.blit(texto_btn, (self.btn_continuar.x + 30, self.btn_continuar.y + 12))