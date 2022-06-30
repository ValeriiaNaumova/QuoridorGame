import pygame
import random
from .bar import Bar
from .pawn import Pawn
from .constants import bar_coord_x, bar_coord_y, RED, BLACK
from .constants import BLACK, ROWS

bar_list = pygame.sprite.Group()
players_list = pygame.sprite.Group()

player1 = Pawn(0, 4, 'pawn-red.png', 1, RED)
players_list.add(player1)

player2 = Pawn(8, 4, 'pawn-blue.png', 2, BLACK)
players_list.add(player2)


def create_board():
    bar_list_loc = pygame.sprite.Group()
    for row in range(0, 9):
        for column in range(0, 8):
            bar_vert = Bar(5, 50, row, column)
            bar_vert.rect.x = bar_coord_x[column]
            bar_vert.rect.y = bar_coord_y[row]
            bar_list_loc.add(bar_vert)

    for row in range(0, 8):
        for column in range(0, 9):
            bar_hor = Bar(50, 5, row, column)
            bar_hor.rect.x = bar_coord_y[column]
            bar_hor.rect.y = bar_coord_x[row]
            bar_list_loc.add(bar_hor)
    return bar_list_loc


class Spot(pygame.sprite.Sprite):
    def __init__(self, row=0, col=0):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col


bar_list_loc = create_board()


