import pygame

class Sprites:
    def __init__(self, image, hitbox):
        self.image = image
        self.hitbox = hitbox

    def get_x(self) -> int:
        return self.hitbox.x

    def get_y(self) -> int:
        return self.hitbox.y

    def set_x(self, int) -> int:
        self.hitbox.x += int

    def set_y(self, int) -> int:
        self.hitbox.y += int