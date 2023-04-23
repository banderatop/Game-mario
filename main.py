from pygame import *
from random import randint

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
    def update(self): #рух спрайту
        keys_pressed = key.get_pressed() 
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < WIDTH - 70:
            self.rect.x += self.speed

platform = sprite.Group()
def get_platform(x, y):
    num = randint(1, 5)
    for platform in range(num):
        block = GameSprite(x , y)
        x += 50



window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("mario")

bg = transform.scale(bg_image, (WIDTH, HEIGHT))

# створення спрайтів
player = Player(player_image, width = 100, height = 100, x = 200, y = HEIGHT-150)


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
    
    player.draw() 


    display.update()
    clock.tick(FPS)