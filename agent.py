import pygame
import os

# states
IDLE_U = "idle_u"
IDLE_D = "idle_d"
IDLE_R = "idle_r"
IDLE_L = "idle_l"

UP = "up"
DOWN = "DOWN"
RIGHT = "RIGHT"
LEFT = "LEFT"

pygame.font.init()
font = pygame.font.SysFont(None, 20)


class Agent(pygame.sprite.Sprite):
    """
    A static character, that the player can initiate a dialog with.
    """

    def __init__(self, position, animation_path):
        super().__init__()
        self.position = position

        self.state = IDLE_R  # initial state
        self.orientation = RIGHT

        self.animation_path = animation_path
        self.animation_frames = []
        self.animation_frames = self.load_animation()
        self.current_frame = self.animation_frames[0]
        self.animation_speed = 4
        self.t_ = 0
        self.ix = 0

        self.reply = ""
        self.offset_x = 30
        self.offset_y = -30

        self.active_convo = None  # is the dialog active?
        self.setup_text = ""

    def update(self, dt):
        # animation
        if self.t_ / 60 > 1 / 4:
            self.next_animation()
            self.t_ = 0
        self.t_ += 1

    def respond_to_talk(self, text):
        # agent responds to player prompt
        self.reply = self.active_convo.new_prompt(text)

    def load_animation(self):
        # animation frames loading
        animation_frames = []
        for i in range(1, 5):
            animation_frames.append(pygame.image.load(os.getcwd() + self.animation_path + str(i) + ".png"))
        return animation_frames

    def scale_char(self, n):
        # scaling animation frames
        for i in range(len(self.animation_frames)):
            x_size = self.animation_frames[i].get_width()
            y_size = self.animation_frames[i].get_height()
            img = pygame.transform.scale(self.animation_frames[i], (x_size * n, y_size * n))
            self.animation_frames[i] = img

    def next_animation(self):
        self.ix += 1
        if self.ix + 1 > len(self.animation_frames):
            self.ix = 0
        self.current_frame = self.animation_frames[self.ix]

    def draw_line(self, line, x, y, screen):
        # display a line of text
        text_surface = font.render(line, False, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect = text_rect.move((x - 5, y - 5))
        text_rect.width += 10
        text_rect.height += 10
        pygame.draw.rect(screen, (255, 255, 255), text_rect)
        screen.blit(text_surface, (x, y))

    def draw_text(self, screen):
        # display the whole character response
        ix = 0
        row = 0
        for i in range(len(self.reply)):
            if (ix >= 30 and self.reply[i] == " "):
                self.draw_line(self.reply[i - ix:i], self.position[0] + self.offset_x,
                               self.position[1] + self.offset_y + 25 * row, screen)
                row += 1
                ix = -1
            elif i == len(self.reply) - 1:
                self.draw_line(self.reply[i - ix:i], self.position[0] + self.offset_x,
                               self.position[1] + self.offset_y + 25 * row, screen)
            ix += 1

    def draw(self, screen):
        # draws itself on the screen and displays the reply, if it exists
        screen.blit(self.current_frame, self.position)
        if self.reply != "":
            self.draw_text(screen)
