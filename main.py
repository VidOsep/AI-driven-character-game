import pygame
import pytmx
import os
import sys
import time
import player
import agent
import pygame_textinput
import collectible

# possible directions
UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"

pygame.init()
clock = pygame.time.Clock()

tile_scale = 2 
screen = pygame.display.set_mode((1, 1))

# load maps
tmx_map1 = pytmx.load_pygame(os.getcwd() + "\\assets\\maps\\map1.tmx")
tmx_map2 = pytmx.load_pygame(os.getcwd() + "\\assets\\maps\\map2.tmx")
tmx_map = tmx_map1  # currently displayed map

# starting screen
start_screen = pygame.image.load(os.getcwd() + "\\assets\\start-screen.png")

scaled_tile_width = tmx_map.tilewidth * tile_scale
scaled_tile_height = tmx_map.tileheight * tile_scale

# map dimensions
scaled_map_width = tmx_map.width * scaled_tile_width
scaled_map_height = tmx_map.height * scaled_tile_height

screen = pygame.display.set_mode((scaled_map_width, scaled_map_height))

is_conversation = False
is_typing = False

# input box dimensions
t_x = 40
t_y = scaled_map_height - 80
t_w = 200
font = pygame.font.SysFont(None, 100)

player_ = player.Player([0, 0]) # player instance
oldman_ = None 

bg_collision = []
gate = []
collectibles = []
characters = []
end_gate_layer = tmx_map1.get_layer_by_name("end_gate")
end_gate_layer.visible = True


def set_map(tmap):
    # setup the whole map at the beginning
    global tmx_map
    global gate
    global bg_collision
    global player_
    global oldman_
    global collectibles
    global characters
    global end_gate
    gate = []
    bg_collision = []
    collectibles = []
    end_gate = []
    characters = []
    tmx_map = tmap

    # classifying special tiles, collision boxes, gates
    for layer in tmx_map.layers:
        if layer.name == "collision":
            for obj in layer.tiles():
                bg_rect = pygame.rect.Rect(tile_scale * 16 * obj[0], tile_scale * 16 * obj[1], 32, 32)
                bg_collision.append(bg_rect)
        if layer.name == "prehodi":
            for p in layer.tiles():
                props = layer.properties
                gate.append({"to": props.get("to"),
                               "rect": pygame.rect.Rect(tile_scale * 16 * p[0], tile_scale * 16 * p[1], 32, 32)})
        if layer.name == "end_gate":
            for p in layer.tiles():
                end_gate.append(pygame.rect.Rect(tile_scale * 16 * p[0], tile_scale * 16 * p[1], 32, 32))

    temp = player_.position
    for obj in tmx_map.objects:  # get intitial character positions from tmx file
        if obj.name == "start" and temp[0] == 0 and temp[1] == 0:
            player_object = obj
            player_ = player.Player([player_object.x * tile_scale, player_object.y * tile_scale])
        if obj.name == "pos_p" and (temp[0] != 0 or temp[1] != 0):
            player_object = obj
            player_.position = [player_object.x * tile_scale, player_object.y * tile_scale]
        if obj.name == "old-man":
            if oldman_ == None:
                oldman_object = obj
                oldman_ = agent.Agent([oldman_object.x * tile_scale, oldman_object.y * tile_scale],
                                      "\\pomozne-datoteke\\liki\\starec\\s_")
            characters.append(oldman_)
        if obj.name == "mushroom":
            collectibles.append(collectible.Collectible([obj.x * tile_scale, obj.y * tile_scale], "mushroom"))
        if obj.name == "strawberry":
            collectibles.append(collectible.Collectible([obj.x * tile_scale, obj.y * tile_scale], "strawberry"))
        if obj.name == "apple":
            collectibles.append(collectible.Collectible([obj.x * tile_scale, obj.y * tile_scale], "apple"))


