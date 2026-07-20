"""
generar_arbol_manual.py

Este archivo es la BASE MATEMATICA del proyecto (la logica original de
armado del arbol de decision "estilo Akinator"), con dos agregados para
poder conectarlo con la interfaz de Pygame:

  1) cargar_personas() ahora acepta tanto archivos .xlsx como .csv, para
     poder usar el CSV que vive dentro de la carpeta data/ del proyecto.

  2) Se agregaron dos funciones nuevas: construir_arbol_datos() y
     construir_grafo_datos(). Hacen EXACTAMENTE el mismo trabajo que
     construir_arbol() y crear_nodo_grupo_indistinguible(), pero en vez de
     dibujar directamente sobre un objeto graphviz.Digraph, devuelven una
     estructura de diccionarios de Python (el arbol "en memoria"). Esa es
     la version que usa core/motor_juego.py para poder recorrer el arbol
     pregunta por pregunta segun lo que responda el jugador en Pygame.

El resto del archivo (construir_arbol, crear_nodo_grupo_indistinguible,
recorrer_grafo_dfs, main) se deja tal cual estaba: sirve para, aparte del
juego, seguir pudiendo generar las imagenes arbol_akinator.png y
grafo_G1.png, etc. (por ejemplo para la sustentacion del proyecto).

El arbol sigue siendo COMPLETAMENTE MANUAL: el orden de las preguntas esta
fijo por el usuario (no se usa DecisionTreeClassifier, plot_tree,
export_graphviz ni sklearn.tree de ninguna forma).
"""

import os
import pandas as pd
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# graphviz es opcional: solo hace falta si se quiere generar las imagenes
# (arbol_akinator.png, grafo_G1.png, etc.) llamando a main(). El juego en
# Pygame NO necesita graphviz para funcionar, asi que si el paquete o el
# binario "dot" no estan instalados, el juego igual puede correr.
try:
    import graphviz
    GRAPHVIZ_DISPONIBLE = True
except ImportError:
    GRAPHVIZ_DISPONIBLE = False


# ---------------------------------------------------------------------------
# Configuracion
# ---------------------------------------------------------------------------

ARCHIVO_EXCEL = "Formulario_proyecto_eda__respuestas__editado.xlsx"
PERSONA_EXCLUIDA = "Emily Dayana"
ARCHIVO_SALIDA = "arbol_akinator"  # graphviz añade la extension .png

# Orden obligatorio de las preguntas (columna del Excel/CSV -> texto a mostrar)
PREGUNTAS = [
    ("Eres mujer?", "Eres mujer?"),
    ("Usas lentes?", "Usas lentes?"),
    ("Eres alto? (+1.70cm en hombres, +1,60cm en mujeres)", "Eres alto?"),
    ("Tienes el cabello largo? (3 dedos por debajo del hombro)", "Tienes el cabello largo?"),
    ("Tienes el cabello rizado?", "Tienes el cabello rizado?"),
    ("Tienes barba?", "Tienes barba?"),
    ("Eres de contextura delgada?", "Eres de contextura delgada?"),
    ("Usas gorra dentro de clase frecuentemente? ", "Usas gorra?"),
    ("Usas saco o hoddie en la universidad frecuentemente?", "Usas saco o hoodie?"),
    ("Eres foraneo?", "Eres foraneo?"),
    ("Sabes conducir?", "Sabes conducir?"),
    ("Vas al gimnasio a menudo ?(mínimo 3 veces por semana)", "Vas al gimnasio?"),
    ("Participas en el coro?", "Participas en el coro?"),
    ("Te gusta apostar ?", "Te gusta apostar?"),
    ("Participas frecuentemente en clase?", "Participas frecuentemente en clase?"),
    ("Te consideras una persona extrovertida?", "Te consideras extrovertido?"),
    ("Sueles llegar tarde a clases?", "Sueles llegar tarde?"),
    ("Te sientas normalmente en la parte delantera del aula?", "Te sientas adelante?"),
    ("Te sientas normalmente en la parte trasera del aula?", "Te sientas atras?"),
    ("¿La primera letra de su nombre está entre la A y la H? ", "Primera letra del nombre A-H?"),
    ("¿La primera letra de su apellido está entre la A y la M? ", "Primera letra del apellido A-M?"),
    ("¿Usa tablet para tomar apuntes? ", "Usa tablet?"),
]

