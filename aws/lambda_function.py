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
            lista_nodos = sorted(list(G.nodes()))
            datalist_options = "".join([f'<option value="{n}">' for n in lista_nodos])
            lista_html = "".join([f'<span class="badge">{n}</span>' for n in lista_nodos])
            
            html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GraphWord API</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh; color: #fff; padding: 20px;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        h1 {{ text-align: center; margin-bottom: 10px; font-size: 2.5em; }}
        .subtitle {{ text-align: center; color: #8892b0; margin-bottom: 30px; }}
        .stats {{ 
            display: flex; justify-content: center; gap: 40px; margin-bottom: 40px;
        }}
        .stat {{ 
            background: rgba(255,255,255,0.1); padding: 20px 40px; border-radius: 10px;
            text-align: center;
        }}
        .stat-value {{ font-size: 2.5em; font-weight: bold; color: #64ffda; }}
        .stat-label {{ color: #8892b0; }}
        .endpoints {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
        .endpoint {{ 
            background: rgba(255,255,255,0.05); border-radius: 10px; padding: 20px;
            border: 1px solid rgba(255,255,255,0.1); transition: all 0.3s;
            display: flex; flex-direction: column; justify-content: space-between;
        }}
        .endpoint:hover {{ background: rgba(255,255,255,0.1); transform: translateY(-2px); }}
        .endpoint h3 {{ color: #64ffda; margin-bottom: 10px; }}
        .endpoint p {{ color: #8892b0; font-size: 0.9em; margin-bottom: 15px; }}
        .btn {{ 
            display: block; width: 100%; background: #64ffda; color: #1a1a2e; padding: 10px;
            border-radius: 5px; text-decoration: none; font-weight: bold; transition: all 0.3s;
            text-align: center; border: none; cursor: pointer;
        }}
        .btn:hover {{ background: #4fd1c5; }}
        .form-group {{ margin-bottom: 10px; }}
        .form-group input {{ 
            padding: 8px 12px; border-radius: 5px; border: none; width: 100%;
            background: rgba(255,255,255,0.1); color: #fff;
        }}
        .form-group input::placeholder {{ color: #8892b0; }}
        
        /* Estilos nuevos para la lista de productos */
        .products-section {{ margin-top: 40px; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); }}
        .products-header {{ cursor: pointer; display: flex; justify-content: space-between; align-items: center; }}
        .products-header h3 {{ color: #64ffda; }}
        .products-content {{ margin-top: 15px; max-height: 200px; overflow-y: auto; display: none; flex-wrap: wrap; gap: 5px; }}
        .badge {{ background: rgba(100, 255, 218, 0.1); color: #64ffda; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; border: 1px solid rgba(100, 255, 218, 0.3); }}
        
        footer {{ text-align: center; margin-top: 40px; color: #8892b0; font-size: 0.9em; }}
    </style>
    <script>
        function toggleProducts() {{
            var content = document.getElementById("products-content");
            var icon = document.getElementById("toggle-icon");
            if (content.style.display === "flex") {{
                content.style.display = "none";
                icon.innerHTML = "▼";
            }} else {{
                content.style.display = "flex";
                icon.innerHTML = "▲";
            }}
        }}
    </script>
</head>
<body>
    <div class="container">
        <h1>GraphWord API</h1>
        <p class="subtitle">Sistema de Analisis de Grafos de Productos</p>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{G.number_of_nodes()}</div>
                <div class="stat-label">Nodos</div>
            </div>
            <div class="stat">
                <div class="stat-value">{G.number_of_edges()}</div>
                <div class="stat-label">Aristas</div>
            </div>
        </div>
        
        <div class="endpoints">
            <div class="endpoint">
                <div>
                    <h3>Top Conectividad</h3>
                    <p>Los 10 productos con mas conexiones en el grafo.</p>
                </div>
                <a href="{base_url}/nodos-alto-grado" class="btn">Ver Top 10</a>
            </div>
            
            <div class="endpoint">
                <div>
                    <h3>Camino Minimo</h3>
                    <p>Ruta mas corta entre dos productos.</p>
                </div>
                <form action="{base_url}/camino-minimo" method="get">
                    <div class="form-group"><input type="text" name="origen" list="productos" placeholder="Origen (ej: pan)" required></div>
                    <div class="form-group"><input type="text" name="destino" list="productos" placeholder="Destino (ej: leche)" required></div>
                    <button type="submit" class="btn">Buscar Camino</button>
                </form>
            </div>
            
            <div class="endpoint">
                <div>
                    <h3>Todos los Caminos</h3>
                    <p>Todas las rutas posibles (max 3 saltos).</p>
                </div>
                <form action="{base_url}/todos-los-caminos" method="get">
                    <div class="form-group"><input type="text" name="origen" list="productos" placeholder="Origen (ej: pan)" required></div>
                    <div class="form-group"><input type="text" name="destino" list="productos" placeholder="Destino (ej: leche)" required></div>
                    <button type="submit" class="btn">Ver Rutas</button>
                </form>
            </div>

            <div class="endpoint">
                <div>
                    <h3>Buscar por Grado</h3>
                    <p>Productos con X conexiones exactas.</p>
                </div>
                <form action="{base_url}/nodos-por-grado" method="get">
                    <div class="form-group"><input type="number" name="grado" placeholder="Grado (ej: 5)" required></div>
                    <button type="submit" class="btn">Buscar</button>
                </form>
            </div>
            
            <div class="endpoint">
                <div>
                    <h3>Distancia Maxima</h3>
                    <p>Diametro del grafo (camino mas largo).</p>
                </div>
                <a href="{base_url}/distancia-maxima" class="btn">Ver Diametro</a>
            </div>
            
            <div class="endpoint">
                <div>
                    <h3>Nodos Aislados</h3>
                    <p>Productos sin conexiones con otros.</p>
                </div>
                <a href="{base_url}/nodos-aislados" class="btn">Ver Aislados</a>
            </div>
            
            <div class="endpoint">
                <div>
                    <h3>Clusters</h3>
                    <p>Comunidades de productos relacionados.</p>
                </div>
                <a href="{base_url}/clusteres" class="btn">Ver Clusters</a>
            </div>
        </div>
        
        <datalist id="productos">
            {datalist_options}
        </datalist>

        <div class="products-section">
            <div class="products-header" onclick="toggleProducts()">
                <h3>📦 Ver Todos los Productos ({len(lista_nodos)})</h3>
                <span id="toggle-icon">▼</span>
            </div>
            <div class="products-content" id="products-content">
                {lista_html}
            </div>
        </div>
        
        <footer>
            <p>GraphWord - Tecnologias de Sistemas para Ciencia de Datos</p>
            <p>API desplegada en AWS Lambda + API Gateway</p>
        </footer>
    </div>
</body>
</html>'''
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html; charset=utf-8'},
                'body': html
            }
        
        elif path == '/nodos-alto-grado':
            top = sorted(dict(G.degree()).items(), key=lambda x: x[1], reverse=True)[:10]
            return response(200, {"top_conectividad": top})
        
        elif path == '/camino-minimo':
            origen = params.get('origen', '').lower()
            destino = params.get('destino', '').lower()
            if not origen or not destino:
                return response(400, {"error": "Parametros origen y destino requeridos"})
            try:
                camino = nx.shortest_path(G, source=origen, target=destino)
                return response(200, {"camino": camino})
            except nx.NetworkXNoPath:
                return response(404, {"error": "No existe camino entre esos nodos"})
            except nx.NodeNotFound as e:
                return response(404, {"error": f"Nodo no encontrado: {e}"})

        elif path == '/todos-los-caminos':
            origen = params.get('origen', '').lower()
            destino = params.get('destino', '').lower()
            if not origen or not destino:
                return response(400, {"error": "Parametros origen y destino requeridos"})
            try:
                caminos = list(nx.all_simple_paths(G, source=origen, target=destino, cutoff=3))
                return response(200, {"total_caminos": len(caminos), "caminos": caminos})
            except nx.NodeNotFound as e:
                return response(404, {"error": f"Nodo no encontrado: {e}"})
            except Exception as e:
                return response(500, {"error": str(e)})

        elif path == '/distancia-maxima':
            try:
                largest_cc = max(nx.connected_components(G), key=len)
                subgraph = G.subgraph(largest_cc)
                diametro = nx.diameter(subgraph)
                return response(200, {"diametro_subgrafo": diametro})
            except Exception as e:
                return response(500, {"error": str(e)})

        elif path == '/nodos-por-grado':
            grado = params.get('grado')
            if grado is None:
                return response(400, {"error": "Parametro grado requerido"})
            try:
                grado_int = int(grado)
                nodos = [node for node, degree in G.degree() if degree == grado_int]
                return response(200, {"grado": grado_int, "total_nodos": len(nodos), "nodos": nodos})
            except ValueError:
                return response(400, {"error": "El grado debe ser un numero entero"})
        
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
