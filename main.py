import pygame
import os
from pygame.locals import *
#-----------------------------------------------------------------------
# Parametry programu
#-----------------------------------------------------------------------
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)



def loadImage(name, useColorKey=False, alpha=False):
    """ Załaduj obraz i przekształć go w powierzchnię.

    Funkcja ładuje obraz z pliku i konwertuje jego piksele
    na format pikseli ekranu. Jeśli flaga useColorKey jest
    ustawiona na True, kolor znajdujący się w pikselu (0,0)
    obrazu będzie traktowany jako przezroczysty (przydatne w
    przypadku ładowania obrazów statków kosmicznych)
    """
    fullname = os.path.join("data",name)
    image = pygame.image.load(fullname)  #plik -> płaszczyzna
    image = image.convert() #przekonwertuj na format pikseli ekranu
    if useColorKey is True:
        colorkey = image.get_at((0,0)) #odczytaj kolor w punkcie (0,0)
        image.set_colorkey(colorkey, RLEACCEL) # ustaw kolor jako przezroczysty
        #flaga RLEACCEL oznacza lepszą wydajność na ekranach bez akceleracji
        #wymaga from pygame.locals import *
    if alpha:
        image = image.convert.a
    return image




class Racket_1(pygame.sprite.Sprite):
    def __init__(self, first_position):
        pygame.sprite.Sprite.__init__(self)
        self.first_height = first_position[1]
        self.image = loadImage("racket.png", True)
        self.rect = self.image.get_rect()
        self.rect.center = first_position
        self.x_velocity = 0
        self.y_velocity = 0
        self.hitting = False
        self.future_position = 0
        self.old_position = 0
        self.back = False

    def update(self):
        self.rect.move_ip((self.x_velocity, self.y_velocity))

        if self.rect.left < 12:
            self.rect.left = 12
        elif self.rect.right > SCREEN_WIDTH - 12:
            self.rect.right = SCREEN_WIDTH - 12

        if self.rect.bottom >= SCREEN_HEIGHT - 12:
            self.rect.bottom = SCREEN_HEIGHT - 12
        if self.rect.top <= SCREEN_HEIGHT/2 + 12:
            self.rect.top = SCREEN_HEIGHT/2 + 12
                # if self.hitting:
                #     self.y_velocity = 0
                #     self.hitting = False

        if self.hitting:
            if self.rect.top <= self.future_position:
                self.stop()
                if self.back:
                    self.go_back()
            elif self.rect.top == SCREEN_HEIGHT/2 + 12:
                if self.back:
                    self.go_back()
            elif self.back and self.rect.top >= self.old_position and self.hitting:
                self.stop()
                self.hitting = False
                self.back = False



    def hit(self):
        if not self.hitting:
            self.old_position = self.rect.top
            self.y_velocity = -20
            self.hitting = True
            self.future_position = self.rect.top - 80

    def stop(self):
        self.y_velocity = 0
    def go_back(self):
        self.y_velocity = 20


