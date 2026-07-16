import pygame
import os
import config
from ui.estilo import COLOR_ACENTO, COLOR_BORDE, COLOR_SUBTEXTO, COLOR_TEXTO, dibujar_boton, dibujar_fondo_tecnologico, dibujar_panel, centrar_texto

# Importamos las dos funciones que necesitas de tu script
from core.generar_arbol_manual import construir_arbol_datos, cargar_personas

class PantallaPreguntas:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_titulo = pygame.font.SysFont("Segoe UI", 46, bold=True)
        self.fuente_pregunta = pygame.font.SysFont("Segoe UI", 38, bold=True)
        self.fuente_btn = pygame.font.SysFont("Segoe UI", 28, bold=True)
        
        self.btn_si = pygame.Rect(200, 420, 180, 56)
        self.btn_no = pygame.Rect(420, 420, 180, 56)
        
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
        dibujar_fondo_tecnologico(pantalla)

        centrar_texto(pantalla, self.fuente_titulo, "ANÁLISIS DEL EXPEDIENTE", 60, COLOR_TEXTO)
        panel = pygame.Rect(70, 150, 660, 185)
        dibujar_panel(pantalla, panel, relleno=(12, 42, 68), borde=COLOR_BORDE, radio=16)

        # Muestra la pregunta real leyendo la clave del diccionario
        pregunta = str(self.nodo_actual.get("pregunta", ""))
        texto_pregunta = self.fuente_pregunta.render(pregunta, True, COLOR_TEXTO)
        pantalla.blit(texto_pregunta, (config.ANCHO // 2 - texto_pregunta.get_width() // 2, 215))

        centrar_texto(pantalla, self.fuente_pregunta, f"Pregunta del árbol #{self.preguntas_arbol + 1}", 170, COLOR_ACENTO)

        # Dibujar botones
        dibujar_boton(pantalla, self.btn_si, self.fuente_btn, "SÍ", fondo=(12, 42, 68), borde=COLOR_ACENTO)
        dibujar_boton(pantalla, self.btn_no, self.fuente_btn, "NO", fondo=(12, 42, 68), borde=COLOR_BORDE)