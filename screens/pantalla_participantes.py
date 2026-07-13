# screens/pantalla_participantes.py

import pygame
import config

class PantallaParticipantes:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_titulo = pygame.font.SysFont(None, 50)
        self.fuente_nombres = pygame.font.SysFont(None, 30)
        self.fuente_btn = pygame.font.SysFont(None, 36)
        
        # Lista de personajes de tu dataset
        self.nombres = ["Andrea", "Jesus", "Ricardo", "Emily", "Alexis", "Valeria", "Esteban", "Orlin", "Tabatha"]
        self.btn_volver = pygame.Rect(50, 500, 150, 45)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.btn_volver.collidepoint(evento.pos):
                self.gestor.cambiar_a("inicio")

    def actualizar(self):
        # Pantalla estática sin animación constante
        self.lista_lista = True

    def dibujar(self, pantalla):
        pantalla.fill(config.NEGRO)

        # Título
        texto_titulo = self.fuente_titulo.render("Participantes del Sapometro", True, config.NARANJA)
        pantalla.blit(texto_titulo, (config.ANCHO // 2 - texto_titulo.get_width() // 2, 40))

        # Dibujar Grilla 3x3
        inicio_x = 120
        inicio_y = 130
        ancho_caja = 150
        alto_caja = 60
        espacio_x = 200
        espacio_y = 100

        for i, nombre in enumerate(self.nombres):
            fila = i // 3
            col = i % 3
            x = inicio_x + col * espacio_x
            y = inicio_y + fila * espacio_y
            
            caja = pygame.Rect(x, y, ancho_caja, alto_caja)
            # Dibujar borde naranja
            pygame.draw.rect(pantalla, config.NARANJA, caja, 3) 
            
            # Texto del nombre centrado en la caja
            texto = self.fuente_nombres.render(nombre, True, config.BLANCO)
            pantalla.blit(texto, (x + (ancho_caja - texto.get_width()) // 2, y + 20))

        # Botón Volver
        pygame.draw.rect(pantalla, config.BLANCO, self.btn_volver)
        texto_volver = self.fuente_btn.render("VOLVER", True, config.NEGRO)
        pantalla.blit(texto_volver, (self.btn_volver.x + 25, self.btn_volver.y + 12))