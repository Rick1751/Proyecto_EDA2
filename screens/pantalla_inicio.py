# screens/pantalla_inicio.py

import pygame
import sys
import config

class PantallaInicio:
    def __init__(self, gestor):
        self.gestor = gestor
        # Usamos fuentes por defecto de Pygame para no depender de archivos externos por ahora
        self.fuente_titulo = pygame.font.SysFont(None, 72)
        self.fuente_botones = pygame.font.SysFont(None, 36)

        # Definir los rectángulos de los botones (x, y, ancho, alto)
        self.btn_jugar = pygame.Rect(250, 200, 300, 50)
        self.btn_participantes = pygame.Rect(250, 280, 300, 50)
        self.btn_acerca_de = pygame.Rect(250, 360, 300, 50)
        self.btn_salir = pygame.Rect(250, 440, 300, 50)

    def manejar_evento(self, evento):
        # Detectar si el usuario hace clic izquierdo (botón 1)
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos_mouse = evento.pos
            
            # Validar con qué botón colisionó el puntero
            if self.btn_jugar.collidepoint(pos_mouse):
                self.gestor.cambiar_a("previa")
            elif self.btn_participantes.collidepoint(pos_mouse):
                self.gestor.cambiar_a("participantes")
            elif self.btn_acerca_de.collidepoint(pos_mouse):
                self.gestor.cambiar_a("acerca_de")
            elif self.btn_salir.collidepoint(pos_mouse):
                pygame.quit()
                sys.exit()

    def actualizar(self):
        # Esta pantalla es estática, no hay lógica que actualizar por frame
        pass 

    def dibujar(self, pantalla):
        pantalla.fill(config.NEGRO)

        # Renderizar y centrar título
        texto_titulo = self.fuente_titulo.render("Sapometro", True, config.NARANJA)
        pantalla.blit(texto_titulo, (config.ANCHO // 2 - texto_titulo.get_width() // 2, 80))

        # Dibujar Botón: JUGAR
        pygame.draw.rect(pantalla, config.BLANCO, self.btn_jugar)
        texto_jugar = self.fuente_botones.render("JUGAR", True, config.NEGRO)
        pantalla.blit(texto_jugar, (self.btn_jugar.x + 110, self.btn_jugar.y + 12))

        # Dibujar Botón: CONOCER PARTICIPANTES
        pygame.draw.rect(pantalla, config.BLANCO, self.btn_participantes)
        texto_part = self.fuente_botones.render("CONOCER PARTICIPANTES", True, config.NEGRO)
        pantalla.blit(texto_part, (self.btn_participantes.x + 10, self.btn_participantes.y + 12))

        # Dibujar Botón: ACERCA DEL PROYECTO
        pygame.draw.rect(pantalla, config.BLANCO, self.btn_acerca_de)
        texto_acerca = self.fuente_botones.render("ACERCA DEL PROYECTO", True, config.NEGRO)
        pantalla.blit(texto_acerca, (self.btn_acerca_de.x + 15, self.btn_acerca_de.y + 12))

        # Dibujar Botón: SALIR
        pygame.draw.rect(pantalla, config.BLANCO, self.btn_salir)
        texto_salir = self.fuente_botones.render("SALIR", True, config.NEGRO)
        pantalla.blit(texto_salir, (self.btn_salir.x + 115, self.btn_salir.y + 12))