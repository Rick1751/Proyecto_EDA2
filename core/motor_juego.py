"""
motor_juego.py

Este archivo conecta la logica del arbol de decision (generar_arbol_manual.py)
con la interfaz grafica de Pygame.

La clase MotorJuego se encarga de:
    - Cargar los datos del CSV/Excel UNA sola vez al crear el motor.
    - Construir el arbol de preguntas EN MEMORIA (una estructura de
      diccionarios, ver construir_arbol_datos en generar_arbol_manual.py),
      en vez de una imagen, para poder recorrerlo pregunta por pregunta
      segun lo que responda el jugador con clics en Pygame.
    - Si el arbol llega a un grupo de personas indistinguibles, activa el
      "modo grafo" y recorre ese grafo con DFS, tambien pregunta por
      pregunta.
    - Llevar la cuenta de "en que parte del arbol/grafo estamos" para que
      las pantallas de Pygame sepan que texto mostrar en cada momento.

IMPORTANTE sobre bloqueos: cargar los datos y construir el arbol se hace
UNA sola vez, al crear el MotorJuego, y eso pasa ANTES de que arranque el
bucle principal de Pygame (el "while ejecutando" de main.py). Como el
archivo de datos es chico, esto toma una fraccion de segundo y no genera
ningun congelamiento perceptible en la ventana.
"""

import sys
import os

# Agregamos la carpeta "core" al path de Python para poder importar
# generar_arbol_manual.py como si fuera un modulo comun, sin depender de
# como se haya lanzado el programa (python main.py desde la raiz, desde
# un IDE, etc.)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import generar_arbol_manual as logica


# Estados posibles del motor de juego. Se usan strings simples (no Enum)
# para mantener el codigo facil de leer a nivel de estudiante.
ESTADO_PREGUNTA = "pregunta"
ESTADO_GRAFO = "grafo"
ESTADO_RESULTADO = "resultado"


class MotorJuego:
    """Guarda todo el estado del juego: el arbol completo, el grafo actual
    (si estamos en modo grafo) y el avance del jugador a traves de ambos."""

    def __init__(self, ruta_datos):
        # 1) Cargar personas desde el archivo (se hace una sola vez)
        self.personas = logica.cargar_personas(ruta_datos)

        # 2) Construir el arbol completo en memoria (estructura de datos).
        #    Esto reemplaza a construir_arbol() del script original, que
        #    dibujaba directamente sobre un objeto de graphviz.
        self.arbol = logica.construir_arbol_datos(self.personas, 0)

        # 3) Puntero al nodo actual del arbol (arrancamos en la raiz)
        self.nodo_actual = self.arbol

        # 4) Variables que solo se usan cuando estamos en "modo grafo"
        #    (grupo de candidatos indistinguibles), para el recorrido DFS
        self.grafo_actual = None        # dict con nombres + adyacencia del grupo
        self.pila_dfs = []              # pila del DFS (version iterativa)
        self.visitados_dfs = []         # nombres ya descartados/visitados
        self.candidato_grafo_actual = None  # de quien estamos preguntando ahora

        # 5) Resultado final del juego (nombre identificado)
        self.resultado = None

        # 6) Estado general: en que pantalla/modo estamos
        self.estado = ESTADO_PREGUNTA

    # ------------------------------------------------------------------
    # Modo pregunta: recorrido normal del arbol de decision
    # ------------------------------------------------------------------
    def obtener_pregunta_actual(self):
        """Devuelve el texto de la pregunta que hay que mostrar en pantalla."""
        if self.nodo_actual["tipo"] == "pregunta":
            return self.nodo_actual["pregunta"]
        return ""

    def responder(self, es_si):
        """Se llama cuando el jugador presiona el boton SI o NO en la
        pantalla de preguntas. Avanza el arbol segun la respuesta."""
        if self.nodo_actual["tipo"] != "pregunta":
            return  # por seguridad, no deberia llamarse en otro momento

        siguiente = self.nodo_actual["si"] if es_si else self.nodo_actual["no"]
        self.nodo_actual = siguiente
        self._revisar_nodo_actual()

    def _revisar_nodo_actual(self):
        """Revisa en que tipo de nodo quedamos despues de avanzar en el
        arbol, y actualiza el estado del motor (pregunta, grafo o
        resultado) para que main.py sepa a que pantalla cambiar."""
        tipo = self.nodo_actual["tipo"]

        if tipo == "pregunta":
            self.estado = ESTADO_PREGUNTA

        elif tipo == "hoja":
            self.resultado = self.nodo_actual["nombre"]
            self.estado = ESTADO_RESULTADO

        elif tipo == "grupo":
            # Llegamos a un grupo de personas indistinguibles: pasamos al
            # modo grafo y arrancamos el recorrido DFS
            self._iniciar_grafo(self.nodo_actual)

    # ------------------------------------------------------------------
    # Modo grafo: recorrido DFS de un grupo de candidatos indistinguibles
    # ------------------------------------------------------------------
    def _iniciar_grafo(self, nodo_grupo):
        self.grafo_actual = nodo_grupo
        self.visitados_dfs = []
        self.pila_dfs = [nodo_grupo["nombres"][0]]
        self.estado = ESTADO_GRAFO
        self._avanzar_dfs()

    def _avanzar_dfs(self):
        """Saca el siguiente candidato de la pila del DFS y lo deja listo
        para preguntarle al jugador ('Es <candidato>?'). Si ya solo queda
        un candidato sin descartar, se deduce directamente sin preguntar
        (misma idea que recorrer_grafo_dfs() en generar_arbol_manual.py)."""
        total = len(self.grafo_actual["nombres"])

        while self.pila_dfs:
            actual = self.pila_dfs.pop()
            if actual in self.visitados_dfs:
                continue
            self.visitados_dfs.append(actual)

            restantes = total - len(self.visitados_dfs)
            if restantes == 0:
                # No quedan mas candidatos por descartar: tiene que ser este
                self.resultado = actual
                self.estado = ESTADO_RESULTADO
                return

            self.candidato_grafo_actual = actual
            return  # nos detenemos aqui, esperando el clic del jugador

        # Si la pila se vacio sin poder identificar a nadie (no deberia
        # pasar con un grafo completo, pero lo cubrimos por seguridad):
        self.resultado = None
        self.estado = ESTADO_RESULTADO

    def responder_grafo(self, es_si):
        """Se llama cuando el jugador responde SI/NO a la pregunta
        '¿Eres <candidato>?' durante el recorrido del grafo."""
        if es_si:
            self.resultado = self.candidato_grafo_actual
            self.estado = ESTADO_RESULTADO
            return

        # Si respondio NO: agregamos los vecinos del candidato actual a la
        # pila (asi sigue el DFS) y avanzamos al siguiente candidato
        vecinos = self.grafo_actual["adyacencia"][self.candidato_grafo_actual]
        for vecino in vecinos:
            if vecino not in self.visitados_dfs:
                self.pila_dfs.append(vecino)

        self._avanzar_dfs()

    # ------------------------------------------------------------------
    # Reinicio del juego
    # ------------------------------------------------------------------
    def reiniciar(self):
        """Vuelve a poner el motor en la raiz del arbol, para poder jugar
        otra ronda sin tener que volver a cargar el archivo de datos."""
        self.nodo_actual = self.arbol
        self.grafo_actual = None
        self.pila_dfs = []
        self.visitados_dfs = []
        self.candidato_grafo_actual = None
        self.resultado = None
        self.estado = ESTADO_PREGUNTA
