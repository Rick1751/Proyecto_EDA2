# screens/pantalla_inicio.py

import math
import sys
import pygame
import config


class PantallaInicio:
    def __init__(self, gestor):
        self.gestor = gestor

        self.volumen = 0.35
        self.mostrando_control_volumen = False
        self.arrastrando_volumen = False

        # Fuentes
        self.fuente_titulo = pygame.font.SysFont(
            "Segoe UI",
            64,
            bold=True
        )

        self.fuente_subtitulo = pygame.font.SysFont(
            "Segoe UI",
            21
        )

        self.fuente_ayuda = pygame.font.SysFont(
            "Segoe UI",
            18
        )

        self.fuente_botones = pygame.font.SysFont(
            "Segoe UI",
            30,
            bold=True
        )

        self.fuente_botones_chicos = pygame.font.SysFont(
            "Segoe UI",
            15
        )

        # Colores
        self.color_fondo = (6, 18, 34)
        self.color_panel = (10, 34, 58)
        self.color_panel_hover = (18, 52, 78)

        self.color_borde = (89, 180, 214)
        self.color_borde_suave = (40, 102, 134)

        self.color_acento = (255, 171, 90)
        self.color_texto = (229, 244, 255)
        self.color_subtexto = (143, 191, 217)

        # Tamaño y posición común de botones
        ancho_boton = 500
        alto_boton = 62
        centro_x = config.ANCHO // 2

        x_boton = centro_x - ancho_boton // 2

        self.btn_jugar = pygame.Rect(
            x_boton,
            250,
            ancho_boton,
            alto_boton
        )

        self.btn_participantes = pygame.Rect(
            x_boton,
            326,
            ancho_boton,
            alto_boton
        )

        self.btn_acerca_de = pygame.Rect(
            x_boton,
            402,
            ancho_boton,
            alto_boton
        )

        self.btn_salir = pygame.Rect(
            x_boton,
            478,
            ancho_boton,
            alto_boton
        )

        self.btn_volumen = pygame.Rect(
            config.ANCHO - 126,
            22,
            104,
            34
        )

        self.panel_volumen = pygame.Rect(
            config.ANCHO - 220,
            68,
            180,
            96
        )

        self.btn_volumen_menos = pygame.Rect(
            self.panel_volumen.x + 14,
            self.panel_volumen.y + 44,
            28,
            28
        )

        self.btn_volumen_mas = pygame.Rect(
            self.panel_volumen.right - 42,
            self.panel_volumen.y + 44,
            28,
            28
        )

        self.barra_volumen = pygame.Rect(
            self.panel_volumen.x + 48,
            self.panel_volumen.y + 54,
            84,
            8
        )

        self._actualizar_volumen(self.volumen)

        self.estrellas = []
        self._crear_estrellas()
        # Animación del radar
        self.angulo_radar = 0
        self.velocidad_radar = 1.8

        # Puntos detectados dentro del radar
        self.puntos_radar = [
            (-48, -10),
            (-23, 18),
            (5, -15),
            (33, 10),
            (52, -10),
            (-15, -38),
            (24, -34),
            (-40, 30),
        ]

    def _crear_estrellas(self):
        self.estrellas = [
            [90, 70, 1, 1],
            [170, 110, 2, 2],
            [270, 80, 1, 1],
            [640, 90, 2, 2],
            [710, 180, 1, 1],
            [610, 240, 2, 1],
            [90, 240, 1, 1],
            [160, 370, 2, 2],
            [690, 380, 1, 1],
            [580, 500, 2, 1],
            [720, 530, 1, 1],
            [120, 520, 1, 1],
        ]

    def _actualizar_volumen(self, valor):
        self.volumen = max(0.0, min(1.0, valor))
        try:
            pygame.mixer.music.set_volume(self.volumen)
        except pygame.error:
            pass

    def _volumen_desde_pos(self, x):
        progreso = (x - self.barra_volumen.x) / max(1, self.barra_volumen.w)
        return max(0.0, min(1.0, progreso))

    def _manejar_control_volumen(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.btn_volumen.collidepoint(evento.pos):
                self.mostrando_control_volumen = not self.mostrando_control_volumen
                return True

            if not self.mostrando_control_volumen:
                return False

            if self.btn_volumen_menos.collidepoint(evento.pos):
                self._actualizar_volumen(self.volumen - 0.1)
                return True

            if self.btn_volumen_mas.collidepoint(evento.pos):
                self._actualizar_volumen(self.volumen + 0.1)
                return True

            if self.barra_volumen.collidepoint(evento.pos):
                self.arrastrando_volumen = True
                self._actualizar_volumen(self._volumen_desde_pos(evento.pos[0]))
                return True

        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            self.arrastrando_volumen = False
        elif evento.type == pygame.MOUSEMOTION and self.arrastrando_volumen:
            self._actualizar_volumen(self._volumen_desde_pos(evento.pos[0]))
            return True

        return False

    def _dibujar_fondo(self, pantalla):
        alto = config.ALTO
        ancho = config.ANCHO

        # Degradado vertical
        for y in range(alto):
            progreso = y / max(1, alto - 1)

            r = int(5 + 8 * progreso)
            g = int(18 + 24 * progreso)
            b = int(34 + 40 * progreso)

            pygame.draw.line(
                pantalla,
                (r, g, b),
                (0, y),
                (ancho, y)
            )

        # Marco exterior
        pygame.draw.rect(
            pantalla,
            self.color_borde_suave,
            pygame.Rect(
                12,
                12,
                ancho - 24,
                alto - 24
            ),
            1
        )

        # Retícula HUD
        for x in range(80, ancho, 80):
            pygame.draw.line(
                pantalla,
                (18, 53, 77),
                (x, 30),
                (x, alto - 30),
                1
            )

        for y in range(70, alto, 70):
            pygame.draw.line(
                pantalla,
                (18, 53, 77),
                (30, y),
                (ancho - 30, y),
                1
            )

        # Estrellas
        for x, y, radio, brillo in self.estrellas:
            pygame.draw.circle(
                pantalla,
                (97, 208, 255),
                (x, y),
                radio
            )

            pygame.draw.circle(
                pantalla,
                (97, 208, 255),
                (x, y),
                radio + brillo,
                1
            )

    def _dibujar_globo(self, pantalla):
        centro = (
            config.ANCHO // 2,
            205
        )

        radio = 92

        superficie_globo = pygame.Surface(
            (radio * 2 + 10, radio * 2 + 10),
            pygame.SRCALPHA
        )

        centro_local = (
            superficie_globo.get_width() // 2,
            superficie_globo.get_height() // 2
        )

        pygame.draw.circle(
            superficie_globo,
            (18, 71, 110, 110),
            centro_local,
            radio
        )

        pygame.draw.circle(
            superficie_globo,
            (69, 183, 255, 180),
            centro_local,
            radio,
            2
        )

        pygame.draw.circle(
            superficie_globo,
            (108, 218, 255, 150),
            centro_local,
            radio - 10,
            1
        )

        for escala in (0.25, 0.5, 0.75):
            ancho_oval = int(
                radio * 2 * (1 - escala * 0.15)
            )

            alto_oval = int(
                radio * 2 * escala
            )

            rect = pygame.Rect(
                0,
                0,
                ancho_oval,
                alto_oval
            )

            rect.center = centro_local

            pygame.draw.ellipse(
                superficie_globo,
                (49, 142, 202, 170),
                rect,
                1
            )

        for angulo in (
            0,
            30,
            60,
            120,
            150
        ):
            rad = math.radians(angulo)

            x1 = centro_local[0] + int(
                math.cos(rad) * radio
            )

            y1 = centro_local[1] + int(
                math.sin(rad) * radio
            )

            x2 = centro_local[0] - int(
                math.cos(rad) * radio
            )

            y2 = centro_local[1] - int(
                math.sin(rad) * radio
            )

            pygame.draw.line(
                superficie_globo,
                (49, 142, 202, 160),
                (x1, y1),
                (x2, y2),
                1
            )

        puntos = [
            (-48, -10),
            (-23, 18),
            (5, -15),
            (33, 10),
            (52, -10),
            (-15, -38),
            (24, -34),
            (-40, 30),
        ]

        for dx, dy in puntos:
            punto = (
                centro_local[0] + dx,
                centro_local[1] + dy
            )

            pygame.draw.circle(
                superficie_globo,
                (255, 113, 95),
                punto,
                4
            )

            pygame.draw.circle(
                superficie_globo,
                (255, 113, 95),
                punto,
                9,
                1
            )
        # Línea principal del radar
        angulo_rad = math.radians(
            self.angulo_radar
        )

        x_final = centro_local[0] + int(
            math.cos(angulo_rad) * radio
        )

        y_final = centro_local[1] + int(
            math.sin(angulo_rad) * radio
        )

        pygame.draw.line(
            superficie_globo,
            (103, 231, 255, 230),
            centro_local,
            (x_final, y_final),
            3
        )

        # Estela del radar
        for desplazamiento in range(
            8,
            55,
            8
        ):
            angulo_estela = math.radians(
                self.angulo_radar
                - desplazamiento
            )

            x_estela = centro_local[0] + int(
                math.cos(angulo_estela) * radio
            )

            y_estela = centro_local[1] + int(
                math.sin(angulo_estela) * radio
            )

            alpha = max(
                20,
                150 - desplazamiento * 2
            )

            pygame.draw.line(
                superficie_globo,
                (
                    103,
                    231,
                    255,
                    alpha
                ),
                centro_local,
                (
                    x_estela,
                    y_estela
                ),
                2
            )

        pantalla.blit(
            superficie_globo,
            (
                centro[0] - centro_local[0],
                centro[1] - centro_local[1]
            )
        )

    def manejar_evento(self, evento):
        if self._manejar_control_volumen(evento):
            return

        if (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
        ):
            pos_mouse = evento.pos

            if self.btn_jugar.collidepoint(pos_mouse):
                self.gestor.cambiar_a("previa")

            elif self.btn_participantes.collidepoint(
                pos_mouse
            ):
                self.gestor.cambiar_a(
                    "participantes"
                )

            elif self.btn_acerca_de.collidepoint(
                pos_mouse
            ):
                self.gestor.cambiar_a(
                    "acerca_de"
                )

            elif self.btn_salir.collidepoint(
                pos_mouse
            ):
                pygame.quit()
                sys.exit()

    def actualizar(self):
        self.angulo_radar += self.velocidad_radar

        if self.angulo_radar >= 360:
            self.angulo_radar = 0

    def _dibujar_boton(
        self,
        pantalla,
        rect,
        texto_principal,
        texto_secundario=None,
        activo=False
    ):
        mouse = pygame.mouse.get_pos()

        hover = rect.collidepoint(mouse)

        if hover or activo:
            base = self.color_panel_hover
            borde = self.color_borde
        else:
            base = self.color_panel
            borde = self.color_borde_suave

        sombra = pygame.Rect(
            rect.x + 5,
            rect.y + 6,
            rect.w,
            rect.h
        )

        pygame.draw.rect(
            pantalla,
            (0, 0, 0),
            sombra,
            border_radius=14
        )

        pygame.draw.rect(
            pantalla,
            base,
            rect,
            border_radius=14
        )

        pygame.draw.rect(
            pantalla,
            borde,
            rect,
            3,
            border_radius=14
        )

        # Flechas decorativas
        tri_izq = [
            (
                rect.x + 14,
                rect.centery
            ),
            (
                rect.x + 31,
                rect.y + 15
            ),
            (
                rect.x + 31,
                rect.bottom - 15
            ),
        ]

        tri_der = [
            (
                rect.right - 14,
                rect.centery
            ),
            (
                rect.right - 31,
                rect.y + 15
            ),
            (
                rect.right - 31,
                rect.bottom - 15
            ),
        ]

        pygame.draw.polygon(
            pantalla,
            borde,
            tri_izq,
            2
        )

        pygame.draw.polygon(
            pantalla,
            borde,
            tri_der,
            2
        )

        # Texto
        if texto_secundario:
            texto = self.fuente_botones.render(
                texto_principal,
                True,
                self.color_texto
            )

            sub = self.fuente_botones_chicos.render(
                texto_secundario,
                True,
                self.color_subtexto
            )

            bloque_alto = (
                texto.get_height()
                + 4
                + sub.get_height()
            )

            inicio_y = (
                rect.centery
                - bloque_alto // 2
            )

            pantalla.blit(
                texto,
                (
                    rect.centerx
                    - texto.get_width() // 2,
                    inicio_y
                )
            )

            pantalla.blit(
                sub,
                (
                    rect.centerx
                    - sub.get_width() // 2,
                    inicio_y
                    + texto.get_height()
                    + 4
                )
            )

        else:
            texto = self.fuente_botones.render(
                texto_principal,
                True,
                self.color_texto
            )

            pantalla.blit(
                texto,
                (
                    rect.centerx
                    - texto.get_width() // 2,
                    rect.centery
                    - texto.get_height() // 2
                )
            )

    def dibujar(self, pantalla):
        self._dibujar_fondo(pantalla)
        self._dibujar_globo(pantalla)

        texto_titulo = self.fuente_titulo.render(
            "Sapómetro",
            True,
            (103, 231, 255)
        )

        sombra_titulo = self.fuente_titulo.render(
            "Sapómetro",
            True,
            (15, 47, 73)
        )

        titulo_x = (
            config.ANCHO // 2
            - texto_titulo.get_width() // 2
        )

        pantalla.blit(
            sombra_titulo,
            (
                titulo_x + 3,
                30 + 3
            )
        )

        pantalla.blit(
            texto_titulo,
            (
                titulo_x,
                30
            )
        )

        # Subtítulo
        subtitulo = self.fuente_subtitulo.render(
            "PROYECTO EXPEDIENTE SECRETO: CLASIFICADO",
            True,
            self.color_texto
        )

        pantalla.blit(
            subtitulo,
            (
                config.ANCHO // 2
                - subtitulo.get_width() // 2,
                104
            )
        )

        texto_ayuda = self.fuente_ayuda.render(
            "Selecciona una opción para entrar al panel de análisis.",
            True,
            self.color_subtexto
        )

        pantalla.blit(
            texto_ayuda,
            (
                config.ANCHO // 2
                - texto_ayuda.get_width() // 2,
                137
            )
        )

        # Boton de volumen
        mouse = pygame.mouse.get_pos()
        hover_volumen = self.btn_volumen.collidepoint(mouse)
        base_volumen = self.color_panel_hover if hover_volumen or self.mostrando_control_volumen else self.color_panel
        borde_volumen = self.color_borde if hover_volumen or self.mostrando_control_volumen else self.color_borde_suave

        pygame.draw.rect(
            pantalla,
            (0, 0, 0),
            self.btn_volumen.move(3, 4),
            border_radius=10
        )
        pygame.draw.rect(
            pantalla,
            base_volumen,
            self.btn_volumen,
            border_radius=10
        )
        pygame.draw.rect(
            pantalla,
            borde_volumen,
            self.btn_volumen,
            2,
            border_radius=10
        )

        texto_volumen = self.fuente_botones_chicos.render(
            "VOLUMEN",
            True,
            self.color_texto
        )
        pantalla.blit(
            texto_volumen,
            (
                self.btn_volumen.centerx - texto_volumen.get_width() // 2,
                self.btn_volumen.centery - texto_volumen.get_height() // 2
            )
        )

        if self.mostrando_control_volumen:
            pygame.draw.rect(
                pantalla,
                self.color_panel,
                self.panel_volumen,
                border_radius=12
            )
            pygame.draw.rect(
                pantalla,
                self.color_borde,
                self.panel_volumen,
                2,
                border_radius=12
            )

            etiqueta = self.fuente_botones_chicos.render(
                f"{int(self.volumen * 100)}%",
                True,
                self.color_texto
            )
            pantalla.blit(
                etiqueta,
                (
                    self.panel_volumen.centerx - etiqueta.get_width() // 2,
                    self.panel_volumen.y + 10
                )
            )

            pygame.draw.rect(
                pantalla,
                self.color_borde_suave,
                self.barra_volumen,
                border_radius=6
            )

            ancho_activo = int(self.barra_volumen.w * self.volumen)
            if ancho_activo > 0:
                barra_activa = pygame.Rect(
                    self.barra_volumen.x,
                    self.barra_volumen.y,
                    ancho_activo,
                    self.barra_volumen.h
                )
                pygame.draw.rect(
                    pantalla,
                    self.color_acento,
                    barra_activa,
                    border_radius=6
                )

            perilla_x = self.barra_volumen.x + ancho_activo
            perilla = pygame.Rect(0, 0, 14, 18)
            perilla.center = (perilla_x, self.barra_volumen.centery)
            pygame.draw.rect(
                pantalla,
                self.color_texto,
                perilla,
                border_radius=5
            )

            for boton, simbolo in (
                (self.btn_volumen_menos, "-"),
                (self.btn_volumen_mas, "+"),
            ):
                pygame.draw.rect(
                    pantalla,
                    self.color_panel_hover,
                    boton,
                    border_radius=8
                )
                pygame.draw.rect(
                    pantalla,
                    self.color_borde_suave,
                    boton,
                    2,
                    border_radius=8
                )
                texto_boton = self.fuente_botones.render(
                    simbolo,
                    True,
                    self.color_texto
                )
                pantalla.blit(
                    texto_boton,
                    (
                        boton.centerx - texto_boton.get_width() // 2,
                        boton.centery - texto_boton.get_height() // 2 - 2
                    )
                )

        # Botones
        self._dibujar_boton(
            pantalla,
            self.btn_jugar,
            "JUGAR",
            activo=True
        )

        self._dibujar_boton(
            pantalla,
            self.btn_participantes,
            "CONOCER PARTICIPANTES",
            "PERFILES DE LOS PARTICIPANTES"
        )

        self._dibujar_boton(
            pantalla,
            self.btn_acerca_de,
            "INSTRUCCIONES",
            "INSTRUCCIONES DE JUEGO"
        )

        self._dibujar_boton(
            pantalla,
            self.btn_salir,
            "SALIR"
        )