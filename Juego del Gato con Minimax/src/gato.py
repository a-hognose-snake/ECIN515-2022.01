import copy
import sys
import pygame
import random
import numpy as np
from constantes import *
# Estados del tablero
# 0: No hay ganador aún | 1: Gana jugador 1 | -1: Gana jugador 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GATO')
screen.fill(BG_COLOR)

# Clases


class Board:

    def __init__(self):
        # El array del juego, filas * columnas
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares  # [squares]
        self.marked_sqrs = 0

    def final_state(self, show=False):
        # 0: No hay ganador | 1: Gana jugador 1 | -1: Gana jugador 2

        # Ganador en columna
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # Ganador en fila
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # Ganador en diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # No hay ganador aún
        return 0

    # Marcar y contar posición
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    # Marcar posición como vacia
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    # Obtener posiciones disponibles
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    # Marcar tablero lleno
    def isfull(self):
        return self.marked_sqrs == 9

    # Marca tablero vacio
    def isempty(self):
        return self.marked_sqrs == 0

# Clase de IA


class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # MINIMAX

    def minimax(self, board, maximizing):

        # Obtener estado del tablero (case)
        case = board.final_state()

        # Gana jugador 1
        if case == 1:
            return 1, None  # eval, move

        # Gana jugador 2
        if case == 2:
            return -1, None

        # Empate
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # Evaluar Movimientos

    def eval(self, main_board):
        eval, move = self.minimax(main_board, False)
        print(f'IA se movió a {move} y el estado de juego es: {eval}')
        return move  # row, col


class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  # 1-cross  #2-circles
        self.gamemode = 'ai'  # pvp or ai
        self.running = True
        self.show_lines()

    # Dibujar tablero en ventana

    def show_lines(self):
        # fondo de la ventana
        screen.fill(BG_COLOR)

        # vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0),
                         (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0),
                         (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE),
                         (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE),
                         (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # Mostrar diagonal
            # Mostral linea desc
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET,
                        row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc,
                             end_desc, CROSS_WIDTH)
            # Mostrar linea asc
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc,
                             end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # Dibujar circulo (jugador 2 - IA)
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()


def main():

    # Setup
    game = Game()
    board = game.board
    ai = game.ai
    ai.level = 1

    # Main Loop
    while True:

        # Eventos de pygame
        for event in pygame.event.get():

            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Eventos de teclado
            if event.type == pygame.KEYDOWN:
                # r: reiniciar juego
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

            # Posicionar con click
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                # Marcar posición de jugador humano
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

        # Jugadas de IA
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # Actualizar ventana
            pygame.display.update()

            # Evaluar tablero
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False

        pygame.display.update()


main()
