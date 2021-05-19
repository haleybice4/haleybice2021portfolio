import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.score = 0
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        # start a new game

        self.all_sprites = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        self.sides = pg.sprite.Group()
        self.p2 = pg.sprite.Group()
        self.sides_list = []

        self.player1 = Player(self)
        self.player2 = Player(self)
        self.p2.add(self.player2)
        self.player2.player_acc *= -1
        self.player2.image.fill(GREEN)
        mob = Mob(self)

        x = r.randrange(0, WIDTH/2-230)

        y = -250
        right_mob = Right_side_mob(self, WIDTH - x , y)

        left_mob = Left_side_mob(self, 0 + x, y)
        self.sides_list.append(left_mob)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        if not self.enemy_group:
            mob = Mob(self)
        if self.sides_list[0].rect.top > 0:
            self.sides_list.remove(self.sides_list[0])
            x = r.randrange(0, WIDTH / 2 - 230)
            y = -250
            right_mob = Right_side_mob(self, WIDTH - x, y)
            left_mob = Left_side_mob(self, 0 + x, y)

            self.sides_list.append(left_mob)





        hits = pg.sprite.spritecollide(self.player1, self.enemy_group, False)
        if hits:
            self.playing = False
        hits = pg.sprite.spritecollide(self.player2, self.enemy_group, False)
        if hits:
            self.playing = False
        hits = pg.sprite.spritecollide(self.player1, self.sides, False)
        if hits:
            self.playing = False
        hits = pg.sprite.spritecollide(self.player2, self.sides, False)
        if hits:
            self.playing = False
        hits = pg.sprite.spritecollide(self.player1, self.p2, False)
        if hits:
            self.score += 1






    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, GREEN, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Space to move", 22, GREEN, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, GREEN, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, GREEN, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, GREEN, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, GREEN, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
        self.score = 0
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False



    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()