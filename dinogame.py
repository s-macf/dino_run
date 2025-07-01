import pygame
import numpy as np
from player import Player

class DinoGame:
    def __init__(self, window_size, screen):
        self.player = Player()
        self.ground = pygame.FRect((0, window_size[1] - 30), (window_size[0], 30))
        self.obj_velocity = 100
        self.objs = [pygame.FRect((500, window_size[1] - 70), (20, 40))]
        self.load_new_obstacle = False
        self.prev_actions = np.zeros(3)
        self.score = 0
        self.screen = screen
        self.font = pygame.font.SysFont(None, 42)

    def load_obstacles(self):
        if self.load_new_obstacle:
            self.objs.append(pygame.FRect((500, self.screen.height - 70), (20, 40)))
            self.load_new_obstacle = False

    def handle_player_movement(self, actions):
        if actions[0]:
            self.player.jump()
        if actions[1] != self.prev_actions[1]:
            if actions[1]:
                self.player.crouch()
            else:
                self.player.stand()

        self.prev_actions = actions

    def update(self, actions, dt):
        self.score += 0.1
        self.load_obstacles()
        self.handle_player_movement(actions)
        self.player.update(self.ground, dt)

        for obj in self.objs:
            obj.left -= self.obj_velocity * dt
            if obj.left < self.screen.width / 3 and len(self.objs) < 2:
                self.load_new_obstacle = True
            if obj.right < 0:
                self.objs.remove(obj)
            if self.player.rect.colliderect(obj):
                self.player.is_dead = True
                break

        reward = self.score if self.player.is_dead else -10
        state = self.get_image_array()
        terminated = self.player.is_dead
        truncated = None

        return state, reward, terminated, truncated
        

    def render(self, screen):
        screen.fill("lightblue")
        text = self.font.render(f"Score: {int(self.score)}", True, "black")
        screen.blit(text, (0, 0))

        for obj in self.objs:
            pygame.draw.rect(screen, "darkgreen", obj)  

        pygame.draw.rect(screen, "black", self.ground)
        pygame.draw.rect(screen, self.player.colour, self.player.rect)

    def reset():
        pass

    def get_image_array(self):
        image_array = pygame.surfarray.array3d(self.screen)
        image_array = np.transpose(image_array, (1, 0, 2))
        return image_array