# screens/pantalla_previa.py

import pygame
import config

from ui.estilo import (
    COLOR_ACENTO,
    COLOR_BORDE,
    COLOR_SUBTEXTO,
    COLOR_TEXTO,
    dibujar_boton,
    dibujar_fondo_tecnologico,
    dibujar_panel,
    centrar_texto,
)


class PantallaPrevia:
    def __init__(self, gestor):
        self.gestor = gestor

        # Fuentes
        self.fuente_titulo = pygame.font.SysFont(
            "Segoe UI",
            44,
            bold=True
        )

        self.fuente_subtitulo = pygame.font.SysFont(
            "Segoe UI",
            25
        )

        self.fuente_texto = pygame.font.SysFont(
            "Segoe UI",
            25
        )

        self.fuente_texto_acento = pygame.font.SysFont(
            "Segoe UI",
            23,
            bold=True
        )

        self.fuente_btn = pygame.font.SysFont(
            "Segoe UI",
            27,
            bold=True
        )

        self.fuente_btn_volver = pygame.font.SysFont(
            "Segoe UI",
            20,
            bold=True
        )

        # Panel central
        ancho_panel = min(700, config.ANCHO - 120)

        self.panel = pygame.Rect(
            config.ANCHO // 2 - ancho_panel // 2,
            190,
            ancho_panel,
            235
        )

        # Botón principal
        self.btn_comenzar = pygame.Rect(
            config.ANCHO // 2 - 220,
            465,
            440,
            64
        )

        # Botón volver
        self.btn_volver = pygame.Rect(
            40,
            config.ALTO - 70,
            150,
            44
        )

        self.esperando_jugador = True

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            if self.btn_comenzar.collidepoint(evento.pos):
                self.gestor.pantallas["preguntas"].reiniciar()
                self.gestor.pantallas["grafo"].reiniciar()
                self.gestor.pantallas["resultado"].reiniciar()

                self.gestor.cambiar_a("preguntas")

            elif self.btn_volver.collidepoint(evento.pos):
                self.gestor.cambiar_a("inicio")

    def actualizar(self):
        # La pantalla es estática
        pass

    def _dibujar_linea_centrada(
        self,
        pantalla,
        texto,
        fuente,
        y,
        color
    ):
        superficie = fuente.render(
            texto,
            True,
            color
        )

        x = (
            config.ANCHO // 2
            - superficie.get_width() // 2
        )

        pantalla.blit(
            superficie,
            (x, y)
        )

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        # Título
        centrar_texto(
            pantalla,
            self.fuente_titulo,
            "PREPARACIÓN DEL EXPEDIENTE",
            60,
            COLOR_TEXTO
        )

        # Subtítulo
        centrar_texto(
            pantalla,
            self.fuente_subtitulo,
            "Antes de continuar, piensa en uno de los participantes.",
            122,
            COLOR_SUBTEXTO
        )

        # Panel de instrucciones
        dibujar_panel(
            pantalla,
            self.panel,
            relleno=(12, 42, 68),
            borde=COLOR_BORDE,
            radio=18
        )

        # Primera instrucción
        self._dibujar_linea_centrada(
            pantalla,
            "No cambies de persona durante el juego.",
            self.fuente_texto,
            self.panel.y + 45,
            COLOR_TEXTO
        )

        # Segunda instrucción dividida en dos líneas
        self._dibujar_linea_centrada(
            pantalla,
            "El sistema recorrerá primero el árbol",
            self.fuente_texto_acento,
            self.panel.y + 105,
            COLOR_ACENTO
        )

        self._dibujar_linea_centrada(
            pantalla,
            "y utilizará un grafo si encuentra varios candidatos.",
            self.fuente_texto_acento,
            self.panel.y + 143,
            COLOR_ACENTO
        )

        # Texto final pequeño
        self._dibujar_linea_centrada(
            pantalla,
            "Responde únicamente con SÍ o NO.",
            self.fuente_texto,
            self.panel.y + 188,
            COLOR_SUBTEXTO
        )

        # Botón principal
        dibujar_boton(
            pantalla,
            self.btn_comenzar,
            self.fuente_btn,
            "COMENZAR PARTIDA",
            fondo=(12, 42, 68),
            borde=COLOR_ACENTO
        )

        # Botón volver
        dibujar_boton(
            pantalla,
            self.btn_volver,
            self.fuente_btn_volver,
            "VOLVER",
            fondo=(12, 42, 68),
            borde=COLOR_BORDE
        )