# test_sapometro.py
import time
from core.multiprocesamiento import ManagerMultiprocesamiento

# Esta función simula una tarea que le toma tiempo al procesador
def calcular_test(numero):
    # Forzamos un retraso de 8 segundos para congelar el proceso y poder verlo
    time.sleep(8)
    return numero * numero

if __name__ == "__main__":
    print("--- INICIANDO PRUEBA DE MULTIPROCESAMIENTO ---")
    
    manager = ManagerMultiprocesamiento()
    
    tareas = list(range(15))
    
    print("\n[!] Disparando tareas en paralelo...")
    print("Abrir el administrador de tareas para observar los procesos")
    print("------------------------------------------------------------")
    
    # 3. Aquí se rompe la inicialización perezosa y se crean los procesos reales
    resultados = manager.procesar_en_paralelo(calcular_test, tareas)
    
    print("\n[✓] ¡Procesamiento completado con éxito!")
    print(f"Resultados obtenidos: {resultados}")
    
    # 4. Limpiamos los procesos al terminar
    manager.limpiar()