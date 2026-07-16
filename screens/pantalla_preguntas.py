import pygame
import os
import config

# Importamos las dos funciones que necesitas de tu script
from core.generar_arbol_manual import construir_arbol_datos, cargar_personas

class PantallaPreguntas:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_pregunta = pygame.font.SysFont(None, 48)
        self.fuente_btn = pygame.font.SysFont(None, 40)
        
        self.btn_si = pygame.Rect(200, 400, 150, 60)
        self.btn_no = pygame.Rect(450, 400, 150, 60)
        
        # 1. Calculamos la ruta absoluta de forma dinámica
        # Esto busca la carpeta del proyecto y entra a "data" de forma segura
        ruta_script = os.path.abspath(__file__) # Dónde está este archivo
        ruta_proyecto = os.path.dirname(os.path.dirname(ruta_script)) # Sube 2 niveles a la raíz
        self.ruta_archivo = os.path.join(ruta_proyecto, "data", "Formulario_proyecto_eda__respuestas__editado.csv")
        
        # Nombre exacto de tu archivo
        
        # 2. Cargamos el archivo CSV usando tu función
        lista_participantes = cargar_personas(self.ruta_archivo)
        
        # 3. Inicializamos el árbol pasándole los datos cargados
        self.nodo_actual = construir_arbol_datos(lista_participantes, 0)
        self.preguntas_arbol = 0
        
    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.btn_si.collidepoint(evento.pos):
                self.preguntas_arbol += 1
                self.nodo_actual = self.nodo_actual["si"] 
                self.verificar_estado()
                
            elif self.btn_no.collidepoint(evento.pos):
                self.preguntas_arbol += 1
                self.nodo_actual = self.nodo_actual["no"]
                self.verificar_estado()

    def verificar_estado(self):
        # Tu script devuelve {"tipo": "hoja", "nombre": "..."} cuando queda 1 persona
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
            
        # Tu script devuelve {"tipo": "grupo", "nombres": [...]} cuando hay empate
        elif self.nodo_actual.get("tipo") == "grupo":
            pantalla_grafo = self.gestor.pantallas["grafo"]
            pantalla_grafo.cargar_candidatos(self.nodo_actual["nombres"], self.preguntas_arbol)
            self.gestor.cambiar_a("transicion")

    def actualizar(self):
        pass

    def reiniciar(self):
        lista_participantes = cargar_personas(self.ruta_archivo)
        self.nodo_actual = construir_arbol_datos(lista_participantes, 0)
        self.preguntas_arbol = 0

    def dibujar(self, pantalla):
        pantalla.fill(config.NEGRO)

        # Muestra la pregunta real leyendo la clave del diccionario
        pregunta = str(self.nodo_actual.get("pregunta", ""))
        texto_pregunta = self.fuente_pregunta.render(pregunta, True, config.BLANCO)
        pantalla.blit(texto_pregunta, (config.ANCHO // 2 - texto_pregunta.get_width() // 2, 200))

        # Dibujar botones
        pygame.draw.rect(pantalla, config.NARANJA, self.btn_si)
        texto_si = self.fuente_btn.render("SÍ", True, config.NEGRO)
        pantalla.blit(texto_si, (self.btn_si.x + 55, self.btn_si.y + 15))

        pygame.draw.rect(pantalla, config.BLANCO, self.btn_no)
        texto_no = self.fuente_btn.render("NO", True, config.NEGRO)
        pantalla.blit(texto_no, (self.btn_no.x + 50, self.btn_no.y + 15))