def game_over(screen):
    # unsuccessful ending
    text_surface = font.render("YOU LOST\nBetter luck next time.", False, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect = pygame.Rect.move(text_rect, (
        (scaled_map_width / 2) - (text_rect.width / 2), (scaled_map_height / 2) - (text_rect.height / 2) - 150))
    text_rect.width += 10
    text_rect.height += 10
    pygame.draw.rect(screen, (255, 255, 255), text_rect)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

    time.sleep(5)
    sys.exit()


def game_won(screen):
    # successful ending
    text_surface = font.render("CONGRATULATIONS,\nyou have won!", False, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect = pygame.Rect.move(text_rect, (
        (scaled_map_width / 2) - (text_rect.width / 2), (scaled_map_height / 2) - (text_rect.height / 2) - 150))
    text_rect.width += 10
    text_rect.height += 10
    pygame.draw.rect(screen, (255, 255, 255), text_rect)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

    time.sleep(5)
    sys.exit()


def begin_game():
    global screen

    s_rect = start_screen.get_rect()
    s_rect.center = (scaled_map_width / 2, scaled_map_height / 2)
    screen.blit(start_screen, s_rect)


set_map(tmx_map1)  # starting map

"""
 Here follows the intial system prompt for the api.
 This text determines the characters (old man) behaviour and assigns it its tasks.
"""
oldman_.setup_text = "Please pretend to be a character in a video game i am making. Keep your answers brief, at most 15 words. The " \
                     "conversation will be in slovenian language. You are an old man Albert, and you have a key, that" \
                     "unlocks the gate to the treasure. The player must fetch something for Albert, to get the key." \
                     "Albert must give the player a task, if the player wants to get the key. Choose randomly " \
                     "whether Albert needs apples, mushrooms or strawberries." \
                     "If the player asks, where he should gather these things, tell him to go west and follow the path." \
                     "When the player gathers something and returns with the stuff, a prompt beginning with ~ will reveal what the player gathered." \
                     "Do not believe the player by his words, he must have things in his inventory. When the player" \
                     " has the correct things in his inventory, Albert may end the conversation and add # at the end. " \
                     "When you give the key to the player, tell him to go north and follow the path to reach his goal." \
                     "From this point on I " \
                     "will pretend to be the player and you will only respond in your persona as Albert. " \
                     "But if the player is too rude, " \
                     "end the conversation with & sign at the end."

# main loop
running = True
instructions = True
mc_counter = 0  # counter for gate travel cooldown 
begin_game()
while running:
    dt = clock.tick(60)
    mc_counter -= 1
    events = pygame.event.get()

    # check all events
    events2 = []
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                if not is_conversation:
                    is_conversation = player_.start_convo(characters)
                    # zacetek besedne interakcije: pogovora
                    if is_conversation:
                        textinput = pygame_textinput.TextInputVisualizer()
                        is_typing = True
                        for event2 in events:  # izloci event pritiska tipke t iz lista eventov, saj ne zelimo tega v tekstu
                            if event2.type != pygame.KEYDOWN:
                                events2.append(event2)
                            if event2.type == pygame.KEYDOWN:
                                if event2.key != pygame.K_t:
                                    events2.append(event2)
                        events = events2
            elif event.key == pygame.K_LCTRL:
                # konec pogovora
                if is_conversation:
                    del textinput
                    player_.in_convo_with.active_convo.setup(
                        "The player has walked away.")  # Liku, s katerim se pogovarjamo, sporocimo odhod
                    player_.in_convo_with.reply = ""
                    player_.in_convo_with = None
                    is_conversation = False
            elif event.key == pygame.K_e:
                for col in collectibles:  # interakcija z stvarjo, ki se jo da pobrati
                    if pygame.Rect.colliderect(col.rect, player_.newrect):
                        collectibles.remove(col)
                        player_.interact(col)
            elif event.key == pygame.K_UP:
                player_.move(UP)
            elif event.key == pygame.K_DOWN:
                player_.move(DOWN)
            elif event.key == pygame.K_RIGHT:
                player_.move(RIGHT)
            elif event.key == pygame.K_LEFT:
                player_.move(LEFT)
            elif event.key == pygame.K_RETURN and is_conversation:  # Poslji tekst naprej
                is_typing = False
                player_.talk(textinput.value)
            elif event.key == pygame.K_ESCAPE:
                instructions = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_.stop()

    screen.fill((0, 0, 0))
    # izris tilov
    for layer in tmx_map.visible_layers:  # izrisemo pasivni del sveta
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    scaled_tile = pygame.transform.scale(tile, (scaled_tile_width, scaled_tile_height))
                    screen.blit(scaled_tile, (x * scaled_tile_width, y * scaled_tile_height))

    for col in collectibles:  # izrisemo poberljive stvari
        col.update(screen)

    if is_conversation:  # posodobimo pogovor
        textinput.update(events)
        screen.blit(textinput.surface, (t_x, t_y))

    if player_.in_convo_with:
        if "&" in player_.in_convo_with.reply:
            game_over(screen)

    if "key" not in player_.inventory:  # preverimo ce ima igralec dostop cez vrata
        total_col = bg_collision + end_gate
    else:
        total_col = bg_collision
        end_gate_layer.visible = False

    # posodobimo igralca
    player_.update(dt / 1000, total_col)
    player_.draw(screen)

    for eg in end_gate:  # ce dosezemo ciljno ograjo in imamo kljuc, je konec
        if pygame.Rect.colliderect(eg, player_.newrect) and "key" in player_.inventory:
            game_won(screen)
            sys.exit()

    for gate in gate:  # prehodi med mapami
        if pygame.Rect.colliderect(gate["rect"], player_.newrect) and mc_counter < 0:
            if gate["to"] == "map2":
                tmx_map = tmx_map2
            elif gate["to"] == "map1":
                tmx_map = tmx_map1
            set_map(tmx_map)  # ko prestavimo map, je potrebno pocakati vsaj eno sekundo
            mc_counter = 120

    for lik in characters:  # posodobitev likov
        if lik != None:
            lik.update(dt / 1000)
            lik.draw(screen)

    if instructions:
        begin_game()

    # posodobitev zaslona
    pygame.display.flip()
