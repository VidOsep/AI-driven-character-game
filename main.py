import pygame
import pytmx

# Initialize Pygame
pygame.init()

# Load the Tiled map
tmx_map = pytmx.load_pygame("path/to/your/map.tmx")

# Access map properties
print("Map width:", tmx_map.width)
print("Map height:", tmx_map.height)
print("Tile width:", tmx_map.tilewidth)
print("Tile height:", tmx_map.tileheight)

# Access map layers
for layer in tmx_map.layers:
    if layer.is_object_layer:
        print("Object layer:", layer.name)
    else:
        print("Tile layer:", layer.name)

        # Access tiles in a tile layer
        for x, y, tile in layer.tiles():
            if tile:
                print(f"Tile at ({x}, {y}): GID={tile.gid}, Properties={tile.properties}")

# Main game loop
while True:
    # Update game logic and render the map

pygame.quit()
