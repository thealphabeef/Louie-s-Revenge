""""""
import pygame
from collideable import PowerupType, UtilityFunctions


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, manager):
        super().__init__()
        self.__sprite_width_x = 112
        self.__sprite_width_y = 75
        self.__assets = {}
        self.__load_assets()
        self.image = self.__assets['regular_image']
        self.rect = self.image.get_rect(center=(x, y))
        self.__manager = manager
        self.__movement_speed = 125
        self.__movement_multiplier = .125
        self.__x_velocity = 0
        self.__y_velocity = 0
        self.__health = 100
        self.__lives = 3
        self.__shield = False
        self.__invincible = False
        self.__invincible_timer = 0.0
        self.__shot_timer = 0

    def __load_assets(self):
        # Load images
        self.__assets['regular_image'] = pygame.image.load("./assets/ship.png").convert_alpha()
        self.__assets['shielded_image'] = pygame.image.load("./assets/shielded_ship.png").convert_alpha()
        self.__assets['invincible_image'] = pygame.image.load("./assets/ship2.png").convert_alpha()
        # Load sound effects
        self.__assets['sfx_fire'] = pygame.mixer.Sound("./assets/sfx_laser1.ogg")
        self.__assets['sfx_damage'] = pygame.mixer.Sound("./assets/sfx_twoTone.ogg")

    def update(self, dt):
        #general logic for what movement should actually look like
        # self.rect.x += self.__x_velocity * dt
        # self.rect.y += self.__y_velocity * dt

        self.__shot_timer += dt
        if self.get_invincible():
            self.__invincible_timer += dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.__x_velocity > -self.__movement_speed:
                self.rect.x -= self.__movement_speed * self.__movement_multiplier
        if keys[pygame.K_RIGHT]:
            if self.__x_velocity < self.__movement_speed:
                self.rect.x += self.__movement_speed * self.__movement_multiplier
        if keys[pygame.K_UP]:
            if self.__y_velocity > -self.__movement_speed:
                self.rect.y -= self.__movement_speed * self.__movement_multiplier
        if keys[pygame.K_DOWN]:
            if self.__y_velocity < self.__movement_speed:
                self.rect.y += self.__movement_speed * self.__movement_multiplier

        if keys[pygame.K_SPACE]:
            if self.__shot_timer > .25:
                self.__shot_timer = 0
                laser = PlayerLaser(self.rect.centerx, self.rect.centery - 20)
                self.__manager.add_object(laser)
                self.__manager.add_object(laser, 'projectiles')
                self.__assets['sfx_fire'].play()

        # Collision with an enemy code
        hits = pygame.sprite.spritecollide(self, self.__manager.get_group('enemies'), False)
        if hits:
            if self.__shield:
                self.__shield = False
                self.image = self.__assets['regular_image']
            elif not self.__invincible:
                self.__health -= 10
                if self.__health <= 0:
                    self.__lives -= 1
                    self.__health = 100
            hits[0].kill()
            self.__assets['sfx_damage'].play()
        # PUT NEW CODE BELOW HERE

        #check if player is out of bounds if it is then set pos to max or min pos INCLUDING the sprite width and height
        if UtilityFunctions.clamp(self.rect.x, 0, 1024) == 0:
            self.rect.x = 0
        elif UtilityFunctions.clamp(self.rect.x, 0, 1024 - self.__sprite_width_x) == 1024 - self.__sprite_width_x:
            self.rect.x = 1024 - self.__sprite_width_x

        if UtilityFunctions.clamp(self.rect.y, 0, 768) == 0:
            self.rect.y = 0
        elif UtilityFunctions.clamp(self.rect.y, 0, 768 - self.__sprite_width_y) == 768 - self.__sprite_width_y:
            self.rect.y = 768- self.__sprite_width_y


        hits = pygame.sprite.spritecollide(self, self.__manager.get_group('powerups'), False)
        if hits:
            pwr_type = hits[0].get_type()
            if pwr_type == PowerupType.CLEAR:
                self.__manager.clear_enemies()
            elif pwr_type == PowerupType.HEALTH:
                self.__health += 100
            elif pwr_type == PowerupType.SHIELD:
                self.image = self.__assets['shielded_image']
                self.__shield = True
            elif pwr_type == PowerupType.INVINCIBLE:
                self.__invincible = True
                self.__invincible_timer = 0
                self.image = self.__assets['invincible_image']
            hits[0].kill()

        # Student to DO

        if self.__invincible_timer > 30.0:
            self.__invincible_timer -= 30.0
            self.__invincible = False
            self.image = self.__assets['regular_image']
    def get_invincible(self):
        return self.__invincible
    
    def get_health(self):
        return self.__health
    
    def get_lives(self):
        return self.__lives


class PlayerLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./assets/playerLaser.png").convert_alpha()  # preserves transparency
        self.rect = self.image.get_rect(center=(x, y))
        self.__speed = 1000

    def update(self, dt):
        self.rect.y -= self.__speed * dt

        if self.rect.y < 0:
            self.kill()