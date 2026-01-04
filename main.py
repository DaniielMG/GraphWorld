<<<<<<< HEAD
from procesamiento import cargar_y_limpiar_datos, generar_co_ocurrencias
from analisis_grafo import GraphAnalyzer

def mostrar_nodos_en_columnas(nodos, columnas=5):
    for i in range(0, len(nodos), columnas):
        fila = nodos[i:i+columnas]
        print("".join(word.ljust(20) for word in fila))

def main():
    print("=== INICIANDO GRAPHWORD (Entorno Distribuido AWS Ready) ===")
    df_listas = cargar_y_limpiar_datos('elestats_lite.csv')
    if df_listas is None: return
    
    df_aristas = generar_co_ocurrencias(df_listas)
    analizador = GraphAnalyzer(df_aristas)
    
    nodos = analizador.obtener_nodos_unicos()
    print("\n" + "="*80)
    print(f"PRODUCTOS DISPONIBLES EN EL GRAFO ({len(nodos)} totales):")
    print("="*80)
    mostrar_nodos_en_columnas(nodos[:50]) 
    if len(nodos) > 50:
        print(f"\n... y {len(nodos) - 50} productos más.")
    print("="*80)

    while True:
        print("\n--- MENU DE CIENCIA DE DATOS (AWS READY) ---")
        print("1. Camino Mínimo | 2. Todos los Caminos | 3. Distancia Máxima")
        print("4. Clusters | 5. Nodos Top Grado | 6. Buscar por Grado")
        print("7. Nodos Aislados | 0. Salir")
        
        op = input("\nSeleccione una opción: ")
        try:
            if op == "1":
                u, v = input("De: "), input("A: ")
                print(f"Camino: {analizador.camino_minimo(u, v)}")
            elif op == "2":
                u, v = input("De: "), input("A: ")
                print(f"Rutas (limitadas): {analizador.todos_los_caminos(u, v)}")
            elif op == "3":
                print(f"Diámetro (subgrafo principal): {analizador.distancia_maxima()}")
            elif op == "4":
                print(f"Clusters principales (muestra): {analizador.identificar_clusteres()}")
            elif op == "5":
                print(f"Top 10 nodos (Grado): {analizador.nodos_alto_grado()}")
            elif op == "6":
                g = int(input("Grado exacto a buscar: "))
                print(f"Nodos con grado {g}: {analizador.nodos_por_grado(g)[:10]}...")
            elif op == "7":
                print(f"Total de nodos aislados: {len(analizador.nodos_aislados())}")
            elif op == "0": 
                print("Cerrando sistema...")
                break
        except Exception as e:
            print(f"Error: {e}. Asegúrese de usar nombres que aparezcan en la lista superior.")

if __name__ == "__main__":
=======
from procesamiento import cargar_y_limpiar_datos, generar_co_ocurrencias
from analisis_grafo import GraphAnalyzer

def mostrar_nodos_en_columnas(nodos, columnas=5):
    for i in range(0, len(nodos), columnas):
        fila = nodos[i:i+columnas]
        print("".join(word.ljust(20) for word in fila))

def main():
    print("=== INICIANDO GRAPHWORD (Entorno Distribuido AWS Ready) ===")
    df_listas = cargar_y_limpiar_datos('elestats_lite.csv')
    if df_listas is None: return
    
    df_aristas = generar_co_ocurrencias(df_listas)
    analizador = GraphAnalyzer(df_aristas)
    
    nodos = analizador.obtener_nodos_unicos()
    print("\n" + "="*80)
    print(f"PRODUCTOS DISPONIBLES EN EL GRAFO ({len(nodos)} totales):")
    print("="*80)
    mostrar_nodos_en_columnas(nodos[:50]) 
    if len(nodos) > 50:
        print(f"\n... y {len(nodos) - 50} productos más.")
    print("="*80)

    while True:
        print("\n--- MENU DE CIENCIA DE DATOS (AWS READY) ---")
        print("1. Camino Mínimo | 2. Todos los Caminos | 3. Distancia Máxima")
        print("4. Clusters | 5. Nodos Top Grado | 6. Buscar por Grado")
        print("7. Nodos Aislados | 0. Salir")
        
        op = input("\nSeleccione una opción: ")
        try:
            if op == "1":
                u, v = input("De: "), input("A: ")
                print(f"Camino: {analizador.camino_minimo(u, v)}")
            elif op == "2":
                u, v = input("De: "), input("A: ")
                print(f"Rutas (limitadas): {analizador.todos_los_caminos(u, v)}")
            elif op == "3":
                print(f"Diámetro (subgrafo principal): {analizador.distancia_maxima()}")
            elif op == "4":
                print(f"Clusters principales (muestra): {analizador.identificar_clusteres()}")
            elif op == "5":
                print(f"Top 10 nodos (Grado): {analizador.nodos_alto_grado()}")
            elif op == "6":
                g = int(input("Grado exacto a buscar: "))
                print(f"Nodos con grado {g}: {analizador.nodos_por_grado(g)[:10]}...")
            elif op == "7":
                print(f"Total de nodos aislados: {len(analizador.nodos_aislados())}")
            elif op == "0": 
                print("Cerrando sistema...")
                break
        except Exception as e:
            print(f"Error: {e}. Asegúrese de usar nombres que aparezcan en la lista superior.")

if __name__ == "__main__":
>>>>>>> 578b0a74ddcf2c8eb15d54920d3bd461a1441912
    main()