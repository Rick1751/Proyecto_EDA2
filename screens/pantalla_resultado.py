import pygame
import os
import unicodedata
import config
from ui.estilo import COLOR_ACENTO, COLOR_BORDE, COLOR_SUBTEXTO, COLOR_TEXTO, dibujar_boton, dibujar_fondo_tecnologico, dibujar_panel, centrar_texto

class PantallaResultado:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_grande = pygame.font.SysFont("Segoe UI", 50, bold=True)
        self.fuente_texto = pygame.font.SysFont("Segoe UI", 28)
        self.fuente_btn = pygame.font.SysFont("Segoe UI", 24, bold=True)
        
        self.btn_jugar = pygame.Rect(180, 505, 230, 52)
        self.btn_menu = pygame.Rect(390, 505, 230, 52)
        
        self.personaje_adivinado = ""
        self.metodo_usado = ""
        self.preguntas_arbol = 0
        self.preguntas_grafo = 0
        self.entro_grafo = False
        self.imagen_personaje = None

        ruta_script = os.path.abspath(__file__)
        ruta_proyecto = os.path.dirname(os.path.dirname(ruta_script))
        self.ruta_imagenes = os.path.join(ruta_proyecto, "assets", "images", "imagenes")
        self._cache_imagenes = {}

    def configurar_victoria(self, nombre, metodo, preguntas_arbol=0, preguntas_grafo=0, entro_grafo=False):
        self.personaje_adivinado = nombre
        self.metodo_usado = metodo
        self.preguntas_arbol = preguntas_arbol
        self.preguntas_grafo = preguntas_grafo
        self.entro_grafo = entro_grafo
        self.imagen_personaje = self._cargar_imagen_personaje(nombre)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
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
        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(caracter for caracter in texto if unicodedata.category(caracter) != "Mn")
        return "".join(caracter.lower() for caracter in texto if caracter.isalnum())

    def _cargar_imagen_personaje(self, nombre):
        nombre_limpio = self._normalizar_texto(nombre)
        if not nombre_limpio:
            return None

        candidatos = []
        nombre_original = " ".join(str(nombre).split())
        if nombre_original:
            primer_nombre = nombre_original.split()[0]
            candidatos.append(self._normalizar_texto(primer_nombre))

        candidatos.append(nombre_limpio)
        candidatos = [candidato for candidato in candidatos if candidato]

        extensiones = [".png", ".jpg", ".jpeg"]
        for candidato in candidatos:
            for extension in extensiones:
                ruta_imagen = os.path.join(self.ruta_imagenes, f"im{candidato}{extension}")
                if ruta_imagen in self._cache_imagenes:
                    return self._cache_imagenes[ruta_imagen]
                if os.path.exists(ruta_imagen):
                    imagen = pygame.image.load(ruta_imagen).convert_alpha()
                    self._cache_imagenes[ruta_imagen] = imagen
                    return imagen

        return None

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        panel = pygame.Rect(60, 170, 680, 290)
        dibujar_panel(pantalla, panel, relleno=(12, 42, 68), borde=COLOR_BORDE, radio=16)

        caja_foto = pygame.Rect(config.ANCHO - 175, 25, 140, 140)
        dibujar_panel(pantalla, caja_foto, relleno=(12, 42, 68), borde=COLOR_BORDE, radio=14)
        if self.imagen_personaje is not None:
            imagen = pygame.transform.smoothscale(self.imagen_personaje, (136, 136))
            pantalla.blit(imagen, (caja_foto.x + 2, caja_foto.y + 2))
        else:
            texto_foto = self.fuente_texto.render("Sin foto", True, COLOR_SUBTEXTO)
            pantalla.blit(texto_foto, (caja_foto.x + 18, caja_foto.y + 55))

        # Nombre real
        centrar_texto(pantalla, self.fuente_grande, f"¡Es {self.personaje_adivinado}!", 215, COLOR_ACENTO)

        # Método real
        centrar_texto(pantalla, self.fuente_texto, f"Método utilizado: {self.metodo_usado}", 280, COLOR_TEXTO)
        
        centrar_texto(pantalla, self.fuente_texto, f"Preguntas en el árbol: {self.preguntas_arbol}", 320, COLOR_SUBTEXTO)

        centrar_texto(pantalla, self.fuente_texto, f"Preguntas en el grafo: {self.preguntas_grafo}", 358, COLOR_SUBTEXTO)

        centrar_texto(pantalla, self.fuente_texto, f"Entró al grafo: {'Sí' if self.entro_grafo else 'No'}", 396, COLOR_TEXTO)

        dibujar_boton(pantalla, self.btn_jugar, self.fuente_btn, "JUGAR OTRA VEZ", fondo=(12, 42, 68), borde=COLOR_ACENTO)

        dibujar_boton(pantalla, self.btn_menu, self.fuente_btn, "VOLVER AL MENÚ", fondo=(12, 42, 68), borde=COLOR_BORDE)