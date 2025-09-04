# Lozano Hernandez Jose Angel 22310220 7-F

def dijkstra(w, a, z):
    L = {node: float('inf') for node in w}
    L[a] = 0  
    predecesores = {node: None for node in w}  
    T = set(w.keys())

    while T:
        v = min(T, key=lambda node: L[node])
        T.remove(v)
        if v == z:
            break  

        for x, weight in w[v].items():
            if x in T:
                nueva_distancia = L[v] + weight
                if nueva_distancia < L[x]:
                    L[x] = nueva_distancia
                    predecesores[x] = v  

    ruta = []
    nodo_actual = z
    while nodo_actual is not None:
        ruta.insert(0, nodo_actual)
        nodo_actual = predecesores[nodo_actual]

    return L[z], ruta

# Grafo con más rutas (tiempo en minutos)
w = {
    'Plaza': {'Escuela': 10, 'Hospital': 15, 'Museo': 20},
    'Escuela': {'Plaza': 10, 'Supermercado': 12, 'Biblioteca': 8},
    'Hospital': {'Plaza': 15, 'Parque': 10, 'Universidad': 18},
    'Supermercado': {'Escuela': 12, 'Parque': 5, 'Mercado': 14},
    'Parque': {'Hospital': 10, 'Supermercado': 5, 'Estacion': 8, 'Cine': 6},
    'Estacion': {'Parque': 8, 'Aeropuerto': 25},
    'Biblioteca': {'Escuela': 8, 'Museo': 6},
    'Museo': {'Plaza': 20, 'Biblioteca': 6, 'Universidad': 15},
    'Universidad': {'Hospital': 18, 'Museo': 15, 'Cine': 9},
    'Cine': {'Parque': 6, 'Universidad': 9, 'Mercado': 7},
    'Mercado': {'Supermercado': 14, 'Cine': 7},
    'Aeropuerto': {'Estacion': 25}
}

# Entrada del usuario
inicio = input("Ingrese el punto de inicio (ej: Plaza, Escuela, Hospital): ").strip().title()
destino = input("Ingrese el punto de destino: ").strip().title()

if inicio in w and destino in w:
    distancia, ruta = dijkstra(w, inicio, destino)
    print(f"\nEl tiempo mínimo de '{inicio}' a '{destino}' es: {distancia} minutos")
    print(f"La ruta más corta es: {' -> '.join(ruta)}")
else:
    print("Uno o ambos puntos ingresados no existen en las rutas de autobuses.")
