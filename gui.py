import pygame
import sys
from sudoku_solver import resolver_sudoku, es_valido

# Definir constantes para la GUI
ANCHO, ALTO = 600, 700  # Aumentado para añadir botones
TAMAÑO_CASILLA = 540 // 9
MARGEN_SUPERIOR = 80
COLOR_FONDO = (240, 240, 240)
COLOR_LINEA = (0, 0, 0)
COLOR_NUMERO = (0, 0, 255)
COLOR_NUMERO_INICIAL = (0, 0, 0)
COLOR_SELECCION = (255, 0, 0)
COLOR_ERROR = (255, 100, 100)
COLOR_BOTON = (70, 130, 180)
COLOR_BOTON_HOVER = (100, 160, 210)
COLOR_TEXTO_BOTON = (255, 255, 255)

class Boton:
    def __init__(self, x, y, ancho, alto, texto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.hover = False
        
    def dibujar(self, pantalla, fuente):
        color = COLOR_BOTON_HOVER if self.hover else COLOR_BOTON
        pygame.draw.rect(pantalla, color, self.rect, border_radius=5)
        texto_surface = fuente.render(self.texto, True, COLOR_TEXTO_BOTON)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        pantalla.blit(texto_surface, texto_rect)
        
    def esta_sobre(self, pos):
        return self.rect.collidepoint(pos)

class SudokuGUI:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("SUDOKING - Sudoku Solver")
        self.tablero_inicial = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.tablero = [fila[:] for fila in self.tablero_inicial]
        self.seleccion = None
        self.error = None
        self.tiempo_error = 0
        self.cargar_fuentes()
        self.crear_botones()
        
    def cargar_fuentes(self):
        self.fuente_numeros = pygame.font.SysFont("arial", 40)
        self.fuente_botones = pygame.font.SysFont("arial", 20)
        self.fuente_titulo = pygame.font.SysFont("arial", 36, bold=True)
        
    def crear_botones(self):
        self.boton_resolver = Boton(50, 620, 150, 40, "Resolver (R)")
        self.boton_limpiar = Boton(230, 620, 150, 40, "Limpiar (C)")
        self.boton_verificar = Boton(410, 620, 150, 40, "Verificar (V)")
        
    def dibujar_titulo(self):
        titulo = self.fuente_titulo.render("SUDOKING", True, COLOR_LINEA)
        rect_titulo = titulo.get_rect(center=(ANCHO//2, 40))
        self.pantalla.blit(titulo, rect_titulo)

    def dibujar_tablero(self):
        # Dibujar el fondo del tablero
        pygame.draw.rect(self.pantalla, (255, 255, 255), 
                        (0, MARGEN_SUPERIOR, 540, 540))
        
        # Dibujar líneas de la cuadrícula
        for i in range(10):
            grosor = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.pantalla, COLOR_LINEA, 
                           (i * TAMAÑO_CASILLA, MARGEN_SUPERIOR), 
                           (i * TAMAÑO_CASILLA, MARGEN_SUPERIOR + 540), grosor)
            pygame.draw.line(self.pantalla, COLOR_LINEA, 
                           (0, MARGEN_SUPERIOR + i * TAMAÑO_CASILLA), 
                           (540, MARGEN_SUPERIOR + i * TAMAÑO_CASILLA), grosor)
        
        # Dibujar los números
        for fila in range(9):
            for col in range(9):
                numero = self.tablero[fila][col]
                if numero != 0:
                    color = COLOR_NUMERO_INICIAL if self.tablero_inicial[fila][col] != 0 else COLOR_NUMERO
                    texto = self.fuente_numeros.render(str(numero), True, color)
                    x = col * TAMAÑO_CASILLA + (TAMAÑO_CASILLA - texto.get_width()) // 2
                    y = MARGEN_SUPERIOR + fila * TAMAÑO_CASILLA + (TAMAÑO_CASILLA - texto.get_height()) // 2
                    self.pantalla.blit(texto, (x, y))

    def dibujar_seleccion(self):
        if self.seleccion:
            fila, col = self.seleccion
            pygame.draw.rect(self.pantalla, COLOR_SELECCION, 
                           (col * TAMAÑO_CASILLA, 
                            MARGEN_SUPERIOR + fila * TAMAÑO_CASILLA, 
                            TAMAÑO_CASILLA, TAMAÑO_CASILLA), 3)

    def dibujar_error(self):
        if self.error and pygame.time.get_ticks() - self.tiempo_error < 1000:
            fila, col = self.error
            pygame.draw.rect(self.pantalla, COLOR_ERROR,
                           (col * TAMAÑO_CASILLA,
                            MARGEN_SUPERIOR + fila * TAMAÑO_CASILLA,
                            TAMAÑO_CASILLA, TAMAÑO_CASILLA), 3)

    def dibujar_botones(self):
        self.boton_resolver.dibujar(self.pantalla, self.fuente_botones)
        self.boton_limpiar.dibujar(self.pantalla, self.fuente_botones)
        self.boton_verificar.dibujar(self.pantalla, self.fuente_botones)

    def seleccionar_casilla(self, x, y):
        if y < MARGEN_SUPERIOR:
            return
        fila = (y - MARGEN_SUPERIOR) // TAMAÑO_CASILLA
        col = x // TAMAÑO_CASILLA
        if 0 <= fila < 9 and 0 <= col < 9:
            if self.tablero_inicial[fila][col] == 0:  # Solo seleccionar casillas vacías inicialmente
                self.seleccion = (fila, col)
            else:
                self.seleccion = None

    def insertar_numero(self, numero):
        if not self.seleccion:
            return
        fila, col = self.seleccion
        if self.tablero_inicial[fila][col] == 0:  # Solo modificar casillas vacías inicialmente
            if es_valido(self.tablero, numero, fila, col):
                self.tablero[fila][col] = numero
            else:
                self.error = (fila, col)
                self.tiempo_error = pygame.time.get_ticks()

    def verificar_tablero(self):
        # Verificar si el tablero está completo y válido
        for fila in range(9):
            for col in range(9):
                if self.tablero[fila][col] == 0:
                    return False
                num = self.tablero[fila][col]
                self.tablero[fila][col] = 0
                if not es_valido(self.tablero, num, fila, col):
                    self.tablero[fila][col] = num
                    return False
                self.tablero[fila][col] = num
        return True

    def limpiar_tablero(self):
        self.tablero = [fila[:] for fila in self.tablero_inicial]
        self.seleccion = None
        self.error = None
    
    def resolver_tablero(self):
        resolver_sudoku(self.tablero)
    
    def actualizar_botones(self, pos):
        self.boton_resolver.hover = self.boton_resolver.esta_sobre(pos)
        self.boton_limpiar.hover = self.boton_limpiar.esta_sobre(pos)
        self.boton_verificar.hover = self.boton_verificar.esta_sobre(pos)
    
    def run(self):
        reloj = pygame.time.Clock()
        while True:
            pos_mouse = pygame.mouse.get_pos()
            self.actualizar_botones(pos_mouse)
            
            self.pantalla.fill(COLOR_FONDO)
            self.dibujar_titulo()
            self.dibujar_tablero()
            self.dibujar_seleccion()
            self.dibujar_error()
            self.dibujar_botones()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evento.pos
                    self.seleccionar_casilla(x, y)
                    
                    if self.boton_resolver.esta_sobre(evento.pos):
                        self.resolver_tablero()
                    elif self.boton_limpiar.esta_sobre(evento.pos):
                        self.limpiar_tablero()
                    elif self.boton_verificar.esta_sobre(evento.pos):
                        if self.verificar_tablero():
                            print("¡Sudoku resuelto correctamente!")
                        else:
                            print("El Sudoku aún no está resuelto correctamente")

                if evento.type == pygame.KEYDOWN:
                    if evento.key in [pygame.K_1, pygame.K_KP1]: self.insertar_numero(1)
                    elif evento.key in [pygame.K_2, pygame.K_KP2]: self.insertar_numero(2)
                    elif evento.key in [pygame.K_3, pygame.K_KP3]: self.insertar_numero(3)
                    elif evento.key in [pygame.K_4, pygame.K_KP4]: self.insertar_numero(4)
                    elif evento.key in [pygame.K_5, pygame.K_KP5]: self.insertar_numero(5)
                    elif evento.key in [pygame.K_6, pygame.K_KP6]: self.insertar_numero(6)
                    elif evento.key in [pygame.K_7, pygame.K_KP7]: self.insertar_numero(7)
                    elif evento.key in [pygame.K_8, pygame.K_KP8]: self.insertar_numero(8)
                    elif evento.key in [pygame.K_9, pygame.K_KP9]: self.insertar_numero(9)
                    elif evento.key == pygame.K_r: self.resolver_tablero()
                    elif evento.key == pygame.K_c: self.limpiar_tablero()
                    elif evento.key == pygame.K_v:
                        if self.verificar_tablero():
                            print("¡Sudoku resuelto correctamente!")
                        else:
                            print("El Sudoku aún no está resuelto correctamente")

            pygame.display.flip()
            reloj.tick(60)  # Limitar a 60 FPS