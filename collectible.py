import pygame
import os

scaled_tile_width = 32
scaled_tile_height = 32

# zloadamo in povecamo slike
jabolko_img = pygame.image.load(os.getcwd() + "\\assets\\jabolko.png")
jabolko_img = pygame.transform.scale(jabolko_img, (scaled_tile_width, scaled_tile_height))

jagoda_img = pygame.image.load(os.getcwd() + "\\assets\\jagoda.png")
jagoda_img = pygame.transform.scale(jagoda_img, (scaled_tile_width, scaled_tile_height))

goba_img = pygame.image.load(os.getcwd() + "\\assets\\goba.png")
goba_img = pygame.transform.scale(goba_img, (scaled_tile_width, scaled_tile_height))


class Collectible(pygame.sprite.Sprite):
    """
    Collectible je statičen objekt, ki ga igralec lahko pobere in pospravi v svojo lastnino
    """

    def __init__(self, position, type):
        super().__init__()

        if type == "goba":  # mozni so trije tipi
            self.image = goba_img
        elif type == "jagoda":
            self.image = jagoda_img
        elif type == "jabolko":
            self.image = jabolko_img

        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.type = type

    def update(self, display):
        display.blit(self.image, self.rect)
