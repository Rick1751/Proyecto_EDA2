# screens/pantalla_participantes.py

import pygame
import config
from ui.estilo import COLOR_ACENTO, COLOR_SUBTEXTO, COLOR_TEXTO, dibujar_boton, dibujar_fondo_tecnologico, dibujar_panel, centrar_texto

class PantallaParticipantes:
    def __init__(self, gestor):
        self.gestor = gestor
        self.fuente_titulo = pygame.font.SysFont("Segoe UI", 52, bold=True)
        self.fuente_subtitulo = pygame.font.SysFont("Segoe UI", 22)
        self.fuente_nombres = pygame.font.SysFont("Segoe UI", 28, bold=True)
        self.fuente_btn = pygame.font.SysFont("Segoe UI", 26, bold=True)
        
        # Lista de personajes de tu dataset
        self.nombres = ["Andrea", "Jesus", "Ricardo", "Emily", "Alexis", "Valeria", "Esteban", "Orlin", "Tabatha"]
        self.btn_volver = pygame.Rect(50, 500, 150, 45)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.btn_volver.collidepoint(evento.pos):
                self.gestor.cambiar_a("inicio")

    def actualizar(self):
        # Pantalla estática sin animación constante
        self.lista_lista = True

    def dibujar(self, pantalla):
        dibujar_fondo_tecnologico(pantalla)

        # Título
        centrar_texto(pantalla, self.fuente_titulo, "PERFILES DE PARTICIPANTES", 38, COLOR_TEXTO)
        centrar_texto(pantalla, self.fuente_subtitulo, "Expediente visual de los candidatos", 86, COLOR_SUBTEXTO)

        # Dibujar Grilla 3x3
        inicio_x = 70
        inicio_y = 140
        ancho_caja = 200
        alto_caja = 62
        espacio_x = 225
        espacio_y = 95

        for i, nombre in enumerate(self.nombres):
            fila = i // 3
            col = i % 3
            x = inicio_x + col * espacio_x
            y = inicio_y + fila * espacio_y
            
            caja = pygame.Rect(x, y, ancho_caja, alto_caja)
            dibujar_panel(pantalla, caja, relleno=(12, 42, 68), borde=COLOR_ACENTO, radio=12)
            
            # Texto del nombre centrado en la caja
            texto = self.fuente_nombres.render(nombre, True, COLOR_TEXTO)
            pantalla.blit(texto, (x + (ancho_caja - texto.get_width()) // 2, y + 18))

        # Botón Volver
        dibujar_boton(pantalla, self.btn_volver, self.fuente_btn, "VOLVER", fondo=(12, 42, 68), borde=COLOR_BORDE_SUAVE if 'COLOR_BORDE_SUAVE' in globals() else (35, 96, 130))