class Board():
    def __init__(self):
        self.selected_piece = None
        self.bar_list = create_board()
        self.player_list = players_list

    def copy(self):
        board_copy = Board()
        board_copy.player_list = pygame.sprite.Group()
        board_copy.bar_list = pygame.sprite.Group()
        board_copy.selected_piece = self.selected_piece
        for bar in self.bar_list:
            board_copy.bar_list.add(bar.copy())
        for pawn in self.player_list:
            board_copy.player_list.add(pawn.copy())
        return board_copy

    def get_player2(self):
        return self.player_list.sprites()[1]

    def get_player1(self):
        return self.player_list.sprites()[0]

    def get_possible_spots(self, pawn):
        possible_spots = pygame.sprite.Group()
        row, col = pawn.row, pawn.col
        player2 = self.get_player2()
        player1 = self.get_player1()

        # FIXME tohle taky není hezky napsaný, celý to je o hooodně copy pastu
        # 1) pawn 1 a pawn 2 mají stejnou logiku, jen vůči sobě inverzní co se týče znamínek
        # 2) každá ta pozice a ty zanořený ify a for cykly se dají alespoň vytknout do nějakých pojmenovaných metod,
        #    aby to dávalo při čtení zdrojáku smysl
        # 3) ta logika je ale stejně podezřelá, jde přeci o to ověřit 4 místa, kam se může hrát pohybovat, ne?
        #    to by mělo být prostě na jednu funkci "is_spot_empty" a její 4x zavolání, ne?
        if (pawn.name == 1):
            if not (player2.row == row + 1 and player2.col == col):
                if (row + 1 < 9):
                    for bar in self.bar_list:
                        if (bar.row == pawn.row and bar.col == pawn.col and bar.width == 50 and bar.color != 'red'):
                            spot = Spot(row + 1, col)
                            if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                                possible_spots.add(spot)
            elif (row + 2 < 9 and not any(list(x for x in self.bar_list if (
                    x.color == 'red' and x.width == 50 and (x.row == row + 1 or x.col == row + 2) and x.col == col)))):
                spot = Spot(row + 2, col)
                if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                    possible_spots.add(spot)
            if not (player2.row == row - 1 and player2.col == col):
                if (row - 1 > -1):
                    for bar in self.bar_list:
                        if (bar.row == pawn.row - 1 and bar.col == pawn.col and bar.width == 50 and bar.color != 'red'):
                            spot = Spot(row - 1, col)
                            if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                                possible_spots.add(spot)
            elif (row - 2 > -1 and not any(list(x for x in self.bar_list if (
                    x.color == 'red' and x.width == 50 and (x.row == row - 1 or x.col == row - 2) and x.col == col)))):
                spot = Spot(row - 2, col)
                if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                    possible_spots.add(spot)
            if (col < 8 and not (player2.col == col + 1 and player2.row == row)):
                for bar in self.bar_list:
                    if (bar.row == pawn.row and bar.col == pawn.col and bar.width == 5 and bar.color != 'red'):
                        spot = Spot(row, col + 1)
                        if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                            possible_spots.add(spot)
            elif (col + 2 < 9 and not any(list(x for x in self.bar_list if (
                    x.color == 'red' and x.width == 5 and (x.col == col + 1 or x.col == col + 2) and x.row == row)))):
                spot = Spot(row, col + 2)
                if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                    possible_spots.add(spot)
            if (col > 0 and not (player2.col == col - 1 and player2.row == row)):
                for bar in self.bar_list:
                    if (bar.row == pawn.row and bar.col == pawn.col - 1 and bar.width == 5 and bar.color != 'red'):
                        spot = Spot(row, col - 1)
                        if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                            possible_spots.add(spot)
            elif (col - 2 > -1 and not any(list(x for x in self.bar_list if (
                    x.color == 'red' and x.width == 5 and (x.col == col - 1 or x.col == col - 2) and x.row == row)))):
                spot = Spot(row, col - 2)
                if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                    possible_spots.add(spot)
        elif (pawn.name == 2):
            if not (player1.row == row - 1 and player1.col == col):
                if (row - 1 > -1):
                    for bar in self.bar_list:
                        if (bar.row + 1 == pawn.row and bar.col == pawn.col and bar.width == 50 and bar.color != 'red'):
                            spot = Spot(row - 1, col)
                            if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                                possible_spots.add(spot)
            elif (row - 2 > -1 and not any(list(x for x in self.bar_list if (
                    x.color == 'red' and x.width == 50 and (x.row == row - 1 or x.col == row - 2) and x.col == col)))):
                spot = Spot(row - 2, col)
                if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                    possible_spots.add(spot)
            if not (player1.row == row + 1 and player1.col == col):
                if (row + 1 < 9):
                    for bar in self.bar_list:
                        if (bar.row == pawn.row and bar.col == pawn.col and bar.width == 50 and bar.color != 'red'):
                            spot = Spot(row + 1, col)
                            if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                                possible_spots.add(spot)
            elif (row + 2 < 9 and not any(list(x for x in self.bar_list if (
                    x.color == 'red' and x.width == 50 and (x.row == row + 1 or x.col == row + 2) and x.col == col)))):
                spot = Spot(row + 2, col)
                if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                    possible_spots.add(spot)
            if (col > 0 and not (player1.col == col - 1 and player1.row == row)):
                for bar in self.bar_list:
                    if (bar.row == pawn.row and bar.col == pawn.col - 1 and bar.width == 5 and bar.color != 'red'):
                        spot = Spot(row, col - 1)
                        if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                            possible_spots.add(spot)
            elif (col - 2 > -1 and col - 2 > -1 and not any(list(x for x in self.bar_list if (
                    x.color == 'red' and x.width == 5 and (x.col == col - 1 or x.col == col - 2) and x.row == row)))):
                spot = Spot(row, col - 2)
                if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                    possible_spots.add(spot)
            if (col < 8 and not (player1.col == col + 1 and player1.row == row)):
                for bar in self.bar_list:
                    if (bar.row == pawn.row and bar.col == pawn.col and bar.width == 5 and bar.color != 'red'):
                        spot = Spot(row, col + 1)
                        if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                            possible_spots.add(spot)
            elif (col + 2 < 9 and not any(list(x for x in self.bar_list if (
                    x.color == 'red' and x.width == 5 and (x.col == col + 1 or x.col == col + 2) and x.row == row)))):
                spot = Spot(row, col + 2)
                if not (any(x for x in possible_spots if (x.row == spot.row and x.col == spot.col))):
                    possible_spots.add(spot)
        return possible_spots

    def winner(self):
        if any(x for x in self.player_list if (x.color == RED and x.row == 8)):
            return 'RED'
        elif any(x for x in self.player_list if (x.color == BLACK and x.row == 0)):
            return 'BLUE'
        return None

    def move(self, pawn, row, col):
        for player in self.player_list:
            if pawn.row == player.row and pawn.col == player.col:
                player.move(row, col)

    def change_bar(self, bar):
        for bar in (x for x in self.bar_list if (x.row == bar.row and x.col == bar.col and x.width == bar.width)):
            bar.change_bar()

    def get_bar(self, bar_temp):
        for bar in (x for x in bar_list_loc if
                    (x.row == bar_temp.row and x.col == bar_temp.col and x.width == bar_temp.width)):
            return bar

    def get_pawn(self, row, col):
        for pawn in self.player_list:
            if pawn.row == row and pawn.col == col:
                return pawn

    def evaluate(self):
        return ((len(self.astar_search(self.player_list.sprites()[1], 0)) -
                 len(self.astar_search(self.player_list.sprites()[0], 8)))*100/8) + ((
                       self.player_list.sprites()[0].walls - self.player_list.sprites()[1].walls)*100/10)

    def ManhattanDistanceToFinish(self, fromCoord, row):
        return abs(row - fromCoord.row)

    def ManhattanDistance(self, fromCoord, toCoord):
        return abs(toCoord.row - fromCoord.row) + abs(toCoord.col - fromCoord.col)

    def astar_search(self, start, end):
        # FIXME open se používá jako funkce na otevření souboru/streamu, určitě není vhodné mít pojmenovanou proměnnou
        # úplně stejně
        open = []
        closed = []
        previous = []
        start_node = start
        goal_node = end
        open.append(start_node)
        start_node.h = self.ManhattanDistanceToFinish(start_node, end)

        while len(open) > 0:
            current_node = open.pop(0)
            closed.append(current_node)

            # FIXME tenhle sort je dost náročný, volá se hooooodněkrát a celý algoritmus taky dokáže hodně zpomalit,
            # psal jsem vám to i při první revizi, že je toto jedno z těch krizových míst
            # správně by tu měl být heapq, protože vás vždy zajímá jen toto: current_node = open.pop(0)
            open.sort(key=takeH)
            if current_node.row == goal_node:
                path = []
                while current_node.row != start_node.row:
                    path.append(current_node)
                    for elem in previous:
                        if elem.id == current_node.prev:
                            result = elem

                    current_node = result
                return path[::-1]

            current_node.name = start_node.name
            current_node.id = unique_id()
            neighbors = self.get_possible_spots(current_node)
            for next in neighbors:
                neighbor = next
                if (neighbor in closed):
                    continue

                g_score = current_node.g + self.ManhattanDistance(current_node, neighbor)

                if not (neighbor in open):
                    open.append(neighbor)
                    improving = True
                elif (g_score < neighbor.g):
                    improving = True
                else:
                    improving = False

                if improving:
                    neighbor.prev = current_node.id
                    previous.append(current_node)
                    neighbor.g = g_score
                    neighbor.h = g_score + self.ManhattanDistanceToFinish(neighbor, goal_node)

                    # FIXME podivný warning opět, end zde nemá efekt
                    end
                    end
        return [None] * 100


def takeH(elem):
    return elem.h


def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f >= node.f):
            return False
    return True


def unique_id():
    seed = random.getrandbits(32)
    while True:
        yield seed
        seed += 1
