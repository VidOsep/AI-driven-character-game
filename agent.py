import pygame
import os
import math
import conversation

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
    Lik, zanj predpostavljamo da je staticen, torej se ne premika in ima konstantno smer.
    """
    def __init__(self, position, animation_path):
        super().__init__()
        self.position = position

        self.state = IDLE_R  # Zacetni state
        self.orientation = RIGHT

        self.animation_path = animation_path
        self.animation_frames = []
        self.animation_frames = self.load_animation()
        self.current_frame = self.animation_frames[0]
        self.animation_speed = 4
        self.t_ = 0
        self.ix=0

        self.reply = ""
        self.offset_x=30
        self.offset_y=-30

        self.active_convo = None
        self.setup_text = ""

    def update(self,dt):
        # Animacija
        if self.t_/60>1/4:
            self.next_animation()
            self.t_=0
        self.t_+=1

    def respond_to_talk(self, text):
        # Odziv lika na govor igralca
        self.reply=self.active_convo.new_prompt(text)

    def load_animation(self):
        # Vrni list z slikami
        animation_frames = []
        for i in range(1,5):
            animation_frames.append(pygame.image.load(os.getcwd()+self.animation_path+str(i)+".png"))
        return animation_frames

    def scale_char(self,n):
        for i in range(len(self.animation_frames)):
            x_size = self.animation_frames[i].get_width()
            y_size = self.animation_frames[i].get_height()
            img = pygame.transform.scale(self.animation_frames[i], (x_size * n, y_size * n))
            self.animation_frames[i] = img


    def next_animation(self):
        self.ix+=1
        if self.ix+1>len(self.animation_frames):
            self.ix=0
        self.current_frame=self.animation_frames[self.ix]

    def draw_line(self,line,x,y,screen):
        text_surface = font.render(line, False, (0,0,0))
        text_rect = text_surface.get_rect()
        text_rect = text_rect.move((x-5,y-5))
        text_rect.width +=10
        text_rect.height +=10
        pygame.draw.rect(screen,(255,255,255),text_rect)
        screen.blit(text_surface, (x,y))

    def draw_text(self,screen):
        ix = 0
        row=0
        for i in range(len(self.reply)):
            if (ix >= 30 and self.reply[i] == " "):
                self.draw_line(self.reply[i-ix:i],self.position[0]+self.offset_x,self.position[1]+self.offset_y+25*row,screen)
                row+=1
                ix=-1
            elif i == len(self.reply) - 1:
                self.draw_line(self.reply[i-ix:i],self.position[0]+self.offset_x,self.position[1]+self.offset_y+25*row,screen)
            ix += 1

    def draw(self,screen):
        screen.blit(self.current_frame,self.position)
        if self.reply!="":
            self.draw_text(screen)