COLUMNA_NOMBRE = "NOMBRES COMPLETOS"


# ---------------------------------------------------------------------------
# Carga y limpieza de datos
# ---------------------------------------------------------------------------

def cargar_personas(ruta_datos):
    """Lee el archivo de respuestas (acepta .xlsx o .csv), limpia nombres
    y respuestas, y elimina a la persona excluida. Devuelve una lista de
    diccionarios (uno por persona)."""

    extension = os.path.splitext(ruta_datos)[1].lower()
    if extension == ".csv":
        df = pd.read_csv(ruta_datos)
    else:
        df = pd.read_excel(ruta_datos)

    # Normalizar nombres de columnas (quitar espacios sobrantes al inicio/fin)
    df.columns = [str(c).strip() if not isinstance(c, str) else c.strip() for c in df.columns]

    personas = []
    for _, fila in df.iterrows():
        nombre_crudo = fila.get(COLUMNA_NOMBRE, "")
        if pd.isna(nombre_crudo):
            continue
        nombre = " ".join(str(nombre_crudo).split())  # colapsa espacios

        if PERSONA_EXCLUIDA.lower() in nombre.lower():
            continue

        persona = {"nombre": nombre}
        for col_excel, _etiqueta in PREGUNTAS:
            valor = fila.get(col_excel.strip(), fila.get(col_excel, ""))
            if pd.isna(valor):
                valor = ""
            valor = str(valor).strip().lower()
            persona[col_excel] = valor

        personas.append(persona)

    return personas


# ---------------------------------------------------------------------------
# Optimizacion: Procesamiento paralelo de personas
# ---------------------------------------------------------------------------

def _procesar_persona_worker(args):
    """Worker para procesamiento paralelo de personas.
    Función estática para poder ser serializada por multiprocessing."""
    
    fila_dict, columna_nombre, preguntas, persona_excluida = args
    
    nombre_crudo = fila_dict.get(columna_nombre, "")
    if pd.isna(nombre_crudo):
        return None
    
    nombre = " ".join(str(nombre_crudo).split())
    
    if persona_excluida.lower() in nombre.lower():
        return None
    
    persona = {"nombre": nombre}
    for col_excel, _etiqueta in preguntas:
        valor = fila_dict.get(col_excel.strip(), fila_dict.get(col_excel, ""))
        if pd.isna(valor):
            valor = ""
        valor = str(valor).strip().lower()
        persona[col_excel] = valor
    
    return persona


def cargar_personas_paralelo(ruta_datos, usar_multiprocesamiento=True):
    """Lee el archivo de respuestas usando multiprocesamiento si está disponible.
    
    Args:
        ruta_datos: ruta al archivo (CSV o XLSX)
        usar_multiprocesamiento: si False, usa el método secuencial
    
    Returns:
        lista de diccionarios con personas procesadas
    """
    
    extension = os.path.splitext(ruta_datos)[1].lower()
    if extension == ".csv":
        df = pd.read_csv(ruta_datos)
    else:
        df = pd.read_excel(ruta_datos)
    
    # Normalizar nombres de columnas
    df.columns = [str(c).strip() if not isinstance(c, str) else c.strip() for c in df.columns]
    
    if not usar_multiprocesamiento or len(df) < 20:
        # Para conjuntos pequeños, es más rápido secuencial
        return cargar_personas(ruta_datos)
    
    # Preparar argumentos para workers
    filas_dicts = [dict(fila) for _, fila in df.iterrows()]
    args_lista = [
        (fila_dict, COLUMNA_NOMBRE, PREGUNTAS, PERSONA_EXCLUIDA)
        for fila_dict in filas_dicts
    ]
    
    # Usar ThreadPoolExecutor (mejor para I/O, evita problemas de serialización)
    personas = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        resultados = executor.map(_procesar_persona_worker, args_lista)
        personas = [p for p in resultados if p is not None]
    
    logger.info(f"Cargadas {len(personas)} personas con multiprocesamiento")
    return personas


