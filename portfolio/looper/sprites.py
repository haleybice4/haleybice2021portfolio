# Sprite classes for platform game
import pygame as pg
from settings import *
import random as r
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT * .75)
        self.pos = vec(WIDTH / 2,HEIGHT * .75)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.player_acc = PLAYER_ACC

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.acc.x = self.player_acc
            self.pos.x += self.player_acc
        # # apply friction
        # self.acc += self.vel * PLAYER_FRICTION
        # # equations of motion
        # self.vel += self.acc
        # self.pos += self.vel + 0.5 * self.acc

        # wrap around the sides of the screen
        if self.pos.x > WIDTH - WIDTH * .25:
            self.player_acc *= -1
        if self.pos.x < 0 + WIDTH * .25:
            self.player_acc *= -1

        self.rect.center = self.pos


class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites,game.enemy_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = r.randrange(-200, -75)
        self.speedy = 5
        print("test")



    def update(self):

        self.rect.y += self.speedy

        if self.rect.top > HEIGHT:
            self.game.score += 50
            self.kill()

class Right_side_mob(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self.groups = game.all_sprites,game.sides
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((175, 1500))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        if self.rect.left < WIDTH/2 + 40:
            self.rect.left = WIDTH/2 + 40
        self.rect.centery = y
        self.speedy = 9


    def update(self):

        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()







class Left_side_mob(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self.groups = game.all_sprites,game.sides
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((175, 1500))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        if self.rect.right > WIDTH/2 - 40:
            self.rect.right = WIDTH/2 - 40
        self.rect.centery = y
        self.speedy = 9



    def update(self):

        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()



