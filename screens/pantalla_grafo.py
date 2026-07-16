import pygame
import config
from ui.estilo import COLOR_ACENTO, COLOR_BORDE, COLOR_SUBTEXTO, COLOR_TEXTO, dibujar_boton, dibujar_fondo_tecnologico, dibujar_panel, centrar_texto

class PantallaGrafo:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_titulo = pygame.font.SysFont("Segoe UI", 42, bold=True)
        self.fuente_pregunta = pygame.font.SysFont("Segoe UI", 34, bold=True)
        self.fuente_btn = pygame.font.SysFont("Segoe UI", 28, bold=True)
        self.fuente_mensaje = pygame.font.SysFont("Segoe UI", 28)
        
        self.btn_si = pygame.Rect(200, 445, 170, 56)
        self.btn_no = pygame.Rect(430, 445, 170, 56)
        self.btn_menu = pygame.Rect(config.ANCHO // 2 - 100, 480, 200, 50)
        
        self.candidatos_empatados = []
        self.indice_actual = 0
        self.candidato_actual = ""
        self.preguntas_arbol = 0
        self.preguntas_grafo = 0
        self.fallo_localizacion = False

    def cargar_candidatos(self, lista, preguntas_arbol=0):
        self.candidatos_empatados = lista
        self.indice_actual = 0
        self.candidato_actual = self.candidatos_empatados[self.indice_actual]
        self.preguntas_arbol = preguntas_arbol
        self.preguntas_grafo = 0
        self.fallo_localizacion = False

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.fallo_localizacion:
                if self.btn_menu.collidepoint(evento.pos):
                    self.gestor.cambiar_a("inicio")
                return

            if self.btn_si.collidepoint(evento.pos):
                self.preguntas_grafo += 1
                # Encontró al personaje
                pantalla_res = self.gestor.pantallas["resultado"]
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
                # Pasa al siguiente candidato de la lista
                self.indice_actual += 1
                if self.indice_actual < len(self.candidatos_empatados):
                    self.candidato_actual = self.candidatos_empatados[self.indice_actual]
                else:
                    # Si se acaban los candidatos, mostramos un cierre explícito
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

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        if self.fallo_localizacion:
            panel = pygame.Rect(70, 170, 660, 230)
            dibujar_panel(pantalla, panel, relleno=(12, 42, 68), borde=COLOR_BORDE, radio=16)
            centrar_texto(pantalla, self.fuente_titulo, "NO SE PUDO LOCALIZAR AL PERSONAJE", 190, COLOR_ACENTO)
            centrar_texto(pantalla, self.fuente_mensaje, "Se agotaron todos los candidatos del grafo.", 245, COLOR_TEXTO)
            centrar_texto(pantalla, self.fuente_mensaje, "Esto parece un intento inválido o una inconsistencia en los datos.", 285, COLOR_SUBTEXTO)

            dibujar_boton(pantalla, self.btn_menu, self.fuente_btn, "VOLVER AL MENÚ", fondo=(12, 42, 68), borde=COLOR_BORDE)
            return

        centrar_texto(pantalla, self.fuente_titulo, "FASE DE GRAFO (DFS)", 52, COLOR_TEXTO)
        panel = pygame.Rect(70, 120, 660, 280)
        dibujar_panel(pantalla, panel, relleno=(12, 42, 68), borde=COLOR_BORDE, radio=16)

        # Nodos visuales
        pygame.draw.circle(pantalla, COLOR_BORDE, (300, 250), 30, 2)
        pygame.draw.circle(pantalla, COLOR_ACENTO, (400, 250), 40, 4) 
        pygame.draw.circle(pantalla, COLOR_BORDE, (500, 250), 30, 2)
        pygame.draw.line(pantalla, COLOR_BORDE, (330, 250), (360, 250), 2)
        pygame.draw.line(pantalla, COLOR_BORDE, (440, 250), (470, 250), 2)

        # Pregunta dinámica
        pregunta = f"¿Tu personaje es {self.candidato_actual}?"
        texto_pregunta = self.fuente_pregunta.render(pregunta, True, COLOR_TEXTO)
        pantalla.blit(texto_pregunta, (config.ANCHO // 2 - texto_pregunta.get_width() // 2, 340))
        centrar_texto(pantalla, self.fuente_mensaje, f"Preguntas en grafo: {self.preguntas_grafo}", 392, COLOR_SUBTEXTO)

        dibujar_boton(pantalla, self.btn_si, self.fuente_btn, "SÍ", fondo=(12, 42, 68), borde=COLOR_ACENTO)
        dibujar_boton(pantalla, self.btn_no, self.fuente_btn, "NO", fondo=(12, 42, 68), borde=COLOR_BORDE)