import pygame
import pytmx
import os
import player
import agent
import pygame_textinput

UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"

pygame.init()

clock = pygame.time.Clock()

tile_scale = 2  # Za koliko povecamo tile
screen = pygame.display.set_mode((1, 1))

# Zloadamo mapo
tmx_map = pytmx.load_pygame(os.getcwd() + "\\assets\\zacetek.tmx")

# Zloadamo slike za animacijo
frames_i_u = ["\\spriti\\igralec\\i_u_1.png","\\spriti\\igralec\\i_u_2.png","\\spriti\\igralec\\i_u_3.png","\\spriti\\igralec\\i_u_4.png"]
frames_i_r = ["\\spriti\\igralec\\i_r_1.png","\\spriti\\igralec\\i_r_2.png","\\spriti\\igralec\\i_r_3.png","\\spriti\\igralec\\i_r_4.png"]
frames_i_d = ["\\spriti\\igralec\\i_d_1.png","\\spriti\\igralec\\i_d_2.png","\\spriti\\igralec\\i_d_3.png","\\spriti\\igralec\\i_d_4.png"]
frames_i_l = ["\\spriti\\igralec\\i_l_1.png","\\spriti\\igralec\\i_l_2.png","\\spriti\\igralec\\i_l_3.png","\\spriti\\igralec\\i_l_4.png"]

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
t_y = scaled_map_height-80
t_w = 200

font = pygame.font.SysFont(None, 100)

for obj in tmx_map.objects:  # Iz tmx mape dobimo zacetne polozaje nasih likov
    if obj.name == "zacetek":
        player_object = obj
        player_ = player.Player([player_object.x, player_object.y])
    if obj.name == "starec":
        oldman_object = obj
        oldman_ = agent.Agent([oldman_object.x, oldman_object.y],"\\spriti\\starec\\s_")

oldman_.setup_text="Please pretend to be a character in a video game i am making. Keep your answers brief. The " \
                "conversation will be in slovenian language. You are an old man Albert, who has information about the " \
                "location of a treasure. Albert has a short temper and doesn't like young brats. From this point on I " \
                "will pretend to be the player and you will only respond in your persona. Never respond as the " \
                "player. You must not give the information to the player right away, but rather the player must " \
                "persuade you into giving the information. Never give the information on the first prompt. Only if " \
                "the player was persuasive enough and well mannered, reveal the location and then add sign % at the " \
                "end of the response. But if the player is too rude and you feel like not talking anymore, " \
                "end the conversation with & sign at the end"

liki = [oldman_]
# Glavna zanka
running = True
while running:
    dt = clock.tick(60)
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

    if is_conversation:
        textinput.update(events)
        screen.blit(textinput.surface, (t_x, t_y))

    player_.update(dt/1000)
    player_.draw(screen)

    for lik in liki:
        lik.update(dt/1000)
        lik.draw(screen)

    # Posodobitev zaslona
    pygame.display.flip()
