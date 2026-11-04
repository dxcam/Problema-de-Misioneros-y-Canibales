from collections import deque

# Estado inicial: (misioneros_izq, canibales_izq, bote_izq)
INICIO = (3, 3, 1)
META = (0, 0, 0)

def es_valido(estado):
    """Verifica si un estado cumple con las reglas del problema."""
    m_izq, c_izq, bote = estado
    
    if not (0 <= m_izq <= 3 and 0 <= c_izq <= 3):
        return False
    
    m_der = 3 - m_izq
    c_der = 3 - c_izq
    
    # Restricción: Los caníbales no pueden superar a los misioneros si hay misioneros presentes
    if m_izq > 0 and m_izq < c_izq:
        return False
    if m_der > 0 and m_der < c_der:
        return False
        
    return True

def obtener_sucesores(estado):
    """Genera todos los estados válidos alcanzables desde el estado actual."""
    sucesores = []
    m_izq, c_izq, bote = estado
    
    # Movimientos posibles: (misioneros, canibales)
    movimientos = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    
    for m, c in movimientos:
        if bote == 1:  # El bote está en la izquierda, viaja a la derecha
            nuevo_estado = (m_izq - m, c_izq - c, 0)
        else:  # El bote está en la derecha, viaja a la izquierda
            nuevo_estado = (m_izq + m, c_izq + c, 1)
            
        if es_valido(nuevo_estado):
            sucesores.append(nuevo_estado)
            
    return sucesores

def imprimir_escenario(estado, paso):
    """Dibuja de forma amigable y gráfica el escenario del río en la consola."""
    m_izq, c_izq, bote = estado
    m_der = 3 - m_izq
    c_der = 3 - c_izq
    
    # Representación visual con emojis
    lados_m_izq = "M " * m_izq
    lados_c_izq = "C " * c_izq
    lados_m_der = "M " * m_der
    lados_c_der = "C " * c_der
    
    # Posición del bote (B)
    if bote == 1:
        rio = "🚢 [BOTE] ~~~~~~~~ "
    else:
        rio = " ~~~~~~~~ [BOTE] 🚢"
        
    print(f"\n--- PASO {paso} ---")
    print(f"Orilla Izquierda        | Río {rio}| Orilla Derecha")
    print(f"Misioneros: [{lados_m_izq.strip()}]       |                  | Misioneros: [{lados_m_der.strip()}]")
    print(f"Caníbales:  [{lados_c_izq.strip()}]       |                  | Caníbales:  [{lados_c_der.strip()}]")
    print("-" * 55)

def ejecutar_busqueda(inicio, meta, modo="BFS"):
    """Ejecuta la búsqueda y muestra la simulación paso a paso del resultado."""
    frontera = deque([inicio]) if modo == "BFS" else [inicio]
    visitados = set([inicio])
    padres = {inicio: None}  # Rastreador de caminos[cite: 1]
    nodos_expandidos = 0

    print(f"\n=========================================")
    print(f" INICIANDO BÚSQUEDA CON: {modo}")
    print(f"=========================================")

    while frontera:
        nodo_actual = frontera.popleft() if modo == "BFS" else frontera.pop()
        nodos_expandidos += 1
        
        if nodo_actual == meta:
            # Reconstrucción del camino[cite: 1]
            camino = []
            rastreador = meta
            while rastreador is not None:
                camino.append(rastreador)
                rastreador = padres[rastreador]
            camino.reverse()
            
            print(f"\n ¡Meta encontrada con {modo}!")
            print(f"Nodos expandidos: {nodos_expandidos} | Longitud del camino: {len(camino) - 1} pasos\n")
            
            print("SIMULACIÓN PASO A PASO DEL CRUCE:")
            for i, est in enumerate(camino):
                imprimir_escenario(est, i)
                
            return nodos_expandidos, camino
            
        for sucesor in obtener_sucesores(nodo_actual):
            if sucesor not in visitados:
                visitados.add(sucesor)
                frontera.append(sucesor)
                padres[sucesor] = nodo_actual  # Guardar padre[cite: 1]
                
    return -1, []

if __name__ == "__main__":
    # Ejecutamos BFS para ver la simulación limpia y óptima
    ejecutar_busqueda(INICIO, META, modo="BFS")