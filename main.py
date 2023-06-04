import pygame
import pytmx
import os
import sys
import player
import agent
import pygame_textinput
import collectible

UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"

pygame.init()

clock = pygame.time.Clock()

tile_scale = 2  # Za koliko povecamo tile
screen = pygame.display.set_mode((1, 1))

# Zloadamo mapo
tmx_map1 = pytmx.load_pygame(os.getcwd() + "\\assets\\zacetek.tmx")
tmx_map2 = pytmx.load_pygame(os.getcwd() + "\\assets\\map2.tmx")
tmx_map = tmx_map1

# Zloadamo slike za animacijo
frames_i_u = ["\\spriti\\igralec\\i_u_1.png", "\\spriti\\igralec\\i_u_2.png", "\\spriti\\igralec\\i_u_3.png",
              "\\spriti\\igralec\\i_u_4.png"]
frames_i_r = ["\\spriti\\igralec\\i_r_1.png", "\\spriti\\igralec\\i_r_2.png", "\\spriti\\igralec\\i_r_3.png",
              "\\spriti\\igralec\\i_r_4.png"]
frames_i_d = ["\\spriti\\igralec\\i_d_1.png", "\\spriti\\igralec\\i_d_2.png", "\\spriti\\igralec\\i_d_3.png",
              "\\spriti\\igralec\\i_d_4.png"]
frames_i_l = ["\\spriti\\igralec\\i_l_1.png", "\\spriti\\igralec\\i_l_2.png", "\\spriti\\igralec\\i_l_3.png",
              "\\spriti\\igralec\\i_l_4.png"]

# Racun dimenzij posameznega tila
scaled_tile_width = tmx_map.tilewidth * tile_scale
scaled_tile_height = tmx_map.tileheight * tile_scale

# Racun dimenzij cele mape
scaled_map_width = tmx_map.width * scaled_tile_width
scaled_map_height = tmx_map.height * scaled_tile_height

screen = pygame.display.set_mode((scaled_map_width, scaled_map_height))

# Ali smo trenutno v pogovoru
is_conversation = False
is_typing = False

t_x = 40
t_y = scaled_map_height - 80
t_w = 200

font = pygame.font.SysFont(None, 100)

player_ = player.Player([0, 0])
oldman_ = None

bg_collision = []
prehod = []
collectibles = []
liki = []
end_gate = []


def set_map(tmap):
    global tmx_map
    global prehod
    global bg_collision
    global player_
    global oldman_
    global collectibles
    global liki
    global end_gate
    prehod = []
    bg_collision = []
    collectibles = []
    end_gate = []
    liki = []
    tmx_map = tmap

    for layer in tmx_map.layers:
        if layer.name == "collision":
            for obj in layer.tiles():
                bg_rect = pygame.rect.Rect(tile_scale * 16 * obj[0], tile_scale * 16 * obj[1], 32, 32)
                bg_collision.append(bg_rect)
        if layer.name == "prehodi":
            print("da")
            for p in layer.tiles():
                props = layer.properties
                print(props)
                prehod.append({"to": props.get("to"),
                               "rect": pygame.rect.Rect(tile_scale * 16 * p[0], tile_scale * 16 * p[1], 32, 32)})
        if layer.name == "end_gate":
            for p in layer.tiles():
                end_gate.append(pygame.rect.Rect(tile_scale * 16 * p[0], tile_scale * 16 * p[1], 32, 32))

    temp = player_.position
    for obj in tmx_map.objects:  # Iz tmx mape dobimo zacetne polozaje nasih likov
        if obj.name == "zacetek" and temp[0] == 0 and temp[1] == 0:
            player_object = obj
            player_ = player.Player([player_object.x * tile_scale, player_object.y * tile_scale])
        if obj.name == "pos_p" and (temp[0] != 0 or temp[1] != 0):
            player_object = obj
            player_.position = [player_object.x * tile_scale, player_object.y * tile_scale]
        if obj.name == "starec":
            if oldman_ == None:
                oldman_object = obj
                oldman_ = agent.Agent([oldman_object.x * tile_scale, oldman_object.y * tile_scale],
                                      "\\spriti\\starec\\s_")
            liki.append(oldman_)

        if obj.name == "goba":
            collectibles.append(collectible.Collectible([obj.x * tile_scale, obj.y * tile_scale], "goba"))
        if obj.name == "jagoda":
            collectibles.append(collectible.Collectible([obj.x * tile_scale, obj.y * tile_scale], "jagoda"))
        if obj.name == "jabolko":
            collectibles.append(collectible.Collectible([obj.x * tile_scale, obj.y * tile_scale], "jabolko"))


