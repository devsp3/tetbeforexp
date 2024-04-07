import pygame
import random

pygame.init()
screen = pygame.display.set_mode([500, 500])
bg_img = pygame.image.load('sky.png')
FONT = pygame.font.SysFont(None, 30)
rockimg = []
exp_img = []
for i in range(1, 4):
    filename = 'rocket' + str(i) + '.PNG'
    rocket_img = pygame.image.load(filename)
    rocket_img = pygame.transform.scale_by(rocket_img, (0.1, 0.1))
    rocket_img = pygame.transform.rotate(rocket_img, 270)
    rocket_img.set_colorkey((255, 255, 255))
    rockimg.append(rocket_img)

mone = 0
clock = pygame.time.Clock()
clouds = pygame.sprite.Group()  # an empty group (a list) of clouds
bombs = pygame.sprite.Group()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('cloud.png')
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=(700, random.randint(0, 500)))
        self.hit = False
        clouds.add(self)  # add the new cloud to the clouds group

    def update(self):
        if self.hit == True:
            self.rect.move_ip(0, 4)
        else:
            self.rect.move_ip(-2, 0)


class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('bomb.png')
        self.image = pygame.transform.scale_by(self.image, (0.3, 0.3))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=(random.randint(0, 500), 0))
        self.hit = False
        bombs.add(self)  # add the new cloud to the clouds group

    def update(self):
        if self.rect.y > 500:
            self.kill()
        if self.hit == True:
            pass
        else:
            self.rect.move_ip(0, 8)


class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        rocket_img = pygame.image.load('rocket1.PNG')
        rocket_img = pygame.transform.scale_by(rocket_img, (0.1, 0.1))
        rocket_img = pygame.transform.rotate(rocket_img, 270)
        rocket_img.set_colorkey((255, 255, 255))
        self.image = rocket_img
        self.rect = self.image.get_rect()
        self.hit = False

    def update(self, pressed_keys):

        if self.hit == False:
            self.image = rockimg[rockframe]
            if pressed_keys[pygame.K_UP]:
                self.rect.move_ip(0, -5)
            if pressed_keys[pygame.K_DOWN]:
                self.rect.move_ip(0, 5)
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)
        else:
            self.rect.move_ip(0, 5)
            # self.image=pygame.transform.rotate(self.image,5)
            self.image.set_colorkey((255, 255, 255))

            if self.rect.y > 500:
                running = False


abba = Rocket()
rockframe = 0
zscore = 0
running = True
pause = False
while running == True:
    pressed_keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
                print(pause)
    if pause == False:
        mone = mone + 1
        rockframe += 1
        rockframe = rockframe % 3

        if mone == 100:
            dd = Cloud()
            ee = Bomb()
            mone = 0
        clouds.update()
        bombs.update()
        if pygame.sprite.spritecollideany(abba, clouds):
            x = pygame.sprite.spritecollideany(abba, clouds)
            if x.hit == False:
                zscore += 1
                x.hit = True
        if pygame.sprite.spritecollideany(abba, bombs):
            abba.hit = True

        abba.update(pressed_keys)
        screen.blit(bg_img, (0, 0))
        screen.blit(abba.image, abba.rect)
        clouds.draw(screen)
        bombs.draw(screen)
        scorepix = FONT.render(str(zscore), True, 'black')
        screen.blit(scorepix, (100, 100))
    else:
        screen.fill((23, 165, 65))
        scorepix = FONT.render('press pause to unpause', True, 'black')
        screen.blit(scorepix, (100, 100))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()