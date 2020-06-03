import pygame
import os
from pygame.locals import *
#-----------------------------------------------------------------------
# Parametry programu
#-----------------------------------------------------------------------
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 700
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)



def loadImage(name, useColorKey=False):
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
    return image




class Racket(pygame.sprite.Sprite):
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
        if self.first_height > SCREEN_HEIGHT/2:
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
            self.future_position = self.rect.top - 60

    def stop(self):
        self.y_velocity = 0
    def go_back(self):
        self.y_velocity = 20








screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Best shooter ever")
pygame.display.flip() #aktualizacja całej sceny


background_image = loadImage("Background.png")
# pygame.transform.smoothscale(background_image, (700, 600))
screen.blit(background_image,(0,0))

first_racket_sprite = pygame.sprite.RenderClear()
first_racket = Racket((SCREEN_WIDTH / 2, 0.9 * SCREEN_HEIGHT))
second_racket = Racket((SCREEN_WIDTH / 2, 0.1 * SCREEN_HEIGHT))
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

        elif event.type == KEYUP:
            if event.key == K_LEFT:
                first_racket.x_velocity = 0
            elif event.key == K_DOWN:
                if not first_racket.hitting:
                    first_racket.y_velocity = 0
            elif event.key == K_UP:
                if not first_racket.hitting:
                    first_racket.y_velocity = 0
            elif event.key == K_RIGHT:
                first_racket.x_velocity = 0
            elif event.key == K_RALT:
                first_racket.back = True

    first_racket_sprite.update()
    first_racket_sprite.clear(screen, background_image)
    first_racket_sprite.draw(screen)
    pygame.display.flip()
