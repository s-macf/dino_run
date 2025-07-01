import pygame

WIDTH = 30
HEIGHT = 30
START_POS = (20, 260)

class Player:
    def __init__(self):
        self.rect = pygame.FRect(START_POS, (WIDTH, HEIGHT))
        self.colour = "red"
        self.velocity = 0
        self.on_ground = False
        self.is_dead = False

    def update(self, ground, dt):
        self.rect.top += self.velocity * dt

        if self.rect.colliderect(ground):
            self.rect.bottom = ground.top
            self.on_ground = True

        self.velocity = min(200, self.velocity + 10)


    def crouch(self):
        self.rect.top += (HEIGHT/2)
        self.rect.size = (WIDTH, self.rect.height/2)

    def stand(self):
        self.rect.top -= (HEIGHT/2)
        self.rect.size = (WIDTH, HEIGHT)

    def jump(self):
        if self.on_ground:
            self.on_ground = False
            self.velocity = -350

    def reset(self):
        self.rect = pygame.FRect(START_POS, (WIDTH, HEIGHT))
        self.on_ground = False
        self.is_dead = False