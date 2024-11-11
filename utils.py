import random
import json
import os
from typing import List, Tuple, Optional, Dict
import time

class SudokuUtils:
    @staticmethod
    def cargar_configuracion(archivo: str = "config.json") -> Dict:
        """
        Carga la configuración del juego desde un archivo JSON.
        
        Args:
            archivo (str): Ruta al archivo de configuración
            
        Returns:
            Dict: Diccionario con la configuración
        """
        config_default = {
            "dificultad": "normal",
            "tema_color": "clasico",
            "mostrar_tiempo": True,
            "sonidos": True,
            "tamano_fuente": 40
        }
        
        try:
            if os.path.exists(archivo):
                with open(archivo, 'r') as f:
                    return json.load(f)
            return config_default
        except Exception as e:
            print(f"Error al cargar la configuración: {e}")
            return config_default

    @staticmethod
    def guardar_configuracion(config: Dict, archivo: str = "config.json") -> bool:
        """
        Guarda la configuración del juego en un archivo JSON.
        
        Args:
            config (Dict): Diccionario con la configuración
            archivo (str): Ruta al archivo de configuración
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            with open(archivo, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar la configuración: {e}")
            return False

    @staticmethod
    def generar_sudoku(dificultad: str = "normal") -> List[List[int]]:
        """
        Genera un nuevo puzzle de Sudoku con la dificultad especificada.
        
        Args:
            dificultad (str): Nivel de dificultad ("facil", "normal", "dificil")
            
        Returns:
            List[List[int]]: Tablero de Sudoku generado
        """
        # Definir número de casillas a eliminar según dificultad
        casillas_eliminar = {
            "facil": 30,
            "normal": 45,
            "dificil": 60
        }
        
        # Generar un Sudoku resuelto
        tablero = [[0 for _ in range(9)] for _ in range(9)]
        SudokuUtils._llenar_diagonal(tablero)
        SudokuUtils._resolver_sudoku(tablero)
        
        # Eliminar números según la dificultad
        num_eliminar = casillas_eliminar.get(dificultad, 45)
        return SudokuUtils._eliminar_numeros(tablero, num_eliminar)

    @staticmethod
    def _llenar_diagonal(tablero: List[List[int]]) -> None:
        """
        Llena las cajas diagonales 3x3 del tablero con números aleatorios.
        
        Args:
            tablero (List[List[int]]): Tablero a llenar
        """
        numeros = list(range(1, 10))
        for i in range(0, 9, 3):
            random.shuffle(numeros)
            for fila in range(3):
                for col in range(3):
                    tablero[fila + i][col + i] = numeros[fila * 3 + col]

    @staticmethod
    def _resolver_sudoku(tablero: List[List[int]]) -> bool:
        """
        Resuelve un tablero de Sudoku usando backtracking.
        
        Args:
            tablero (List[List[int]]): Tablero a resolver
            
        Returns:
            bool: True si se encontró una solución, False en caso contrario
        """
        vacio = SudokuUtils._encontrar_vacio(tablero)
        if not vacio:
            return True
            
        fila, col = vacio
        numeros = list(range(1, 10))
        random.shuffle(numeros)
        
        for num in numeros:
            if SudokuUtils._es_valido(tablero, num, fila, col):
                tablero[fila][col] = num
                if SudokuUtils._resolver_sudoku(tablero):
                    return True
                tablero[fila][col] = 0
                
        return False

    @staticmethod
    def _encontrar_vacio(tablero: List[List[int]]) -> Optional[Tuple[int, int]]:
        """
        Encuentra una posición vacía en el tablero.
        
        Args:
            tablero (List[List[int]]): Tablero a analizar
            
        Returns:
            Optional[Tuple[int, int]]: Coordenadas de la posición vacía o None
        """
        for i in range(9):
            for j in range(9):
                if tablero[i][j] == 0:
                    return (i, j)
        return None

    @staticmethod
    def _es_valido(tablero: List[List[int]], num: int, fila: int, col: int) -> bool:
        """
        Verifica si un número es válido en una posición específica.
        
        Args:
            tablero (List[List[int]]): Tablero a verificar
            num (int): Número a validar
            fila (int): Fila a verificar
            col (int): Columna a verificar
            
        Returns:
            bool: True si el número es válido, False en caso contrario
        """
        # Verificar fila
        for x in range(9):
            if tablero[fila][x] == num and x != col:
                return False
                
        # Verificar columna
        for x in range(9):
            if tablero[x][col] == num and x != fila:
                return False
                
        # Verificar caja 3x3
        inicio_fila = fila - fila % 3
        inicio_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if tablero[i + inicio_fila][j + inicio_col] == num and (i + inicio_fila != fila or j + inicio_col != col):
                    return False
                    
        return True

    @staticmethod
    def _eliminar_numeros(tablero: List[List[int]], cantidad: int) -> List[List[int]]:
        """
        Elimina números del tablero manteniendo una única solución.
        
        Args:
            tablero (List[List[int]]): Tablero completo
            cantidad (int): Cantidad de números a eliminar
            
        Returns:
            List[List[int]]: Tablero con números eliminados
        """
        posiciones = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(posiciones)
        
        tablero_final = [fila[:] for fila in tablero]
        eliminados = 0
        
        for fila, col in posiciones:
            if eliminados >= cantidad:
                break
                
            valor_temp = tablero_final[fila][col]
            tablero_final[fila][col] = 0
            
            # Hacer una copia para verificar
            tablero_prueba = [fila[:] for fila in tablero_final]
            
            # Si hay múltiples soluciones, restaurar el número
            if not SudokuUtils._tiene_solucion_unica(tablero_prueba):
                tablero_final[fila][col] = valor_temp
            else:
                eliminados += 1
                
        return tablero_final

    @staticmethod
    def _tiene_solucion_unica(tablero: List[List[int]]) -> bool:
        """
        Verifica si el tablero tiene una única solución.
        
        Args:
            tablero (List[List[int]]): Tablero a verificar
            
        Returns:
            bool: True si tiene solución única, False en caso contrario
        """
        soluciones = [0]
        
        def backtrack():
            if soluciones[0] > 1:
                return
                
            vacio = SudokuUtils._encontrar_vacio(tablero)
            if not vacio:
                soluciones[0] += 1
                return
                
            fila, col = vacio
            for num in range(1, 10):
                if SudokuUtils._es_valido(tablero, num, fila, col):
                    tablero[fila][col] = num
                    backtrack()
                    tablero[fila][col] = 0
                    
        backtrack()
        return soluciones[0] == 1

    @staticmethod
    def formatear_tiempo(segundos: int) -> str:
        """
        Formatea un tiempo en segundos a formato mm:ss.
        
        Args:
            segundos (int): Tiempo en segundos
            
        Returns:
            str: Tiempo formateado
        """
        minutos = segundos // 60
        segundos = segundos % 60
        return f"{minutos:02d}:{segundos:02d}"

    @staticmethod
    def calcular_puntaje(tiempo: int, dificultad: str, pistas_usadas: int) -> int:
        """
        Calcula el puntaje basado en el tiempo, dificultad y pistas usadas.
        
        Args:
            tiempo (int): Tiempo en segundos
            dificultad (str): Nivel de dificultad
            pistas_usadas (int): Número de pistas utilizadas
            
        Returns:
            int: Puntaje calculado
        """
        # Puntos base según dificultad
        puntos_base = {
            "facil": 1000,
            "normal": 2000,
            "dificil": 3000
        }
        
        # Obtener puntos base
        base = puntos_base.get(dificultad, 2000)
        
        # Penalización por tiempo (menos puntos mientras más tiempo pase)
        factor_tiempo = max(0.1, 1 - (tiempo / 3600))  # 1 hora máximo
        
        # Penalización por pistas
        penalizacion_pistas = pistas_usadas * 100
        
        # Cálculo final
        puntaje = int((base * factor_tiempo) - penalizacion_pistas)
        return max(0, puntaje)  # Asegurar que no sea negativo

    @staticmethod
    def guardar_puntaje(nombre: str, puntaje: int, dificultad: str) -> None:
        """
        Guarda un puntaje en el archivo de puntajes altos.
        
        Args:
            nombre (str): Nombre del jugador
            puntaje (int): Puntaje obtenido
            dificultad (str): Nivel de dificultad
        """
        archivo = "puntajes.json"
        puntajes = []
        
        try:
            if os.path.exists(archivo):
                with open(archivo, 'r') as f:
                    puntajes = json.load(f)
        except:
            puntajes = []
            
        puntajes.append({
            "nombre": nombre,
            "puntaje": puntaje,
            "dificultad": dificultad,
            "fecha": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Ordenar por puntaje y mantener solo los mejores 10
        puntajes.sort(key=lambda x: x["puntaje"], reverse=True)
        puntajes = puntajes[:10]
        
        try:
            with open(archivo, 'w') as f:
                json.dump(puntajes, f, indent=4)
        except Exception as e:
            print(f"Error al guardar puntajes: {e}")