def pregunta_separa(personas, col_excel):
    """Devuelve True si la pregunta 'col_excel' divide a 'personas' en dos
    grupos no vacios (SI / NO). Si todos responden igual, no separa nada."""
    tiene_si = any(p[col_excel] == "si" for p in personas)
    tiene_no = any(p[col_excel] != "si" for p in personas)
    return tiene_si and tiene_no


# ---------------------------------------------------------------------------
# Construccion del arbol EN MEMORIA (estructura de datos)
# ---------------------------------------------------------------------------
# Esta es la version que usa el juego de Pygame. En vez de dibujar nodos y
# aristas sobre un objeto graphviz, arma diccionarios anidados con toda la
# informacion necesaria para recorrer el arbol pregunta por pregunta.
#
# Tipos de nodo posibles:
#   {"tipo": "pregunta", "pregunta": str, "columna": str, "si": nodo, "no": nodo}
#   {"tipo": "hoja", "nombre": str}
#   {"tipo": "grupo", "etiqueta": str, "nombres": [str, ...], "adyacencia": {...}}

GRUPOS_INDISTINGUIBLES = []  # se va llenando a medida que aparecen (si aparecen)


def construir_arbol_datos(personas, indice_pregunta):
    """Version 'de datos' de construir_arbol(): arma el arbol completo como
    diccionarios de Python en vez de una imagen, para poder recorrerlo
    interactivamente desde Pygame."""

    # Caso base: queda una sola persona -> hoja con su nombre
    if len(personas) == 1:
        return {"tipo": "hoja", "nombre": personas[0]["nombre"]}

    # Buscar, a partir de indice_pregunta, la siguiente pregunta que
    # realmente separe al grupo actual en dos subgrupos no vacios
    indice = indice_pregunta
    while indice < len(PREGUNTAS):
        col_excel, etiqueta_pregunta = PREGUNTAS[indice]
        if pregunta_separa(personas, col_excel):
            break
        indice += 1
    else:
        # Ninguna pregunta restante separa al grupo -> son indistinguibles,
        # se arma un grafo para identificarlos con DFS
        return construir_grafo_datos(personas)

    grupo_si = [p for p in personas if p[col_excel] == "si"]
    grupo_no = [p for p in personas if p[col_excel] != "si"]

    return {
        "tipo": "pregunta",
        "pregunta": etiqueta_pregunta,
        "columna": col_excel,
        "si": construir_arbol_datos(grupo_si, indice + 1),
        "no": construir_arbol_datos(grupo_no, indice + 1),
    }


def construir_grafo_datos(personas):
    """Version 'de datos' de crear_nodo_grupo_indistinguible(): arma un
    grafo NO dirigido completo (cada candidato conectado con todos los
    demas) para un grupo de personas indistinguibles. No depende de
    graphviz, por eso puede usarse directamente dentro del juego."""

    nombres = [p["nombre"] for p in personas]
    numero_grupo = len(GRUPOS_INDISTINGUIBLES) + 1
    etiqueta_grupo = f"G{numero_grupo}"

    adyacencia = {nombre: [] for nombre in nombres}
    for i in range(len(nombres)):
        for j in range(i + 1, len(nombres)):
            origen, destino = nombres[i], nombres[j]
            adyacencia[origen].append(destino)
            adyacencia[destino].append(origen)

    grupo = {
        "tipo": "grupo",
        "numero": numero_grupo,
        "etiqueta": etiqueta_grupo,
        "nombres": nombres,
        "adyacencia": adyacencia,
    }
    GRUPOS_INDISTINGUIBLES.append(grupo)
    return grupo


# ---------------------------------------------------------------------------
# Construccion del arbol como IMAGEN (graphviz) -- opcional, solo para
# generar arbol_akinator.png / grafo_G1.png, no la usa el juego en Pygame.
# ---------------------------------------------------------------------------

contador_nodos = 0


def nuevo_id():
    global contador_nodos
    contador_nodos += 1
    return f"nodo{contador_nodos}"


