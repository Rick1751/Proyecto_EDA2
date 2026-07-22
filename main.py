# main.py

from pathlib import Path
import sys
import atexit
import logging
import multiprocessing


import pygame

import config
from core.multiprocesamiento import obtener_manager, limpiar_manager
from screens.gestor_pantallas import GestorPantallas
from screens.pantalla_acerca_de import PantallaAcercaDe
from screens.pantalla_grafo import PantallaGrafo
from screens.pantalla_inicio import PantallaInicio
from screens.pantalla_participantes import PantallaParticipantes
from screens.pantalla_preguntas import PantallaPreguntas
from screens.pantalla_previa import PantallaPrevia
from screens.pantalla_resultado import PantallaResultado
from screens.pantalla_transicion import PantallaTransicion

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



def iniciar_musica_fondo():
    try:
        pygame.mixer.init()
    except pygame.error:
        return

    ruta_base = Path(__file__).resolve().parent / Path(config.MUSICA_FONDO)
    rutas_posibles = [
        ruta_base,
        ruta_base.with_suffix(".ogg"),
        ruta_base.with_suffix(".wav"),
        ruta_base.with_suffix(".mp3"),
    ]

    for ruta_musica in rutas_posibles:
        if not ruta_musica.exists():
            continue

        try:
            pygame.mixer.music.load(str(ruta_musica))
            pygame.mixer.music.set_volume(0.35)
            pygame.mixer.music.play(-1)
            return
        except pygame.error:
            continue

    print("No se pudo cargar la musica de fondo.")

def main():
    # Inicializar manager de multiprocesamiento
    manager = obtener_manager()
    logger.info("Iniciando aplicación con multiprocesamiento")
    
    # Registrar limpieza al salir
    atexit.register(limpiar_manager)
    
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    iniciar_musica_fondo()
    pantalla = pygame.display.set_mode((config.ANCHO, config.ALTO))
    pygame.display.set_caption(config.TITULO)
    reloj = pygame.time.Clock()

    # --------------------------------------------------
    # GESTOR DE PANTALLAS
    # --------------------------------------------------

    gestor = GestorPantallas()

    # --------------------------------------------------
    # REGISTRO DE PANTALLAS
    # --------------------------------------------------

    gestor.registrar_pantalla(
        "inicio",
        PantallaInicio(gestor)
    )

    gestor.registrar_pantalla(
        "participantes",
        PantallaParticipantes(gestor)
    )

    gestor.registrar_pantalla(
        "acerca_de",
        PantallaAcercaDe(gestor)
    )

    gestor.registrar_pantalla(
        "previa",
        PantallaPrevia(gestor)
    )

    gestor.registrar_pantalla(
        "transicion",
        PantallaTransicion(gestor)
    )

    gestor.registrar_pantalla(
        "preguntas",
        PantallaPreguntas(gestor)
    )

    gestor.registrar_pantalla(
        "grafo",
        PantallaGrafo(gestor)
    )

    gestor.registrar_pantalla(
        "resultado",
        PantallaResultado(gestor)
    )

    # Primera pantalla sin animación
    gestor.cambiar_a(
        "inicio",
        inmediato=True
    )

    ejecutando = True

    # --------------------------------------------------
    # BUCLE PRINCIPAL
    # --------------------------------------------------

    while ejecutando:
        # Tiempo transcurrido desde el frame anterior,
        # expresado en segundos.
        delta_tiempo = (
            reloj.tick(config.FPS) / 1000.0
        )

        pantalla_activa = gestor.obtener_activa()

        # ----------------------------------------------
        # 1. EVENTOS
        # ----------------------------------------------

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                continue

            # Durante el fade se bloquean los clics
            # para evitar cambiar varias veces de pantalla.
            if gestor.esta_transicionando():
                continue

            if pantalla_activa is not None:
                pantalla_activa.manejar_evento(
                    evento
                )

        # ----------------------------------------------
        # 2. ACTUALIZACIÓN
        # ----------------------------------------------

        pantalla_activa = gestor.obtener_activa()

        if pantalla_activa is not None:
            pantalla_activa.actualizar()

        gestor.actualizar_transicion(
            delta_tiempo
        )

        # Después de actualizar la transición,
        # la pantalla activa puede haber cambiado.
        pantalla_activa = gestor.obtener_activa()

        # ----------------------------------------------
        # 3. DIBUJO
        # ----------------------------------------------

        if pantalla_activa is not None:
            pantalla_activa.dibujar(
                pantalla
            )

        else:
            pantalla.fill(config.NEGRO)

            fuente = pygame.font.SysFont(
                None,
                48
            )

            texto = fuente.render(
                "Pantalla en construcción...",
                True,
                config.BLANCO
            )

            pantalla.blit(
                texto,
                (
                    config.ANCHO // 2
                    - texto.get_width() // 2,
                    config.ALTO // 2
                    - texto.get_height() // 2
                )
            )

        # Capa negra del fade.
        # Debe dibujarse después de la pantalla activa.
        gestor.dibujar_transicion(
            pantalla
        )
        pygame.display.flip()

    pygame.quit()
    limpiar_manager()
    logger.info("Aplicación cerrada correctamente")
    sys.exit()


if __name__ == "__main__":
    multiprocessing.freeze_support() 
    main()