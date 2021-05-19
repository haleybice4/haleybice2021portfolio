import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.DIFF = DIFF
        self.THRESHOLD = THRESHOLD
        self.score = 0
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "imgs")
        self.car_image = pg.image.load(path.join(img_folder,"car.png"))
        self.car_image = pg.transform.scale(self.car_image, (30,40))
        self.car_imageD = pg.transform.rotate(self.car_image, 180)
        self.man_image = pg.image.load(path.join(img_folder,"Commando_right.png"))
        self.man_image = pg.transform.scale(self.man_image,(30,30))
        self.background_image = pg.image.load(path.join(img_folder,"background.png"))
        self.background_image = pg.transform.scale(self.background_image,(WIDTH,HEIGHT))
        self.background_rect = self.background_image.get_rect()

        self.music_dir = path.join(game_folder, 'music')
        self.bg_music=pg.mixer.music.load(path.join(self.music_dir,'peaceful.wav'))
        self.jump_sound = pg.mixer.Sound(path.join(self.music_dir, 'Jump33.wav'))





    def new(self):

        # start a new game
        self.player = Player(self)
        self.lwall = Walls(0,0,150,HEIGHT)
        self.rwall = Walls(WIDTH, 0, 150, HEIGHT)
        self.all_sprites = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.walls.add(self.lwall)
        # self.all_sprites.add(self.lwall)
        self.walls.add(self.rwall)
        # self.all_sprites.add(self.rwall)
        self.all_sprites.add(self.player)
        self.spawn()




        self.run()

    def spawn(self):
        for x in self.all_sprites:
            if x == MobD or x== MobU:
                self.all_sprites.remove(x)
        self.enemy_group = pg.sprite.Group()
        for i in range(self.DIFF):
            m = MobD(self)
            self.all_sprites.add(m)
            self.enemy_group.add(m)
            m = MobU(self)
            self.all_sprites.add(m)
            self.enemy_group.add(m)

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump()


    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player,self.walls, False)
        if hits and self.player.vel.x < 0:
            self.player.vel.x = 0
            self.man_image = pg.transform.flip(self.man_image, True, False)
            self.player.image = self.man_image
            self.player.image.set_colorkey(BLACK)
            self.player.rect.left = hits[0].rect.right
            self.player.on_right_wall = False
        elif hits and self.player.vel.x > 0:
            self.player.vel.x = 0
            self.player.rect.right = hits[0].rect.left
            self.man_image = pg.transform.flip(self.man_image, True, False)
            self.player.image = self.man_image
            self.player.image.set_colorkey(BLACK)
            self.player.on_right_wall = True
        if self.player.vel.x != 0:
            self.score += 1
        if self.score % self.THRESHOLD == 0 and self.score != 0:
            self.DIFF += 1
            self.THRESHOLD *= 2
            self.spawn()
        hits = pg.sprite.spritecollide(self.player, self.enemy_group,False)
        if hits:
            self.playing = False




    def draw(self):
        # Game Loop - draw
        self.screen.fill(DARKGREY)
        self.screen.blit(self.background_image, self.background_rect)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, MOONGLOW, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, GREEN, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, PINK, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
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