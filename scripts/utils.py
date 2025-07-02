import pygame
import random
from PIL import Image

RESCALE_VALUE = 0.8

def load_image(file_path, scale=RESCALE_VALUE):
    # image = pygame.image.load(file_path).convert_alpha()
    # image = pygame.transform.scale_by(image, scale)

    image = Image.open(file_path).convert('RGBA')
    mode = image.mode
    size = image.size
    data = image.tobytes()
    image = pygame.image.frombytes(data, size, mode)
    image = pygame.transform.scale_by(image, scale)

    return image


def load_sprite_sequence(file_path, sprite_width):
    sprites = []

    sprite_sheet = load_image(file_path)
    sheet_width = sprite_sheet.width
    sheet_height = sprite_sheet.height

    sprite_width *= RESCALE_VALUE
    sprite_height = sheet_height

    index = 0
    while index < (sheet_width//sprite_width):
        selection = sprite_width * index
        texture = pygame.Surface((sprite_width, sheet_height))
        texture.blit(sprite_sheet, (0, 0), pygame.Rect(selection, 0, sprite_width, sprite_height))
        texture.set_colorkey("black")
        sprites.append(texture)
        index += 1

    return sprites

def sample_sheet(sheet, sprite_dims, sequence_length):
    sprite_width, sprite_height = sprite_dims[0] * RESCALE_VALUE, sprite_dims[1] * RESCALE_VALUE
    upperbround = int(sheet.width // sprite_width)

    if sequence_length == 2:
        upperbround -= 1
    elif sequence_length == 3:
        upperbround -= 2

    surface = pygame.Surface((sprite_width * sequence_length, sprite_height))
    index = 0
    while index < sequence_length:
        rand_int = random.randint(0, upperbround)
        selection = sprite_width * rand_int
        surface.blit(sheet, (sprite_width * index, 0), pygame.Rect(selection, 0, sprite_width, sprite_height))
        index += 1

    surface.set_colorkey("black")
    return surface