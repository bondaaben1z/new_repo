#Создай собственный Шутер!

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top,15, 15,20)
        bullets.add(bullet)
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed//2
        global lost
        if self.rect.y > 550:
            self.rect.x = randint(80, 500)
            self.rect.y = 0
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == 0:
            self.kill()

window = display.set_mode((700, 500))
display.set_caption('pygame window')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, 600), -40, randint(2,5), 80, 50)
    monsters.add(monster)
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(80, 600), -40, randint(2,5), 80, 50)
    asteroids.add(asteroid)
bullets = sprite.Group()
game = True
player = Player('rocket.png', 350, 390, 5, 80, 100)
clock = time.Clock()
finish = False
font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 50)
mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()

points = 0
lifes = 3
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    if finish != True:
        window.blit(background, (0, 0))
        text_lose = font1.render('Пропущено: '+ str(lost), True, (255, 255, 255))
        window.blit(text_lose, (10, 20))
        text_points = font1.render('Счет: '+str(points), True, (255, 255,255))
        window.blit(text_points, (10, 50))
        text_life = font1.render('Жизни: '+str(lifes), True, (255, 255,255))
        window.blit(text_life, (10, 80))
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        player.reset()
        player.update()
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        collides1 = sprite.groupcollide(asteroids, bullets, True, True)
        for i in collides:
            points += 1
            monster = Enemy('ufo.png', randint(80, 600), -40, randint(2,5), 80, 50)
            monsters.add(monster)
        for i in collides1:
            points += 1
            asteroid = Enemy('asteroid.png', randint(80, 600), -40, randint(2,5), 80, 50)
            asteroids.add(asteroid)
        if points > 10:
            finish = True
            text_win = font2.render('YOU WIN!', True, (255, 255, 255))
            window.blit(text_win, (300, 250))
        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, asteroids, True):
            lifes -= 1
        if lost > 3 or lifes == 0:
            finish = True
            text_lose = font2.render('YOU LOSE!', True, (255, 255, 255))
            window.blit(text_lose, (300, 250))
    time.delay(5)
    display.update()
    clock.tick(60)
