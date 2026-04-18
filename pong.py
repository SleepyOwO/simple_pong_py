from pygame import *

size = (1080, 720)
win = display.set_mode(size)
display.set_caption('Pong')

class GameSprite(sprite.Sprite):
    def __init__(self, img, xpos, ypos, speed):
        super().__init__()
        self.image = image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, img, xpos, ypos, w, h, speed, col):
        super().__init__(img, xpos, ypos, speed)
        self.image = Surface((w, h))
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.points = 0

    def move_l(self, keys):
        if keys[K_w] and self.rect.y > 10:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 625:
            self.rect.y += self.speed
    
    def move_r(self, keys):
        if keys[K_UP] and self.rect.y > 10:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 625:
            self.rect.y += self.speed

class Ball(sprite.Sprite):
    def __init__(self, img, xpos, ypos, w, h, speed_x, speed_y):
        super().__init__()
        self.image = transform.scale(image.load(img), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.sp_x = speed_x
        self.sp_y = speed_y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        self.rect.x += self.sp_x
        self.rect.y += self.sp_y
        if self.rect.y <= 5:
            self.sp_y *= -1
        if self.rect.y >= 680:
            self.sp_y *= -1   
    def speed_up(self, s):
        if self.sp_x > 0:
            self.sp_x += s
        else:
            self.sp_x -= s
        if self.sp_y > 0: 
            self.sp_y += s
        else:
            self.sp_y -= s     
        
font.init()

fon = font.SysFont('Arial', 30, True)


left_pl = Player('Безымянный.png', 25, 10, 15, 80, 10, (255, 255, 255))
right_pl = Player('Безымянный.png', 1040, 10, 15, 80, 10, (255, 255, 255)) 
back = Player('Безымянный.png', 0, 0, 1080, 720, 0, (0, 0, 0))
ball = Ball('ball.png', 520, 340, 40, 40, 3, 3)

game = True
clock = time.Clock()
FPS = 60

while game:
    clock.tick(FPS)

    for e in event.get():
        if e.type == QUIT:
            game = False

    keys = key.get_pressed()

    back.reset()
    win.blit(fon.render(str(left_pl.points), False, (255, 255, 255)), (500, 20))
    win.blit(fon.render(str(right_pl.points), False, (255, 255, 255)), (560, 20))
    left_pl.reset()
    left_pl.move_l(keys)

    right_pl.reset()
    right_pl.move_r(keys)

    ball.reset()
    ball.update()

    if sprite.collide_rect(left_pl, ball):
        ball.sp_x *= -1
        ball.speed_up(0.3)
    if sprite.collide_rect(right_pl, ball):
        ball.sp_x *= -1
        ball.speed_up(0.3)
    if ball.rect.x < -30:
        right_pl.points += 1
        ball.rect.x = 520
        ball.rect.y = 340
        ball.sp_x = 3
        ball.sp_y = 3
    if ball.rect.x > 1070:
        left_pl.points += 1
        ball.rect.x = 520
        ball.rect.y = 340
        ball.sp_x = -3
        ball.sp_y = -3

    display.update()
