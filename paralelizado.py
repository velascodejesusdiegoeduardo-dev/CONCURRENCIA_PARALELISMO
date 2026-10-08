import multiprocessing
import time

def procesar_cuadrante(cuadrante_id, area, profundidad):
    time.sleep(0.1)
    volumen = area * profundidad
    return f"Cuadrante {cuadrante_id}: {volumen} m³"

if __name__ == "__main__":
    # --- Registro de datos ---
    area_total = float(input("Ingrese el área total: "))
    profundidad = float(input("Ingrese la profundidad: "))

    # Dividimos el área en 4 cuadrantes iguales
    cuadrantes = [(i+1, area_total/4, profundidad) for i in range(4)]
    
    # --- Paralelo ---
    inicio_par = time.time()
    with multiprocessing.Pool(processes=4) as pool:
        resultados_par = pool.starmap(procesar_cuadrante, cuadrantes)
    tiempo_par = time.time() - inicio_par

    print("\n--- Procesamiento Paralelo ---")
    for r in resultados_par:
        print(r)
    print(f"Tiempo paralelo: {tiempo_par:.2f} segundos")