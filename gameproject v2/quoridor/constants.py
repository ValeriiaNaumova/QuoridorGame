import pygame
WIDTH, HEIGHT = 470, 470
ROWS, COLS = 9, 9
SQUARE_SIZE = 50

#RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

#Bar
bar_list = pygame.sprite.Group()
bar_coord_x = [60, 110, 160, 210, 260, 310, 360, 410]
bar_coord_y = [10, 60, 110, 160, 210, 260, 310, 360, 410]

class Coord:
    def __init__(self, spot1=0, spot2=0):
        self.coord1 = spot1
        self.coord2 = spot2
