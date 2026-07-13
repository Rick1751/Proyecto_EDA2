# main.py

import pygame
import sys
import config
from screens.gestor_pantallas import GestorPantallas
from screens.pantalla_inicio import PantallaInicio
from screens.pantalla_participantes import PantallaParticipantes
from screens.pantalla_acerca_de import PantallaAcercaDe
from screens.pantalla_previa import PantallaPrevia
from screens.pantalla_transicion import PantallaTransicion
from screens.pantalla_preguntas import PantallaPreguntas
from screens.pantalla_grafo import PantallaGrafo
from screens.pantalla_resultado import PantallaResultado

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((config.ANCHO, config.ALTO))
    pygame.display.set_caption(config.TITULO)
    reloj = pygame.time.Clock()

    # Inicializar el cerebro de las pantallas
    gestor = GestorPantallas()

    # Registrar la pantalla inicial (Iremos añadiendo las demás aquí)
    gestor.registrar_pantalla("inicio", PantallaInicio(gestor))
    gestor.registrar_pantalla("participantes", PantallaParticipantes(gestor))
    gestor.registrar_pantalla("acerca_de", PantallaAcercaDe(gestor))
    gestor.registrar_pantalla("previa", PantallaPrevia(gestor))
    gestor.registrar_pantalla("transicion", PantallaTransicion(gestor))
    # Arrancar en el menú
    gestor.registrar_pantalla("preguntas", PantallaPreguntas(gestor))
    gestor.registrar_pantalla("grafo", PantallaGrafo(gestor))
    gestor.registrar_pantalla("resultado", PantallaResultado(gestor))
    gestor.cambiar_a("inicio")

    ejecutando = True
    while ejecutando:
        pantalla_activa = gestor.obtener_activa()

        # 1. Manejo de Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            else:
                if pantalla_activa:
                    pantalla_activa.manejar_evento(evento)

        # 2. Actualización de Lógica
        if pantalla_activa:
            pantalla_activa.actualizar()

        # 3. Renderizado Visual
        if pantalla_activa:
            pantalla_activa.dibujar(pantalla)
        else:
            # Failsafe: Si el botón te lleva a una pantalla que aún no hemos creado, no explota, solo muestra negro
            pantalla.fill(config.NEGRO)
            fuente = pygame.font.SysFont(None, 48)
            texto = fuente.render("Pantalla en construcción...", True, config.BLANCO)
            pantalla.blit(texto, (config.ANCHO // 2 - texto.get_width() // 2, config.ALTO // 2))

        pygame.display.flip()
        reloj.tick(config.FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()