def construir_grafo_candidatos(nombres):
    """Dibuja (con graphviz) el grafo completo de un grupo de candidatos
    indistintos. Devuelve (objeto graphviz.Graph, lista de adyacencia)."""

    dibujo = graphviz.Graph(format="png")
    dibujo.attr("node", fontname="Helvetica", fontsize="11", shape="ellipse",
                style="filled", fillcolor="#ffe0b2")
    dibujo.attr("edge", fontname="Helvetica", fontsize="10")

    adyacencia = {nombre: [] for nombre in nombres}

    for nombre in nombres:
        dibujo.node(nombre, nombre)

    for i in range(len(nombres)):
        for j in range(i + 1, len(nombres)):
            origen, destino = nombres[i], nombres[j]
            dibujo.edge(origen, destino)
            adyacencia[origen].append(destino)
            adyacencia[destino].append(origen)

    return dibujo, adyacencia


def crear_nodo_grupo_indistinguible(personas, grafo_arbol):
    """Version grafica (graphviz) de construir_grafo_datos(): ademas de
    guardar el grupo, genera el archivo grafo_GN.png y deja constancia en
    el arbol principal con un nodo especial tipo "Ir al Grafo GN"."""

    nombres = [p["nombre"] for p in personas]
    numero_grupo = len(GRUPOS_INDISTINGUIBLES) + 1
    etiqueta_grupo = f"G{numero_grupo}"

    dibujo_grafo, adyacencia = construir_grafo_candidatos(nombres)
    nombre_archivo = f"grafo_{etiqueta_grupo}"
    dibujo_grafo.render(filename=nombre_archivo, cleanup=True)

    GRUPOS_INDISTINGUIBLES.append({
        "numero": numero_grupo,
        "etiqueta": etiqueta_grupo,
        "nombres": nombres,
        "adyacencia": adyacencia,
        "imagen": f"{nombre_archivo}.png",
    })

    id_nodo = nuevo_id()
    etiqueta_nodo = f"Ir al Grafo {etiqueta_grupo}\n{len(nombres)} candidatos"
    grafo_arbol.node(
        id_nodo,
        etiqueta_nodo,
        shape="ellipse",
        style="filled",
        fillcolor="#ffe0b2",
    )
    return id_nodo


# ---------------------------------------------------------------------------
# Optimizacion: Generación paralela de gráficos
# ---------------------------------------------------------------------------

def _generar_grafo_worker(args):
    """Worker para generar gráficos en paralelo."""
    numero_grupo, etiqueta_grupo, nombres = args
    
    if not GRAPHVIZ_DISPONIBLE:
        return None
    
    try:
        dibujo = graphviz.Graph(format="png")
        dibujo.attr("node", fontname="Helvetica", fontsize="11", shape="ellipse",
                    style="filled", fillcolor="#ffe0b2")
        dibujo.attr("edge", fontname="Helvetica", fontsize="10")
        
        for nombre in nombres:
            dibujo.node(nombre, nombre)
        
        for i in range(len(nombres)):
            for j in range(i + 1, len(nombres)):
                origen, destino = nombres[i], nombres[j]
                dibujo.edge(origen, destino)
        
        nombre_archivo = f"grafo_{etiqueta_grupo}"
        dibujo.render(filename=nombre_archivo, cleanup=True)
        return f"{nombre_archivo}.png"
    except Exception as e:
        logger.error(f"Error generando grafo {etiqueta_grupo}: {e}")
        return None


def generar_graficos_paralelo(grupos_para_generar):
    """Genera múltiples gráficos de grupos en paralelo.
    
    Args:
        grupos_para_generar: lista de tuplas (numero, etiqueta, nombres)
    
    Returns:
        lista de rutas de archivos generados
    """
    
    if not GRAPHVIZ_DISPONIBLE or not grupos_para_generar:
        return []
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        resultados = list(executor.map(_generar_grafo_worker, grupos_para_generar))
    
    return [r for r in resultados if r is not None]


