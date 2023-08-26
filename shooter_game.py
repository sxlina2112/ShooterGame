#Create your own shooter

from pygame import *
from random import randint
from time import time as timer


window = display.set_mode((700, 500))
display.set_caption("shooter game")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

FPS = 60
clock = time.Clock()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound("fire.ogg")

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

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

    def fire(self):
        bullet = Bullet("bullet.png", -10, self.rect.centerx, self.rect.top)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > 500:
            self.rect.x = randint(0,700)
            self.rect.y = 0
            lost += 1
lost = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()
    
        

player = Player("rocket.png", 10, 325, 420)

enemies = sprite.Group()
asteroids = sprite.Group()


for i in range(5):
    enemy = Enemy("ufo.png", 1, randint(0, 700), randint(0, 150))
    enemies.add(enemy)

for i in range(3):
    asteroid = Enemy("asteroid.png", 1 , randint(0, 700), randint(0, 150))
    asteroids.add(asteroid)

bullets = sprite.Group()

font.init()
style = font.Font(None, 36)
win = style.render("YOU WIN!! :D", True, (0, 255, 0))
lose = style.render("YOU LOST :(", True, (255, 0, 0))

score = 0

game = True
finish = False
life = 3
num_fire = 0
reload = False

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and reload == False:
                    player.fire()
                    fire.play()
                    num_fire += 1
                if num_fire >= 10 and reload == False:
                    last_time = timer()
                    reload = True

    if finish == False:
        window.blit(background, (0, 0))
        player.reset()
        enemies.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        player.update()
        enemies.update()
        asteroids.update()
        bullets.update()
        
        collision = sprite.groupcollide(enemies, bullets, True, True)
        for c in collision:
            score += 1
            enemy = Enemy("ufo.png", 1, randint(0, 700), randint(0, 150))
            enemies.add(enemy)
        
        if lost >= 5 or life == 0:
            finish = True 
            window.blit(lose, (250, 350))

        if sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, enemies, True)
            sprite.spritecollide(player, asteroids, True)
            life -= 1
        
        if score >= 10:
            finish = True
            window.blit(win, (250, 350))

        if reload == True:
            new_time = timer()
            if new_time - last_time < 3:
                reload = style.render("reloading...", 1, (255, 255, 255))
                window.blit(reload, (250, 350))
            else:
                num_fire = 0
                reload = False
        
        text_lose = style.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 20))

        text_score = style.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 40))

        text_health = style.render("Health: " + str(life), 1, (255, 255, 255))
        window.blit(text_health, (550, 20))

        time.delay(10)
        display.update()
    
    else: 
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for e in enemies:
            e.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(5):
            enemy = Enemy("ufo.png", 1, randint(0, 700), randint(0, 150))
            enemies.add(enemy)

        for i in range(3):
            asteroid = Enemy("asteroid.png", 1 , randint(0, 700), randint(0, 150))
            asteroids.add(asteroid)

time.delay(50)
        
    # clock.tick(FPS)