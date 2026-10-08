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

    # --- Secuencial ---
    inicio_seq = time.time()
    resultados_seq = [procesar_cuadrante(*c) for c in cuadrantes]
    tiempo_seq = time.time() - inicio_seq

    print("\n--- Procesamiento Secuencial ---")
    for r in resultados_seq:
        print(r)
    print(f"Tiempo secuencial: {tiempo_seq:.2f} segundos")