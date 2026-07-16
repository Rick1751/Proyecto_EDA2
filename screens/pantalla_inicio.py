# screens/pantalla_inicio.py

import pygame
import sys
import math
import config

class PantallaInicio:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_titulo = pygame.font.SysFont("Segoe UI", 76, bold=True)
        self.fuente_subtitulo = pygame.font.SysFont("Segoe UI", 24, bold=False)
        self.fuente_botones = pygame.font.SysFont("Segoe UI", 34, bold=True)
        self.fuente_botones_chicos = pygame.font.SysFont("Segoe UI", 20, bold=False)

        self.btn_jugar = pygame.Rect(210, 250, 380, 56)
        self.btn_participantes = pygame.Rect(210, 325, 380, 56)
        self.btn_acerca_de = pygame.Rect(210, 400, 380, 56)
        self.btn_salir = pygame.Rect(210, 475, 380, 56)

        self.color_fondo = (6, 18, 34)
        self.color_panel = (10, 34, 58)
        self.color_borde = (89, 180, 214)
        self.color_borde_suave = (40, 102, 134)
        self.color_acento = (255, 171, 90)
        self.color_texto = (229, 244, 255)
        self.color_subtexto = (143, 191, 217)

        self.estrellas = []
        self._crear_estrellas()

    def _crear_estrellas(self):
        self.estrellas = [
            [90, 70, 1, 1], [170, 110, 2, 2], [270, 80, 1, 1], [640, 90, 2, 2],
            [710, 180, 1, 1], [610, 240, 2, 1], [90, 240, 1, 1], [160, 370, 2, 2],
            [690, 380, 1, 1], [580, 500, 2, 1], [720, 530, 1, 1], [120, 520, 1, 1],
        ]

    def _dibujar_fondo(self, pantalla):
        alto = config.ALTO
        ancho = config.ANCHO
        for y in range(alto):
            progreso = y / max(1, alto - 1)
            r = int(5 + 8 * progreso)
            g = int(18 + 24 * progreso)
            b = int(34 + 40 * progreso)
            pygame.draw.line(pantalla, (r, g, b), (0, y), (ancho, y))

        # Marco y retícula de estilo HUD
        pygame.draw.rect(pantalla, self.color_borde_suave, pygame.Rect(12, 12, ancho - 24, alto - 24), 1)
        for x in range(80, ancho, 80):
            pygame.draw.line(pantalla, (18, 53, 77), (x, 30), (x, alto - 30), 1)
        for y in range(70, alto, 70):
            pygame.draw.line(pantalla, (18, 53, 77), (30, y), (ancho - 30, y), 1)

        # Luces y puntos de interfaz
        for x, y, radio, brillo in self.estrellas:
            pygame.draw.circle(pantalla, (97, 208, 255), (x, y), radio)
            pygame.draw.circle(pantalla, (97, 208, 255), (x, y), radio + brillo, 1)

    def _dibujar_globo(self, pantalla):
        centro = (config.ANCHO // 2, 155)
        radio = 128
        pygame.draw.circle(pantalla, (18, 71, 110), centro, radio)
        pygame.draw.circle(pantalla, (69, 183, 255), centro, radio, 2)
        pygame.draw.circle(pantalla, (108, 218, 255), centro, radio - 10, 1)

        for escala in (0.25, 0.5, 0.75):
            ancho_oval = int(radio * 2 * (1 - escala * 0.15))
            alto_oval = int(radio * 2 * escala)
            rect = pygame.Rect(0, 0, ancho_oval, alto_oval)
            rect.center = centro
            pygame.draw.ellipse(pantalla, (49, 142, 202), rect, 1)

        for angulo in (0, 30, 60, 120, 150):
            rad = math.radians(angulo)
            x1 = centro[0] + int(math.cos(rad) * radio)
            y1 = centro[1] + int(math.sin(rad) * radio)
            x2 = centro[0] - int(math.cos(rad) * radio)
            y2 = centro[1] - int(math.sin(rad) * radio)
            pygame.draw.line(pantalla, (49, 142, 202), (x1, y1), (x2, y2), 1)

        puntos = [
            (centro[0] - 68, centro[1] - 18), (centro[0] - 30, centro[1] + 25),
            (centro[0] + 6, centro[1] - 20), (centro[0] + 40, centro[1] + 8),
            (centro[0] + 72, centro[1] - 15), (centro[0] - 20, centro[1] - 55),
            (centro[0] + 30, centro[1] - 48), (centro[0] - 58, centro[1] + 42),
        ]
        for punto in puntos:
            pygame.draw.circle(pantalla, (255, 113, 95), punto, 4)
            pygame.draw.circle(pantalla, (255, 113, 95), punto, 10, 1)

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

    def _dibujar_boton(self, pantalla, rect, texto_principal, texto_secundario=None, activo=False):
        base = self.color_panel if not activo else (18, 52, 78)
        borde = self.color_borde if activo else self.color_borde_suave
        sombra = pygame.Rect(rect.x + 4, rect.y + 5, rect.w, rect.h)
        pygame.draw.rect(pantalla, (0, 0, 0), sombra, border_radius=14)
        pygame.draw.rect(pantalla, base, rect, border_radius=14)
        pygame.draw.rect(pantalla, borde, rect, 3, border_radius=14)

        tri_izq = [(rect.x + 10, rect.centery), (rect.x + 26, rect.y + 12), (rect.x + 26, rect.bottom - 12)]
        tri_der = [(rect.right - 10, rect.centery), (rect.right - 26, rect.y + 12), (rect.right - 26, rect.bottom - 12)]
        pygame.draw.polygon(pantalla, borde, tri_izq, 2)
        pygame.draw.polygon(pantalla, borde, tri_der, 2)

        texto = self.fuente_botones.render(texto_principal, True, self.color_texto)
        pantalla.blit(texto, (rect.centerx - texto.get_width() // 2, rect.y + 8))
        if texto_secundario:
            sub = self.fuente_botones_chicos.render(texto_secundario, True, self.color_subtexto)
            pantalla.blit(sub, (rect.centerx - sub.get_width() // 2, rect.y + 34))

    def dibujar(self, pantalla):
        self._dibujar_fondo(pantalla)
        self._dibujar_globo(pantalla)

        texto_titulo = self.fuente_titulo.render("Sapometro", True, (103, 231, 255))
        sombra_titulo = self.fuente_titulo.render("Sapometro", True, (15, 47, 73))
        pantalla.blit(sombra_titulo, (config.ANCHO // 2 - sombra_titulo.get_width() // 2 + 3, 42 + 3))
        pantalla.blit(texto_titulo, (config.ANCHO // 2 - texto_titulo.get_width() // 2, 42))

        subtitulo = self.fuente_subtitulo.render("PROYECTO EXPEDIENTE SECRETO: CLASIFICADO", True, self.color_texto)
        pantalla.blit(subtitulo, (config.ANCHO // 2 - subtitulo.get_width() // 2, 116))

        texto_ayuda = self.fuente_subtitulo.render("Selecciona una opción para entrar al panel de análisis.", True, self.color_subtexto)
        pantalla.blit(texto_ayuda, (config.ANCHO // 2 - texto_ayuda.get_width() // 2, 145))

        self._dibujar_boton(pantalla, self.btn_jugar, "JUGAR", activo=True)
        self._dibujar_boton(pantalla, self.btn_participantes, "CONOCER PARTICIPANTES", "PERFILES DE PARTICIPANTES")
        self._dibujar_boton(pantalla, self.btn_acerca_de, "ACERCA DEL PROYECTO")
        self._dibujar_boton(pantalla, self.btn_salir, "SALIR")