import os
import pygame
import config
from core.generar_arbol_manual import construir_arbol_datos, cargar_personas
from ui.estilo import (
    COLOR_ACENTO,
    COLOR_BORDE,
    COLOR_SUBTEXTO,
    COLOR_TEXTO,
    centrar_texto,
    dibujar_boton,
    dibujar_fondo_tecnologico,
    dibujar_panel,
)


class PantallaPreguntas:
    def __init__(self, gestor):
        self.gestor = gestor

        # Fuentes
        self.fuente_titulo = pygame.font.SysFont(
            "Segoe UI",
            46,
            bold=True
        )

        self.fuente_pregunta = pygame.font.SysFont(
            "Segoe UI",
            38,
            bold=True
        )

        self.fuente_btn = pygame.font.SysFont(
            "Segoe UI",
            28,
            bold=True
        )

        self.fuente_progreso = pygame.font.SysFont(
            "Segoe UI",
            18,
            bold=True
        )

        # Botones
        self.btn_si = pygame.Rect(
            200,
            420,
            180,
            56
        )

        self.btn_no = pygame.Rect(
            420,
            420,
            180,
            56
        )

        # Barra de progreso
        self.rect_barra_fondo = pygame.Rect(
            150,
            535,
            500,
            22
        )

        # Número aproximado máximo de preguntas del árbol
        self.max_preguntas_estimadas = 6

        # Ruta del archivo CSV
        ruta_script = os.path.abspath(__file__)

        ruta_proyecto = os.path.dirname(
            os.path.dirname(ruta_script)
        )

        self.ruta_archivo = os.path.join(
            ruta_proyecto,
            "data",
            "Formulario_proyecto_eda__respuestas__editado.csv"
        )

        # Cargar participantes y construir árbol
        lista_participantes = cargar_personas(
            self.ruta_archivo
        )

        self.nodo_actual = construir_arbol_datos(
            lista_participantes,
            0
        )

        self.preguntas_arbol = 0

    def manejar_evento(self, evento):
        if (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
        ):
            if self.btn_si.collidepoint(evento.pos):
                self.preguntas_arbol += 1

                self.nodo_actual = self.nodo_actual["si"]

                self.verificar_estado()

            elif self.btn_no.collidepoint(evento.pos):
                self.preguntas_arbol += 1

                self.nodo_actual = self.nodo_actual["no"]

                self.verificar_estado()

    def verificar_estado(self):
        if self.nodo_actual.get("tipo") == "hoja":
            pantalla_res = self.gestor.pantallas["resultado"]

            pantalla_res.configurar_victoria(
                self.nodo_actual["nombre"],
                "Árbol de Decisión",
                preguntas_arbol=self.preguntas_arbol,
                preguntas_grafo=0,
                entro_grafo=False,
            )

            self.gestor.cambiar_a("resultado")

        elif self.nodo_actual.get("tipo") == "grupo":
            pantalla_grafo = self.gestor.pantallas["grafo"]

            pantalla_grafo.cargar_candidatos(
                self.nodo_actual["nombres"],
                self.preguntas_arbol
            )

            self.gestor.cambiar_a("transicion")

    def actualizar(self):
        pass

    def reiniciar(self):
        lista_participantes = cargar_personas(
            self.ruta_archivo
        )

        self.nodo_actual = construir_arbol_datos(
            lista_participantes,
            0
        )

        self.preguntas_arbol = 0

    def _dibujar_barra_progreso(self, pantalla):
        # Evita que la barra supere el 100 %
        progreso = min(
            self.preguntas_arbol / self.max_preguntas_estimadas,
            1.0
        )

        # Fondo de la barra
        pygame.draw.rect(
            pantalla,
            (7, 25, 43),
            self.rect_barra_fondo,
            border_radius=11
        )

        # Borde
        pygame.draw.rect(
            pantalla,
            COLOR_BORDE,
            self.rect_barra_fondo,
            2,
            border_radius=11
        )

        # Parte completada
        ancho_completado = int(
            self.rect_barra_fondo.width * progreso
        )

        if ancho_completado > 0:
            rect_completado = pygame.Rect(
                self.rect_barra_fondo.x,
                self.rect_barra_fondo.y,
                ancho_completado,
                self.rect_barra_fondo.height
            )

            pygame.draw.rect(
                pantalla,
                COLOR_ACENTO,
                rect_completado,
                border_radius=11
            )

        # Texto de progreso
        porcentaje = int(progreso * 100)

        texto = self.fuente_progreso.render(
            f"Progreso del análisis: {porcentaje} %",
            True,
            COLOR_SUBTEXTO
        )

        pantalla.blit(
            texto,
            (
                config.ANCHO // 2
                - texto.get_width() // 2,
                self.rect_barra_fondo.y - 32
            )
        )

    def _dibujar_pregunta_centrada(
        self,
        pantalla,
        texto,
        panel
    ):
        # Si la pregunta cabe, se dibuja en una sola línea
        superficie = self.fuente_pregunta.render(
            texto,
            True,
            COLOR_TEXTO
        )

        max_ancho = panel.width - 70

        if superficie.get_width() <= max_ancho:
            pantalla.blit(
                superficie,
                (
                    panel.centerx
                    - superficie.get_width() // 2,
                    panel.centery
                    - superficie.get_height() // 2
                )
            )

            return

        # Si es demasiado larga, dividirla aproximadamente
        palabras = texto.split()
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            prueba = (
                f"{linea_actual} {palabra}".strip()
            )

            superficie_prueba = self.fuente_pregunta.render(
                prueba,
                True,
                COLOR_TEXTO
            )

            if (
                superficie_prueba.get_width() <= max_ancho
                or not linea_actual
            ):
                linea_actual = prueba
            else:
                lineas.append(linea_actual)
                linea_actual = palabra

        if linea_actual:
            lineas.append(linea_actual)

        separacion = 48
        alto_total = len(lineas) * separacion

        y_inicial = panel.centery - alto_total // 2

        for indice, linea in enumerate(lineas):
            superficie_linea = self.fuente_pregunta.render(
                linea,
                True,
                COLOR_TEXTO
            )

            pantalla.blit(
                superficie_linea,
                (
                    panel.centerx
                    - superficie_linea.get_width() // 2,
                    y_inicial + indice * separacion
                )
            )

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        centrar_texto(
            pantalla,
            self.fuente_titulo,
            "ANÁLISIS DEL EXPEDIENTE",
            60,
            COLOR_TEXTO
        )

        panel = pygame.Rect(
            70,
            150,
            660,
            185
        )

        dibujar_panel(
            pantalla,
            panel,
            relleno=(12, 42, 68),
            borde=COLOR_BORDE,
            radio=16
        )

        # Pregunta actual sin texto redundante
        pregunta = str(
            self.nodo_actual.get(
                "pregunta",
                ""
            )
        )

        self._dibujar_pregunta_centrada(
            pantalla,
            pregunta,
            panel
        )

        # Botones
        dibujar_boton(
            pantalla,
            self.btn_si,
            self.fuente_btn,
            "SÍ",
            fondo=(12, 42, 68),
            borde=COLOR_ACENTO
        )

        dibujar_boton(
            pantalla,
            self.btn_no,
            self.fuente_btn,
            "NO",
            fondo=(12, 42, 68),
            borde=COLOR_BORDE
        )

        # Barra de progreso
        self._dibujar_barra_progreso(
            pantalla
        )