def construir_arbol(personas, indice_pregunta, grafo, generar_graficos_en_paralelo=True):
    """Construye recursivamente el arbol de decision como IMAGEN
    (graphviz.Digraph). Devuelve el id del nodo creado (raiz del subarbol).
    
    Args:
        personas: lista de personas
        indice_pregunta: índice de pregunta actual
        grafo: objeto graphviz.Digraph
        generar_graficos_en_paralelo: si True, genera gráficos en threads paralelos
    """

    if len(personas) == 1:
        id_nodo = nuevo_id()
        grafo.node(
            id_nodo,
            personas[0]["nombre"],
            shape="ellipse",
            style="filled",
            fillcolor="#c8e6c9",
        )
        return id_nodo

    indice = indice_pregunta
    while indice < len(PREGUNTAS):
        col_excel, etiqueta_pregunta = PREGUNTAS[indice]
        if pregunta_separa(personas, col_excel):
            break
        indice += 1
    else:
        return crear_nodo_grupo_indistinguible(personas, grafo)

    grupo_si = [p for p in personas if p[col_excel] == "si"]
    grupo_no = [p for p in personas if p[col_excel] != "si"]

    id_nodo = nuevo_id()
    grafo.node(
        id_nodo,
        etiqueta_pregunta,
        shape="box",
        style="rounded,filled",
        fillcolor="#bbdefb",
    )

    id_si = construir_arbol(grupo_si, indice + 1, grafo, generar_graficos_en_paralelo)
    id_no = construir_arbol(grupo_no, indice + 1, grafo, generar_graficos_en_paralelo)

    grafo.edge(id_nodo, id_si, label="Si")
    grafo.edge(id_nodo, id_no, label="No")

    return id_nodo


# ---------------------------------------------------------------------------
# Recorrido del grafo de candidatos indistinguibles (DFS) -- version consola
# ---------------------------------------------------------------------------

def recorrer_grafo_dfs(adyacencia, nombres_grupo, inicio):
    """Recorre el grafo de un grupo indistinguible usando DFS (pila
    explicita = version iterativa), preguntando por consola en cada nodo
    visitado si es la persona buscada. El juego en Pygame usa la MISMA
    idea, pero implementada dentro de MotorJuego para poder pausarse y
    esperar el clic del jugador en cada paso."""

    total = len(nombres_grupo)
    visitados = []
    pila = [inicio]

    while pila:
        actual = pila.pop()
        if actual in visitados:
            continue
        visitados.append(actual)

        restantes = total - len(visitados)
        if restantes == 0:
            print(f"Entonces es {actual}.")
            return actual

        respuesta = input(f"¿Tu personaje es {actual}? (si/no): ").strip().lower()
        if respuesta == "si":
            return actual

        for vecino in adyacencia[actual]:
            if vecino not in visitados:
                pila.append(vecino)

    return None


# ---------------------------------------------------------------------------
# Programa principal (solo para generar las imagenes .png, opcional)
# ---------------------------------------------------------------------------

def main():
    if not GRAPHVIZ_DISPONIBLE:
        print("El paquete 'graphviz' no esta instalado; no se pueden generar imagenes.")
        print("Esto no afecta al juego en Pygame, que no necesita graphviz.")
        return

    ruta_datos = os.path.join(os.path.dirname(__file__), "..", "data",
                               "Formulario_proyecto_eda__respuestas__editado.csv")
    if not os.path.exists(ruta_datos):
        ruta_datos = ARCHIVO_EXCEL

    personas = cargar_personas(ruta_datos)

    grafo = graphviz.Digraph("ArbolAkinator", format="png")
    grafo.attr(rankdir="TB")
    grafo.attr("node", fontname="Helvetica", fontsize="11")
    grafo.attr("edge", fontname="Helvetica", fontsize="10")
    grafo.attr(bgcolor="white")

    construir_arbol(personas, 0, grafo)

    grafo.render(filename=ARCHIVO_SALIDA, cleanup=True)
    print(f"Arbol generado correctamente: {ARCHIVO_SALIDA}.png")

    if not GRUPOS_INDISTINGUIBLES:
        print("No se detectaron grupos indistinguibles; no fue necesario crear ningun grafo.")
        return

    print(f"\nSe detectaron {len(GRUPOS_INDISTINGUIBLES)} grafo(s):")
    for grupo in GRUPOS_INDISTINGUIBLES:
        print(f"  {grupo['etiqueta']}: {', '.join(grupo['nombres'])}  ->  {grupo['imagen']}")


if __name__ == "__main__":
    main()
