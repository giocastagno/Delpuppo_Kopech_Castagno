from simpleai.search import breadth_first, SearchProblem, astar, greedy, depth_first
from simpleai.search.viewers import BaseViewer

soldados = (
    (1,0,1,0,1,0,1,0,0,0),
    (0,0,0,0,1,0,0,0,0,0),
    (1,0,0,0,0,0,0,0,0,0),
    (0,1,0,0,0,0,1,1,0,1),
    (1,0,0,0,0,0,0,1,1,0),
    (0,0,0,0,1,0,0,0,0,1),
    (1,0,0,0,0,1,0,0,0,1),
    (1,0,0,0,0,0,0,1,0,0),
    (0,0,1,0,1,0,0,0,0,1),
    (0,1,0,0,1,0,1,1,0,0),
)

pos_rey = (5,3)

def donde_esta_rey(state, rey):
    for indice_fila, fila in enumerate(state):
        for indice_columna, numero_actual in enumerate(fila):
            if numero_actual == rey:
                return indice_fila, indice_columna

def t2l(t):
    return list(list(r) for r in t)

def l2t(l):
    return tuple(tuple(r) for r in l)

def colocar_rey(soldados, pos_rey):
    c = 0
    tamanio = len(soldados[0])
    fila_rey = pos_rey[0]
    col_rey = pos_rey[1]
    """if tamanio == pos_rey[0] or tamanio == pos_rey[1]:
        return 'No se puede colocar el rey en el borde del tablero'"""
    if soldados[fila_rey][col_rey] == 0:
        if fila_rey > 0 and soldados[fila_rey - 1][col_rey] == 1:
            c += 1
        if fila_rey < tamanio-1 and soldados[fila_rey + 1][col_rey] == 1:
            c += 1
        if col_rey > 0 and soldados[fila_rey][col_rey - 1] == 1:
            c += 1
        if col_rey < tamanio-1 and soldados[fila_rey][col_rey + 1] == 1:
            c += 1
        if c <= 1:
            soldados = t2l(soldados)
            soldados[pos_rey[0]][pos_rey[1]] = 2
            soldados = l2t(soldados)
        else:
            return 'El rey no puede estar entre 2 o mas soldados'
    else:
        return 'La posicion no existe o hay un soldado en dicha posicion'
    return soldados
soldados = colocar_rey(soldados, pos_rey)

def definir_soluciones(soldados):
    rango = len(soldados[0])
    soluciones = []
    for f_casilla in range(rango):
        for c_casilla in range(rango):
            c = 0
            if soldados[f_casilla][c_casilla] == 0:
                #PREGUNTAMOS SI LA SOLUCION PUEDE ESTAR EN ALGUNA DE LAS 4 ESQUINAS
                #ARRIBA-IZQUIERDA
                if f_casilla == 0 and c_casilla == 0:
                    if not (soldados[0][1] == 1 and soldados[1][0] == 1):
                        soluciones.append((f_casilla,c_casilla))
                #ARRIBA-DERECHA
                if f_casilla == 0 and c_casilla == rango-1:
                    if not(soldados[0][rango-2] == 1 and soldados[1][rango-1] == 1):
                        soluciones.append((f_casilla,c_casilla))
                #ABAJO-IZQUIERDA
                if f_casilla == rango-1 and c_casilla == 0:
                    if not(soldados[rango-2][0] == 1 and soldados[rango-1][1] == 1):
                        soluciones.append((f_casilla,c_casilla))
                #ABAJO-DERECHA
                if f_casilla == rango-1 and c_casilla == rango-1:
                    if not(soldados[rango-2][rango-1] == 1 and soldados[rango-1][rango-2] == 1):
                        soluciones.append((f_casilla,c_casilla))
                #PREGUNTAMOS SI LA SOLUCION PUEDE ESTAR EN LOS BORDES SIN LAS ESQUINAS
                #BORDE DE ARRIBA        
                if f_casilla == 0 and c_casilla > 0 and c_casilla < rango-1:
                    if soldados[0][c_casilla-1] == 1:
                        c += 1
                    if soldados[0][c_casilla+1] == 1:
                        c += 1
                    if soldados[1][c_casilla] == 1:
                        c += 1
                    if c <= 1:
                        soluciones.append((f_casilla,c_casilla))
                #BORDE DE ABAJO
                if f_casilla == rango-1 and c_casilla > 0 and c_casilla < rango-1:
                    if soldados[rango-1][c_casilla-1] == 1:
                        c += 1
                    if soldados[rango-1][c_casilla+1] == 1:
                        c += 1
                    if soldados[rango-2][c_casilla] == 1:
                        c += 1
                    if c <= 1:
                        soluciones.append((f_casilla,c_casilla))
                #BORDE IZQUIERDA
                if f_casilla > 0 and f_casilla < rango-1 and c_casilla == 0:
                    if soldados[f_casilla-1][0] == 1:
                        c += 1
                    if soldados[f_casilla+1][0] == 1:
                        c += 1
                    if soldados[f_casilla][1] == 1:
                        c += 1
                    if c <= 1:
                        soluciones.append((f_casilla,c_casilla))
                #BORDE DERECHA
                if f_casilla > 0 and f_casilla < rango-1 and c_casilla == rango-1:
                    if soldados[f_casilla-1][rango-1] == 1:
                        c += 1
                    if soldados[f_casilla+1][rango-1] == 1:
                        c += 1
                    if soldados[f_casilla][rango-2] == 1:
                        c += 1
                    if c <= 1:
                        soluciones.append((f_casilla,c_casilla))
    return soluciones
