import pygame
import random

class StarField(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.__stars = []
        for i in range(100):
            x_value = random.uniform(0, 1024)
            y_value = random.uniform(0, 768)
            speed = random.randrange(50, 200)
            self.__stars.append([x_value, y_value, speed])

    def update(self, dt):
        for i in range(len(self.__stars)):
            self.__stars[i][1] += self.__stars[i][2]

    def draw(self, surface):
        for i in range(len(self.__stars)):
            pygame.draw.circle(surface, (0, 255, 255), (self.__stars[i][0], self.__stars[i][1]), 2)

