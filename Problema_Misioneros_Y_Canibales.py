# -------------------------------------------------------------------------
# Declaración de uso de IA: Estructura general y lógica de búsqueda asistida por IA 
# (Claude/ Sonnet 5.5) el [03-11-2026]. La solución final fue revisada por Camila Caicedo.
# -------------------------------------------------------------------------
import os
import sys
import time
from collections import deque

# Definir variables 
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
    if m_izq > 0 and c_izq > m_izq:      # izquierda en peligro
        return False
    if m_der > 0 and c_der > m_der:      # derecha en peligro
        return False
    return True


def generar_sucesores(estado):
    """Devuelve lista de (nuevo_estado, accion) válidos desde 'estado'."""
    m_izq, c_izq, bote = estado
    sucesores = []
    # Si el bote está a la izquierda, las personas salen de la izquierda (-);
    # si está a la derecha, regresan a la izquierda (+).
    signo = -1 if bote == 1 else 1       # signo = -sigma(b)

    for dm, dc in ACCIONES:
        nuevo = (m_izq + signo * dm, c_izq + signo * dc, 1 - bote)
        if es_valido(nuevo):
            sucesores.append((nuevo, (dm, dc)))
    return sucesores


def describir_accion(estado, accion): 
    dm, dc = accion
    sentido = "izq -> der" if estado[2] == 1 else "der -> izq"
    return f"Cruzan {dm} misionero(s) y {dc} caníbal(es) ({sentido})"

# Función principal de búsqueda no informada (BFS/DFS) 
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
                "generados": len(visitados),     # nodos que llegaron a la frontera (incluye el inicial)
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

# Función para imprimir la solución encontrada
def imprimir_solucion(res):
    print(f"\n{'=' * 60}")
    print(f"  {res['modo']}: secuencia de acciones")
    print(f"{'=' * 60}")
    print(f"Estado inicial: {res['estados'][0]}")
    for i, (padre, accion) in enumerate(res["acciones"], start=1):
        print(f"{i:2d}. {describir_accion(padre, accion)}  ->  {res['estados'][i]}")

def tabla_comparativa(resultados):
    print(f"\n{'=' * 60}")
    print(" TABLA COMPARATIVA DE RESULTADOS")
    print(f"{'=' * 60}")
    print(f"{'Algoritmo':<10}{'Longitud':>10}{'Expandidos':>13}{'Máx.Frontera':>14}{'Tiempo (ms)':>13}")
    for r in resultados:
        print(f"{r['modo']:<10}{r['longitud']:>10}{r['expandidos']:>13}"
              f"{r['max_frontera']:>14}{r['tiempo'] * 1000:>13.4f}")

# ---------------------------------------------------------------
# SIMULACIÓN ANIMADA EN CONSOLA | M = misionero, C = caníbal
# ---------------------------------------------------------------
PAUSA_CUADRO = 0.12      # segundos entre cuadros (velocidad de la animación)
PAUSA_ESTADO = 0.9       # pausa cuando el bote está en una orilla
FRAMES_CRUCE = 10        # cuadros que dura cada cruce del río
ANCHO_RIO = 30
ANCHO_ORILLA = 13
ALTO_CUADRO = 7          # líneas que ocupa cada cuadro (fijo)

def _orilla(m, c):
    return " ".join("M" * m + "C" * c).center(ANCHO_ORILLA)

def construir_cuadro(titulo, mensaje, izq, der, pos_bote, carga=(0, 0)):
    """Devuelve las 7 líneas del cuadro: izq/der = (m, c) en cada orilla."""
    texto_bote = "\\_" + ("M" * carga[0] + "C" * carga[1]).center(2) + "_/"
    rio = list("~" * ANCHO_RIO)
    rio[pos_bote:pos_bote + len(texto_bote)] = list(texto_bote)

    borde = "+" + "-" * ANCHO_ORILLA + "+" + "-" * ANCHO_RIO + "+" + "-" * ANCHO_ORILLA + "+"
    ancho_total = len(borde)
    cabecera = ("|" + "ORILLA IZQ".center(ANCHO_ORILLA) + "|" + "RÍO".center(ANCHO_RIO)
                + "|" + "ORILLA DER".center(ANCHO_ORILLA) + "|")
    escena = f"|{_orilla(*izq)}|{''.join(rio)}|{_orilla(*der)}|"
    return [
        titulo.ljust(ancho_total),
        mensaje.ljust(ancho_total),
        borde, cabecera, borde, escena, borde,
    ]

