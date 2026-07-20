# screens/pantalla_preguntas.py
import os
import pygame
import logging
import config
from core.generar_arbol_manual import (
    construir_arbol_datos,
    cargar_personas,
    cargar_personas_paralelo,
)
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

logger = logging.getLogger(__name__)


class PantallaPreguntas:
    def __init__(self, gestor):
        self.gestor = gestor

        # --------------------------------------------------
        # FUENTES
        # --------------------------------------------------

        self.fuente_titulo = pygame.font.SysFont(
            "Segoe UI",
            46,
            bold=True
        )

        self.fuente_pregunta = pygame.font.SysFont(
            "Segoe UI",
            36,
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

        # --------------------------------------------------
        # BOTONES
        # --------------------------------------------------

        ancho_boton = 190
        alto_boton = 58
        separacion = 50

        ancho_total = ancho_boton * 2 + separacion
        inicio_x = config.ANCHO // 2 - ancho_total // 2

        self.btn_si = pygame.Rect(
            inicio_x,
            410,
            ancho_boton,
            alto_boton
        )

        self.btn_no = pygame.Rect(
            inicio_x + ancho_boton + separacion,
            410,
            ancho_boton,
            alto_boton
        )

        # --------------------------------------------------
        # BARRA DE PROGRESO
        # --------------------------------------------------

        self.rect_barra_fondo = pygame.Rect(
            config.ANCHO // 2 - 250,
            525,
            500,
            22
        )

        # Cantidad máxima estimada de preguntas del árbol
        self.max_preguntas_estimadas = 6

        # --------------------------------------------------
        # RUTA DEL ARCHIVO CSV
        # --------------------------------------------------

        ruta_script = os.path.abspath(__file__)

        ruta_proyecto = os.path.dirname(
            os.path.dirname(ruta_script)
        )

        self.ruta_archivo = os.path.join(
            ruta_proyecto,
            "data",
            "Formulario_proyecto_eda__respuestas__editado.csv"
        )

        # --------------------------------------------------
        # CARGAR DATOS Y CONSTRUIR ÁRBOL
        # --------------------------------------------------

        try:
            lista_participantes = cargar_personas_paralelo(
                self.ruta_archivo,
                usar_multiprocesamiento=True
            )
        except Exception as e:
            logger.warning(f"Error en carga paralela: {e}, usando carga secuencial")
            lista_participantes = cargar_personas(
                self.ruta_archivo
            )

        self.nodo_actual = construir_arbol_datos(
            lista_participantes,
            0
        )

        self.preguntas_arbol = 0

    # --------------------------------------------------
    # EVENTOS
    # --------------------------------------------------

    def manejar_evento(self, evento):
        if (
            evento.type != pygame.MOUSEBUTTONDOWN
            or evento.button != 1
        ):
            return

        # Evitar errores si por alguna razón ya no estamos
        # en un nodo de pregunta
        if self.nodo_actual.get("tipo") != "pregunta":
            return

        if self.btn_si.collidepoint(evento.pos):
            self.preguntas_arbol += 1

            self.nodo_actual = self.nodo_actual["si"]

            self.verificar_estado()

        elif self.btn_no.collidepoint(evento.pos):
            self.preguntas_arbol += 1

            self.nodo_actual = self.nodo_actual["no"]

            self.verificar_estado()

    # --------------------------------------------------
    # VERIFICACIÓN DEL ESTADO
    # --------------------------------------------------

    def verificar_estado(self):
        tipo_nodo = self.nodo_actual.get("tipo")

        # Se identificó directamente a una persona
        if tipo_nodo == "hoja":
            pantalla_resultado = (
                self.gestor.pantallas["resultado"]
            )

            pantalla_resultado.configurar_victoria(
                self.nodo_actual["nombre"],
                "Árbol de Decisión",
                preguntas_arbol=self.preguntas_arbol,
                preguntas_grafo=0,
                entro_grafo=False,
            )

            self.gestor.cambiar_a("resultado")

        # Quedó un grupo de candidatos
        elif tipo_nodo == "grupo":
            pantalla_grafo = (
                self.gestor.pantallas["grafo"]
            )

            pantalla_grafo.cargar_candidatos(
                self.nodo_actual["nombres"],
                self.preguntas_arbol
            )

            self.gestor.cambiar_a("transicion")

    def actualizar(self):
        pass

    # --------------------------------------------------
    # REINICIAR PARTIDA
    # --------------------------------------------------

    def reiniciar(self):
        try:
            lista_participantes = cargar_personas_paralelo(
                self.ruta_archivo,
                usar_multiprocesamiento=True
            )
        except Exception as e:
            logger.warning(f"Error en carga paralela: {e}, usando carga secuencial")
            lista_participantes = cargar_personas(
                self.ruta_archivo
            )

        self.nodo_actual = construir_arbol_datos(
            lista_participantes,
            0
        )

        self.preguntas_arbol = 0

    # --------------------------------------------------
    # FORMATEAR PREGUNTAS
    # --------------------------------------------------

    def _formatear_pregunta(self, pregunta):
        """
        Convierte las preguntas originales del árbol
        a una redacción uniforme con 'tu personaje'.

        Ejemplo:
        'Eres mujer?' -> '¿Tu personaje es mujer?'
        """

        pregunta = str(pregunta).strip()

        reemplazos = {
            "Eres mujer?":
                "¿Tu personaje es mujer?",

            "Usas lentes?":
                "¿Tu personaje usa lentes?",

            "Eres alto?":
                "¿Tu personaje es alto?",

            "Tienes el cabello largo?":
                "¿Tu personaje tiene el cabello largo?",

            "Tienes el cabello rizado?":
                "¿Tu personaje tiene el cabello rizado?",

            "Tienes barba?":
                "¿Tu personaje tiene barba?",

            "Eres de contextura delgada?":
                "¿Tu personaje es de contextura delgada?",

            "Usas gorra?":
                "¿Tu personaje usa gorra?",

            "Usas saco o hoodie?":
                "¿Tu personaje usa saco o hoodie?",

            "Eres foraneo?":
                "¿Tu personaje es foráneo?",

            "Eres foráneo?":
                "¿Tu personaje es foráneo?",

            "Sabes conducir?":
                "¿Tu personaje sabe conducir?",

            "Vas al gimnasio?":
                "¿Tu personaje va al gimnasio?",

            "Participas en el coro?":
                "¿Tu personaje participa en el coro?",

            "Te gusta apostar?":
                "¿A tu personaje le gusta apostar?",

            "Participas frecuentemente en clase?":
                "¿Tu personaje participa frecuentemente en clase?",

            "Te consideras extrovertido?":
                "¿Tu personaje es una persona extrovertida?",

            "Sueles llegar tarde?":
                "¿Tu personaje suele llegar tarde a clases?",

            "Te sientas adelante?":
                "¿Tu personaje se sienta normalmente adelante?",

            "Te sientas atras?":
                "¿Tu personaje se sienta normalmente atrás?",

            "Te sientas atrás?":
                "¿Tu personaje se sienta normalmente atrás?",

            "Primera letra del nombre A-H?":
                "¿El nombre de tu personaje empieza entre la A y la H?",

            "Primera letra del apellido A-M?":
                "¿El apellido de tu personaje empieza entre la A y la M?",

            "Usa tablet?":
                "¿Tu personaje usa tablet para tomar apuntes?",
        }

        # Si existe una redacción exacta, usarla
        if pregunta in reemplazos:
            return reemplazos[pregunta]

        # Respaldo genérico para preguntas no registradas
        pregunta_sin_signos = pregunta

        if pregunta_sin_signos.startswith("¿"):
            pregunta_sin_signos = pregunta_sin_signos[1:]

        if pregunta_sin_signos.endswith("?"):
            pregunta_sin_signos = pregunta_sin_signos[:-1]

        if not pregunta_sin_signos:
            return ""

        pregunta_sin_signos = (
            pregunta_sin_signos[0].lower()
            + pregunta_sin_signos[1:]
        )

        return (
            f"¿Tu personaje "
            f"{pregunta_sin_signos}?"
        )

    # --------------------------------------------------
    # BARRA DE PROGRESO
    # --------------------------------------------------

    def _dibujar_barra_progreso(self, pantalla):
        progreso = min(
            self.preguntas_arbol
            / self.max_preguntas_estimadas,
            1.0
        )

        # Fondo
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

        # Avance
        ancho_completado = int(
            self.rect_barra_fondo.width
            * progreso
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

        # Porcentaje
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
                self.rect_barra_fondo.y - 31
            )
        )

    # --------------------------------------------------
    # DIBUJAR PREGUNTA CENTRADA
    # --------------------------------------------------

    def _dibujar_pregunta_centrada(
        self,
        pantalla,
        texto,
        panel
    ):
        max_ancho = panel.width - 80

        superficie = self.fuente_pregunta.render(
            texto,
            True,
            COLOR_TEXTO
        )

        # Si cabe en una sola línea
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

        # Dividir automáticamente en varias líneas
        palabras = texto.split()
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            prueba = (
                f"{linea_actual} {palabra}".strip()
            )

            superficie_prueba = (
                self.fuente_pregunta.render(
                    prueba,
                    True,
                    COLOR_TEXTO
                )
            )

            if (
                superficie_prueba.get_width()
                <= max_ancho
                or not linea_actual
            ):
                linea_actual = prueba
            else:
                lineas.append(linea_actual)
                linea_actual = palabra

        if linea_actual:
            lineas.append(linea_actual)

        separacion = 48

        alto_total = (
            len(lineas) * separacion
        )

        y_inicial = (
            panel.centery
            - alto_total // 2
            + 4
        )

        for indice, linea in enumerate(lineas):
            superficie_linea = (
                self.fuente_pregunta.render(
                    linea,
                    True,
                    COLOR_TEXTO
                )
            )

            pantalla.blit(
                superficie_linea,
                (
                    panel.centerx
                    - superficie_linea.get_width() // 2,
                    y_inicial
                    + indice * separacion
                )
            )

    # --------------------------------------------------
    # DIBUJO PRINCIPAL
    # --------------------------------------------------

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        # Título
        centrar_texto(
            pantalla,
            self.fuente_titulo,
            "ANÁLISIS DEL EXPEDIENTE",
            58,
            COLOR_TEXTO
        )

        # Panel de pregunta
        panel = pygame.Rect(
            70,
            150,
            config.ANCHO - 140,
            185
        )

        dibujar_panel(
            pantalla,
            panel,
            relleno=(12, 42, 68),
            borde=COLOR_BORDE,
            radio=16
        )

        # Obtener y adaptar la pregunta
        pregunta_original = self.nodo_actual.get(
            "pregunta",
            ""
        )

        pregunta_formateada = (
            self._formatear_pregunta(
                pregunta_original
            )
        )

        self._dibujar_pregunta_centrada(
            pantalla,
            pregunta_formateada,
            panel
        )

        # Botón SÍ
        dibujar_boton(
            pantalla,
            self.btn_si,
            self.fuente_btn,
            "SÍ",
            fondo=(12, 42, 68),
            borde=COLOR_ACENTO
        )

        # Botón NO
        dibujar_boton(
            pantalla,
            self.btn_no,
            self.fuente_btn,
            "NO",
            fondo=(12, 42, 68),
            borde=COLOR_BORDE
        )

        # Progreso
        self._dibujar_barra_progreso(
            pantalla
        )