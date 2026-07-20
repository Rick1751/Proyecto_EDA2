# screens/pantalla_acerca_de.py

import pygame
import config

from ui.estilo import (
    COLOR_ACENTO,
    COLOR_BORDE,
    COLOR_PANEL,
    COLOR_SUBTEXTO,
    COLOR_TEXTO,
    centrar_texto,
    dibujar_boton,
    dibujar_fondo_tecnologico,
    dibujar_panel,
)


class PantallaAcercaDe:
    def __init__(self, gestor):
        self.gestor = gestor
        self.pagina_actual = 0

        self.fuente_titulo = pygame.font.SysFont(
            "Segoe UI",
            39,
            bold=True
        )

        self.fuente_seccion = pygame.font.SysFont(
            "Segoe UI",
            28,
            bold=True
        )

        self.fuente_texto = pygame.font.SysFont(
            "Segoe UI",
            21
        )

        self.fuente_texto_chico = pygame.font.SysFont(
            "Segoe UI",
            18
        )

        self.fuente_numero = pygame.font.SysFont(
            "Segoe UI",
            22,
            bold=True
        )

        self.fuente_btn = pygame.font.SysFont(
            "Segoe UI",
            17,
            bold=True
        )

        # Panel principal
        self.panel = pygame.Rect(
            90,
            120,
            config.ANCHO - 180,
            365
        )

        # --------------------------------------------------
        # BOTONES
        # --------------------------------------------------

        ancho_boton = 175
        alto_boton = 46
        margen_lateral = 40

        # Botón a la izquierda
        self.btn_volver = pygame.Rect(
            margen_lateral,
            config.ALTO - 66,
            ancho_boton,
            alto_boton
        )

        # Botón centrado
        self.btn_anterior = pygame.Rect(
            config.ANCHO // 2 - ancho_boton // 2,
            config.ALTO - 66,
            ancho_boton,
            alto_boton
        )

        # Botón a la derecha
        self.btn_siguiente = pygame.Rect(
            config.ANCHO - margen_lateral - ancho_boton,
            config.ALTO - 66,
            ancho_boton,
            alto_boton
        )

    # --------------------------------------------------
    # EVENTOS
    # --------------------------------------------------

    def manejar_evento(self, evento):
        if (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
        ):
            if self.btn_volver.collidepoint(evento.pos):
                self.pagina_actual = 0
                self.gestor.cambiar_a("inicio")
                return

            if (
                self.pagina_actual == 1
                and self.btn_anterior.collidepoint(evento.pos)
            ):
                self.pagina_actual = 0
                return

            if (
                self.pagina_actual == 0
                and self.btn_siguiente.collidepoint(evento.pos)
            ):
                self.pagina_actual = 1

    def actualizar(self):
        pass

    # --------------------------------------------------
    # UTILIDADES DE TEXTO
    # --------------------------------------------------

    def _dibujar_texto(
        self,
        pantalla,
        texto,
        x,
        y,
        color,
        fuente=None
    ):
        if fuente is None:
            fuente = self.fuente_texto

        superficie = fuente.render(
            texto,
            True,
            color
        )

        pantalla.blit(
            superficie,
            (x, y)
        )

    def _dividir_texto(
        self,
        texto,
        fuente,
        ancho_maximo
    ):
        palabras = texto.split()
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            prueba = f"{linea_actual} {palabra}".strip()

            if fuente.size(prueba)[0] <= ancho_maximo:
                linea_actual = prueba
            else:
                if linea_actual:
                    lineas.append(linea_actual)

                linea_actual = palabra

        if linea_actual:
            lineas.append(linea_actual)

        return lineas

    def _dibujar_parrafo(
        self,
        pantalla,
        texto,
        rect,
        color,
        fuente=None,
        separacion=28
    ):
        if fuente is None:
            fuente = self.fuente_texto_chico

        lineas = self._dividir_texto(
            texto,
            fuente,
            rect.width
        )

        y = rect.y

        for linea in lineas:
            if y + separacion > rect.bottom:
                break

            superficie = fuente.render(
                linea,
                True,
                color
            )

            pantalla.blit(
                superficie,
                (rect.x, y)
            )

            y += separacion

        return y

    # --------------------------------------------------
    # PASOS DE LAS INSTRUCCIONES
    # --------------------------------------------------

    def _dibujar_paso(
        self,
        pantalla,
        numero,
        titulo,
        descripcion,
        y
    ):
        centro_numero = (
            self.panel.x + 55,
            y + 22
        )

        pygame.draw.circle(
            pantalla,
            COLOR_ACENTO,
            centro_numero,
            22,
            3
        )

        numero_surface = self.fuente_numero.render(
            str(numero),
            True,
            COLOR_ACENTO
        )

        pantalla.blit(
            numero_surface,
            (
                centro_numero[0]
                - numero_surface.get_width() // 2,
                centro_numero[1]
                - numero_surface.get_height() // 2
            )
        )

        self._dibujar_texto(
            pantalla,
            titulo,
            self.panel.x + 95,
            y,
            COLOR_TEXTO,
            self.fuente_texto
        )

        self._dibujar_texto(
            pantalla,
            descripcion,
            self.panel.x + 95,
            y + 31,
            COLOR_SUBTEXTO,
            self.fuente_texto_chico
        )

    # --------------------------------------------------
    # PÁGINA 1: INSTRUCCIONES
    # --------------------------------------------------

    def _dibujar_pagina_instrucciones(self, pantalla):
        centrar_texto(
            pantalla,
            self.fuente_titulo,
            "¿CÓMO FUNCIONA EL SAPÓMETRO?",
            38,
            COLOR_TEXTO
        )

        centrar_texto(
            pantalla,
            self.fuente_texto_chico,
            "Sigue estos pasos para iniciar una investigación.",
            87,
            COLOR_SUBTEXTO
        )

        dibujar_panel(
            pantalla,
            self.panel,
            relleno=COLOR_PANEL,
            borde=COLOR_BORDE,
            radio=18
        )

        self._dibujar_paso(
            pantalla,
            1,
            "Piensa en un participante",
            "Elige mentalmente una persona y no la cambies.",
            self.panel.y + 28
        )

        self._dibujar_paso(
            pantalla,
            2,
            "Responde únicamente SÍ o NO",
            "Cada respuesta permite avanzar por el árbol.",
            self.panel.y + 102
        )

        self._dibujar_paso(
            pantalla,
            3,
            "El árbol filtra a los candidatos",
            "Las características reducen las posibles personas.",
            self.panel.y + 176
        )

        self._dibujar_paso(
            pantalla,
            4,
            "Puede activarse el grafo",
            "Si quedan tres candidatos, comienza el recorrido DFS.",
            self.panel.y + 250
        )

        aviso_rect = pygame.Rect(
            self.panel.x + 35,
            self.panel.bottom - 52,
            self.panel.width - 70,
            35
        )

        pygame.draw.rect(
            pantalla,
            (20, 50, 73),
            aviso_rect,
            border_radius=9
        )

        aviso = self.fuente_texto_chico.render(
            "IMPORTANTE: no cambies de personaje durante la partida.",
            True,
            COLOR_ACENTO
        )

        pantalla.blit(
            aviso,
            (
                aviso_rect.centerx
                - aviso.get_width() // 2,
                aviso_rect.centery
                - aviso.get_height() // 2
            )
        )

        # Botones
        dibujar_boton(
            pantalla,
            self.btn_volver,
            self.fuente_btn,
            "VOLVER AL MENÚ",
            fondo=COLOR_PANEL,
            borde=COLOR_BORDE
        )

        dibujar_boton(
            pantalla,
            self.btn_siguiente,
            self.fuente_btn,
            "SIGUIENTE",
            fondo=COLOR_PANEL,
            borde=COLOR_ACENTO
        )

        indicador = self.fuente_texto_chico.render(
            "1 / 2",
            True,
            COLOR_SUBTEXTO
        )

        pantalla.blit(
            indicador,
            (
                config.ANCHO // 2
                - indicador.get_width() // 2,
                config.ALTO - 54
            )
        )

    # --------------------------------------------------
    # BLOQUE DE UNA ESTRUCTURA
    # --------------------------------------------------

    def _dibujar_estructura(
        self,
        pantalla,
        titulo,
        descripcion,
        x,
        y,
        ancho
    ):
        pygame.draw.circle(
            pantalla,
            COLOR_ACENTO,
            (x + 8, y + 10),
            5
        )

        self._dibujar_texto(
            pantalla,
            titulo,
            x + 25,
            y - 5,
            COLOR_TEXTO,
            self.fuente_texto
        )

        rect_descripcion = pygame.Rect(
            x + 25,
            y + 27,
            ancho - 25,
            58
        )

        self._dibujar_parrafo(
            pantalla,
            descripcion,
            rect_descripcion,
            COLOR_SUBTEXTO,
            self.fuente_texto_chico,
            separacion=24
        )

    # --------------------------------------------------
    # PÁGINA 2: ACERCA DEL PROYECTO
    # --------------------------------------------------

    def _dibujar_pagina_proyecto(self, pantalla):
        centrar_texto(
            pantalla,
            self.fuente_titulo,
            "ACERCA DEL PROYECTO",
            38,
            COLOR_TEXTO
        )

        centrar_texto(
            pantalla,
            self.fuente_texto_chico,
            "Proyecto final de Estructuras de Datos y Algoritmos I",
            87,
            COLOR_SUBTEXTO
        )

        dibujar_panel(
            pantalla,
            self.panel,
            relleno=COLOR_PANEL,
            borde=COLOR_BORDE,
            radio=18
        )

        x = self.panel.x + 38
        ancho_texto = self.panel.width - 76

        # Título de descripción
        self._dibujar_texto(
            pantalla,
            "¿QUÉ ES EL SAPÓMETRO?",
            x,
            self.panel.y + 24,
            COLOR_ACENTO,
            self.fuente_seccion
        )

        descripcion = (
            "El Sapómetro es un juego de adivinanza que identifica "
            "a un compañero de clase mediante preguntas binarias. "
            "El sistema combina un árbol de decisión con grafos para "
            "resolver los casos en los que varias personas comparten "
            "características similares."
        )

        rect_descripcion = pygame.Rect(
            x,
            self.panel.y + 70,
            ancho_texto,
            100
        )

        self._dibujar_parrafo(
            pantalla,
            descripcion,
            rect_descripcion,
            COLOR_TEXTO,
            self.fuente_texto_chico,
            separacion=26
        )

        # Separador
        pygame.draw.line(
            pantalla,
            COLOR_BORDE,
            (
                x,
                self.panel.y + 172
            ),
            (
                self.panel.right - 38,
                self.panel.y + 172
            ),
            2
        )

        self._dibujar_texto(
            pantalla,
            "ESTRUCTURAS UTILIZADAS",
            x,
            self.panel.y + 190,
            COLOR_ACENTO,
            self.fuente_seccion
        )

        # Tres columnas para evitar que el texto se salga
        espacio_columnas = 18
        ancho_columna = (
            ancho_texto - espacio_columnas * 2
        ) // 3

        y_estructuras = self.panel.y + 245

        self._dibujar_estructura(
            pantalla,
            "Árbol de decisión",
            "Filtra candidatos mediante preguntas de SÍ o NO.",
            x,
            y_estructuras,
            ancho_columna
        )

        self._dibujar_estructura(
            pantalla,
            "Grafo no dirigido",
            "Relaciona personas que comparten las mismas respuestas.",
            x + ancho_columna + espacio_columnas,
            y_estructuras,
            ancho_columna
        )

        self._dibujar_estructura(
            pantalla,
            "Recorrido DFS",
            "Visita los nodos hasta encontrar al participante.",
            x + (ancho_columna + espacio_columnas) * 2,
            y_estructuras,
            ancho_columna
        )

        # Botones
        dibujar_boton(
            pantalla,
            self.btn_volver,
            self.fuente_btn,
            "VOLVER AL MENÚ",
            fondo=COLOR_PANEL,
            borde=COLOR_BORDE
        )

        dibujar_boton(
            pantalla,
            self.btn_anterior,
            self.fuente_btn,
            "ANTERIOR",
            fondo=COLOR_PANEL,
            borde=COLOR_ACENTO
        )

        indicador = self.fuente_texto_chico.render(
            "2 / 2",
            True,
            COLOR_SUBTEXTO
        )

        pantalla.blit(
            indicador,
            (
                config.ANCHO // 2
                - indicador.get_width() // 2,
                config.ALTO - 54
            )
        )

    # --------------------------------------------------
    # DIBUJO PRINCIPAL
    # --------------------------------------------------

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        if self.pagina_actual == 0:
            self._dibujar_pagina_instrucciones(
                pantalla
            )
        else:
            self._dibujar_pagina_proyecto(
                pantalla
            )