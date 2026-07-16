import pygame
import os
import unicodedata
import config

class PantallaResultado:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_grande = pygame.font.SysFont(None, 60)
        self.fuente_texto = pygame.font.SysFont(None, 35)
        self.fuente_btn = pygame.font.SysFont(None, 30)
        
        self.btn_jugar = pygame.Rect(200, 500, 200, 50)
        self.btn_menu = pygame.Rect(420, 500, 200, 50)
        
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
        pantalla.fill(config.NEGRO)

        caja_foto = pygame.Rect(config.ANCHO - 175, 25, 140, 140)
        pygame.draw.rect(pantalla, config.BLANCO, caja_foto, 2)
        if self.imagen_personaje is not None:
            imagen = pygame.transform.smoothscale(self.imagen_personaje, (136, 136))
            pantalla.blit(imagen, (caja_foto.x + 2, caja_foto.y + 2))
        else:
            texto_foto = self.fuente_texto.render("Sin foto", True, config.BLANCO)
            pantalla.blit(texto_foto, (caja_foto.x + 18, caja_foto.y + 55))

        # Nombre real
        texto_nombre = self.fuente_grande.render(f"¡Es {self.personaje_adivinado}!", True, config.NARANJA)
        pantalla.blit(texto_nombre, (config.ANCHO // 2 - texto_nombre.get_width() // 2, 230))

        # Método real
        texto_metodo = self.fuente_texto.render(f"Método utilizado: {self.metodo_usado}", True, config.BLANCO)
        pantalla.blit(texto_metodo, (config.ANCHO // 2 - texto_metodo.get_width() // 2, 320))
        
        texto_arbol = self.fuente_texto.render(f"Preguntas en el árbol: {self.preguntas_arbol}", True, config.BLANCO)
        pantalla.blit(texto_arbol, (config.ANCHO // 2 - texto_arbol.get_width() // 2, 360))

        texto_grafo = self.fuente_texto.render(f"Preguntas en el grafo: {self.preguntas_grafo}", True, config.BLANCO)
        pantalla.blit(texto_grafo, (config.ANCHO // 2 - texto_grafo.get_width() // 2, 400))

        texto_grafo_usado = self.fuente_texto.render(
            f"Entró al grafo: {'Sí' if self.entro_grafo else 'No'}",
            True,
            config.BLANCO,
        )
        pantalla.blit(texto_grafo_usado, (config.ANCHO // 2 - texto_grafo_usado.get_width() // 2, 440))

        pygame.draw.rect(pantalla, config.BLANCO, self.btn_jugar)
        texto_btn_jugar = self.fuente_btn.render("JUGAR OTRA VEZ", True, config.NEGRO)
        pantalla.blit(texto_btn_jugar, (self.btn_jugar.x + 12, self.btn_jugar.y + 15))

        pygame.draw.rect(pantalla, config.BLANCO, self.btn_menu)
        texto_btn_menu = self.fuente_btn.render("VOLVER AL MENÚ", True, config.NEGRO)
        pantalla.blit(texto_btn_menu, (self.btn_menu.x + 15, self.btn_menu.y + 15))