import re

def get_list(cadena):
    regex_lista = r'\{.+\}'
    if re.match(regex_lista, cadena):
        cadena = cadena[1:]
        cadena = cadena[:-1]
        resultado = re.split(r'\s*,\s*', cadena)
        return sorted(resultado)
    return [cadena]

def get_nodo_transicion( nodo, tabla_transicion, funcion_transicion):
    for fila in tabla_transicion:
        if fila[0] == nodo:
            for indice in range(1, len(fila)):
                if tabla_transicion[0][indice] == funcion_transicion:
                    resultado = fila[indice]
                    if resultado == "---":
                        resultado = None
                    return resultado

def get_lista_transicion( lista, tabla_transicion):
    lista_transicion = []
    for func in tabla_transicion[0][1:]:
        lista_nodos = []
        for nodo in lista:
            nodo_transicion = get_nodo_transicion(nodo, tabla_transicion, func)            
            if nodo_transicion:
                for nodo_lista in re.split(r"\s*,\s*", re.sub(r"({|})", "", nodo_transicion)):
                    if nodo_lista not in lista_nodos:
                        lista_nodos.append(nodo_lista)
                
        sorted(lista_nodos)
        if len(lista_nodos) == 0:
            lista_nodos = "---"
        lista_transicion.append(to_string(lista_nodos))
    return lista_transicion

def to_string(elmnt):
    
    if type(elmnt).__name__ == "str":
        return elmnt
    elif type(elmnt).__name__ == "set":
        return str(elmnt)
    elif len(elmnt) == 1:
        for x in elmnt:
            return x
    return str(sorted(elmnt)).replace(r'[', "{").replace(r']', '}').replace('\'', '')

def get_hash(cadena):
    return hash(tuple(get_list(cadena)))


def get_tabla_det(tablaOriginal):


    idx_fila = 0
    origen = tablaOriginal[1][0]
    automataDeterminista = []
    diccionario_nodos = []
    nueva_fila = get_lista_transicion(get_list(origen), tablaOriginal)
    nueva_fila.insert(0, origen)
    
    
    automataDeterminista.append(nueva_fila)
    while ( idx_fila < len(automataDeterminista) and idx_fila < 7):
            
            for nodo in automataDeterminista[idx_fila][1:]:
                
                origen = automataDeterminista[idx_fila][0]
                hash_nodo = get_hash(nodo)
                if hash_nodo not in diccionario_nodos:

                    diccionario_nodos.append(hash_nodo)
                    nueva_fila = get_lista_transicion(get_list(nodo), tablaOriginal)
                    nueva_fila.insert(0, nodo)
                    automataDeterminista.append(nueva_fila)

            idx_fila = idx_fila + 1
        
    
    return automataDeterminista



def imprimir_solucion(tabla):
    print(str(get_tabla_det(tabla)).replace(r'],',"],\n"))
    print()
          

imprimir_solucion( [ [".", "A", "B"],
                      ["q0", "{q1, q3}", "---"],
                      ["q1", "{q1, q2}", "---"],
                      ["q2", "---", "---"],
                      ["q3", "q4", "q3"],
                      ["q4", "---", "---"],
    ])




imprimir_solucion( [ [".", "A",     "B",   "C"],
                       ["p", "q",     "---", "---"],
                       ["q", "p,r,s", "p,r", "s"],
                       ["r", "---",   "p,s", "r,s"],
                       ["s", "---",   "---", "r"]
    ])