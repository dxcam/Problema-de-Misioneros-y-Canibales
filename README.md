**Nombre:** Camila Caicedo

**Paralelo:** GR1CC

**Fecha de entrega:** 03/11/2026

---

# Problema de Misioneros y Caníbales

## Objetivo

Modelar matemáticamente un problema clásico de IA, abstraerlo a código Python y evaluar empíricamente el rendimiento de las estrategias de búsqueda no informada (BFS y DFS).

## Reto

Tres misioneros y tres caníbales deben cruzar un río en un bote que solo puede llevar a dos personas. Si en algún momento hay más caníbales que misioneros en cualquiera de las dos orillas, los caníbales se comerán a los misioneros.

## Comparación de resultados

| Algoritmo | Longitud | Expandidos | Máx. Frontera | Tiempo (ms) |
|-----------|-----------|------------|---------------|-------------|
| BFS | 11 | 15 | 3 | 0.0463 |
| DFS | 11 | 12 | 4 | 0.0364 |