soluciones = definir_soluciones(soldados)

class Hnefatafl(SearchProblem):
        
    def cost(self, state1, action, state2):
        return 1
    
    def is_goal(self, state):
        fila_rey, col_rey = donde_esta_rey(state, 2)
        return (fila_rey, col_rey) in soluciones

    def actions(self, state):
        acciones = []
        c = 0
        fila_rey, col_rey = donde_esta_rey(state, 2)
        if state[fila_rey - 1][col_rey] == 0:
            if (fila_rey - 1) > 0 and state[fila_rey - 2][col_rey] == 1:
                c += 1
            if state[fila_rey - 1][col_rey - 1] == 1:
                c += 1
            if state[fila_rey - 1][col_rey + 1] == 1:
                c += 1
            if c <= 1:
                acciones.append((fila_rey - 1,col_rey))
        c = 0
        if state[fila_rey + 1][col_rey] == 0:
            if (fila_rey + 1) < len(state[0])-1 and state[fila_rey + 2][col_rey] == 1:
                c += 1
            if state[fila_rey + 1][col_rey - 1] == 1:
                c += 1
            if state[fila_rey + 1][col_rey + 1] == 1:
                c += 1
            if c <= 1:
                acciones.append((fila_rey + 1,col_rey))
        c = 0
        if state[fila_rey][col_rey - 1] == 0:
            if (col_rey - 1) > 0 and state[fila_rey][col_rey - 2] == 1:
                c += 1
            if state[fila_rey - 1][col_rey - 1] == 1:
                c += 1
            if state[fila_rey + 1][col_rey - 1] == 1:
                c += 1
            if c <= 1:
                acciones.append((fila_rey,col_rey - 1))
        c = 0
        if state[fila_rey][col_rey + 1] == 0:
            if (col_rey + 1) < len(state[0])-1 and state[fila_rey][col_rey + 2] == 1:
                c += 1
            if state[fila_rey - 1][col_rey + 1] == 1:
                c += 1
            if state[fila_rey + 1][col_rey + 1] == 1:
                c += 1
            if c <= 1:
                acciones.append((fila_rey,col_rey + 1))
        return acciones
    
    def result(self, state, action):
        fila_rey, col_rey = donde_esta_rey(state, 2)
        fila_new, col_new = action
        state = t2l(state)
        state[fila_rey][col_rey] = 0
        state[fila_new][col_new] = 2
        state = l2t(state)
        return state

    def heuristic(self, state):
        tamanio_fila = 0
        tamanio_col = 0
        fila_rey, col_rey = donde_esta_rey(state, 2)
        if fila_rey >= len(state[0])/ 2:
            tamanio_fila = len(state[0]) - 1 - fila_rey
        else:
            tamanio_fila = fila_rey
        if col_rey >= len(state[0])/ 2:
            tamanio_col = len(state[0]) - 1 - col_rey
        else:
            tamanio_col = col_rey
        if tamanio_col >= tamanio_fila:
            return tamanio_fila
        else:
            return tamanio_col

def resolver(metodo_busqueda, posicion_rey, controlar_estados_repetidos):
    problema = Hnefatafl(soldados)
    if metodo_busqueda == "astar":
        return astar(problema, graph_search = controlar_estados_repetidos)
    if metodo_busqueda == "breadth_first":
        resultado = breadth_first(problema, graph_search = controlar_estados_repetidos)
        return resultado
    if metodo_busqueda == "depth_first":
        return depth_first(problema, graph_search = controlar_estados_repetidos)
    if metodo_busqueda == "greedy":
        return greedy(problema, graph_search = controlar_estados_repetidos)


    
if __name__ == '__main__':
    problema = Hnefatafl(soldados)
    Visor = BaseViewer()
# Amplitud - arbol
    #resultado = breadth_first(problema,graph_search=False,viewer=Visor)

# Amplitud - grafo
    #resultado = breadth_first(problema, graph_search=True, viewer=Visor)

# Profundidad - arbol
    #resultado = depth_first(problema, graph_search=False, viewer=Visor)

# Profundidad - grafo
    #resultado = depth_first(problema, graph_search=True,viewer=Visor)

# Avara - arbol
    #resultado = greedy(problema, graph_search=False,viewer=Visor)

# Avara - grafo
    #resultado = greedy(problema, graph_search=True,viewer=Visor)

# A* - arbol
    #resultado = astar(problema, graph_search=False, viewer=Visor)

# A* - grafo
    resultado = astar(problema, graph_search=True,viewer=Visor)


    print 'Estado meta:'
    print resultado.state
    print 'Camino:'
    print len(resultado.path())
    for accion, estado in resultado.path():
        print 'Movi', accion
        print 'Llegue a', estado

    print 'Estadisticas',Visor.stats

