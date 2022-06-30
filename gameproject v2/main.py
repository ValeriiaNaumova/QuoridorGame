# FIXME vyřešte si warningy ve všech souborech
import pygame
import psutil
import os
import time
import pygame_menu
from quoridor.constants import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, RED, BLACK

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Quoridor")
# FIXME warning, importy patří nahoru
from pygame.locals import *
from quoridor.board import player1, player2, Board
from quoridor.pawn import Pawn
from quoridor.game import Game
from quoridor.minimax.algorithm import minimax

board = Board()
back = pygame.Surface((WIDTH, HEIGHT))
background = back.convert()
# FIXME nepoužitá proměnná, ihned redeklarovaná
background = pygame.image.load('wood.png').convert()
screen.blit(background, (0, 0))
pygame.draw.rect(screen, (0, 0, 0), Rect((10, 10), (450, 450)), 5)
board.bar_list.draw(screen)
game = Game()
board.player_list.draw(screen)
run = True
bar_count = 0
first_bar = None
font = pygame.font.SysFont("Palatino", 15)

radius = SQUARE_SIZE // 2 - 15
possible_spots = pygame.sprite.Group()


def get_row_col_from_mouse(mouse):
    for pawn in board.player_list:
        if pawn.rect.collidepoint(mouse):
            return pawn


def get_bar(mouse):
    for bar in board.bar_list:
        if bar.rect.collidepoint(mouse):
            return bar


def calc_position(row, col):
    y = SQUARE_SIZE * row + 40
    x = SQUARE_SIZE * col + 36
    return (x, y)


# FIXME board proměnnou máte nastavenou jako globální, a tady ji máte znovu jako lokální -> kryjí se vám názvy
def _draw_board(board):
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (0, 0, 0), Rect((10, 10), (450, 450)), 5)
    board.bar_list.draw(screen)
    board.player_list.draw(screen)
    pygame.display.update()
    wall_board(board)


# FIXME taky
def wall_board(board):
    pygame.draw.rect(screen, (0, 0, 0), [0, 0, 90, 20], 0)
    screen.blit(font.render('Red:' + str(board.player_list.sprites()[0].walls) + ', Blue:' + str(player2.walls), True,
                            (255, 255, 255)), (5, 5))


def start_the_game():
    global run, board, possible_spots, bar_count

    # FIXME opět globál vs local
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    background = back.convert()
    # FIXME opět globál vs local
    background = pygame.image.load('wood.png').convert()
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (0, 0, 0), Rect((10, 10), (450, 450)), 5)
    board.bar_list.draw(screen)
    board.player_list.draw(screen)
    start_time = time.time()

    while run:
        if game.turn == RED:
            value, new_board = minimax(board, difficulty, RED)
            game.ai_move(new_board)
            board = new_board
            _draw_board(board)
        if board.winner() is not None:
            end_time = time.time()
            process = psutil.Process(os.getpid())
            per_cpu = psutil.cpu_percent(round(end_time - start_time))
            ram_usage = process.memory_percent()

            menu_win = pygame_menu.Menu('Quoridor', 400, 300,
                                        theme=pygame_menu.themes.THEME_DARK)

            menu_win.add.label(board.winner() + ' wins!')
            menu_win.add.label(str(per_cpu) + '% CPU usage.')
            menu_win.add.label(str(round(ram_usage, 4)) + '% of RAM.')
            menu_win.add.button('Quit', pygame_menu.events.EXIT)
            menu_win.mainloop(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and game.turn == BLACK:
                pos = pygame.mouse.get_pos()
                x, y = pos
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE

                # FIXME srovnejte si syntaxi -> někdy používáte závorky kolem if, někdy ne, tak to dělejte konzistentně
                if (get_row_col_from_mouse(pygame.mouse.get_pos()) != None):
                    pawn = get_row_col_from_mouse(pygame.mouse.get_pos())
                    if game.turn == BLACK and pawn.color == BLACK:
                        row, col = get_row_col_from_mouse(pygame.mouse.get_pos()).row, get_row_col_from_mouse(
                            pygame.mouse.get_pos()).col
                        possible_spots = board.get_possible_spots(pawn)
                        for spot in possible_spots:
                            pygame.draw.circle(screen, WHITE, calc_position(spot.row, spot.col), radius + 2)
                        pygame.display.update()
                if (any(x for x in possible_spots if (x.row == row and x.col == col)) and (pawn != Pawn())):
                    if game.turn == BLACK and pawn.color == BLACK:
                        pawn.move(row, col)
                        _draw_board(board)
                        pawn = Pawn()
                        possible_spots = pygame.sprite.Group()
                        game.change_turn()
                if (get_bar(pygame.mouse.get_pos()) != None and bar_count != 2):
                    _draw_board(board)
                    if bar_count == 0:
                        first_bar = get_bar(pygame.mouse.get_pos())
                        board.bar_list.update(pygame.mouse.get_pos(), board.bar_list)
                        board.bar_list.draw(screen)
                    if bar_count == 1:
                        second_row = get_bar(pygame.mouse.get_pos())
                        # FIXME tady už je dost ošklivý zanoření, ani není vidět čitelně celý řádek,
                        # je třeba to rozdělit na vícero metod a kód lépe strukturovat, aby půl řádku nezabíralo samotné odsazení
                        if (
                                second_row.row == first_bar.row + 1 and second_row.col == first_bar.col and first_bar.width == second_row.width == 5) or (
                                second_row.row == first_bar.row - 1 and second_row.col == first_bar.col and first_bar.width == second_row.width == 5) or (
                                second_row.col == first_bar.col + 1 and second_row.row == first_bar.row and first_bar.width == second_row.width == 50) or (
                                second_row.col == first_bar.col - 1 and second_row.row == first_bar.row and first_bar.width == second_row.width == 50):
                            board.bar_list.update(pygame.mouse.get_pos(), board.bar_list)
                            board.bar_list.draw(screen)
                        else:
                            break
                    bar_count += 1
                    if bar_count == 2:
                        if game.turn == RED and player1.walls != 0:
                            player1.walls = player1.walls - 1
                        elif player2.walls != 0:
                            player2.walls = player2.walls - 1
                        else:
                            break
                        bar_count = 0
                        first_bar = None
                        wall_board(board)
                        game.change_turn()
        pygame.display.update()
        wall_board(board)


def set_difficulty(value, number):
    # FIXME undefined difficulty
    global difficulty
    difficulty = number


def disable():
    # FIXME undefined difficulty
    global difficulty
    try:
        difficulty
    except NameError:
        difficulty = 4
    menu.disable()
    start_the_game()


menu = pygame_menu.Menu('Quoridor', 400, 300,
                        theme=pygame_menu.themes.THEME_DARK)

menu.add.selector('Difficulty :', [('Hard', 4), ('Medium', 3), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', disable)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)
