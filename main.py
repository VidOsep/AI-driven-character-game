import pygame
import pytmx
import os
import player
import agent


UP = [0,-1]
DOWN = [0,1]
RIGHT = [1,0]
LEFT = [-1,0]

pygame.init()

tile_scale = 2  # Za koliko povecamo tile
screen = pygame.display.set_mode((1, 1))

# Zloadamo mapo
tmx_map = pytmx.load_pygame(os.getcwd() + "\\assets\\zacetek.tmx")

# Racun dimenzij posameznega tila
scaled_tile_width = tmx_map.tilewidth * tile_scale
scaled_tile_height = tmx_map.tileheight * tile_scale

# Racun dimenzij cele mape
scaled_map_width = tmx_map.width * scaled_tile_width
scaled_map_height = tmx_map.height * scaled_tile_height

screen = pygame.display.set_mode((scaled_map_width, scaled_map_height))

for obj in tmx_map.objects:
    if obj.name == "zacetek":
        player_object = obj
        player_ = player.Player([player_object.x,player_object.y])
    if obj.name == "starec":
        oldman_object = obj
        oldman_ = agent.Agent([oldman_object.x,oldman_object.y])

# Glavna zanka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move(UP)
    if keys[pygame.K_DOWN]:
        player.move(DOWN)
    if keys[pygame.K_LEFT]:
        player.move(LEFT)
    if keys[pygame.K_RIGHT]:
        player.move(RIGHT)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Izris tilov
    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    scaled_tile = pygame.transform.scale(tile, (scaled_tile_width, scaled_tile_height))
                    screen.blit(scaled_tile, (x * scaled_tile_width, y * scaled_tile_height))

    # Posodobitev zaslona
    pygame.display.flip()

