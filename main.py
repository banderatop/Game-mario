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
coin_image = image.load("hud/hud_coins.png")



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
        self.jump_speed = 15
        self.ground = True
        self.speed_y = 0
        self.speed_x = self.speed
        self.gravity = 1

    def update(self):
        self.speed_x = 0

        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.speed_x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < WIDTH - 70:
            self.move = True
            if self.rect.x < WIDTH/2:
                self.speed_x += self.speed
        else:
            self.move = False

        if keys_pressed[K_SPACE] and self.rect.y > 0 and self.ground:
            self.speed_y -= self.jump_speed
            self.ground = False
        
        self.speed_y += self.gravity
        self.rect.move_ip(self.speed_x, self.speed_y)
        collide_list = sprite.spritecollide(player, platform, False, sprite.collide_mask)
        if collide_list:
            if self.speed_y > 0:
                self.rect.bottom = collide_list[0].rect.top
                self.speed_y = 0
                self.ground = True 
        
class Text(sprite.Sprite):
    def __init__(self, text, x, y, font_size=22, font_name="Impact", color=(255,255,255)):
        self.font = font.SysFont(font_name, font_size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        
    def draw(self): #відрисовуємо спрайт у вікні
        window.blit(self.image, self.rect)
    
    def set_text(self, new_text): #змінюємо текст напису
        self.image = self.font.render(new_text, True, self.color)

       
platform = sprite.Group()
coins = sprite.Group()
last_platform = None

def get_platform(x, y):
    global last_platform

    num = randint(1, 8)
    for i in range(num):
        block = GameSprite(platform_image, 50, 50, x, y, )
        last_platform = block
        platform.add(block)
        num2 = randint(0,5)
        if num2 == 3:
            coins.add(GameSprite(coin_image, 20, 20, x+15, y-40))
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
score_text = Text("Рахунок: 0", 20, 50)
result_text = Text("Перемога!", 350, 250, font_size = 50)
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
    
    for c in coins:
        c.rect.x -= player.speed * 1.5
        if c.rect.right < 0:
            c.kill()
        
        generate_platforms()
    if player.move:
        score += 1
        score_text.set_text("Збито:" + str(score))

    if score >= 5000:
        finish = True
        result_text.draw()

        

        

    player.update()
    player.draw() 
    platform.draw(window)
    coins.draw(window)
    score_text.draw()

    display.update()
    clock.tick(FPS)