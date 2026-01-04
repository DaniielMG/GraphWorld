import networkx as nx

class GraphAnalyzer:
    def __init__(self, df_edges):
        """Inicializa el grafo pesado para el análisis."""
        self.G = nx.from_pandas_edgelist(df_edges, source='item_a', target='item_b', edge_attr='Frecuencia')

    def obtener_nodos_unicos(self):
        """Devuelve la lista alfabética de productos/nodos en el grafo."""
        return sorted(list(self.G.nodes()))

    def camino_minimo(self, u, v): 
        """Calcula el camino más corto entre dos nodos."""
        return nx.shortest_path(self.G, source=u.lower(), target=v.lower(), weight='Frecuencia')

    def todos_los_caminos(self, u, v): 
        """Devuelve todas las rutas posibles entre dos nodos (limitado a profundidad 3)."""
        return list(nx.all_simple_paths(self.G, source=u.lower(), target=v.lower(), cutoff=3))

    def distancia_maxima(self): 
        """Calcula el camino más largo sin ciclos (diámetro) en el subgrafo principal."""
        largest_cc = max(nx.connected_components(self.G), key=len)
        return nx.diameter(self.G.subgraph(largest_cc))

    def identificar_clusteres(self): 
        """Detecta subgrafos densamente conectados (comunidades)."""
        from networkx.algorithms import community
        comunidades = list(community.greedy_modularity_communities(self.G))
        return [list(c)[:5] for c in comunidades[:5]] 

    def nodos_alto_grado(self): 
        """Identifica los 10 nodos con mayor número de conexiones."""
        return sorted(dict(self.G.degree()).items(), key=lambda x: x[1], reverse=True)[:10]

    def nodos_por_grado(self, n): 
        """Selecciona nodos que tienen un número específico de conexiones."""
        return [node for node, degree in self.G.degree() if degree == n]

    def nodos_aislados(self): 
        """Devuelve la lista de nodos que no tienen ninguna conexión."""
        return list(nx.isolates(self.G))