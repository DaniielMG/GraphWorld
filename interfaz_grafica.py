import streamlit as st
import pandas as pd
from procesamiento import cargar_y_limpiar_datos, generar_co_ocurrencias
from analisis_grafo import GraphAnalyzer

st.set_page_config(page_title="GraphWord Dashboard", layout="wide")

st.title(" GraphWord: Análisis de Grafos Distribuido")
st.markdown("Construcción de una Arquitectura Escalable y Distribuida [cite: 3]")

@st.cache_resource
def inicializar_datos():
    df_listas = cargar_y_limpiar_datos('elestats.csv')
    df_aristas = generar_co_ocurrencias(df_listas)
    return GraphAnalyzer(df_aristas)

analizador = inicializar_datos()
nodos = analizador.obtener_nodos_unicos()

st.sidebar.header("Funcionalidades de la API [cite: 49]")
opcion = st.sidebar.selectbox("Seleccione operación", 
    ["Camino Mínimo", "Clusters", "Top Conectividad", "Nodos Aislados"])

if opcion == "Camino Mínimo":
    st.subheader(" Calcular Camino Mínimo [cite: 52]")
    col1, col2 = st.columns(2)
    with col1:
        u = st.selectbox("Producto Origen", nodos)
    with col2:
        v = st.selectbox("Producto Destino", nodos)
    
    if st.button("Calcular Ruta"):
        try:
            camino = analizador.camino_minimo(u, v)
            st.success(f"Camino encontrado: {' ➡️ '.join(camino)}")
        except:
            st.error("No existe conexión entre estos nodos.")

elif opcion == "Top Conectividad":
    st.subheader(" Nodos con Alto Grado de Conectividad ")
    top_nodos = analizador.nodos_alto_grado()
    df_top = pd.DataFrame(top_nodos, columns=['Producto', 'Conexiones'])
    st.bar_chart(df_top.set_index('Producto'))
