import pygame
from collideable import ObjectSpawner
from starfield import StarField
from hud_elements import HudElement
from player import Player

class GameManager:
    def __init__(self, engine):
        self.__engine = engine
        self.__player = Player(512, 384, self)
        self.__groups = {}
        self.__object_spawner = ObjectSpawner(self)
        self.__score = 0
        self.__time = 0.0
        self.__elapsed_time = 0.0
        self.__speed_multiplier = 1.0
        self.__hud_font = pygame.font.Font(None, 36)
        self.__setup_groups()
        self.__setup_hud()

    def get_score(self):
        return self.__score
    def add_to_score(self, points):
        if isinstance(points, int):
            if points:
                self.__score += points
    def get_speed_multiplier(self):
        return self.__speed_multiplier
    def get_time(self):
        return self.__time
    def add_group(self, group):
        self.__groups[group] = pygame.sprite.Group()
    def get_group(self, group):
        return self.__groups[group]
    def add_object(self, obj, group='all'):
        if group not in self.__groups:
            self.add_group(group)
        self.__groups[group].add(obj)
    def clear_enemies(self):
        for enemy in self.__groups['enemies']:
            enemy.kill()

    def __setup_groups(self):
        # Add sprite groups
        self.add_group('all')
        self.add_group('enemies')
        self.add_group('projectiles')
        self.add_group('powerups')
        self.__groups['starfield'] = StarField()

        self.add_object(self.__player)
        self.add_object(self.__object_spawner)

    def __setup_hud(self):
        self.__score_hud = HudElement("Score: 0", self.__hud_font, (100, 20))
        self.__time_hud = HudElement("Time: 0", self.__hud_font, (400, 20))
        self.__health_hud = HudElement("Health: 100", self.__hud_font, (700, 20))
        self.__lives_hud = HudElement("Lives: 3", self.__hud_font, (900, 20))
        self.add_object(self.__score_hud)
        self.add_object(self.__time_hud)
        self.add_object(self.__health_hud)
        self.add_object(self.__lives_hud)

    def update(self, dt):
        self.__time += dt
        self.__time_hud.change_text(f"Time: {self.__time:.2f}")
        self.__health_hud.change_text(f"Health: {self.__player.get_health()}")
        self.__lives_hud.change_text(f"Lives: {self.__player.get_lives()}")
        #self.__lives_hud.change_text(42)

        self.__elapsed_time += dt
        if self.__elapsed_time >= 10.0:
            self.__elapsed_time -= 10.0
            self.__speed_multiplier += 0.1
        if self.__player.get_lives() < 0:
            self.__engine.running = False


