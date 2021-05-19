# Sprite classes for platform game
import pygame as pg
import random as r
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.on_right_wall = True

        # self.image = pg.Surface((30, 40))
        # self.image.fill(GREEN)
        self.image = game.man_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT / 2)
        self.pos = vec(WIDTH/2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        self.game.jump_sound.play()
        if self.on_right_wall == True:
            self.vel.x = - 30
        else:
            self.vel.x = 30




    def update(self):
        self.acc = vec(0,0)

        keys = pg.key.get_pressed()
        # if keys[pg.K_SPACE]:
        #     self.jump()
        if keys[pg.K_UP]:
            self.acc.y = -PLAYER_ACC
        if keys[pg.K_DOWN]:
            self.acc.y = PLAYER_ACC

        self.acc.y += self.vel.y * PLAYER_FRICTION
        #equations of motion
        self. vel.y += self.acc.y
        self.pos += self.vel + 0.5 * self.acc
        #wrap around the top of the screen

        if self.pos.y <= 0:
            self.pos.y = 0
        if self.pos.y >= HEIGHT:
            self.pos.y = HEIGHT
        self.rect.center = self.pos


class MobD(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        # self.image = pg.Surface((30, 40))
        # self.image.fill(PINK)
        self.image = game.car_imageD
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = r.randint(75, WIDTH -100)
        self.rect.y = r.randint(-100, -40)
        self.speedy = r.randint(1, 8)




    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = r.randint(75, WIDTH - 100)
            self.rect.y = r.randrange(-100, -40)
            self.speedy = r.randrange(1, 8)

class MobU(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        # self.image = pg.Surface((30, 40))
        # self.image.fill(PINK)
        self.image = game.car_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = r.randint(75, WIDTH -100)
        self.rect.y = r.randrange(HEIGHT + 40, HEIGHT + 100)
        self.speedy = r.randint(-8, -1)




    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.rect.x = r.randint(75, WIDTH - 100)
            self.rect.y = r.randrange(HEIGHT + 40, HEIGHT + 100)
            self.speedy = r.randrange(-8, -1)

class Walls(pg.sprite.Sprite):
    def __init__(self, x,y,w,h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y