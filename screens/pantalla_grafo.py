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


class PantallaGrafo:
    def __init__(self, gestor):
        self.gestor = gestor

        # Fuentes
        self.fuente_titulo = pygame.font.SysFont(
            "Segoe UI",
            38,
            bold=True
        )

        self.fuente_pregunta = pygame.font.SysFont(
            "Segoe UI",
            30,
            bold=True
        )

        self.fuente_nombre_nodo = pygame.font.SysFont(
            "Segoe UI",
            16,
            bold=True
        )

        self.fuente_btn = pygame.font.SysFont(
            "Segoe UI",
            25,
            bold=True
        )

        self.fuente_mensaje = pygame.font.SysFont(
            "Segoe UI",
            20
        )

        # Colores de los estados del DFS
        self.color_actual = COLOR_ACENTO
        self.color_visitado = (92, 190, 138)
        self.color_pendiente = COLOR_BORDE
        self.color_relleno_nodo = (12, 42, 68)

        # Panel principal
        self.panel = pygame.Rect(
            80,
            130,
            config.ANCHO - 160,
            330
        )

        # Botones centrados
        ancho_boton = 210
        alto_boton = 58
        separacion = 45

        ancho_total = ancho_boton * 2 + separacion
        inicio_x = config.ANCHO // 2 - ancho_total // 2

        self.btn_si = pygame.Rect(
            inicio_x,
            485,
            ancho_boton,
            alto_boton
        )

        self.btn_no = pygame.Rect(
            inicio_x + ancho_boton + separacion,
            485,
            ancho_boton,
            alto_boton
        )

        self.btn_menu = pygame.Rect(
            config.ANCHO // 2 - 130,
            460,
            260,
            54
        )

        self.candidatos_empatados = []
        self.indice_actual = 0
        self.candidato_actual = ""

        self.preguntas_arbol = 0
        self.preguntas_grafo = 0

        self.fallo_localizacion = False

    def cargar_candidatos(
        self,
        lista,
        preguntas_arbol=0
    ):
        self.candidatos_empatados = list(lista)
        self.indice_actual = 0
        self.preguntas_arbol = preguntas_arbol
        self.preguntas_grafo = 0
        self.fallo_localizacion = False

        if self.candidatos_empatados:
            self.candidato_actual = (
                self.candidatos_empatados[0]
            )
        else:
            self.candidato_actual = ""
            self.fallo_localizacion = True

    def manejar_evento(self, evento):
        if (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
        ):
            if self.fallo_localizacion:
                if self.btn_menu.collidepoint(evento.pos):
                    self.gestor.cambiar_a("inicio")

                return

            if self.btn_si.collidepoint(evento.pos):
                self.preguntas_grafo += 1

                pantalla_res = (
                    self.gestor.pantallas["resultado"]
                )

                pantalla_res.configurar_victoria(
                    self.candidato_actual,
                    "Árbol + Grafo (DFS)",
                    preguntas_arbol=self.preguntas_arbol,
                    preguntas_grafo=self.preguntas_grafo,
                    entro_grafo=True,
                )

                self.gestor.cambiar_a("resultado")

            elif self.btn_no.collidepoint(evento.pos):
                self.preguntas_grafo += 1
                self.indice_actual += 1

                if (
                    self.indice_actual
                    < len(self.candidatos_empatados)
                ):
                    self.candidato_actual = (
                        self.candidatos_empatados[
                            self.indice_actual
                        ]
                    )

                else:
                    self.fallo_localizacion = True

    def actualizar(self):
        pass

    def reiniciar(self):
        self.candidatos_empatados = []
        self.indice_actual = 0
        self.candidato_actual = ""

        self.preguntas_arbol = 0
        self.preguntas_grafo = 0

        self.fallo_localizacion = False

    def _nombre_corto(self, nombre_completo):
        """
        Obtiene primer nombre y primer apellido.

        Andrea Nicol Cumbal Gordon
        -> Andrea Cumbal
        """

        partes = str(nombre_completo).strip().split()

        if len(partes) >= 3:
            return f"{partes[0]} {partes[2]}"

        if len(partes) == 2:
            return f"{partes[0]} {partes[1]}"

        if len(partes) == 1:
            return partes[0]

        return ""

    def _obtener_posiciones_nodos(self):
        """
        Devuelve posiciones centradas según
        la cantidad de candidatos.
        """

        cantidad = len(self.candidatos_empatados)

        centro_x = config.ANCHO // 2
        y = 255

        if cantidad == 1:
            return [(centro_x, y)]

        if cantidad == 2:
            return [
                (centro_x - 110, y),
                (centro_x + 110, y),
            ]

        if cantidad == 3:
            return [
                (centro_x - 145, y),
                (centro_x, y),
                (centro_x + 145, y),
            ]

        # Por si después agregan cuatro candidatos
        if cantidad == 4:
            return [
                (centro_x - 195, y),
                (centro_x - 65, y),
                (centro_x + 65, y),
                (centro_x + 195, y),
            ]

        # Distribución genérica para más candidatos
        separacion = 120
        inicio_x = (
            centro_x
            - ((cantidad - 1) * separacion) // 2
        )

        return [
            (
                inicio_x + indice * separacion,
                y
            )
            for indice in range(cantidad)
        ]

    def _dibujar_grafo(self, pantalla):
        posiciones = self._obtener_posiciones_nodos()

        if not posiciones:
            return

        # Primero dibujar las aristas
        for indice in range(len(posiciones) - 1):
            pygame.draw.line(
                pantalla,
                COLOR_BORDE,
                posiciones[indice],
                posiciones[indice + 1],
                3
            )

        # Agregar una arista entre primero y último
        # cuando hay al menos tres nodos.
        # Así se forma un ciclo/triángulo.
        if len(posiciones) >= 3:
            pygame.draw.line(
                pantalla,
                COLOR_BORDE,
                posiciones[0],
                posiciones[-1],
                2
            )

        # Después dibujar cada nodo
        for indice, posicion in enumerate(posiciones):

            if indice < self.indice_actual:
                color_borde = self.color_visitado
                grosor = 4
                radio = 36

            elif indice == self.indice_actual:
                color_borde = self.color_actual
                grosor = 6
                radio = 44

            else:
                color_borde = self.color_pendiente
                grosor = 3
                radio = 36

            # Sombra
            pygame.draw.circle(
                pantalla,
                (0, 0, 0),
                (
                    posicion[0] + 4,
                    posicion[1] + 5
                ),
                radio
            )

            # Relleno
            pygame.draw.circle(
                pantalla,
                self.color_relleno_nodo,
                posicion,
                radio
            )

            # Borde según el estado
            pygame.draw.circle(
                pantalla,
                color_borde,
                posicion,
                radio,
                grosor
            )

            # Número del nodo dentro del círculo
            fuente_numero = pygame.font.SysFont(
                "Segoe UI",
                22,
                bold=True
            )

            texto_numero = fuente_numero.render(
                str(indice + 1),
                True,
                color_borde
            )

            pantalla.blit(
                texto_numero,
                (
                    posicion[0]
                    - texto_numero.get_width() // 2,
                    posicion[1]
                    - texto_numero.get_height() // 2
                )
            )

            # Nombre corto debajo del nodo
            nombre = self._nombre_corto(
                self.candidatos_empatados[indice]
            )

            texto_nombre = self.fuente_nombre_nodo.render(
                nombre,
                True,
                color_borde
            )

            pantalla.blit(
                texto_nombre,
                (
                    posicion[0]
                    - texto_nombre.get_width() // 2,
                    posicion[1] + radio + 12
                )
            )

    def _dibujar_texto_multilinea(
        self,
        pantalla,
        texto,
        centro_y,
        ancho_maximo
    ):
        """
        Divide una pregunta larga en varias líneas.
        """

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
                <= ancho_maximo
                or not linea_actual
            ):
                linea_actual = prueba

            else:
                lineas.append(linea_actual)
                linea_actual = palabra

        if linea_actual:
            lineas.append(linea_actual)

        separacion = 38
        alto_total = len(lineas) * separacion

        y_inicial = centro_y - alto_total // 2

        for indice, linea in enumerate(lineas):
            superficie = self.fuente_pregunta.render(
                linea,
                True,
                COLOR_TEXTO
            )

            pantalla.blit(
                superficie,
                (
                    config.ANCHO // 2
                    - superficie.get_width() // 2,
                    y_inicial + indice * separacion
                )
            )

    def _dibujar_fallo(self, pantalla):
        panel = pygame.Rect(
            100,
            160,
            config.ANCHO - 200,
            270
        )

        dibujar_panel(
            pantalla,
            panel,
            relleno=(12, 42, 68),
            borde=COLOR_BORDE,
            radio=18
        )

        centrar_texto(
            pantalla,
            self.fuente_titulo,
            "NO SE PUDO LOCALIZAR",
            185,
            COLOR_ACENTO
        )

        centrar_texto(
            pantalla,
            self.fuente_mensaje,
            "Se agotaron todos los candidatos del grafo.",
            255,
            COLOR_TEXTO
        )

        centrar_texto(
            pantalla,
            self.fuente_mensaje,
            "Revisa las respuestas o vuelve a intentarlo.",
            295,
            COLOR_SUBTEXTO
        )

        dibujar_boton(
            pantalla,
            self.btn_menu,
            self.fuente_btn,
            "VOLVER AL MENÚ",
            fondo=(12, 42, 68),
            borde=COLOR_BORDE
        )

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        if self.fallo_localizacion:
            self._dibujar_fallo(pantalla)
            return

        # Título
        centrar_texto(
            pantalla,
            self.fuente_titulo,
            "FASE DE GRAFO — RECORRIDO DFS",
            48,
            COLOR_TEXTO
        )

        # Panel
        dibujar_panel(
            pantalla,
            self.panel,
            relleno=(12, 42, 68),
            borde=COLOR_BORDE,
            radio=18
        )

        # Grafo dinámico
        self._dibujar_grafo(pantalla)

        # Pregunta actual
        nombre_corto = self._nombre_corto(
            self.candidato_actual
        )

        pregunta = (
            f"¿Tu personaje es {nombre_corto}?"
        )

        self._dibujar_texto_multilinea(
            pantalla,
            pregunta,
            centro_y=385,
            ancho_maximo=self.panel.width - 70
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

        # Estado del recorrido
        texto_estado = (
            f"Nodo visitado: "
            f"{self.indice_actual + 1} de "
            f"{len(self.candidatos_empatados)}"
            f"   |   Preguntas: "
            f"{self.preguntas_grafo}"
        )

        centrar_texto(
            pantalla,
            self.fuente_mensaje,
            texto_estado,
            558,
            COLOR_SUBTEXTO
        )