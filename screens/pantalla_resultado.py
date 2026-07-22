# screens/pantalla_resultado.py

import os
import unicodedata
import pygame
import config
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


class PantallaResultado:
    def __init__(self, gestor):
        self.gestor = gestor

        # Fuentes
        self.fuente_titulo = pygame.font.SysFont(
            "Segoe UI",
            38,
            bold=True
        )

        self.fuente_nombre = pygame.font.SysFont(
            "Segoe UI",
            34,
            bold=True
        )

        self.fuente_texto = pygame.font.SysFont(
            "Segoe UI",
            21
        )

        self.fuente_btn = pygame.font.SysFont(
            "Segoe UI",
            20,
            bold=True
        )

        # Panel principal
        self.panel = pygame.Rect(
            90,
            70,
            config.ANCHO - 180,
            430
        )

        # Caja de fotografía centrada
        self.caja_foto = pygame.Rect(
            config.ANCHO // 2 - 105,
            105,
            210,
            210
        )

        # Botones inferiores
        ancho_boton = 240
        alto_boton = 54
        separacion = 24

        ancho_total = ancho_boton * 2 + separacion
        inicio_x = config.ANCHO // 2 - ancho_total // 2

        self.btn_jugar = pygame.Rect(
            inicio_x,
            520,
            ancho_boton,
            alto_boton
        )

        self.btn_menu = pygame.Rect(
            inicio_x + ancho_boton + separacion,
            520,
            ancho_boton,
            alto_boton
        )

        self.personaje_adivinado = ""
        self.metodo_usado = ""
        self.preguntas_arbol = 0
        self.preguntas_grafo = 0
        self.entro_grafo = False
        self.imagen_personaje = None

        ruta_script = os.path.abspath(__file__)
        ruta_proyecto = os.path.dirname(
            os.path.dirname(ruta_script)
        )

        self.ruta_imagenes = os.path.join(
            ruta_proyecto,
            "assets",
            "images",
            "imagenes"
        )

        self._cache_imagenes = {}

    def configurar_victoria(
        self,
        nombre,
        metodo,
        preguntas_arbol=0,
        preguntas_grafo=0,
        entro_grafo=False
    ):
        self.personaje_adivinado = nombre
        self.metodo_usado = metodo
        self.preguntas_arbol = preguntas_arbol
        self.preguntas_grafo = preguntas_grafo
        self.entro_grafo = entro_grafo

        self.imagen_personaje = (
            self._cargar_imagen_personaje(nombre)
        )

    def manejar_evento(self, evento):
        if (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
        ):
            if self.btn_jugar.collidepoint(evento.pos):
                self.gestor.cambiar_a("previa")

            elif self.btn_menu.collidepoint(evento.pos):
                self.gestor.cambiar_a("inicio")

    def actualizar(self):
        pass

    def reiniciar(self):
        self.personaje_adivinado = ""
        self.metodo_usado = ""
        self.preguntas_arbol = 0
        self.preguntas_grafo = 0
        self.entro_grafo = False
        self.imagen_personaje = None

    def _normalizar_texto(self, texto):
        texto = unicodedata.normalize(
            "NFD",
            str(texto)
        )

        texto = "".join(
            caracter
            for caracter in texto
            if unicodedata.category(caracter) != "Mn"
        )

        return "".join(
            caracter.lower()
            for caracter in texto
            if caracter.isalnum()
        )

    def _obtener_nombre_corto(self, nombre_completo):

        partes = str(nombre_completo).strip().split()

        if not partes:
            return ""

        if len(partes) >= 3:
            return f"{partes[0]} {partes[2]}"

        if len(partes) == 2:
            return f"{partes[0]} {partes[1]}"

        return partes[0]

    def _cargar_imagen_personaje(self, nombre):
        nombre_limpio = self._normalizar_texto(nombre)

        if not nombre_limpio:
            return None

        candidatos = []

        nombre_original = " ".join(
            str(nombre).split()
        )

        if nombre_original:
            primer_nombre = nombre_original.split()[0]

            candidatos.append(
                self._normalizar_texto(primer_nombre)
            )

        candidatos.append(nombre_limpio)

        candidatos = [
            candidato
            for candidato in candidatos
            if candidato
        ]

        extensiones = [
            ".png",
            ".jpg",
            ".jpeg"
        ]

        for candidato in candidatos:
            for extension in extensiones:
                nombre_archivo = (
                    f"im{candidato}{extension}"
                )

                ruta_imagen = os.path.join(
                    self.ruta_imagenes,
                    nombre_archivo
                )

                if ruta_imagen in self._cache_imagenes:
                    return self._cache_imagenes[
                        ruta_imagen
                    ]

                if os.path.exists(ruta_imagen):
                    imagen = pygame.image.load(
                        ruta_imagen
                    ).convert_alpha()

                    self._cache_imagenes[
                        ruta_imagen
                    ] = imagen

                    return imagen

        return None

    def _escalar_imagen_sin_deformar(
        self,
        imagen,
        ancho_maximo,
        alto_maximo
    ):

        ancho_original = imagen.get_width()
        alto_original = imagen.get_height()

        if ancho_original <= 0 or alto_original <= 0:
            return imagen

        escala = min(
            ancho_maximo / ancho_original,
            alto_maximo / alto_original
        )

        nuevo_ancho = max(
            1,
            int(ancho_original * escala)
        )

        nuevo_alto = max(
            1,
            int(alto_original * escala)
        )

        return pygame.transform.smoothscale(
            imagen,
            (
                nuevo_ancho,
                nuevo_alto
            )
        )

    def _dibujar_foto(self, pantalla):
        dibujar_panel(
            pantalla,
            self.caja_foto,
            relleno=(7, 27, 47),
            borde=COLOR_BORDE,
            radio=18
        )

        if self.imagen_personaje is None:
            texto_foto = self.fuente_texto.render(
                "Sin fotografía",
                True,
                COLOR_SUBTEXTO
            )

            pantalla.blit(
                texto_foto,
                (
                    self.caja_foto.centerx
                    - texto_foto.get_width() // 2,
                    self.caja_foto.centery
                    - texto_foto.get_height() // 2
                )
            )

            return

        margen = 10

        imagen_escalada = (
            self._escalar_imagen_sin_deformar(
                self.imagen_personaje,
                self.caja_foto.width - margen * 2,
                self.caja_foto.height - margen * 2
            )
        )

        x = (
            self.caja_foto.centerx
            - imagen_escalada.get_width() // 2
        )

        y = (
            self.caja_foto.centery
            - imagen_escalada.get_height() // 2
        )

        pantalla.blit(
            imagen_escalada,
            (x, y)
        )

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        # Panel central
        dibujar_panel(
            pantalla,
            self.panel,
            relleno=(12, 42, 68),
            borde=COLOR_BORDE,
            radio=18
        )

        # Título superior
        centrar_texto(
            pantalla,
            self.fuente_titulo,
            "RESULTADO DEL ANÁLISIS",
            22,
            COLOR_TEXTO
        )

        # Foto centrada
        self._dibujar_foto(pantalla)

        # Nombre corto: primer nombre + primer apellido
        nombre_corto = self._obtener_nombre_corto(
            self.personaje_adivinado
        )

        centrar_texto(
            pantalla,
            self.fuente_nombre,
            f"¡Es {nombre_corto}!",
            330,
            COLOR_ACENTO
        )

        # Método
        centrar_texto(
            pantalla,
            self.fuente_texto,
            f"Método utilizado: {self.metodo_usado}",
            380,
            COLOR_TEXTO
        )

        # Información resumida
        if self.entro_grafo:
            resumen = (
                f"Árbol: {self.preguntas_arbol} preguntas"
                f"   |   Grafo: {self.preguntas_grafo} preguntas"
            )
        else:
            resumen = (
                f"Preguntas realizadas en el árbol: "
                f"{self.preguntas_arbol}"
            )

        centrar_texto(
            pantalla,
            self.fuente_texto,
            resumen,
            420,
            COLOR_SUBTEXTO
        )

        # Indicador de estructuras usadas
        estructura = (
            "Árbol + Grafo"
            if self.entro_grafo
            else "Árbol de decisión"
        )

        centrar_texto(
            pantalla,
            self.fuente_texto,
            f"Estructura utilizada: {estructura}",
            456,
            COLOR_TEXTO
        )

        # Botones
        dibujar_boton(
            pantalla,
            self.btn_jugar,
            self.fuente_btn,
            "JUGAR OTRA VEZ",
            fondo=(12, 42, 68),
            borde=COLOR_ACENTO
        )

        dibujar_boton(
            pantalla,
            self.btn_menu,
            self.fuente_btn,
            "VOLVER AL MENÚ",
            fondo=(12, 42, 68),
            borde=COLOR_BORDE
        )