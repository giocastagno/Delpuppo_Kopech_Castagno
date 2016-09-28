import random
from simpleai.search import (SearchProblem, hill_climbing,
                             hill_climbing_random_restarts,
                             hill_climbing_stochastic,
                             simulated_annealing, beam)
from simpleai.search.viewers import BaseViewer

def t2l(t):
    return list(list(r) for r in t)

def l2t(l):
    return tuple(tuple(r) for r in l)

def sumar_puntos(estado,fila,columna):
    #Abajo
    c = 0
    puntos = 0
    if fila - 1 >= 0:
        if estado[fila-1][columna] == 1:
            c += 1
    #Arriba
    if fila + 1 <= 9:
        if estado[fila+1][columna] == 1:
            c += 1        
    #Izquierda
    if columna - 1 >= 0:
        if estado[fila][columna-1] == 1:
            c += 1 
    #Derecha
    if columna + 1 <= 9:
        if estado[fila][columna+1] == 1:
            c += 1
    if c > 1:
        if fila == 0 or fila == 9 or columna == 0 or columna == 9:
            puntos = 3
        else:
            puntos = 1
    return puntos

def dibujar_tablero():
    for fila in range(10):
        for columna in range(10):
            if result.state[fila][columna] == 1:
                print '|*',
            else:
                print '| ',
        print
        print '-' * 40
    return None

INICIAL = ((1, ) * 10, ) * 3 + ((0, ) * 10, ) * 7

class Hnefatafl2(SearchProblem):
    def actions(self, state):
        acciones = []
        for lugarfila in range(10):
            for lugarcol in range(10):
                if state[lugarfila][lugarcol] != 1:
                    for soldadofila in range(10):
                        for soldadocol in range(10):
                            if state[soldadofila][soldadocol] == 1:
                                acciones.append((soldadofila, soldadocol, lugarfila, lugarcol))
        return acciones

    def result(self, state, action):
        
        fila_soldado, col_soldado = action[0], action[1]
        fila_lugar, col_lugar = action[2], action[3]
        state = t2l(state)
        state[fila_soldado][col_soldado] = 0
        state[fila_lugar][col_lugar] = 1
        state = l2t(state)
        return state
            
    def value(self, state):
        total = 0
        for fila in range(10):
            for col in range(10):
                if state[fila][col] == 0:
                    total += sumar_puntos(state,fila,col)
        return total

    def generate_random_state(self):
        estado = ((0, ) * 10, ) * 10
        estado = t2l(estado)
        c = 0;
        while (c < 30): 
            fila = random.randint(0, 9)
            col = random.randint(0, 9)
            if estado[fila][col] == 0:
                estado[fila][col] = 1
                c += 1
        estado = l2t(estado)
        return estado

def resolver(metodo_busqueda, iteraciones, haz, reinicios):
    problema_inicial = Hnefatafl2(INICIAL)
    if metodo_busqueda == "hill_climbing":
        return hill_climbing(problema_inicial, iteraciones)
    if metodo_busqueda == "hill_climbing_stochastic":
        return hill_climbing_stochastic(problema_inicial, iteraciones)
    if metodo_busqueda == "beam":
        return beam(problema_inicial, haz, iteraciones)
    if metodo_busqueda == "hill_climbing_random_restarts":
        return hill_climbing_random_restarts(problema_inicial, reinicios, iteraciones)
    if metodo_busqueda == "simulated_annealing":
        return simulated_annealing(problema_inicial, iterations_limit = iteraciones)

if __name__ == '__main__':
##    print 'ASCENSO DE COLINA'
##    for i in range(10):
##        result = hill_climbing(Hnefatafl2(INICIAL), 200)
##        dibujar_tablero()
##        print result.value
##
##    print 'ASCENSO DE COLINA ESTOCASTICA'
##    for i in range(10):
##        result = hill_climbing_stochastic(Hnefatafl2(INICIAL), 200)
##        dibujar_tablero()
##        print result.value
##
    print 'HAZ LOCAL'
    for i in range(10):
        result = beam(Hnefatafl2(INICIAL), 20, 200)
        dibujar_tablero()
        print result.value

##    print 'ASCENSO DE COLINA CON REINICIOS ALEATORIOS'
##    for i in range(10):
##        result = hill_climbing_random_restarts(Hnefatafl2(INICIAL), 20, iterations_limit = 200)
##        dibujar_tablero()
##        print result.value

##    print 'TEMPLE SIMULADO'
##    for i in range(10):
##        result = simulated_annealing(Hnefatafl2(INICIAL), iterations_limit = 200)
##        dibujar_tablero()
##        print result.value




