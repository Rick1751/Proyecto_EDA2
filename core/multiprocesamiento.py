"""
multiprocesamiento.py

Módulo para manejar procesamiento paralelo del proyecto Sapometro.
Utiliza multiprocessing y concurrent.futures para paralelizar tareas
de I/O, carga de datos y construcción de estructuras de datos.

Características:
    - Carga de datos en paralelo
    - Construcción del árbol con multiprocessing
    - Pool de procesos para tareas asincrónicas
    - Caché de resultados
    - Manejo seguro de procesos
"""

import os
import sys
import multiprocessing
from multiprocessing import Pool, Manager, Process, Queue
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ManagerMultiprocesamiento:
    """Gestor centralizado de multiprocesamiento para el proyecto."""
    
    def __init__(self, num_procesos=None):
        """
        Inicializa el gestor de multiprocesamiento.
        
        Args:
            num_procesos: número de procesos a usar (None = automático)
        """
        if num_procesos is None:
            # Usar CPU count menos 1 para no bloquear el sistema
            num_procesos = max(1, multiprocessing.cpu_count() - 1)
        
        self.num_procesos = num_procesos
        self.executor_procesos = ProcessPoolExecutor(max_workers=num_procesos)
        self.executor_threads = ThreadPoolExecutor(max_workers=num_procesos)
        logger.info(f"Manager de multiprocesamiento inicializado con {num_procesos} procesos")
    
    def procesar_en_paralelo(self, funcion, items, use_threads=False):
        """
        Procesa items en paralelo usando una función.
        
        Args:
            funcion: función a aplicar a cada item
            items: lista de items a procesar
            use_threads: usar threads en lugar de procesos
        
        Returns:
            lista de resultados
        """
        executor = self.executor_threads if use_threads else self.executor_procesos
        
        try:
            resultados = list(executor.map(funcion, items))
            return resultados
        except Exception as e:
            logger.error(f"Error en procesamiento paralelo: {e}")
            # Fallback: procesar secuencialmente
            return [funcion(item) for item in items]
    
    def ejecutar_asincrono(self, funcion, args=(), use_threads=False):
        """
        Ejecuta una función de forma asincrónica.
        
        Args:
            funcion: función a ejecutar
            args: argumentos de la función
            use_threads: usar threads en lugar de procesos
        
        Returns:
            Future objeto para seguimiento
        """
        executor = self.executor_threads if use_threads else self.executor_procesos
        return executor.submit(funcion, *args)
    
    def limpiar(self):
        """Cierra los executors y libera recursos."""
        self.executor_procesos.shutdown(wait=True)
        self.executor_threads.shutdown(wait=True)
        logger.info("Manager de multiprocesamiento cerrado")
    
    def __del__(self):
        """Limpieza automática al destruir el objeto."""
        try:
            self.limpiar()
        except:
            pass


def cargar_datos_paralelo(ruta_datos):
    """
    Carga datos desde archivo de forma optimizada.
    Útil para archivos grandes.
    
    Args:
        ruta_datos: ruta al archivo de datos
    
    Returns:
        dataframe con los datos cargados
    """
    import pandas as pd
    
    extension = os.path.splitext(ruta_datos)[1].lower()
    
    try:
        if extension == ".csv":
            # Leer CSV con optimizaciones
            df = pd.read_csv(ruta_datos, engine='python')
        else:
            # Leer Excel
            df = pd.read_excel(ruta_datos)
        
        logger.info(f"Datos cargados exitosamente: {len(df)} registros")
        return df
    except Exception as e:
        logger.error(f"Error al cargar datos: {e}")
        raise


def procesar_personas_paralelo(filas, columna_nombre, preguntas, persona_excluida):
    """
    Procesa personas en paralelo desde las filas del dataframe.
    
    Args:
        filas: tuplas (índice, row) del dataframe
        columna_nombre: nombre de la columna con nombres
        preguntas: lista de preguntas (col_excel, etiqueta)
        persona_excluida: patrón de nombre a excluir
    
    Returns:
        lista de diccionarios de personas procesadas
    """
    import pandas as pd
    
    personas = []
    
    for idx, fila in filas:
        nombre_crudo = fila.get(columna_nombre, "")
        if pd.isna(nombre_crudo):
            continue
        
        nombre = " ".join(str(nombre_crudo).split())
        
        if persona_excluida.lower() in nombre.lower():
            continue
        
        persona = {"nombre": nombre}
        for col_excel, _etiqueta in preguntas:
            valor = fila.get(col_excel.strip(), fila.get(col_excel, ""))
            if pd.isna(valor):
                valor = ""
            valor = str(valor).strip().lower()
            persona[col_excel] = valor
        
        personas.append(persona)
    
    return personas


