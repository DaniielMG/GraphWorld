from fastapi import FastAPI
from analisis_grafo import GraphAnalyzer
from procesamiento import cargar_y_limpiar_datos, generar_co_ocurrencias

app = FastAPI(title="GraphWord API - Sistema Completo")

df_listas = cargar_y_limpiar_datos('elestats_lite.csv')
df_aristas = generar_co_ocurrencias(df_listas)
analizador = GraphAnalyzer(df_aristas)

@app.get("/")
def home():
    return {"mensaje": "API de GraphWord operativa con las 7 funcionalidades"}

@app.get("/camino-minimo")
def obtener_camino(origen: str, destino: str):
    try:
        return {"resultado": analizador.camino_minimo(origen, destino)}
    except:
        return {"error": "Nodos no conectados o no encontrados"}

@app.get("/todos-los-caminos")
def obtener_todos_caminos(origen: str, destino: str):
    try:
        return {"resultado": analizador.todos_los_caminos(origen, destino)}
    except:
        return {"error": "Error al calcular rutas"}

@app.get("/distancia-maxima")
def obtener_distancia_maxima():
    return {"diametro_subgrafo": analizador.distancia_maxima()}

@app.get("/identificar-clusteres")
def obtener_clusteres():
    return {"clusteres_principales": analizador.identificar_clusteres()}

@app.get("/nodos-alto-grado")
def obtener_nodos_top():
    return {"top_conectividad": analizador.nodos_alto_grado()}

@app.get("/nodos-por-grado/{grado}")
def obtener_nodos_grado(grado: int):
    return {"nodos": analizador.nodos_por_grado(grado)}

@app.get("/nodos-aislados")
def obtener_aislados():
    return {"total_aislados": len(analizador.nodos_aislados()), "lista_ejemplo": analizador.nodos_aislados()[:10]}