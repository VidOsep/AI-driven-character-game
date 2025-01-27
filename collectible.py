import pygame
import os

scaled_tile_width = 32
scaled_tile_height = 32

# load and scale images
apple_img = pygame.image.load(os.getcwd() + "\\assets\\collectibles\\apple.png")
apple_img = pygame.transform.scale(apple_img, (scaled_tile_width, scaled_tile_height))

strawberry_img = pygame.image.load(os.getcwd() + "\\assets\\collectibles\\strawberry.png")
strawberry_img = pygame.transform.scale(strawberry_img, (scaled_tile_width, scaled_tile_height))

mushroom_img = pygame.image.load(os.getcwd() + "\\assets\\collectibles\\mushroom.png")
mushroom_img = pygame.transform.scale(mushroom_img, (scaled_tile_width, scaled_tile_height))


class Collectible(pygame.sprite.Sprite):
    """
    An object, that the player can interact with and pick up.
    Three types exist: apple, mushroom and strawberry.
    """

    def __init__(self, position, type):
        super().__init__()

        if type == "mushroom":
            self.image = mushroom_img
        elif type == "strawberry":
            self.image = strawberry_img
        elif type == "apple":
            self.image = apple_img

        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.type = type

    def update(self, display):
        display.blit(self.image, self.rect)
