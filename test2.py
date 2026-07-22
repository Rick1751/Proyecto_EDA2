# test_sapometro.py
import time
from core.multiprocesamiento import ManagerMultiprocesamiento

# Esta función simula una tarea que le toma tiempo al procesador
def calcular_test(numero):
    # Forzamos un retraso de 4 segundos para congelar el proceso y poder verlo
    time.sleep(8)
    return numero * numero

if __name__ == "__main__":
    print("--- INICIANDO PRUEBA DE MULTIPROCESAMIENTO ---")
    
    # 1. Inicializamos tu manager (usará tus 15 procesos por defecto)
    manager = ManagerMultiprocesamiento()
    
    # 2. Creamos una lista con 15 tareas (una para cada proceso)
    tareas = list(range(15))
    
    print("\n[!] Disparando tareas en paralelo...")
    print("[!] REVISA TU ADMINISTRADOR DE TAREAS EN 'DETALLES' ¡AHORA!")
    print("------------------------------------------------------------")
    
    # 3. Aquí se rompe la inicialización perezosa y se crean los procesos reales
    resultados = manager.procesar_en_paralelo(calcular_test, tareas)
    
    print("\n[✓] ¡Procesamiento completado con éxito!")
    print(f"Resultados obtenidos: {resultados}")
    
    # 4. Limpiamos los procesos al terminar
    manager.limpiar()