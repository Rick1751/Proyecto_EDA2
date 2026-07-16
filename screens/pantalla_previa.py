# screens/pantalla_previa.py

import pygame
import config
from ui.estilo import COLOR_ACENTO, COLOR_BORDE, COLOR_SUBTEXTO, COLOR_TEXTO, dibujar_boton, dibujar_fondo_tecnologico, dibujar_panel, centrar_texto

class PantallaPrevia:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_titulo = pygame.font.SysFont("Segoe UI", 48, bold=True)
        self.fuente_texto = pygame.font.SysFont("Segoe UI", 30)
        self.fuente_btn = pygame.font.SysFont("Segoe UI", 28, bold=True)
        
        # Botón centrado
        self.btn_comenzar = pygame.Rect(config.ANCHO // 2 - 170, 430, 340, 56)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.btn_comenzar.collidepoint(evento.pos):
                self.gestor.pantallas["preguntas"].reiniciar()
                self.gestor.pantallas["grafo"].reiniciar()
                self.gestor.pantallas["resultado"].reiniciar()
                self.gestor.cambiar_a("preguntas")

    def actualizar(self):
        self.esperando_jugador = True

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        centrar_texto(pantalla, self.fuente_titulo, "PREPARACIÓN DEL EXPEDIENTE", 70, COLOR_TEXTO)
        centrar_texto(pantalla, self.fuente_texto, "Antes de continuar, piensa en uno de los participantes.", 125, COLOR_SUBTEXTO)

        panel = pygame.Rect(90, 185, 620, 185)
        dibujar_panel(pantalla, panel, relleno=(12, 42, 68), borde=COLOR_BORDE, radio=16)

        # Instrucciones
        linea1 = self.fuente_texto.render("No cambies de persona durante el juego.", True, COLOR_TEXTO)
        linea2 = self.fuente_texto.render("El sistema analizará primero el árbol y luego el grafo si hace falta.", True, COLOR_ACENTO)

        pantalla.blit(linea1, (config.ANCHO // 2 - linea1.get_width() // 2, 235))
        pantalla.blit(linea2, (config.ANCHO // 2 - linea2.get_width() // 2, 285))

        # Botón Comenzar
        dibujar_boton(pantalla, self.btn_comenzar, self.fuente_btn, "COMENZAR PARTIDA", fondo=(12, 42, 68), borde=COLOR_ACENTO)