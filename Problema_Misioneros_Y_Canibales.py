import time
from collections import deque

# ---------------------------------------------------------------
# MODELADO DEL PROBLEMA
# Estado: (misioneros_izq, canibales_izq, bote_izq)
#   bote_izq = 1 -> el bote está en la orilla izquierda
#   bote_izq = 0 -> el bote está en la orilla derecha
# Las cantidades de la orilla derecha se deducen: 3 - izq
# ---------------------------------------------------------------
TOTAL_M = 3
TOTAL_C = 3
CAPACIDAD_BOTE = 2

INICIO = (3, 3, 1)
META = (0, 0, 0)

# Acciones posibles: (misioneros que suben, caníbales que suben)
ACCIONES = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]


def es_valido(estado):
    """Un estado es válido si no hay más caníbales que misioneros
    en ninguna orilla (salvo que no haya misioneros en esa orilla)."""
    m_izq, c_izq, _ = estado
    m_der, c_der = TOTAL_M - m_izq, TOTAL_C - c_izq

    if not (0 <= m_izq <= TOTAL_M and 0 <= c_izq <= TOTAL_C):
        return False
    if m_izq > 0 and c_izq > m_izq:
        return False
    if m_der > 0 and c_der > m_der:
        return False
    return True


def generar_sucesores(estado):
    """Devuelve lista de (nuevo_estado, accion) válidos desde 'estado'."""
    m_izq, c_izq, bote = estado
    sucesores = []
    # Si el bote está a la izquierda, las personas salen de la izquierda (-);
    # si está a la derecha, regresan a la izquierda (+).
    signo = -1 if bote == 1 else 1

    for dm, dc in ACCIONES:
        nuevo = (m_izq + signo * dm, c_izq + signo * dc, 1 - bote)
        if es_valido(nuevo):
            sucesores.append((nuevo, (dm, dc)))
    return sucesores


def describir_accion(estado, accion):
    dm, dc = accion
    sentido = "izquierda -> derecha" if estado[2] == 1 else "derecha -> izquierda"
    return f"Cruzan {dm} misionero(s) y {dc} caníbal(es) ({sentido})"


# ---------------------------------------------------------------
# BÚSQUEDA NO INFORMADA (misma estructura que el código del laberinto)
# ---------------------------------------------------------------
def ejecutar_busqueda(inicio, meta, modo="BFS"):
    frontera = deque([inicio]) if modo == "BFS" else [inicio]
    visitados = set([inicio])
    padres = {inicio: (None, None)}  # estado -> (estado_padre, accion)
    nodos_expandidos = 0
    max_frontera = 1
    t0 = time.perf_counter()

    while frontera:
        if modo == "BFS":
            nodo_actual = frontera.popleft()   # Cola (FIFO)
        else:
            nodo_actual = frontera.pop()       # Pila (LIFO)

        nodos_expandidos += 1

        if nodo_actual == meta:
            # Reconstrucción del camino desde la meta hacia el inicio
            estados, acciones = [], []
            rastreador = meta
            while rastreador is not None:
                estados.append(rastreador)
                padre, accion = padres[rastreador]
                if accion is not None:
                    acciones.append((padre, accion))
                rastreador = padre
            estados.reverse()
            acciones.reverse()

            return {
                "modo": modo,
                "estados": estados,
                "acciones": acciones,
                "longitud": len(estados) - 1,
                "expandidos": nodos_expandidos,
                "max_frontera": max_frontera,
                "tiempo": time.perf_counter() - t0,
            }

        for sucesor, accion in generar_sucesores(nodo_actual):
            if sucesor not in visitados:
                visitados.add(sucesor)
                frontera.append(sucesor)
                padres[sucesor] = (nodo_actual, accion)

        max_frontera = max(max_frontera, len(frontera))

    return None


def imprimir_solucion(res):
    print(f"\n{'=' * 60}")
    print(f"  {res['modo']}: secuencia de acciones")
    print(f"{'=' * 60}")
    print(f"Estado inicial: {res['estados'][0]}")
    for i, (padre, accion) in enumerate(res["acciones"], start=1):
        print(f"{i:2d}. {describir_accion(padre, accion)}  ->  {res['estados'][i]}")
    print(f"\nLongitud del camino : {res['longitud']} cruces")
    print(f"Nodos expandidos    : {res['expandidos']}")
    print(f"Tamaño máx. frontera: {res['max_frontera']}")
    print(f"Tiempo de ejecución : {res['tiempo'] * 1000:.4f} ms")


def tabla_comparativa(resultados):
    print(f"\n{'=' * 60}")
    print("  COMPARACIÓN EMPÍRICA")
    print(f"{'=' * 60}")
    print(f"{'Algoritmo':<10}{'Longitud':>10}{'Expandidos':>13}{'Máx.Frontera':>14}{'Tiempo (ms)':>13}")
    for r in resultados:
        print(f"{r['modo']:<10}{r['longitud']:>10}{r['expandidos']:>13}"
              f"{r['max_frontera']:>14}{r['tiempo'] * 1000:>13.4f}")


if __name__ == "__main__":
    resultados = []
    for modo in ("BFS", "DFS"):
        res = ejecutar_busqueda(INICIO, META, modo)
        if res is None:
            print(f"{modo}: no se encontró solución")
            continue
        imprimir_solucion(res)
        resultados.append(res)

    tabla_comparativa(resultados)