import pygame

class Agent:
    def __init__(self, position):
        self.position = position  # Agent's position
        self.state = IDLE  # Initial state is idle
        self.load_animations()  # Load animations for different states
        self.current_animation = self.animations[self.state]  # Current animation based on state

    def load_animations(self):
        # Load animations for different states
        self.animations = {
            WALK: self.load_animation('walk_animation_folder'),
            IDLE: self.load_animation('idle_animation_folder'),
            TALK: self.load_animation('talk_animation_folder')
        }

    def load_animation(self, folder):
        # Load animation frames from the specified folder
        animation_frames = []
        # Load frames using Pygame or your preferred animation library
        # Append each frame to the animation_frames list
        return animation_frames

    def set_state(self, state):
        # Set the player's state and update the current animation accordingly
        if state in self.animations:
            self.state = state
            self.current_animation = self.animations[state]

    def play_current_animation(self):
        # Play the current animation frame
        # Render the current frame using Pygame or your preferred rendering method
        pass

    def respond_to_talk(self,text):
        # Method called when the player talks with the agent
        print("Agent: Hello! How can I assist you?")

    def draw(self, surface):
        # Draw the agent on the given surface at its current position
        surface.blit(self.image, self.position)
