# screens/pantalla_participantes.py

import os
import unicodedata

import pygame
import config
from core.generar_arbol_manual import PREGUNTAS, cargar_personas
from ui.estilo import COLOR_ACENTO, COLOR_BORDE, COLOR_PANEL, COLOR_SUBTEXTO, COLOR_TEXTO, dibujar_boton, dibujar_fondo_tecnologico, dibujar_panel, centrar_texto


class PantallaParticipantes:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_titulo = pygame.font.SysFont("Segoe UI", 50, bold=True)
        self.fuente_subtitulo = pygame.font.SysFont("Segoe UI", 22)
        self.fuente_texto = pygame.font.SysFont("Segoe UI", 24)
        self.fuente_texto_grande = pygame.font.SysFont("Segoe UI", 28, bold=True)
        self.fuente_btn = pygame.font.SysFont("Segoe UI", 24, bold=True)
        self.fuente_chica = pygame.font.SysFont("Segoe UI", 18)

        self.btn_volver = pygame.Rect(35, 530, 150, 42)
        self.btn_prev = pygame.Rect(220, 530, 130, 42)
        self.btn_next = pygame.Rect(450, 530, 130, 42)

        ruta_script = os.path.abspath(__file__)
        ruta_proyecto = os.path.dirname(os.path.dirname(ruta_script))
        self.ruta_imagenes = os.path.join(ruta_proyecto, "assets", "images", "imagenes")
        self.ruta_csv = os.path.join(ruta_proyecto, "data", "Formulario_proyecto_eda__respuestas__editado.csv")
        self._cache_imagenes = {}

        self.personajes = self._cargar_personajes()
        self.personaje_seleccionado = None
        self.ruta_seleccionada = []
        self.pagina_actual = 0
        self.personajes_por_pagina = 9
        self.rects_personajes = []

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.personaje_seleccionado is not None:
                if self.btn_volver.collidepoint(evento.pos):
                    self.personaje_seleccionado = None
                    self.ruta_seleccionada = []
                return

            if self.btn_prev.collidepoint(evento.pos) and self.pagina_actual > 0:
                self.pagina_actual -= 1
                return

            if self.btn_next.collidepoint(evento.pos) and self._hay_siguiente_pagina():
                self.pagina_actual += 1
                return

            if self.btn_volver.collidepoint(evento.pos):
                self.gestor.cambiar_a("inicio")
                return

            for indice, rect in self.rects_personajes:
                if rect.collidepoint(evento.pos):
                    self.personaje_seleccionado = self.personajes[indice]
                    self.ruta_seleccionada = self._construir_ruta_personaje(self.personaje_seleccionado)
                    break

    def actualizar(self):
        self.lista_lista = True

    def _normalizar_texto(self, texto):
        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(caracter for caracter in texto if unicodedata.category(caracter) != "Mn")
        return "".join(caracter.lower() for caracter in texto if caracter.isalnum())

    def _cargar_imagen_personaje(self, nombre):
        nombre_normalizado = self._normalizar_texto(nombre)
        if not nombre_normalizado:
            return None

        candidatos = [nombre_normalizado]
        partes = str(nombre).split()
        if partes:
            candidatos.insert(0, self._normalizar_texto(partes[0]))

        for candidato in candidatos:
            for extension in (".png", ".jpg", ".jpeg"):
                ruta_imagen = os.path.join(self.ruta_imagenes, f"im{candidato}{extension}")
                if ruta_imagen in self._cache_imagenes:
                    return self._cache_imagenes[ruta_imagen]
                if os.path.exists(ruta_imagen):
                    imagen = pygame.image.load(ruta_imagen).convert_alpha()
                    self._cache_imagenes[ruta_imagen] = imagen
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
                "imagen": self._cargar_imagen_personaje(nombre),
            })
        return personajes

    def _hay_siguiente_pagina(self):
        inicio = self.pagina_actual * self.personajes_por_pagina
        return inicio + self.personajes_por_pagina < len(self.personajes)

    def _formatear_respuesta(self, valor):
        return "Sí" if str(valor).strip().lower() == "si" else "No"

    def _nombre_corto(self, nombre):
        partes = str(nombre).strip().split()
        return partes[0] if partes else str(nombre).strip()

    def _construir_ruta_personaje(self, personaje):
        restantes = self.personajes[:]
        ruta = []
        respuestas = personaje["datos"]

        for columna, etiqueta in PREGUNTAS:
            respuestas_restantes = {p["datos"].get(columna, "") for p in restantes}
            if len(respuestas_restantes) <= 1:
                continue

            valor = respuestas.get(columna, "")
            ruta.append((etiqueta, self._formatear_respuesta(valor)))
            restantes = [p for p in restantes if p["datos"].get(columna, "") == valor]

            if len(restantes) == 1:
                break

        if len(restantes) > 1:
            nombres_restantes = ", ".join(p["nombre"] for p in restantes)
            ruta.append(("Grafo", f"Candidatos finales: {nombres_restantes}"))

        return ruta

    def _dibujar_foto(self, pantalla, rect, personaje):
        dibujar_panel(pantalla, rect, relleno=COLOR_PANEL, borde=COLOR_BORDE, radio=10)
        imagen = personaje["imagen"]
        if imagen is not None:
            imagen = pygame.transform.smoothscale(imagen, (rect.w - 4, rect.h - 4))
            pantalla.blit(imagen, (rect.x + 2, rect.y + 2))
        else:
            iniciales = "".join(parte[0] for parte in personaje["nombre"].split()[:2]).upper()
            texto = self.fuente_texto_grande.render(iniciales, True, COLOR_ACENTO)
            pantalla.blit(texto, (rect.centerx - texto.get_width() // 2, rect.centery - texto.get_height() // 2))

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        if self.personaje_seleccionado is None:
            centrar_texto(pantalla, self.fuente_titulo, "CONOCE A LOS PARTICIPANTES", 34, COLOR_TEXTO)
            centrar_texto(pantalla, self.fuente_subtitulo, "Toca una ficha para ver la ruta que te lleva a ese personaje.", 84, COLOR_SUBTEXTO)

            inicio = self.pagina_actual * self.personajes_por_pagina
            fin = min(inicio + self.personajes_por_pagina, len(self.personajes))
            visibles = self.personajes[inicio:fin]

            self.rects_personajes = []
            origen_x = 70
            origen_y = 125
            ancho = 210
            alto = 118
            espacio_x = 225
            espacio_y = 138

            for indice_local, personaje in enumerate(visibles):
                fila = indice_local // 3
                col = indice_local % 3
                x = origen_x + col * espacio_x
                y = origen_y + fila * espacio_y
                rect = pygame.Rect(x, y, ancho, alto)
                self.rects_personajes.append((inicio + indice_local, rect))

                dibujar_panel(pantalla, rect, relleno=COLOR_PANEL, borde=COLOR_BORDE, radio=14)
                foto_rect = pygame.Rect(x + 12, y + 10, 56, 56)
                self._dibujar_foto(pantalla, foto_rect, personaje)

                nombre_surface = self.fuente_texto.render(self._nombre_corto(personaje["nombre"]), True, COLOR_TEXTO)
                pantalla.blit(nombre_surface, (x + 76, y + 18))

                pista = self.fuente_chica.render("Clic para abrir ficha", True, COLOR_SUBTEXTO)
                pantalla.blit(pista, (x + 76, y + 62))

            dibujar_boton(pantalla, self.btn_volver, self.fuente_btn, "VOLVER", fondo=COLOR_PANEL, borde=COLOR_BORDE)
            dibujar_boton(pantalla, self.btn_prev, self.fuente_btn, "ANTERIOR", fondo=COLOR_PANEL, borde=COLOR_BORDE if self.pagina_actual > 0 else COLOR_SUBTEXTO)
            dibujar_boton(pantalla, self.btn_next, self.fuente_btn, "SIGUIENTE", fondo=COLOR_PANEL, borde=COLOR_BORDE if self._hay_siguiente_pagina() else COLOR_SUBTEXTO)

            paginas_total = max(1, (len(self.personajes) + self.personajes_por_pagina - 1) // self.personajes_por_pagina)
            indicador = self.fuente_chica.render(f"Página {self.pagina_actual + 1} de {paginas_total}", True, COLOR_SUBTEXTO)
            pantalla.blit(indicador, (config.ANCHO // 2 - indicador.get_width() // 2, 502))
            return

        personaje = self.personaje_seleccionado
        centrar_texto(pantalla, self.fuente_titulo, "FICHA DEL PERSONAJE", 34, COLOR_TEXTO)

        panel = pygame.Rect(55, 100, 690, 380)
        dibujar_panel(pantalla, panel, relleno=COLOR_PANEL, borde=COLOR_BORDE, radio=18)

        foto_rect = pygame.Rect(80, 145, 165, 165)
        self._dibujar_foto(pantalla, foto_rect, personaje)

        nombre_surface = self.fuente_texto_grande.render(self._nombre_corto(personaje["nombre"]), True, COLOR_ACENTO)
        pantalla.blit(nombre_surface, (270, 145))

        ruta_title = self.fuente_texto.render("Camino de respuesta", True, COLOR_TEXTO)
        pantalla.blit(ruta_title, (270, 192))

        y = 228
        if self.ruta_seleccionada:
            for indice, (pregunta, respuesta) in enumerate(self.ruta_seleccionada[:7], start=1):
                linea = self.fuente_chica.render(f"{indice}. {pregunta} -> {respuesta}", True, COLOR_SUBTEXTO)
                pantalla.blit(linea, (270, y))
                y += 28
        else:
            linea = self.fuente_chica.render("No se pudo construir un camino único.", True, COLOR_SUBTEXTO)
            pantalla.blit(linea, (270, y))

        estado = self.fuente_chica.render(
            "Llega al grafo" if self.ruta_seleccionada and self.ruta_seleccionada[-1][0] == "Grafo" else "Llega directo en el árbol",
            True,
            COLOR_TEXTO,
        )
        pantalla.blit(estado, (270, 435))

        dibujar_boton(pantalla, self.btn_volver, self.fuente_btn, "VOLVER", fondo=COLOR_PANEL, borde=COLOR_BORDE)