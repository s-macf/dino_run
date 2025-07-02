import pygame
from scripts.utils import load_sprite_sequence, RESCALE_VALUE

START_POS = (20, 152 - 20 - (43 * RESCALE_VALUE))

class Player:
    def __init__(self):
        self.standing_sprites = load_sprite_sequence("sprites/dino/dino.png", 40)
        self.crouched_sprites = load_sprite_sequence("sprites/dino/dino_crouch.png", 55)
        self.sprite = self.standing_sprites[0]
        self.animation_timer = 0
        self.is_standing = True

        self.rect = self.sprite.get_rect().move(*START_POS)
        self.colour = "red"
        self.velocity = 0
        self.on_ground = False
        self.is_dead = False

    def update(self, grounds, dt):
        self.rect.top += self.velocity * dt
        if self.is_standing:
            self.sprite = self.standing_sprites[int(self.animation_timer % len(self.standing_sprites))]
        else:
            self.sprite = self.crouched_sprites[int(self.animation_timer % len(self.crouched_sprites))]

        self.animation_timer += 0.1

        for ground in grounds:
            if self.rect.colliderect(ground):
                self.rect.bottom = ground.top
                self.on_ground = True

        self.velocity = min(300, self.velocity + 20)


    def crouch(self):
        self.rect.top += abs(self.crouched_sprites[0].height - self.standing_sprites[0].height)
        self.rect.size = (self.crouched_sprites[0].width, self.crouched_sprites[0].height)
        self.is_standing = False

    def stand(self):
        self.rect.top -= (self.standing_sprites[0].height/2)
        self.rect.size = self.standing_sprites[0].size
        self.is_standing = True

    def jump(self):
        if self.on_ground:
            self.on_ground = False
            self.velocity = -500

    def reset(self):
        self.rect = pygame.FRect(START_POS, (self.rect.width, self.rect.height))
        self.on_ground = False
        self.is_dead = False
        self.sprite = self.standing_sprites[0]
        self.animation_timer = 0
        self.is_standing = True