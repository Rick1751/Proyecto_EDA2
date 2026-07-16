import pygame

import config


COLOR_FONDO_SUPERIOR = (5, 17, 31)
COLOR_FONDO_INFERIOR = (9, 28, 48)
COLOR_PANEL = (11, 38, 63)
COLOR_BORDE = (91, 186, 220)
COLOR_BORDE_SUAVE = (35, 96, 130)
COLOR_TEXTO = (232, 246, 255)
COLOR_SUBTEXTO = (146, 198, 223)
COLOR_ACENTO = (255, 171, 90)


def dibujar_fondo_tecnologico(pantalla):
    for y in range(config.ALTO):
        progreso = y / max(1, config.ALTO - 1)
        r = int(COLOR_FONDO_SUPERIOR[0] + (COLOR_FONDO_INFERIOR[0] - COLOR_FONDO_SUPERIOR[0]) * progreso)
        g = int(COLOR_FONDO_SUPERIOR[1] + (COLOR_FONDO_INFERIOR[1] - COLOR_FONDO_SUPERIOR[1]) * progreso)
        b = int(COLOR_FONDO_SUPERIOR[2] + (COLOR_FONDO_INFERIOR[2] - COLOR_FONDO_SUPERIOR[2]) * progreso)
        pygame.draw.line(pantalla, (r, g, b), (0, y), (config.ANCHO, y))

    pygame.draw.rect(pantalla, COLOR_BORDE_SUAVE, pygame.Rect(12, 12, config.ANCHO - 24, config.ALTO - 24), 1)
    for x in range(80, config.ANCHO, 80):
        pygame.draw.line(pantalla, (18, 52, 77), (x, 30), (x, config.ALTO - 30), 1)
    for y in range(70, config.ALTO, 70):
        pygame.draw.line(pantalla, (18, 52, 77), (30, y), (config.ANCHO - 30, y), 1)

    puntos = [(80, 70), (180, 110), (270, 80), (640, 90), (710, 180), (610, 240), (90, 240), (160, 370), (690, 380), (580, 500), (720, 530), (120, 520)]
    for x, y in puntos:
        pygame.draw.circle(pantalla, (97, 208, 255), (x, y), 1)
        pygame.draw.circle(pantalla, (97, 208, 255), (x, y), 3, 1)


def dibujar_panel(pantalla, rect, relleno=COLOR_PANEL, borde=COLOR_BORDE_SUAVE, radio=14):
    sombra = pygame.Rect(rect.x + 4, rect.y + 5, rect.w, rect.h)
    pygame.draw.rect(pantalla, (0, 0, 0), sombra, border_radius=radio)
    pygame.draw.rect(pantalla, relleno, rect, border_radius=radio)
    pygame.draw.rect(pantalla, borde, rect, 2, border_radius=radio)


def dibujar_boton(pantalla, rect, fuente, texto, color_texto=COLOR_TEXTO, fondo=COLOR_PANEL, borde=COLOR_BORDE, subtitulo=None, fuente_subtitulo=None):
    dibujar_panel(pantalla, rect, relleno=fondo, borde=borde, radio=14)
    tri_izq = [(rect.x + 10, rect.centery), (rect.x + 26, rect.y + 12), (rect.x + 26, rect.bottom - 12)]
    tri_der = [(rect.right - 10, rect.centery), (rect.right - 26, rect.y + 12), (rect.right - 26, rect.bottom - 12)]
    pygame.draw.polygon(pantalla, borde, tri_izq, 2)
    pygame.draw.polygon(pantalla, borde, tri_der, 2)

    texto_surface = fuente.render(texto, True, color_texto)
    pantalla.blit(texto_surface, (rect.centerx - texto_surface.get_width() // 2, rect.y + 8 if subtitulo else rect.centery - texto_surface.get_height() // 2 - 2))

    if subtitulo and fuente_subtitulo is not None:
        subtitulo_surface = fuente_subtitulo.render(subtitulo, True, COLOR_SUBTEXTO)
        pantalla.blit(subtitulo_surface, (rect.centerx - subtitulo_surface.get_width() // 2, rect.y + 34))


def centrar_texto(pantalla, fuente, texto, y, color=COLOR_TEXTO):
    surface = fuente.render(texto, True, color)
    pantalla.blit(surface, (config.ANCHO // 2 - surface.get_width() // 2, y))