set_map(tmx_map1)

oldman_.setup_text = "Please pretend to be a character in a video game i am making. Keep your answers brief, at most 70 words. The " \
                     "conversation will be in slovenian language. You are an old man Albert, and you have a key, that" \
                     "unlocks the gate to the treasure. The player must fetch something for Albert, to get the key." \
                     "Albert must give the player a task, if the player wants to get the key. Choose randomly " \
                     "whether Albert needs apples, mushrooms or strawberries." \
                     "When the player gathers something and returns with the stuff, a prompt beginning with ~ will reveal what the player gathered." \
                     "Do not believe the player by his words, he must have things in his inventory. When the player" \
                     " has the correct things in his inventory, Albert may end the conversation and add # at the end. " \
                     "From this point on I " \
                     "will pretend to be the player and you will only respond in your persona as Albert. " \
                     "But if the player is too rude, " \
                     "end the conversation with & sign at the end."
# Glavna zanka
running = True
mc_counter = 0
while running:
    dt = clock.tick(60)
    mc_counter -= 1
    events = pygame.event.get()

    events2 = []
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                if not is_conversation:
                    is_conversation = player_.start_convo(liki)
                    # Zacetek besedne interakcije: pogovora
                    if is_conversation:
                        textinput = pygame_textinput.TextInputVisualizer()
                        is_typing = True
                        for event2 in events:  # Izloci event pritiska tipke t iz lista eventov, saj ne zelimo tega v tekstu
                            if event2.type != pygame.KEYDOWN:
                                events2.append(event2)
                            if event2.type == pygame.KEYDOWN:
                                if event2.key != pygame.K_t:
                                    events2.append(event2)
                        events = events2
            elif event.key == pygame.K_LCTRL:
                # Konec pogovora
                if is_conversation:
                    del textinput
                    player_.in_convo_with.active_convo.setup("The player has walked away.")
                    player_.in_convo_with.reply = ""
                    player_.in_convo_with = None
                    is_conversation = False
            elif event.key == pygame.K_e:
                for col in collectibles:
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
            elif event.key == pygame.K_RETURN and is_conversation:
                is_typing = False
                player_.talk(textinput.value)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_.stop()

    screen.fill((0, 0, 0))

    # Izris tilov
    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    scaled_tile = pygame.transform.scale(tile, (scaled_tile_width, scaled_tile_height))
                    screen.blit(scaled_tile, (x * scaled_tile_width, y * scaled_tile_height))

    for col in collectibles:
        col.update(screen)

    if is_conversation:
        textinput.update(events)
        screen.blit(textinput.surface, (t_x, t_y))

    if "key" not in player_.inventory:
        total_col = bg_collision+end_gate
    else:
        total_col = bg_collision
    player_.update(dt / 1000, total_col)
    player_.draw(screen)

    for eg in end_gate:
        if pygame.Rect.colliderect(eg, player_.newrect) and "key" in player_.inventory:
            print("Zmagal si!")
            sys.exit()

    for gate in prehod:
        if pygame.Rect.colliderect(gate["rect"], player_.newrect) and mc_counter < 0:
            if gate["to"] == "map2":
                tmx_map = tmx_map2
            elif gate["to"] == "map1":
                tmx_map = tmx_map1
            set_map(tmx_map)  # ko prestavimo map, je potrebno pocakati vsaj eno sekundo
            mc_counter = 120
    for lik in liki:
        if lik != None:
            lik.update(dt / 1000)
            lik.draw(screen)

    # Posodobitev zaslona
    pygame.display.flip()
