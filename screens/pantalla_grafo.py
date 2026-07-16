import pygame
import config

class PantallaGrafo:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_titulo = pygame.font.SysFont(None, 35)
        self.fuente_pregunta = pygame.font.SysFont(None, 50)
        self.fuente_btn = pygame.font.SysFont(None, 40)
        
        self.btn_si = pygame.Rect(200, 450, 150, 60)
        self.btn_no = pygame.Rect(450, 450, 150, 60)
        
        self.candidatos_empatados = []
        self.indice_actual = 0
        self.candidato_actual = ""
        self.preguntas_arbol = 0
        self.preguntas_grafo = 0

    def cargar_candidatos(self, lista, preguntas_arbol=0):
        self.candidatos_empatados = lista
        self.indice_actual = 0
        self.candidato_actual = self.candidatos_empatados[self.indice_actual]
        self.preguntas_arbol = preguntas_arbol
        self.preguntas_grafo = 0

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
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
                    # Si se acaban los candidatos (failsafe)
                    self.gestor.cambiar_a("inicio")

    def actualizar(self):
        pass

    def reiniciar(self):
        self.candidatos_empatados = []
        self.indice_actual = 0
        self.candidato_actual = ""
        self.preguntas_arbol = 0
        self.preguntas_grafo = 0

    def dibujar(self, pantalla):
        pantalla.fill(config.NEGRO)

        titulo = self.fuente_titulo.render("FASE DE GRAFO (DFS)", True, config.NARANJA)
        pantalla.blit(titulo, (config.ANCHO // 2 - titulo.get_width() // 2, 50))

        # Nodos visuales
        pygame.draw.circle(pantalla, config.BLANCO, (300, 250), 30, 2)
        pygame.draw.circle(pantalla, config.NARANJA, (400, 250), 40, 4) 
        pygame.draw.circle(pantalla, config.BLANCO, (500, 250), 30, 2)
        pygame.draw.line(pantalla, config.BLANCO, (330, 250), (360, 250), 2)
        pygame.draw.line(pantalla, config.BLANCO, (440, 250), (470, 250), 2)

        # Pregunta dinámica
        pregunta = f"¿Tu personaje es {self.candidato_actual}?"
        texto_pregunta = self.fuente_pregunta.render(pregunta, True, config.BLANCO)
        pantalla.blit(texto_pregunta, (config.ANCHO // 2 - texto_pregunta.get_width() // 2, 350))

        pygame.draw.rect(pantalla, config.NARANJA, self.btn_si)
        texto_si = self.fuente_btn.render("SÍ", True, config.NEGRO)
        pantalla.blit(texto_si, (self.btn_si.x + 55, self.btn_si.y + 15))

        pygame.draw.rect(pantalla, config.BLANCO, self.btn_no)
        texto_no = self.fuente_btn.render("NO", True, config.NEGRO)
        pantalla.blit(texto_no, (self.btn_no.x + 50, self.btn_no.y + 15))