# test_sapometro.py
import time
import multiprocessing
from core.multiprocesamiento import ManagerMultiprocesamiento

def tarea_pesada_cpu(numero):
    inicio = time.time()
    while time.time() - inicio < 0.5:
        _ = 12345 * 67890
    return numero * numero

if __name__ == "__main__":
    print("====================================================")
    print("   BENCHMARK DE RENDIMIENTO - PROYECTO SAPOMETRO   ")
    print("====================================================\n")
    
    # 1. Detectar hardware actual
    nucleos_totales = multiprocessing.cpu_count()
    manager = ManagerMultiprocesamiento()
    procesos_asignados = manager.num_procesos
    
    print(f"[PC INFO] Núcleos físicos detectados: {nucleos_totales}")
    # Tu lógica original usa cpu_count() - 1
    print(f"[PC INFO] Procesos asignados al test: {procesos_asignados}\n")
    
    # Creamos un lote grande de tareas (ej. 30 tareas) para estresar el CPU
    tareas = list(range(30))
    
    # --- PRUEBA 1: SECUENCIAL (Simula 1 solo núcleo / Compu poco potente) ---
    print("[1/2] Ejecutando de forma SECUENCIAL (Lento)...")
    t_inicio_seq = time.time()
    resultados_seq = [tarea_pesada_cpu(t) for t in tareas]
    t_final_seq = time.time()
    tiempo_secuencial = t_final_seq - t_inicio_seq
    print(f"      -> Tiempo Secuencial: {tiempo_secuencial:.2f} segundos\n")
    
    # --- PRUEBA 2: PARALELO (Usa toda la potencia de la máquina actual) ---
    print(f"[2/2] Ejecutando en PARALELO con {procesos_asignados} procesos (Rápido)...")
    t_inicio_par = time.time()
    resultados_par = manager.procesar_en_paralelo(tarea_pesada_cpu, tareas)
    t_final_par = time.time()
    tiempo_paralelo = t_final_par - t_inicio_par
    print(f"      -> Tiempo Paralelo: {tiempo_paralelo:.2f} segundos\n")
    
    # --- MÉTRICAS DE COMPARACIÓN ---
    factor_aceleracion = tiempo_secuencial / tiempo_paralelo
    # Eficiencia de uso de los núcleos asignados
    eficiencia = (factor_aceleracion / procesos_asignados) * 100
    
    print("====================================================")
    print("               REPORTE DE RESULTADOS                ")
    print("====================================================")
    print(f"Tiempo ahorrado en esta PC : {(tiempo_secuencial - tiempo_paralelo):.2f} segundos")
    print(f"Factor de Aceleración      : {factor_aceleracion:.2f}x más rápido")
    print(f"Eficiencia del Multi-Core  : {eficiencia:.1f}%")
    print("====================================================\n")
    
    # Validación de datos
    if resultados_seq == resultados_par:
        print("[✓] Datos íntegros. El procesamiento paralelo es idéntico al secuencial.")
    
    manager.limpiar()
