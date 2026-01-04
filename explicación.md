# Análisis de Resultados - Proyecto GraphWord

Este documento detalla la interpretación de las métricas obtenidas a través del sistema, relacionándolas con los objetivos de Ciencia de Datos del proyecto.

Para lanzar el programa, hay que poner el siguiente comando en la terminal: 
py -m uvicorn api:app --reload

Y para verlo en el navegador, hay que ir a 
http://127.0.0.1:8000/docs

---

## 1. Camino Mínimo (Algoritmo de Dijkstra / A*)
* **Definición:** Encuentra la ruta más corta entre dos nodos basándose en las conexiones de co-ocurrencia.
* **Interpretación:** Representa la relación indirecta más fuerte entre dos productos. Si el camino entre `Pan` y `Agua` es `['pan', 'pebre', 'agua']`, significa que el `pebre` es el nexo de unión principal en el comportamiento de compra para esos artículos.

## 2. Todos los Caminos
* **Definición:** Lista todas las trayectorias posibles (sin ciclos) entre dos nodos dentro de un límite de profundidad.
* **Interpretación:** Permite observar la densidad de la red. En un sistema de recomendación, estos caminos sugieren alternativas de navegación o combinaciones de productos secundarias para el usuario.

## 3. Distancia Máxima (Diámetro del Grafo)
* **Definición:** Es el camino más largo entre cualquier par de nodos en el componente conexo principal.
* **Interpretación:** Mide la "extensión" del ecosistema de datos. Un diámetro pequeño sugiere un grafo donde los productos están muy relacionados entre sí, mientras que un diámetro grande indica categorías muy distantes o aisladas.

## 4. Identificación de Clústeres (Comunidades)
* **Definición:** Detecta subgrafos donde la densidad de conexiones internas es mayor que la externa.
* **Interpretación:** Revela agrupaciones lógicas de productos (ej. Lácteos, Limpieza o Desayuno) de forma automática, basándose únicamente en la topología del grafo y el comportamiento del usuario.

## 5. Nodos con Alto Grado de Conectividad
* **Definición:** Identifica los nodos que poseen el mayor número de conexiones directas (aristas).
* **Interpretación:** Representa los productos "Hub". Son artículos esenciales que actúan como puentes entre múltiples categorías y son críticos para la robustez y navegación de la red.

## 6. Selección de Nodos por Grado
* **Definición:** Filtra aquellos nodos que tienen exactamente un número N de conexiones.
* **Interpretación:** Útil para identificar productos de nicho (grado bajo) o productos de consumo masivo (grado alto). Ayuda a segmentar el grafo para análisis de marketing específicos.

## 7. Nodos Aislados
* **Definición:** Identifica nodos con grado cero (sin ninguna conexión).
* **Interpretación:** Representa productos que no guardan relación con ningún otro en el conjunto de datos actual. Detectar estos nodos permite identificar productos que se compran siempre de forma individual o fallos en la red de distribución.
