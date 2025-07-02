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

        self.action_space = gym.spaces.Discrete(3)
        self.render_mode = render_mode
        self.game = DinoGame(self.window_size, self.screen)


    def reset(self):
        state = self.game.reset()
        return state

    def step(self, action):
        dt = 1/60
        actions = [0, 0, 0]
        actions[action] = 1
        
        state, reward, terminated, truncated = self.game.update(actions, dt)
        
        return state, reward, terminated, truncated
    
    def render(self):
        if self.render_mode == "human":
            self.game.render(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        else:
            self.game.render(self.screen)
            image_array = self.game.get_state()

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
        if keys[pygame.K_s]:
            action = 2
        elif keys[pygame.K_w]:
            action = 1
        else:
            action = 0

        return running, action

    def training_loop(self):
        running = True
        scores = []
        while running:
            if self.render_mode == "human":
                self.render()
                running, action = self.human_mode()
                state, reward, terminated, truncated = self.step(action)
            else:
                self.render()
                state, reward, terminated, truncated = self.step([1, 0])

            if terminated or truncated:
                state = self.game.reset()
                scores.append(reward)
        print(max(scores))

window_size = (480, 152)
DinoGameWrapper(env_size=window_size, render_mode="human").training_loop()
# DinoGameWrapper(env_size=window_size).training_loop()
