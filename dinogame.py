import pygame
import numpy as np
from player import Player
import random
from scripts.utils import load_sprite_sequence, load_image, sample_sheet

DELTA_TIME = 1/60
SMALL_CACTUS_DIMS = (17, 33)
BIG_CACTUS_DIMS = (24, 46)

class Obstacle:

    def __init__(self, sprite, window_size):
        self.sprite = sprite
        pos = (window_size[0], window_size[1] - 20 - self.sprite.get_height())
        self.rect = pygame.FRect(pos, (self.sprite.width, self.sprite.height))

class FlyingDino(Obstacle):

    def __init__(self, sprite, window_size):
        super().__init__(sprite, window_size)
        random_y = random.randint(window_size[1] / 2 - self.sprite.height, window_size[1] - 60)
        self.rect = pygame.FRect((window_size[0], random_y), (self.sprite.width, self.sprite.height))
        self.animation_timer = 0

    def update(self, sheet):
        self.sprite = sheet[int(self.animation_timer % len(sheet))]
        self.animation_timer += 0.1

class DinoGame:
    def __init__(self, window_size, screen):
        self.player = Player()
        self.ground_sprite = load_image("sprites/ground.png", scale=1)
        self.grounds = [pygame.FRect((0, window_size[1] - 20), (window_size[0], 20)), pygame.FRect((window_size[0], window_size[1] - 20), (window_size[0], 20))]

        self.small_cactus = load_image('sprites/cacti/small_cactus.png')
        self.big_cactus = load_image('sprites/cacti/big_cactus.png')
        self.four_cacti = load_image('sprites/cacti/four_cacti.png')

        self.flying_dino_sheet = load_sprite_sequence('sprites/flying_dino/flying_dino.png', 41)

        self.obj_velocity = 150
        self.objs = []
        self.obj_spawn_timer = 2

        self.prev_actions = np.zeros(3)
        self.score = 0
        self.screen = screen

    def add_cactus_sequence(self, sequence_length):
        rand_int = random.randint(0, 1)
        sprite_sheet = self.small_cactus if rand_int == 0 else self.big_cactus
        cactus_dims = SMALL_CACTUS_DIMS if rand_int == 0 else BIG_CACTUS_DIMS
        cactus = sample_sheet(sprite_sheet, cactus_dims, sequence_length)
        return cactus

    def add_random_object(self):
        randint = random.randint(1, 5)
        if randint <= 3:
            obstacle =  Obstacle(self.add_cactus_sequence(randint), (self.screen.width, self.screen.height))
        elif randint == 4:
            obstacle =  Obstacle(self.four_cacti, (self.screen.width, self.screen.height))
        else:
            obstacle = FlyingDino(self.flying_dino_sheet[0], (self.screen.width, self.screen.height))

        self.objs.append(obstacle)

    def load_obstacles(self, dt):
        if len(self.objs) == 0:
            self.add_random_object()
            self.obj_spawn_timer = 2
        else:
            self.obj_spawn_timer -= 1 * dt
            if random.random() < 0.05 and self.obj_spawn_timer <= 0:
                self.add_random_object()
                self.obj_spawn_timer = 2

    def handle_player_movement(self, actions):
        if actions[1]:
            self.player.jump()
        if actions[2] != self.prev_actions[2]:
            if actions[2]:
                self.player.crouch()
            else:
                self.player.stand()

        self.prev_actions = actions

    def update(self, actions, dt):
        self.score += 0.1
        self.load_obstacles(dt)
        self.handle_player_movement(actions)
        self.player.update(self.grounds, dt)
        self.obj_spawn_timer -= 1 * dt

        for ground in self.grounds:
            ground.x -= self.obj_velocity * dt
            if ground.right < 0:
                ground.left = self.screen.width

        obj_index = 0
        while obj_index < len(self.objs):
            obj = self.objs[obj_index]
            obj_rect = obj.rect
            obj_rect.x -= self.obj_velocity * dt

            if type(obj) is FlyingDino:
                obj.update(self.flying_dino_sheet)

            if obj_rect.right < 0:
                if len(self.objs) == 1:
                    self.objs.pop()
                else:
                    temp = self.objs[-1]
                    self.objs[obj_index] = temp
                    self.objs.pop()
                continue
            if self.player.rect.colliderect(obj_rect):
                self.player.is_dead = True
                break
            obj_index += 1

        reward = self.score if self.player.is_dead else -10
        state = self.get_state()
        terminated = self.player.is_dead
        truncated = None

        return state, reward, terminated, truncated
        

    def render(self, screen):
        screen.fill("white")
        score = str(int(self.score)).zfill(5)
        self.font = pygame.font.SysFont(None, 28)
        text = self.font.render(score, True, "black")
        screen.blit(text, (screen.width - text.width-10, 0))

        # screen.blit(self.ground_sprite, (self.ground.x, self.ground.y-10))
        for ground in self.grounds:
            # pygame.draw.rect(screen, (0, 255, 0), x)
            screen.blit(self.ground_sprite, (ground.x, ground.y-10))

        # pygame.draw.rect(screen, "black", self.ground)
        for obj in self.objs:
            # pygame.draw.rect(screen, "green", obj)
            screen.blit(obj.sprite, obj.rect)



        # pygame.draw.rect(screen, self.player.colour, self.player.rect)
        screen.blit(self.player.sprite, (self.player.rect.x, self.player.rect.y))

    def reset(self):
        self.objs = []
        self.prev_actions = np.zeros(3)
        self.player.reset()
        self.score = 0
        self.obj_spawn_timer = 0

        return self.get_state()

    def get_state(self):
        image_array = pygame.surfarray.array3d(self.screen)
        image_array = np.transpose(image_array, (1, 0, 2))
        return image_array