import pygame
class Bar(pygame.sprite.Sprite):
    def __init__(self, width = 0, height = 0, row = 0, col = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height)).convert()
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.color = "black"
        self.col = col
        self.row = row
        self.width = width
        self.id = id(self)



    def copy(self):
        bar = Bar()
        bar.image = pygame.Surface.copy(self.image)
        bar.rect = self.rect
        bar.color = self.color
        bar.col = self.col
        bar.row = self.row
        bar.width = self.width
        bar.id = self.id
        return bar



    def update(self, mouse, bar_list):
        if self.rect.collidepoint(mouse):
            self.color = "red"
            self.image.fill((255, 0, 0))

    def change_bar(self):
        self.color = "red"
        self.image.fill((255, 0, 0))

