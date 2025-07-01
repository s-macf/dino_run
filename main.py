import gymnasium as gym
import pygame
import numpy as np
from dinogame import DinoGame

TESTING = False

class DinoGameWrapper(gym.Env):

    def __init__(self, env_size, render_mode="rgb_array"):
        super().__init__()

        self.window_size = env_size
        pygame.init() if render_mode == "human" else None
        pygame.display.set_caption("Dino Run") if render_mode == "human" else None
        self.screen = pygame.display.set_mode(self.window_size) if render_mode == "human" else pygame.Surface(self.window_size)
        self.clock = pygame.Clock() if render_mode == "human" else None

        # Modify observation/action/reward spaces if needed
        self.action_space = gym.spaces.Discrete(3)
        self.render_mode = render_mode
        self.game = DinoGame(self.window_size, self.screen)


    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        # Modify observation if needed
        return obs, info

    def step(self, actions):
        dt = 1/60
        
        state, reward, terminated, truncated = self.game.update(actions, dt)
        
        return state, reward, terminated, truncated
    
    def render(self):
        if self.render_mode == "human":
            self.game.render(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        else:
            self.game.render(self.screen)
            image_array = self.game.get_image_array()

            if TESTING:
                pygame.init()
                display = pygame.display.set_mode(self.window_size)
                display.blit(self.screen)
                pygame.display.flip()

            print(image_array)

    def human_mode(self):
        running = True
        if self.render_mode == "human":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        keys = pygame.key.get_pressed()
        keys_pressed = [keys[pygame.K_w], keys[pygame.K_s], 0]

        return running, keys_pressed

    def training_loop(self):
        running = True
        while running:
            if self.render_mode == "human":
                self.render()
                running, action = self.human_mode()
                state, reward, terminated, truncated = self.step(action)
            else:
                self.render()
                state, reward, terminated, truncated = self.step([1, 0])

window_size = (640, 320)
DinoGameWrapper(env_size=window_size, render_mode="human").training_loop()
# DinoGameWrapper(env_size=window_size).training_loop()
