from pygame import *
from random import randint, uniform
from time import sleep
from time import time as timer
mixer.init()
font.init()

score = 0

#коментарий

win_width = 700
win_height = 500
mw = display.set_mode((win_width, win_height))
backround =  transform.scale(image.load('galaxy.jpg'), (win_width,win_height))
mw.blit(backround, (0,0))
clock = time.Clock()

mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def init(self, player_image, player_x, player_y, player_speed, w, h):
        super().init()
        self.image = transform.scale(image.load( player_image), (w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

    
class Player(GameSprite):
    def move(self):
        key_p = key.get_pressed()
        if key_p[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if key_p[K_RIGHT] and self.rect.x < 640:
            self.rect.x += self.speed


    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x + 32 , self.rect.y, 15, 10, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost 
        self.rect.y += self.speed
        if self.rect.y >= 500:
            lost += 1
            self.speed = uniform(1.0, 3.5)
            self.rect.y = -80
            self.rect.x = randint(0, win_width-65)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -5:
            self.kill()

class asteroide(GameSprite):
    def update(self): 
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.speed = uniform(1.0, 5.7)
            self.rect.y = -50
            self.rect.x = randint(0, win_width-65)
        
bullets = sprite.Group()
asteroids = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    e1 = Enemy('ufo.png', randint(0, win_width-65), -80, uniform(1.0, 3.5), 85, 55) 
    monsters.add(e1)    

for i in range(3):
    a1 = asteroide('asteroid.png', randint(0, win_width-50), -50, uniform(3.2, 5.5 ), 50, 50) 
    asteroids.add(a1)


p = Player('rocket.png', 0, 415, 10, 65, 85)

rel_time = False
num_fire = 0
lost = 0
game_false = False
game = True
healse = 5
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire.play()
                    p.fire()

                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_shoot = timer()

    mw.blit(backround, (0,0))
        
    collide = sprite.spritecollide(p, monsters, True)

    collidea = sprite.spritecollide(p, asteroids, True)

    if score == 15:
        game_false = True
        mw.blit(win_txt, (300, 250))

    if lost >= 10:
        game_false = True
        mw.blit(lose_txt, (300, 250))

    for c in collide:
        healse -= 1
        e1 = Enemy('ufo.png', randint(0, win_width-65), -80, uniform(1.0, 3.5), 85, 55) 
        monsters.add(e1) 

    for i in collidea:
        healse -= 1
        a1 = asteroide('asteroid.png', randint(0, win_width-50), -50, uniform(3.2, 5.5 ), 50, 50) 
        asteroids.add(a1)

    if healse == 0:
        game_false = True
        mw.blit(lose_txt, (300, 250))

        
    
    lost_txt = font.Font(None, 36).render('lost: ' + str(lost), True, (255, 255, 255))
    t_txt = font.Font(None, 36).render('touch: ' + str(score), True, (255, 255, 255))

    win_txt = font.Font(None, 50).render('YOU WIN', True, (0, 255, 0))
    lose_txt = font.Font(None, 50).render('YOU LOSE', True, (0, 255, 0))

    healse_txt = font.Font(None, 36).render('Healse: ' + str(healse), True, (255, 255, 255))


    s_txt = font.Font(None, 36).render(str(num_fire), True, (255, 255, 255))
    mw.blit(s_txt, (p.rect.x + 10, p.rect.y - 10))
    mw.blit(t_txt, (10, 40))
    mw.blit(lost_txt, (10,10))
    mw.blit(healse_txt, (585, 10))
    monsters.draw(mw)
    bullets.draw(mw)
    asteroids.draw(mw)
    p.move()
    p.reset()
    monsters.update()
    bullets.update()
    asteroids.update()

    if rel_time:
        now_time = timer()
        if now_time - last_shoot < 3:
            reload_shoot = font.Font(None, 50).render('wait reolading', True, (0, 0, 255))
            mw.blit(reload_shoot, (win_width-290, 440))

        else:
            num_fire = 0
            rel_time = False

    if game_false:
        game = False
    
    collides = sprite.groupcollide(monsters, bullets, True, True)

    for c in collides:
        score += 1
        e1 = Enemy('ufo.png', randint(0, win_width-65), -80, uniform(1.0, 3.5), 85, 55) 
        monsters.add(e1)


    display.update()
    clock.tick(60)
sleep(3)