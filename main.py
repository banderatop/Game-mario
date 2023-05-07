from pygame import *
from random import *

import os

init()
font.init()
mixer.init()

# розміри вікна
WIDTH, HEIGHT = 900, 600

# картинка фону
bg_image = image.load("bg.png")
#картинки для спрайтів
player_image = image.load("player/p1_walk01.png")
platform_image = image.load("platforms/grass.png")



class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y, speed = 3):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.mask = mask.from_surface(self.image)  

    def draw(self): #відрисовуємо спрайт у вікні
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def __init__(self, sprite_img, width, height, x, y, speed = 3):
        super().__init__(sprite_img, width, height, x, y, speed)
        self.move = False
        self.jump_speed = 150
        self.ground = True
        self.fall_speed = 0


    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < WIDTH - 70:
            self.move = True
            if self.rect.x < WIDTH/2:
                self.rect.x += self.speed
        else:
            self.move = False

        if keys_pressed[K_SPACE] and self.rect.y > 0 and self.ground:
            self.rect.y -= self.jump_speed
            self.ground = False
        
        if self.ground == False:
            self.fall_speed += 0.25
            self.rect.y += self.fall_speed
        
        collide_list = sprite.spritecollide(player, platform, False, sprite.collide_mask)
        if len(collide_list) > 0:
            self.ground = True
        else:
            self.ground = False
        


       
platform = sprite.Group()
last_platform = None

def get_platform(x, y):
    global last_platform

    num = randint(1, 8)
    for i in range(num):
        block = GameSprite(platform_image, 50, 50, x, y, )
        last_platform = block
        platform.add(block)
        x += 50

get_platform(0, 300)
coords = [-100, -50, 0, 50, 100]

def generate_platforms():
    global last_platform

    while last_platform.rect.right < WIDTH:
        next_x = last_platform.rect.right + randint(50, 100)
        next_y = last_platform.rect.y + choice(coords)
        if next_y > 500:
            next_y = 500
        elif next_y < 150:
            next_y = 150

        get_platform(next_x, next_y)

generate_platforms()



window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("mario")

bg = transform.scale(bg_image, (WIDTH, HEIGHT))

# створення спрайтів
player = Player(player_image, width = 70, height = 70, x = 50, y = 150)


run = True
finish = False
clock = time.Clock()
FPS = 60
score = 0
lost = 0

# ігровий цикл
while run:
    window.blit(bg, (0, 0)) 
    for e in event.get():
        if e.type == QUIT:
            run = False
    if player.move:
        for p in platform:
            p.rect.x -= player.speed * 1.5
            if p.rect.right < 0:
                p.kill()
        generate_platforms()

    player.update()
    player.draw() 
    platform.draw(window)

    display.update()
    clock.tick(FPS)