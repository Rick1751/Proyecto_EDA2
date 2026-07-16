import pygame
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
        self.preguntas_realizadas = 0

    def configurar_victoria(self, nombre, metodo, preguntas_realizadas=0):
        self.personaje_adivinado = nombre
        self.metodo_usado = metodo
        self.preguntas_realizadas = preguntas_realizadas

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
        self.preguntas_realizadas = 0

    def dibujar(self, pantalla):
        pantalla.fill(config.NEGRO)

        caja_foto = pygame.Rect(config.ANCHO // 2 - 75, 50, 150, 150)
        pygame.draw.rect(pantalla, config.BLANCO, caja_foto, 2)
        texto_foto = self.fuente_texto.render("[ FOTO ]", True, config.BLANCO)
        pantalla.blit(texto_foto, (caja_foto.x + 35, caja_foto.y + 65))

        # Nombre real
        texto_nombre = self.fuente_grande.render(f"¡Es {self.personaje_adivinado}!", True, config.NARANJA)
        pantalla.blit(texto_nombre, (config.ANCHO // 2 - texto_nombre.get_width() // 2, 230))

        # Método real
        texto_metodo = self.fuente_texto.render(f"Método utilizado: {self.metodo_usado}", True, config.BLANCO)
        pantalla.blit(texto_metodo, (config.ANCHO // 2 - texto_metodo.get_width() // 2, 320))
        
        texto_preguntas = self.fuente_texto.render(f"Preguntas realizadas: {self.preguntas_realizadas}", True, config.BLANCO)
        pantalla.blit(texto_preguntas, (config.ANCHO // 2 - texto_preguntas.get_width() // 2, 370))

        pygame.draw.rect(pantalla, config.BLANCO, self.btn_jugar)
        texto_btn_jugar = self.fuente_btn.render("JUGAR OTRA VEZ", True, config.NEGRO)
        pantalla.blit(texto_btn_jugar, (self.btn_jugar.x + 12, self.btn_jugar.y + 15))

        pygame.draw.rect(pantalla, config.BLANCO, self.btn_menu)
        texto_btn_menu = self.fuente_btn.render("VOLVER AL MENÚ", True, config.NEGRO)
        pantalla.blit(texto_btn_menu, (self.btn_menu.x + 15, self.btn_menu.y + 15))