def _mostrar(lineas, primera):
    """Dibuja el cuadro. Si no es el primero, sube el cursor y sobrescribe."""
    if not primera:
        sys.stdout.write(f"\033[{ALTO_CUADRO}A")
    for linea in lineas:
        sys.stdout.write("\033[K" + linea + "\n")
    sys.stdout.flush()

def animar_solucion(res):
    """Anima en el mismo sitio la solución encontrada por el algoritmo."""
    os.system("")                       # habilita secuencias ANSI en Windows
    estados, acciones = res["estados"], res["acciones"]
    modo, total = res["modo"], len(acciones)
    pos_izq, pos_der = 0, ANCHO_RIO - 6  # posiciones del bote en cada orilla

    def orillas(m_izq, c_izq):
        return (m_izq, c_izq), (TOTAL_M - m_izq, TOTAL_C - c_izq)

    sys.stdout.write("\033[?25l")       # oculta el cursor durante la animación
    try:
        titulo = f" SIMULACIÓN {modo}"
        izq, der = orillas(*estados[0][:2])
        _mostrar(construir_cuadro(f"{titulo} | Viaje 0/{total} | Estado {estados[0]}",
                                  " Situación inicial", izq, der, pos_izq), True)
        time.sleep(PAUSA_ESTADO)

        for i, (padre, (dm, dc)) in enumerate(acciones, start=1):
            nuevo = estados[i]
            hacia_der = padre[2] == 1
            texto = f" {describir_accion(padre, (dm, dc))}"
            cabecera = f"{titulo} | Viaje {i}/{total} | Estado {padre}"

            # Orillas durante el cruce: los pasajeros no están en ninguna orilla
            der_antes = (TOTAL_M - padre[0], TOTAL_C - padre[1])
            if hacia_der:
                izq = (nuevo[0], nuevo[1])                   # izquierda sin los pasajeros
                der = der_antes
                ini, fin = pos_izq, pos_der
            else:
                izq = (padre[0], padre[1])
                der = (der_antes[0] - dm, der_antes[1] - dc)  # derecha sin los pasajeros
                ini, fin = pos_der, pos_izq

            for f in range(FRAMES_CRUCE + 1):
                pos = round(ini + (fin - ini) * f / FRAMES_CRUCE)
                _mostrar(construir_cuadro(cabecera, texto, izq, der, pos, (dm, dc)), False)
                time.sleep(PAUSA_CUADRO)

            # Llegada: el estado resultante
            izq, der = orillas(nuevo[0], nuevo[1])
            pos_final = pos_izq if nuevo[2] == 1 else pos_der
            _mostrar(construir_cuadro(f"{titulo} | Viaje {i}/{total} | Estado {nuevo}",
                                      " Llegaron a la otra orilla", izq, der, pos_final), False)
            time.sleep(PAUSA_ESTADO)

        _mostrar(construir_cuadro(f"{titulo} | Viaje {total}/{total} | Estado {estados[-1]}",
                                  f" ¡META ALCANZADA en {total} viajes!", izq, der, pos_final), False)
        time.sleep(1.5)
    finally:
        sys.stdout.write("\033[?25h")   # vuelve a mostrar el cursor
        sys.stdout.flush()

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

    try:
        input("\nPresiona Enter para ver la simulación animada...")
    except EOFError:
        pass

    for res in resultados:
        print()
        animar_solucion(res)