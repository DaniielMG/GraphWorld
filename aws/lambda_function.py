import json
import boto3
import pandas as pd
import networkx as nx
from io import StringIO

# Configuración S3
S3_BUCKET = 'graphword-data-bucket-2026'
S3_KEY = 'elestats_lite.csv'

# Variables globales para cachear
_analyzer = None

def get_analyzer():
    """Carga el grafo desde S3 (con cache)."""
    global _analyzer
    if _analyzer is None:
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
        csv_content = obj['Body'].read().decode('utf-8')
        
        # Procesar datos
        df = pd.read_csv(StringIO(csv_content), sep=';')
        df_compras = df[df['element_state'] == 'DEL'].copy()
        df_compras.dropna(subset=['text'], inplace=True)
        df_compras['text'] = df_compras['text'].str.lower().str.strip()
        
        from itertools import combinations
        listas = df_compras.groupby('listid')['text'].apply(list).reset_index()
        listas = listas[listas['text'].apply(len) >= 2]
        
        pares = listas['text'].apply(lambda x: [tuple(sorted(p)) for p in combinations(set(x), 2)]).explode()
        frecuencia = pares.value_counts().reset_index()
        frecuencia.columns = ['Par', 'Frecuencia']
        frecuencia[['item_a', 'item_b']] = pd.DataFrame(frecuencia['Par'].tolist(), index=frecuencia.index)
        df_edges = frecuencia[['item_a', 'item_b', 'Frecuencia']]
        
        G = nx.from_pandas_edgelist(df_edges, source='item_a', target='item_b', edge_attr='Frecuencia')
        _analyzer = G
    return _analyzer

def lambda_handler(event, context):
    """Handler principal de Lambda."""
    try:
        path = event.get('rawPath', event.get('path', '/'))
        params = event.get('queryStringParameters', {}) or {}
        
        G = get_analyzer()
        
        if path == '/' or path == '':
            base_url = "https://nujkmosb6l.execute-api.us-east-1.amazonaws.com"
            return response(200, {
                "mensaje": "🚀 API GraphWord operativa",
                "estadisticas": {
                    "nodos": G.number_of_nodes(),
                    "aristas": G.number_of_edges()
                },
                "endpoints_disponibles": {
                    "/nodos-alto-grado": "Top 10 productos más conectados",
                    "/camino-minimo?origen=X&destino=Y": "Camino mínimo entre dos productos",
                    "/nodos-aislados": "Productos sin conexiones",
                    "/clusteres": "Comunidades de productos detectadas"
                },
                "ejemplos": {
                    "nodos_alto_grado": f"{base_url}/nodos-alto-grado",
                    "camino_minimo": f"{base_url}/camino-minimo?origen=pan&destino=leche",
                    "nodos_aislados": f"{base_url}/nodos-aislados",
                    "clusteres": f"{base_url}/clusteres"
                }
            })
        
        elif path == '/nodos-alto-grado':
            top = sorted(dict(G.degree()).items(), key=lambda x: x[1], reverse=True)[:10]
            return response(200, {"top_conectividad": top})
        
        elif path == '/camino-minimo':
            origen = params.get('origen', '').lower()
            destino = params.get('destino', '').lower()
            if not origen or not destino:
                return response(400, {"error": "Parámetros origen y destino requeridos"})
            try:
                camino = nx.shortest_path(G, source=origen, target=destino)
                return response(200, {"camino": camino})
            except nx.NetworkXNoPath:
                return response(404, {"error": "No existe camino entre esos nodos"})
            except nx.NodeNotFound as e:
                return response(404, {"error": f"Nodo no encontrado: {e}"})
        
        elif path == '/nodos-aislados':
            aislados = list(nx.isolates(G))
            return response(200, {"total": len(aislados), "muestra": aislados[:10]})
        
        elif path == '/clusteres':
            # Usar componentes conectados (mucho más rápido que detección de comunidades)
            componentes = list(nx.connected_components(G))
            # Ordenar por tamaño y tomar los 5 más grandes
            componentes_ordenados = sorted(componentes, key=len, reverse=True)[:5]
            resultado = [list(c)[:10] for c in componentes_ordenados]
            return response(200, {
                "clusteres": resultado,
                "total_componentes": len(componentes),
                "nota": "Clusters basados en componentes conectados del grafo"
            })
        
        else:
            return response(404, {"error": f"Ruta no encontrada: {path}"})
            
    except Exception as e:
        return response(500, {"error": str(e)})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, ensure_ascii=False)
    }