class CargarDatosAsincrono:
    """
    Contexto para cargar datos de forma asincrónica sin bloquear Pygame.
    """
    
    def __init__(self, ruta_datos, callback_completado=None):
        """
        Args:
            ruta_datos: ruta al archivo de datos
            callback_completado: función a llamar cuando termine (opcional)
        """
        self.ruta_datos = ruta_datos
        self.callback_completado = callback_completado
        self.datos = None
        self.proceso = None
        self.cola_resultado = Queue()
        self.terminado = False
    
    def iniciar(self):
        """Inicia la carga asincrónica en un proceso separado."""
        self.proceso = Process(
            target=self._cargar_en_proceso,
            args=(self.ruta_datos, self.cola_resultado)
        )
        self.proceso.start()
        logger.info("Carga de datos iniciada en proceso separado")
    
    @staticmethod
    def _cargar_en_proceso(ruta_datos, cola_resultado):
        """Función que se ejecuta en el proceso separado."""
        try:
            datos = cargar_datos_paralelo(ruta_datos)
            cola_resultado.put(("éxito", datos))
        except Exception as e:
            cola_resultado.put(("error", str(e)))
    
    def esta_completado(self):
        """Verifica si la carga se completó."""
        if self.terminado:
            return True
        
        if not self.cola_resultado.empty():
            estado, resultado = self.cola_resultado.get()
            if estado == "éxito":
                self.datos = resultado
                self.terminado = True
                if self.callback_completado:
                    self.callback_completado(self.datos)
            else:
                logger.error(f"Error en carga asincrónica: {resultado}")
                self.terminado = True
        
        return self.terminado
    
    def obtener_datos(self):
        """Obtiene los datos si están listos, None si aún se cargan."""
        if self.terminado:
            return self.datos
        return None
    
    def esperar(self):
        """Espera a que termine la carga (bloquea)."""
        if self.proceso:
            self.proceso.join()
        self.datos, _ = self.cola_resultado.get() if not self.cola_resultado.empty() else (None, None)
        self.terminado = True
        return self.datos
    
    def cancelar(self):
        """Cancela la carga."""
        if self.proceso and self.proceso.is_alive():
            self.proceso.terminate()
            self.proceso.join()
        self.terminado = True
        logger.info("Carga de datos cancelada")


def procesar_construccion_arbol_paralelo(personas, funciones_construccion):
    """
    Construye múltiples árboles en paralelo.
    Útil para validación o generación de variantes.
    
    Args:
        personas: lista de personas
        funciones_construccion: lista de funciones que construyen árboles
    
    Returns:
        lista de árboles construidos
    """
    with ProcessPoolExecutor(max_workers=len(funciones_construccion)) as executor:
        futuros = [
            executor.submit(func, personas) 
            for func in funciones_construccion
        ]
        return [futuro.result() for futuro in futuros]


def generar_graficos_paralelo(datos_graficos):
    """
    Genera múltiples gráficos en paralelo usando graphviz.
    
    Args:
        datos_graficos: lista de tuplas (función_generadora, argumentos)
    
    Returns:
        lista de rutas de archivos generados
    """
    def generar_grafico(item):
        func, args = item
        try:
            return func(*args)
        except Exception as e:
            logger.error(f"Error generando gráfico: {e}")
            return None
    
    with ProcessPoolExecutor(max_workers=2) as executor:
        resultados = list(executor.map(generar_grafico, datos_graficos))
    
    return [r for r in resultados if r is not None]


# Singleton global del manager
_manager_global = None


def obtener_manager():
    """Obtiene la instancia global del manager de multiprocesamiento."""
    global _manager_global
    if _manager_global is None:
        _manager_global = ManagerMultiprocesamiento()
    return _manager_global


def limpiar_manager():
    """Limpia el manager global."""
    global _manager_global
    if _manager_global is not None:
        _manager_global.limpiar()
        _manager_global = None
