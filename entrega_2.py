from simpleai.search import (CspProblem, backtrack, min_conflicts,
                             MOST_CONSTRAINED_VARIABLE, 
                             LEAST_CONSTRAINING_VALUE, 
                             HIGHEST_DEGREE_VARIABLE)


casillas = list('abcdefghijklmnopq')

dominios = {casilla: ['laser','motor','cabina','bahia','sistema','escudo','bateria']
            for casilla in casillas}


#Motores ubicarse en slots traseros o en los 4 slots laterales 
for casilla in casillas:
    if casilla not in list('efmnopq'):
        dominios[casilla].remove('motor')

#combinaciones de a pares SE FUE =P
combinaciones = (('a', 'b'),('a', 'c'),('b', 'd'),('c', 'd'),('d', 'f'),('e', 'c'),('e', 'g'),
    ('f', 'h'),('g', 'h'),('g', 'i'),('h', 'i'),('i', 'j'),('j', 'k'),('k', 'l'),
    ('l', 'm'),('l', 'n'),('l', 'p'),('o', 'p'),('p', 'q'),
    )

#combinaciones de vecinos conectados LINEAS VERDES ;)
combinaciones2 = (('a', 'b', 'c'),
    ('b', 'a', 'd'),
    ('c', 'a', 'd', 'e'),
    ('d', 'b', 'c', 'f'),
    ('e', 'c', 'g'),
    ('f', 'd', 'h'),
    ('g', 'e', 'h', 'i'),
    ('h', 'f', 'g', 'i'),
    ('i', 'g', 'h', 'j'),
    ('j', 'i', 'k'),
    ('k', 'j', 'l'),
    ('l', 'k', 'm', 'n', 'p'),
    ('m', 'l'),
    ('n', 'l'),
    ('o', 'p'),
    ('q', 'p'),
    ('p', 'l', 'o', 'q'),
    )


#No es posible instalar dos modulos iguales conectados entre si
def diferentes (variables, valores):
    return valores[0] != valores[1]

#No puede haber baterias conectadas a lasers
def bateria_laser (variables, valores):
    if valores[0] == 'laser':
        return ('bateria' not in valores)
    if valores[0] == 'bateria':
        return ('laser' not in valores)
    return True

#Sistemas de vida extraterrestre tienen que ubicarse conectados a cabinas.
def sistema_cabina(variables, valores):
    if valores[0] == 'sistema': 
        return 'cabina' in valores
    return True
    

#Las cabinas no pueden estar conectadas a los motores
def cabina_motor (variables, valores):
    if valores[0] == 'motor':
        return ('cabina' not in valores)
    if valores[0] == 'cabina':
        return ('motor' not in valores)
    return True

#Los escudos y sistemas de vida extraterrestre no pueden estar conectados entre si
def sistema_escudo (variables, valores):
    if valores[0] == 'sistema':
        return ('escudo' not in valores)
    if valores[0] == 'escudo':
        return ('sistema' not in valores)
    return True

#Bahias de carga al menos una cabina conectada
def bahia_cabina (variables, valores):
    if valores[0] == 'bahia': 
        return 'cabina' in valores
    return True    

#Baterias tienen 2 de: Lasers, Cabinas, Escudos y Sistemas de vida E
def bateria_2 (variables, valores):
    c = 0
    if valores[0] == 'bateria':
        for val in ['laser','cabina','escudo','sistema']:
            c += 1
        return c > 1
    return True

#Que no queden casillas vacias
def casillas_llenas(variables, valores):
    for casilla in casillas:
        if  len(dominios[casilla]) > 0:
            return True
    
restricciones = []
    
for variable in combinaciones:
    restricciones.append((variable, diferentes))

for variable in combinaciones2:
    restricciones.append((variable, sistema_cabina))
    restricciones.append((variable, bahia_cabina))
    restricciones.append((variable, bateria_2))
    restricciones.append((variable, bateria_laser)) 
    restricciones.append((variable, cabina_motor)) 
    restricciones.append((variable, sistema_escudo))
    
restricciones.append((casillas, casillas_llenas))

def resolver(metodo_busqueda, iteraciones):
    problema = CspProblem(casillas, dominios, restricciones)
    if metodo_busqueda == "backtrack":
        return backtrack(problema) 
    if metodo_busqueda == "min_conflicts":
        return min_conflicts(problema, iterations_limit = iteraciones)

if __name__ == '__main__':
    problema = CspProblem(casillas, dominios, restricciones)
    resultado = backtrack(problema)
    print 'backtrack:'
    print resultado

    resultado = min_conflicts(problema, iterations_limit=500)
    print 'min conflicts:'
    print resultado
