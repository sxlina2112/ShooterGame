#create a Maze game!

from pygame import *

window = display.set_mode((700, 500))
display.set_caption("Maze game")
background = transform.scale(image.load("background.jpg"), (700, 500))

FPS =60
clock = time.Clock()

mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys_pressed[K_s] and self.rect.y < 420:
            self.rect.y += self.speed

        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys_pressed[K_d] and self.rect.x < 620:
            self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        if self.rect.x >= 600:
            self.direction = "left"
        if self.rect.x <= 500:
            self.direction = "right"
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


hero = Player("hero.png", 70, 400, 10)
enemy = Enemy("cyborg.png", 600, 270, 1)
treasure = GameSprite("treasure.png", 570, 50, 0)
wall1 = Wall(0, 255, 0, 50, 50, 10, 350)
wall2 = Wall(0, 255, 0, 150, 150, 10, 300)
wall3 = Wall(0, 255, 0, 250, 50, 10, 300)
wall4 = Wall(0, 255, 0, 50, 50, 200, 10)
wall5 = Wall(0, 255, 0, 250, 350, 250, 10)
wall6 = Wall(0, 255, 0, 150, 450, 350, 10)



font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN :D', True, (255, 215, 0))
lose = font.render('GAME OVER :(', True, (255, 0, 0))



game = True
finish = False

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0,0))
        hero.reset()
        enemy.reset()
        treasure.reset()

        wall1.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()
        wall5.draw_wall()
        wall6.draw_wall()

        hero.update()
        enemy.update()

        if sprite.collide_rect(hero, treasure):
            window.blit(win, (200, 200))
            finish = True
            money.play()

        if sprite.collide_rect(hero, enemy):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

        if sprite.collide_rect(hero, wall1) or sprite.collide_rect(hero, wall2) or sprite.collide_rect(hero, wall3) or sprite.collide_rect(hero, wall4) or sprite.collide_rect(hero, wall5) or sprite.collide_rect(hero, wall6):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

    display.update()
    clock.tick(FPS)
    
