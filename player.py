import pygame
import os
import math
import conversation

# stanja
WALK_U = "walk_u"
WALK_D = "walk_d"
WALK_R = "walk_r"
WALK_L = "walk_l"

IDLE_U = "idle_u"
IDLE_D = "idle_d"
IDLE_R = "idle_r"
IDLE_L = "idle_l"

UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"

frames_i_u = ["\\spriti\\igralec\\i_u_1.png", "\\spriti\\igralec\\i_u_2.png", "\\spriti\\igralec\\i_u_3.png",
              "\\spriti\\igralec\\i_u_4.png"]
frames_i_r = ["\\spriti\\igralec\\i_r_1.png", "\\spriti\\igralec\\i_r_2.png", "\\spriti\\igralec\\i_r_3.png",
              "\\spriti\\igralec\\i_r_4.png"]
frames_i_d = ["\\spriti\\igralec\\i_d_1.png", "\\spriti\\igralec\\i_d_2.png", "\\spriti\\igralec\\i_d_3.png",
              "\\spriti\\igralec\\i_d_4.png"]
frames_i_l = ["\\spriti\\igralec\\i_l_1.png", "\\spriti\\igralec\\i_l_2.png", "\\spriti\\igralec\\i_l_3.png",
              "\\spriti\\igralec\\i_l_4.png"]


class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.velocity = [0, 0]
        self.v_max = 50
        self.newrect = None

        self.in_convo_with = None
        self.min_rad = 30

        self.state = IDLE_R
        self.orientation = RIGHT
        self.load_animations()
        self.current_animation = self.animations[self.state]
        self.current_frame = self.load_animation(IDLE_R)[0]
        self.animation_speed = 4
        self.t_ = 0
        self.ix = 0

        self.inventory = []

    def update(self, dt, bg_collision):
        collides = False
        newpos = [self.position[0] + self.velocity[0] * dt, self.position[1] + self.velocity[1] * dt]
        self.newrect = pygame.rect.Rect(newpos, (32, 32))
        for tile in bg_collision:
            if pygame.Rect.colliderect(tile, self.newrect):
                collides = True
        if not collides:
            self.position = newpos

        if self.t_ / 60 > 1 / 4:
            self.next_animation()
            self.t_ = 0
        self.t_ += 1

    def move(self, dir):
        if dir == "right":
            self.velocity = (self.v_max, 0)
            self.set_state(WALK_R)
        if dir == "left":
            self.velocity = (-self.v_max, 0)
            self.set_state(WALK_L)
        if dir == "up":
            self.velocity = (0, -self.v_max)
            self.set_state(WALK_U)
        if dir == "down":
            self.velocity = (0, self.v_max)
            self.set_state(WALK_D)

    def stop(self):
        self.velocity = [0, 0]
        if self.state == WALK_U:
            self.set_state(IDLE_U)
        elif self.state == WALK_D:
            self.set_state(IDLE_D)
        elif self.state == WALK_R:
            self.set_state(IDLE_R)
        elif self.state == WALK_L:
            self.set_state(IDLE_L)

    def talk(self, text):
        self.in_convo_with.respond_to_talk(text)

        if "#" in self.in_convo_with.reply:
            self.inventory.append("key")

    def load_animations(self):
        # Shrani vse slike v en dict
        self.animations = {
            WALK_U: self.load_animation(WALK_U),
            WALK_D: self.load_animation(WALK_D),
            WALK_R: self.load_animation(WALK_R),
            WALK_L: self.load_animation(WALK_L),
            IDLE_U: self.load_animation(IDLE_U),
            IDLE_D: self.load_animation(IDLE_D),
            IDLE_L: self.load_animation(IDLE_L),
            IDLE_R: self.load_animation(IDLE_R),
        }

    def load_animation(self, state):
        # Vrni list z slikami
        animation_frames = []
        if state == WALK_U:
            for addr in frames_i_u:
                animation_frames.append(pygame.image.load(os.getcwd() + addr))
        if state == WALK_D:
            for addr in frames_i_d:
                animation_frames.append(pygame.image.load(os.getcwd() + addr))
        if state == WALK_R:
            for addr in frames_i_r:
                animation_frames.append(pygame.image.load(os.getcwd() + addr))
        if state == WALK_L:
            for addr in frames_i_l:
                animation_frames.append(pygame.image.load(os.getcwd() + addr))
        if state == IDLE_U:
            animation_frames = [pygame.image.load(os.getcwd() + frames_i_u[0])]
        if state == IDLE_D:
            animation_frames = [pygame.image.load(os.getcwd() + frames_i_d[0])]
        if state == IDLE_R:
            animation_frames = [pygame.image.load(os.getcwd() + frames_i_r[0])]
        if state == IDLE_L:
            animation_frames = [pygame.image.load(os.getcwd() + frames_i_l[0])]
        # Load frames using Pygame or your preferred animation library
        # Append each frame to the animation_frames list

        for i in range(len(animation_frames)):
            x_size = animation_frames[i].get_width()
            y_size = animation_frames[i].get_height()
            img = pygame.transform.scale(animation_frames[i], (x_size * 2, y_size * 2))
            animation_frames[i] = img
        return animation_frames

    def set_state(self, state):
        if state in self.animations:
            self.state = state
            self.current_animation = self.animations[state]
            self.current_frame = self.current_animation[0]

    def next_animation(self):
        self.ix += 1
        if self.ix + 1 > len(self.current_animation):
            self.ix = 0
        self.current_frame = self.current_animation[self.ix]

    def draw(self, screen):
        screen.blit(self.current_frame, self.position)

    def start_convo(self, liki):
        # Preveri ce je v zadostni blizini drugih likov
        for lik in liki:
            if math.sqrt((self.position[0] - lik.position[0]) ** 2 + (
                    self.position[1] - lik.position[1]) ** 2) < self.min_rad:
                self.in_convo_with = lik

                if not self.in_convo_with.active_convo is None:
                    if len(self.inventory) > 0:
                        self.in_convo_with.active_convo.setup(
                            "~The player has returned with the following things in his inventory: " + ", ".join(
                                self.inventory) + ".")
                    else:
                        self.in_convo_with.active_convo.setup("~The player has returned with nothing in his inventory.")

                if self.in_convo_with.active_convo is None:
                    self.in_convo_with.active_convo = conversation.Conversation()
                    self.in_convo_with.active_convo.setup(self.in_convo_with.setup_text)
                return True

    def interact(self, col):
        self.inventory.append(col.type)
        print(self.inventory)
