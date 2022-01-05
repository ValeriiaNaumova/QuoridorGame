import pygame
from .constants import RED, WHITE, SQUARE_SIZE


class Pawn(pygame.sprite.Sprite):
    def __init__(self, row=0, col=0, image='piece1.png', name='', color=''):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.row = row
        self.name = name
        self.color = color
        self.picture = image
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.walls = 10
        self.id = id(self)
        self.g = 0
        self.h = 0
        self.f = 0
        self.prev = -1

        self.calc_position()

    def copy(self):
        pawn = Pawn()
        pawn.picture = self.picture
        pawn.image = pygame.image.load(pawn.picture)
        pawn.image = pygame.transform.scale(pawn.image, (40, 40))
        pawn.rect = self.image.get_rect()
        pawn.color = self.color
        pawn.col = self.col
        pawn.row = self.row
        pawn.walls = self.walls
        pawn.name = self.name
        pawn.prev = self.prev
        pawn.calc_position()
        return pawn

    def calc_position(self):
        self.rect.y = SQUARE_SIZE * self.row + 17
        self.rect.x = SQUARE_SIZE * self.col + 17

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_position()
