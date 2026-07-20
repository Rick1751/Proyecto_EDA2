# screens/pantalla_participantes.py

import os
import unicodedata

import pygame

import config
from core.generar_arbol_manual import cargar_personas
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


class PantallaParticipantes:
    def __init__(self, gestor):
        self.gestor = gestor

        # Fuentes
        self.fuente_titulo = pygame.font.SysFont(
            "Segoe UI", 43, bold=True
        )
        self.fuente_subtitulo = pygame.font.SysFont(
            "Segoe UI", 20
        )
        self.fuente_nombre = pygame.font.SysFont(
            "Segoe UI", 22, bold=True
        )
        self.fuente_nombre_ficha = pygame.font.SysFont(
            "Segoe UI", 31, bold=True
        )
        self.fuente_texto = pygame.font.SysFont(
            "Segoe UI", 21
        )
        self.fuente_narrativa = pygame.font.SysFont(
            "Segoe UI", 20
        )
        self.fuente_chica = pygame.font.SysFont(
            "Segoe UI", 16
        )
        self.fuente_btn = pygame.font.SysFont(
            "Segoe UI", 19, bold=True
        )

        # Botones de la galería
        self.btn_volver = pygame.Rect(
            42, config.ALTO - 62, 155, 44
        )
        self.btn_prev = pygame.Rect(
            config.ANCHO // 2 - 175,
            config.ALTO - 62,
            155,
            44
        )
        self.btn_next = pygame.Rect(
            config.ANCHO // 2 + 20,
            config.ALTO - 62,
            155,
            44
        )

        # Botón de la ficha individual
        self.btn_volver_ficha = pygame.Rect(
            config.ANCHO // 2 - 115,
            config.ALTO - 67,
            230,
            48
        )

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

        self.ruta_csv = os.path.join(
            ruta_proyecto,
            "data",
            "Formulario_proyecto_eda__respuestas__editado.csv"
        )

        self._cache_imagenes = {}

        self.personajes = self._cargar_personajes()

        self.personaje_seleccionado = None
        self.pagina_actual = 0

        # 6 fichas: 3 columnas × 2 filas
        self.personajes_por_pagina = 6
        self.rects_personajes = []

    # ---------------------------------------------------------
    # EVENTOS
    # ---------------------------------------------------------

    def manejar_evento(self, evento):
        if (
            evento.type != pygame.MOUSEBUTTONDOWN
            or evento.button != 1
        ):
            return

        # Ficha individual abierta
        if self.personaje_seleccionado is not None:
            if self.btn_volver_ficha.collidepoint(evento.pos):
                self.personaje_seleccionado = None
            return

        # Galería
        if self.btn_volver.collidepoint(evento.pos):
            self.gestor.cambiar_a("inicio")
            return

        if (
            self.btn_prev.collidepoint(evento.pos)
            and self.pagina_actual > 0
        ):
            self.pagina_actual -= 1
            return

        if (
            self.btn_next.collidepoint(evento.pos)
            and self._hay_siguiente_pagina()
        ):
            self.pagina_actual += 1
            return

        for indice, rect in self.rects_personajes:
            if rect.collidepoint(evento.pos):
                self.personaje_seleccionado = (
                    self.personajes[indice]
                )
                return

    def actualizar(self):
        pass

    # ---------------------------------------------------------
    # DATOS
    # ---------------------------------------------------------

    def _normalizar_texto(self, texto):
        texto = unicodedata.normalize(
            "NFD", str(texto)
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

    def _es_si(self, valor):
        return (
            str(valor).strip().lower()
            in ("si", "sí")
        )

    def _nombre_corto(self, nombre):
        """
        Primer nombre + primer apellido.

        Andrea Nicol Cumbal Gordon
        -> Andrea Cumbal
        """

        partes = str(nombre).strip().split()

        if len(partes) >= 3:
            return f"{partes[0]} {partes[2]}"

        if len(partes) == 2:
            return f"{partes[0]} {partes[1]}"

        return partes[0] if partes else ""

    def _cargar_imagen_personaje(self, nombre):
        nombre_normalizado = self._normalizar_texto(nombre)

        if not nombre_normalizado:
            return None

        partes = str(nombre).split()

        candidatos = []

        if partes:
            candidatos.append(
                self._normalizar_texto(partes[0])
            )

        candidatos.append(nombre_normalizado)

        for candidato in candidatos:
            for extension in (
                ".png",
                ".jpg",
                ".jpeg"
            ):
                ruta_imagen = os.path.join(
                    self.ruta_imagenes,
                    f"im{candidato}{extension}"
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

    def _cargar_personajes(self):
        personas = cargar_personas(self.ruta_csv)
        personajes = []

        for persona in personas:
            nombre = persona["nombre"]

            personajes.append({
                "nombre": nombre,
                "datos": persona,
                "imagen": self._cargar_imagen_personaje(
                    nombre
                ),
            })

        return personajes

    def _hay_siguiente_pagina(self):
        inicio = (
            self.pagina_actual
            * self.personajes_por_pagina
        )

        return (
            inicio + self.personajes_por_pagina
            < len(self.personajes)
        )

    # ---------------------------------------------------------
    # NARRATIVA
    # ---------------------------------------------------------

    def _crear_narrativa(self, personaje):
        datos = personaje["datos"]
        nombre = self._nombre_corto(
            personaje["nombre"]
        )
        primer_nombre = nombre.split()[0]

        es_mujer = self._es_si(
            datos.get("Eres mujer?", "")
        )

        sujeto = "Ella" if es_mujer else "Él"
        alto = "alta" if es_mujer else "alto"
        delgado = (
            "delgada" if es_mujer else "delgado"
        )
        extrovertido = (
            "extrovertida"
            if es_mujer
            else "extrovertido"
        )
        foraneo = (
            "foránea" if es_mujer else "foráneo"
        )

        frases = []

        # Presentación física
        rasgos_fisicos = []

        if self._es_si(
            datos.get(
                "Eres alto? (+1.70cm en hombres, +1,60cm en mujeres)",
                ""
            )
        ):
            rasgos_fisicos.append(f"es {alto}")

        if self._es_si(
            datos.get("Usas lentes?", "")
        ):
            rasgos_fisicos.append("usa lentes")

        if self._es_si(
            datos.get(
                "Eres de contextura delgada?",
                ""
            )
        ):
            rasgos_fisicos.append(
                f"es de contextura {delgado}"
            )

        if rasgos_fisicos:
            frases.append(
                self._unir_elementos(
                    rasgos_fisicos,
                    inicio=f"{nombre} "
                ) + "."
            )
        else:
            frases.append(
                f"{nombre} forma parte de los "
                "participantes del Sapómetro."
            )

        # Cabello
        caracteristicas_cabello = []

        if self._es_si(
            datos.get(
                "Tienes el cabello largo? (3 dedos por debajo del hombro)",
                ""
            )
        ):
            caracteristicas_cabello.append("largo")

        if self._es_si(
            datos.get(
                "Tienes el cabello rizado?",
                ""
            )
        ):
            caracteristicas_cabello.append("rizado")

        if caracteristicas_cabello:
            cabello = " y ".join(
                caracteristicas_cabello
            )

            frases.append(
                f"{sujeto} tiene el cabello "
                f"{cabello}."
            )

        # Hábitos y actividades
        actividades = []

        if self._es_si(
            datos.get("Sabes conducir?", "")
        ):
            actividades.append("sabe conducir")

        if self._es_si(
            datos.get(
                "Vas al gimnasio a menudo ?(mínimo 3 veces por semana)",
                ""
            )
        ):
            actividades.append(
                "va frecuentemente al gimnasio"
            )

        if self._es_si(
            datos.get(
                "Participas en el coro?",
                ""
            )
        ):
            actividades.append(
                "participa en el coro"
            )

        if self._es_si(
            datos.get(
                "Te gusta apostar ?",
                ""
            )
        ):
            actividades.append(
                "le gusta apostar"
            )

        if actividades:
            frases.append(
                self._unir_elementos(
                    actividades,
                    inicio="Además, "
                ) + "."
            )

        # Personalidad y comportamiento en clases
        personalidad = []

        if self._es_si(
            datos.get(
                "Participas frecuentemente en clase?",
                ""
            )
        ):
            personalidad.append(
                "participa frecuentemente en clase"
            )

        if self._es_si(
            datos.get(
                "Te consideras una persona extrovertida?",
                ""
            )
        ):
            personalidad.append(
                f"se considera una persona "
                f"{extrovertido}"
            )

        if self._es_si(
            datos.get(
                "Sueles llegar tarde a clases?",
                ""
            )
        ):
            personalidad.append(
                "suele llegar tarde a clases"
            )

        if personalidad:
            frases.append(
                self._unir_elementos(
                    personalidad,
                    inicio=f"{sujeto} "
                ) + "."
            )

        # Lugar donde se sienta
        if self._es_si(
            datos.get(
                "Te sientas normalmente en la parte delantera del aula?",
                ""
            )
        ):
            frases.append(
                f"Normalmente se sienta en la "
                "parte delantera del aula."
            )

        elif self._es_si(
            datos.get(
                "Te sientas normalmente en la parte trasera del aula?",
                ""
            )
        ):
            frases.append(
                "Normalmente se sienta en la "
                "parte trasera del aula."
            )

        else:
            frases.append(
                "Normalmente se sienta en la "
                "parte media del aula."
            )

        # Otros detalles
        detalles = []

        if self._es_si(
            datos.get(
                "Usas saco o hoddie en la universidad frecuentemente?",
                ""
            )
        ):
            detalles.append(
                "suele usar saco o hoodie "
                "en la universidad"
            )

        if self._es_si(
            datos.get(
                "¿Usa tablet para tomar apuntes? ",
                ""
            )
        ):
            detalles.append(
                "utiliza una tablet para "
                "tomar apuntes"
            )

        if self._es_si(
            datos.get("Eres foraneo?", "")
        ):
            detalles.append(
                f"es estudiante {foraneo}"
            )

        if detalles:
            frases.append(
                self._unir_elementos(
                    detalles,
                    inicio=f"{primer_nombre} "
                ) + "."
            )

        return " ".join(frases)

    def _unir_elementos(
        self,
        elementos,
        inicio=""
    ):
        if not elementos:
            return inicio.strip()

        if len(elementos) == 1:
            return inicio + elementos[0]

        if len(elementos) == 2:
            return (
                inicio
                + elementos[0]
                + " y "
                + elementos[1]
            )

        return (
            inicio
            + ", ".join(elementos[:-1])
            + " y "
            + elementos[-1]
        )

    # ---------------------------------------------------------
    # TEXTO E IMÁGENES
    # ---------------------------------------------------------

    def _dividir_texto(
        self,
        texto,
        fuente,
        ancho_maximo
    ):
        palabras = texto.split()
        lineas = []
        linea = ""

        for palabra in palabras:
            prueba = f"{linea} {palabra}".strip()

            if (
                fuente.size(prueba)[0]
                <= ancho_maximo
            ):
                linea = prueba
            else:
                if linea:
                    lineas.append(linea)
                linea = palabra

        if linea:
            lineas.append(linea)

        return lineas

    def _dibujar_parrafo(
        self,
        pantalla,
        texto,
        rect,
        color
    ):
        lineas = self._dividir_texto(
            texto,
            self.fuente_narrativa,
            rect.width
        )

        y = rect.y
        alto_linea = 27

        for linea in lineas:
            if y + alto_linea > rect.bottom:
                break

            superficie = (
                self.fuente_narrativa.render(
                    linea,
                    True,
                    color
                )
            )

            pantalla.blit(
                superficie,
                (rect.x, y)
            )

            y += alto_linea

    def _escalar_imagen(
        self,
        imagen,
        ancho_maximo,
        alto_maximo
    ):
        ancho = imagen.get_width()
        alto = imagen.get_height()

        if ancho <= 0 or alto <= 0:
            return imagen

        escala = min(
            ancho_maximo / ancho,
            alto_maximo / alto
        )

        return pygame.transform.smoothscale(
            imagen,
            (
                max(1, int(ancho * escala)),
                max(1, int(alto * escala))
            )
        )

    def _dibujar_foto(
        self,
        pantalla,
        rect,
        personaje
    ):
        dibujar_panel(
            pantalla,
            rect,
            relleno=(7, 27, 47),
            borde=COLOR_BORDE,
            radio=12
        )

        imagen = personaje["imagen"]

        if imagen is not None:
            imagen = self._escalar_imagen(
                imagen,
                rect.width - 10,
                rect.height - 10
            )

            x = (
                rect.centerx
                - imagen.get_width() // 2
            )
            y = (
                rect.centery
                - imagen.get_height() // 2
            )

            pantalla.blit(imagen, (x, y))
            return

        iniciales = "".join(
            parte[0]
            for parte in personaje["nombre"].split()[:2]
        ).upper()

        texto = self.fuente_nombre.render(
            iniciales,
            True,
            COLOR_ACENTO
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

    # ---------------------------------------------------------
    # DIBUJO GALERÍA
    # ---------------------------------------------------------

    def _dibujar_galeria(self, pantalla):
        centrar_texto(
            pantalla,
            self.fuente_titulo,
            "BASE DE DATOS DE PARTICIPANTES",
            25,
            COLOR_TEXTO
        )

        centrar_texto(
            pantalla,
            self.fuente_subtitulo,
            "Selecciona un expediente para conocer "
            "mejor al participante.",
            77,
            COLOR_SUBTEXTO
        )

        inicio = (
            self.pagina_actual
            * self.personajes_por_pagina
        )

        fin = min(
            inicio + self.personajes_por_pagina,
            len(self.personajes)
        )

        visibles = self.personajes[inicio:fin]

        self.rects_personajes = []

        # 3 columnas × 2 filas
        ancho_tarjeta = 226
        alto_tarjeta = 172
        espacio_x = 242
        espacio_y = 187

        ancho_total = (
            ancho_tarjeta * 3
            + (espacio_x - ancho_tarjeta) * 2
        )

        origen_x = (
            config.ANCHO // 2
            - ancho_total // 2
        )
        origen_y = 115

        mouse = pygame.mouse.get_pos()

        for indice_local, personaje in enumerate(
            visibles
        ):
            fila = indice_local // 3
            columna = indice_local % 3

            x = origen_x + columna * espacio_x
            y = origen_y + fila * espacio_y

            rect = pygame.Rect(
                x,
                y,
                ancho_tarjeta,
                alto_tarjeta
            )

            indice_real = inicio + indice_local

            self.rects_personajes.append(
                (indice_real, rect)
            )

            hover = rect.collidepoint(mouse)

            borde = (
                COLOR_ACENTO
                if hover
                else COLOR_BORDE
            )

            relleno = (
                (17, 52, 78)
                if hover
                else COLOR_PANEL
            )

            # Sombra
            sombra = rect.move(5, 6)

            pygame.draw.rect(
                pantalla,
                (0, 0, 0),
                sombra,
                border_radius=15
            )

            dibujar_panel(
                pantalla,
                rect,
                relleno=relleno,
                borde=borde,
                radio=15
            )

            foto_rect = pygame.Rect(
                x + 12,
                y + 12,
                ancho_tarjeta - 24,
                103
            )

            self._dibujar_foto(
                pantalla,
                foto_rect,
                personaje
            )

            nombre = self._nombre_corto(
                personaje["nombre"]
            )

            nombre_surface = (
                self.fuente_nombre.render(
                    nombre,
                    True,
                    COLOR_TEXTO
                )
            )

            pantalla.blit(
                nombre_surface,
                (
                    rect.centerx
                    - nombre_surface.get_width() // 2,
                    y + 121
                )
            )

            pista = self.fuente_chica.render(
                "ABRIR EXPEDIENTE",
                True,
                borde
            )

            pantalla.blit(
                pista,
                (
                    rect.centerx
                    - pista.get_width() // 2,
                    y + 148
                )
            )

        # Botones inferiores
        dibujar_boton(
            pantalla,
            self.btn_volver,
            self.fuente_btn,
            "VOLVER",
            fondo=COLOR_PANEL,
            borde=COLOR_BORDE
        )

        dibujar_boton(
            pantalla,
            self.btn_prev,
            self.fuente_btn,
            "ANTERIOR",
            fondo=COLOR_PANEL,
            borde=(
                COLOR_BORDE
                if self.pagina_actual > 0
                else COLOR_SUBTEXTO
            )
        )

        dibujar_boton(
            pantalla,
            self.btn_next,
            self.fuente_btn,
            "SIGUIENTE",
            fondo=COLOR_PANEL,
            borde=(
                COLOR_BORDE
                if self._hay_siguiente_pagina()
                else COLOR_SUBTEXTO
            )
        )

        paginas_total = max(
            1,
            (
                len(self.personajes)
                + self.personajes_por_pagina
                - 1
            )
            // self.personajes_por_pagina
        )

        indicador = self.fuente_chica.render(
            f"EXPEDIENTE {self.pagina_actual + 1} "
            f"DE {paginas_total}",
            True,
            COLOR_SUBTEXTO
        )

        pantalla.blit(
            indicador,
            (
                config.ANCHO // 2
                - indicador.get_width() // 2,
                config.ALTO - 92
            )
        )

    # ---------------------------------------------------------
    # DIBUJO FICHA INDIVIDUAL
    # ---------------------------------------------------------

    def _dibujar_ficha(self, pantalla):
        personaje = self.personaje_seleccionado

        centrar_texto(
            pantalla,
            self.fuente_titulo,
            "EXPEDIENTE DEL PARTICIPANTE",
            23,
            COLOR_TEXTO
        )

        panel = pygame.Rect(
            55,
            88,
            config.ANCHO - 110,
            420
        )

        dibujar_panel(
            pantalla,
            panel,
            relleno=COLOR_PANEL,
            borde=COLOR_BORDE,
            radio=18
        )

        # Foto grande
        foto_rect = pygame.Rect(
            panel.x + 25,
            panel.y + 28,
            225,
            300
        )

        self._dibujar_foto(
            pantalla,
            foto_rect,
            personaje
        )

        # Nombre
        nombre = self._nombre_corto(
            personaje["nombre"]
        )

        nombre_surface = (
            self.fuente_nombre_ficha.render(
                nombre,
                True,
                COLOR_ACENTO
            )
        )

        pantalla.blit(
            nombre_surface,
            (
                panel.x + 280,
                panel.y + 35
            )
        )

        etiqueta = self.fuente_chica.render(
            "PERFIL DEL PARTICIPANTE",
            True,
            COLOR_SUBTEXTO
        )

        pantalla.blit(
            etiqueta,
            (
                panel.x + 282,
                panel.y + 80
            )
        )

        # Línea divisoria
        pygame.draw.line(
            pantalla,
            COLOR_BORDE,
            (
                panel.x + 280,
                panel.y + 112
            ),
            (
                panel.right - 25,
                panel.y + 112
            ),
            2
        )

        # Narrativa
        narrativa = self._crear_narrativa(
            personaje
        )

        rect_texto = pygame.Rect(
            panel.x + 280,
            panel.y + 135,
            panel.width - 315,
            235
        )

        self._dibujar_parrafo(
            pantalla,
            narrativa,
            rect_texto,
            COLOR_TEXTO
        )

        # Etiqueta confidencial
        confidencial = self.fuente_chica.render(
            "ARCHIVO CLASIFICADO · SAPÓMETRO",
            True,
            COLOR_ACENTO
        )

        pantalla.blit(
            confidencial,
            (
                foto_rect.centerx
                - confidencial.get_width() // 2,
                panel.bottom - 47
            )
        )

        dibujar_boton(
            pantalla,
            self.btn_volver_ficha,
            self.fuente_btn,
            "VOLVER A LA GALERÍA",
            fondo=COLOR_PANEL,
            borde=COLOR_ACENTO
        )

    # ---------------------------------------------------------
    # DIBUJO PRINCIPAL
    # ---------------------------------------------------------

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        if self.personaje_seleccionado is None:
            self._dibujar_galeria(pantalla)
        else:
            self._dibujar_ficha(pantalla)