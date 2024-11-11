def encontrar_vacio(tablero):
    """
    Encuentra una posición vacía en el tablero (representada por 0).
    
    Args:
        tablero (List[List[int]]): El tablero de Sudoku 9x9
        
    Returns:
        tuple: (fila, columna) de la posición vacía, o None si no hay espacios vacíos
    """
    for fila in range(9):
        for columna in range(9):
            if tablero[fila][columna] == 0:
                return (fila, columna)
    return None

def es_valido(tablero, numero, posicion_fila, posicion_columna):
    """
    Verifica si es válido colocar un número en una posición específica.
    
    Args:
        tablero (List[List[int]]): El tablero de Sudoku 9x9
        numero (int): Número a verificar (1-9)
        posicion_fila (int): Índice de la fila
        posicion_columna (int): Índice de la columna
        
    Returns:
        bool: True si es válido colocar el número, False en caso contrario
    """
    # Verificar fila
    for columna in range(9):
        if tablero[posicion_fila][columna] == numero and columna != posicion_columna:
            return False
    
    # Verificar columna
    for fila in range(9):
        if tablero[fila][posicion_columna] == numero and fila != posicion_fila:
            return False
    
    # Verificar cuadrícula 3x3
    cuadricula_fila = (posicion_fila // 3) * 3
    cuadricula_columna = (posicion_columna // 3) * 3
    
    for fila in range(cuadricula_fila, cuadricula_fila + 3):
        for columna in range(cuadricula_columna, cuadricula_columna + 3):
            if tablero[fila][columna] == numero and (fila, columna) != (posicion_fila, posicion_columna):
                return False
    
    return True

def resolver_sudoku(tablero):
    """
    Resuelve el tablero de Sudoku usando backtracking.
    
    Args:
        tablero (List[List[int]]): El tablero de Sudoku 9x9
        
    Returns:
        bool: True si se encontró una solución, False en caso contrario
    """
    vacio = encontrar_vacio(tablero)
    if not vacio:
        return True
    
    fila, columna = vacio
    
    for numero in range(1, 10):
        if es_valido(tablero, numero, fila, columna):
            tablero[fila][columna] = numero
            
            if resolver_sudoku(tablero):
                return True
            
            tablero[fila][columna] = 0
    
    return False

def validar_tablero_completo(tablero):
    """
    Verifica si un tablero de Sudoku está completamente resuelto y es válido.
    
    Args:
        tablero (List[List[int]]): El tablero de Sudoku 9x9
        
    Returns:
        bool: True si el tablero está resuelto correctamente, False en caso contrario
    """
    # Verificar que no haya espacios vacíos
    if encontrar_vacio(tablero):
        return False
    
    # Verificar todas las filas
    for fila in range(9):
        if set(tablero[fila]) != set(range(1, 10)):
            return False
    
    # Verificar todas las columnas
    for columna in range(9):
        if set(tablero[fila][columna] for fila in range(9)) != set(range(1, 10)):
            return False
    
    # Verificar todas las cuadrículas 3x3
    for bloque_fila in range(3):
        for bloque_columna in range(3):
            numeros = set()
            for fila in range(3):
                for columna in range(3):
                    numeros.add(tablero[bloque_fila * 3 + fila][bloque_columna * 3 + columna])
            if numeros != set(range(1, 10)):
                return False
    
    return True

def generar_sudoku_vacio():
    """
    Genera un tablero de Sudoku vacío.
    
    Returns:
        List[List[int]]: Un tablero de Sudoku 9x9 vacío
    """
    return [[0 for _ in range(9)] for _ in range(9)]

def copiar_tablero(tablero):
    """
    Crea una copia profunda del tablero de Sudoku.
    
    Args:
        tablero (List[List[int]]): El tablero de Sudoku 9x9 a copiar
        
    Returns:
        List[List[int]]: Una nueva copia del tablero
    """
    return [fila[:] for fila in tablero]

def imprimir_tablero(tablero):
    """
    Imprime el tablero de Sudoku en un formato legible.
    
    Args:
        tablero (List[List[int]]): El tablero de Sudoku 9x9 a imprimir
    """
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            
            if j == 8:
                print(tablero[i][j])
            else:
                print(str(tablero[i][j]) + " ", end="")

def obtener_candidatos(tablero, fila, columna):
    """
    Obtiene todos los números válidos posibles para una posición dada.
    
    Args:
        tablero (List[List[int]]): El tablero de Sudoku 9x9
        fila (int): Índice de la fila
        columna (int): Índice de la columna
        
    Returns:
        List[int]: Lista de números válidos para esa posición
    """
    candidatos = []
    if tablero[fila][columna] == 0:
        for numero in range(1, 10):
            if es_valido(tablero, numero, fila, columna):
                candidatos.append(numero)
    return candidatos