class Racket_2(pygame.sprite.Sprite):
    def __init__(self, first_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("racket.png", True)
        self.rect = self.image.get_rect()
        self.rect.center = first_position
        self.x_velocity = 0
        self.y_velocity = 0
        self.hitting = False
        self.future_position = 0
        self.old_position = 0
        self.back = False

    def update(self):
        self.rect.move_ip((self.x_velocity, self.y_velocity))

        if self.rect.left < 12:
            self.rect.left = 12
        elif self.rect.right > SCREEN_WIDTH - 12:
            self.rect.right = SCREEN_WIDTH - 12

        if self.rect.bottom >= SCREEN_HEIGHT/2 - 12:
            self.rect.bottom = SCREEN_HEIGHT/2 - 12
        if self.rect.top <=  12:
            self.rect.top = 12

        if self.hitting:
            if self.rect.top >= self.future_position:
                self.stop()
                if self.back:
                    self.go_back()
            elif self.rect.bottom == SCREEN_HEIGHT/2 - 12:
                if self.back:
                    self.go_back()
            elif self.back and self.rect.top <= self.old_position and self.hitting:
                self.stop()
                self.hitting = False
                self.back = False


    def hit(self):
        if not self.hitting:
            self.old_position = self.rect.top
            self.y_velocity = 20
            self.hitting = True
            self.future_position = self.rect.top + 80

    def stop(self):
        self.y_velocity = 0
    def go_back(self):
        self.y_velocity = -20


class Puck(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/puck.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.75)
        self.x_velocity = 0
        self.y_velocity = 0
    def update(self):
        self.rect.move_ip((self.x_velocity, self.y_velocity))

        if self.rect.left < 12:
            self.rect.left = 12
            self.x_velocity = - self.x_velocity
        elif self.rect.right > SCREEN_WIDTH - 12:
            self.rect.right = SCREEN_WIDTH - 12
            self.x_velocity = - self.x_velocity

        if self.rect.top <= 13:
            self.rect.top = 13
            self.y_velocity = -self.y_velocity
        elif self.rect.bottom >= SCREEN_HEIGHT - 13:
            self.rect.bottom = SCREEN_HEIGHT-13
            self.y_velocity = - self.y_velocity




screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Cymbergaj")



background_image = loadImage("Background.png")
screen.blit(background_image,(0,0))

cage1 = loadImage("cage.png")
screen.blit(cage1, (180, 688))

cage2 = loadImage("cage.png")
screen.blit(cage2, (180, 0))


puck_sprite = pygame.sprite.RenderClear()
puck = Puck((100, 0))
puck_sprite.add(puck)

first_racket_sprite = pygame.sprite.RenderClear()
first_racket = Racket_1((SCREEN_WIDTH / 2, 0.9 * SCREEN_HEIGHT))
second_racket = Racket_2((SCREEN_WIDTH / 2, 0.1 * SCREEN_HEIGHT))
first_racket_sprite.add(first_racket)
first_racket_sprite.add(second_racket)

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                first_racket.x_velocity = -6
            elif event.key == K_DOWN:
                if not first_racket.hitting:
                    first_racket.y_velocity = 6
            elif event.key == K_UP:
                if not first_racket.hitting:
                    first_racket.y_velocity = -6
            elif event.key == K_RIGHT:
                first_racket.x_velocity = 6
            elif event.key == K_RALT:
                first_racket.hit()
            elif event.key == K_w:
                second_racket.y_velocity = -6
            elif event.key == K_s:
                second_racket.y_velocity = 6
            elif event.key == K_a:
                second_racket.x_velocity = -6
            elif event.key == K_d:
                second_racket.x_velocity = 6
            elif event.key == K_SPACE:
                second_racket.hit()


        elif event.type == KEYUP:
            if event.key == K_LEFT:
                if first_racket.x_velocity == -6:
                    first_racket.x_velocity = 0
            elif event.key == K_DOWN:
                if not first_racket.hitting and first_racket.y_velocity==6:
                    first_racket.y_velocity = 0
            elif event.key == K_UP:
                if not first_racket.hitting and first_racket.y_velocity==-6:
                    first_racket.y_velocity = 0
            elif event.key == K_RIGHT:
                if first_racket.x_velocity == 6:
                    first_racket.x_velocity = 0
            elif event.key == K_RALT:
                first_racket.back = True
            elif event.key == K_w:
                if second_racket.y_velocity ==-6:
                    second_racket.y_velocity = 0
            elif event.key == K_s:
                if second_racket.y_velocity == 6:
                    second_racket.y_velocity = 0
            elif event.key == K_a:
                if second_racket.x_velocity == -6:
                    second_racket.x_velocity = 0
            elif event.key == K_d:
                if second_racket.x_velocity == 6:
                    second_racket.x_velocity = 0
            elif event.key == K_SPACE:
                second_racket.back = True



    puck_sprite.update()
    first_racket_sprite.update()

    puck_sprite.clear(screen, background_image)
    first_racket_sprite.clear(screen, background_image)

    puck_sprite.draw(screen)

    first_racket_sprite.draw(screen)



    pygame.display.flip()




