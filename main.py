import pygame
import os
from pygame.locals import *
import math
import pandas as pd

#-----------------------------------------------------------------------
# Parametry programu
#-----------------------------------------------------------------------
SCREEN_WIDTH = 850
SCREEN_HEIGHT = 1000
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
PUCKEVENT_1 = pygame.USEREVENT
PUCKEVENT_2 = pygame.USEREVENT + 1
TIMEREVENT = pygame.USEREVENT + 2


#colors
white = (255,255,255)
red = (198,0,0)
dark_green = (92,136,44)
gray = (95,93,93)
dark_blue = (34,75,145)
COLOR_INACTIVE = (143,149,152)
COLOR_ACTIVE = (35,42,66)

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

def loadSound(name):
    fullname = os.path.join("data", name)
    sound = pygame.mixer.Sound(fullname)
    return sound


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
    def __init__(self, color, position):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.image.load("data/puck.png").convert_alpha()
        self.image = pygame.Surface((80,80))
        self.image.fill((255,255,255))
        pygame.draw.circle(self.image, (color), (40,40), 40)
        colorkey = self.image.get_at((0, 0))  # odczytaj kolor w punkcie (0,0)
        self.image.set_colorkey(colorkey, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.x_velocity = 0
        self.y_velocity = 0
        self.collision = False
        self.sin_1 = math.sin(math.radians(68))
        self.sin_2 = math.sin(math.radians(22))
        self.ang = False

    def update(self):
        self.rect.move_ip((self.x_velocity, self.y_velocity))

        if self.rect.left < 12:
            self.rect.left = 12
            self.x_velocity = - self.x_velocity
            sound1.play()
        elif self.rect.right > SCREEN_WIDTH - 12:
            self.rect.right = SCREEN_WIDTH - 12
            self.x_velocity = - self.x_velocity
            sound1.play()


        if self.rect.top <= 13 and (self.rect.right < 268 or self.rect.left > 578):
            self.rect.top = 13
            self.y_velocity = -self.y_velocity
            sound1.play()
        elif self.rect.bottom >= SCREEN_HEIGHT - 13 and (self.rect.right < 268 or self.rect.left > 578):
            self.rect.bottom = SCREEN_HEIGHT-13
            self.y_velocity = - self.y_velocity
            sound1.play()
        elif self.rect.top >= SCREEN_HEIGHT - 10 and not (self.rect.right < 268 or self.rect.left > 578):
            print("GOAL! 1 !")
            self.kill()
            round.new_point(1)
            pygame.time.set_timer(PUCKEVENT_1, 2500)

        elif self.rect.bottom <  10 and not (self.rect.right < 268 or self.rect.left > 578):
            print("GOAL!! 2")
            self.kill()
            round.new_point(2)
            pygame.time.set_timer(PUCKEVENT_2, 2500)


        # collisions
        x1, y1 = self.rect.center
        x2, y2 = first_racket.rect.center
        x3, y3 = second_racket.rect.center
        first_length = math.hypot(x1- x2, y1- y2)
        second_length = math.hypot(x1 - x3, y1 - y3)

        v_len = math.hypot(self.x_velocity, self.y_velocity)
        #first racket
        if first_length <= 110 and not self.collision:
            sound2.play()
            sin = (y1 - y2) / first_length
            cos = (x1 - x2) / first_length

                # odbicie
            if abs(sin) > self.sin_1:
                self.y_velocity = -self.y_velocity
                if self.y_velocity < 5:
                    self.y_velocity += math.ceil(first_racket.y_velocity * 1.2)
                else:
                    self.y_velocity += math.ceil(first_racket.y_velocity*0.9)
            elif abs(sin) < self.sin_2:
                self.x_velocity = -self.x_velocity
                self.x_velocity += math.ceil(first_racket.x_velocity*0.9)
            else:
                first_velocity = math.hypot(first_racket.x_velocity, first_racket.y_velocity)
                if x1 < x2 and y1 < y2:
                    self.x_velocity = v_len * sin
                    self.y_velocity = v_len * cos
                    self.x_velocity += first_velocity * sin
                    self.y_velocity += first_velocity * cos
                elif y1 < y2:
                    self.x_velocity = -v_len * sin
                    self.y_velocity = -v_len * cos
                    self.x_velocity += -first_velocity * sin
                    self.y_velocity += -first_velocity * cos
                elif x1 > x2 and y1 > y2:
                    self.x_velocity = v_len * sin
                    self.y_velocity = v_len * cos
                    self.x_velocity += first_velocity * sin
                    self.y_velocity += first_velocity * cos

                else:
                    self.x_velocity = -v_len * sin
                    self.y_velocity = -v_len * cos
                    self.x_velocity += -first_velocity * sin
                    self.y_velocity += -first_velocity * cos



                # self.x_velocity = v_len * sin
                # self.y_velocity = v_len * cos

            if not first_racket.hitting:
                new_x1 = x2 + math.ceil(115* cos)
                new_y1 = y2 + math.ceil(115* sin)

            else:
                new_x1 = x2 + math.ceil(120 * cos)
                new_y1 = y2 + math.ceil(120 * sin)

            self.rect.center = (new_x1, new_y1)
            self.collision = True

        #second racket
        elif second_length <= 110 and not self.collision:

            sin = (y1 - y3) / second_length
            cos = (x1 - x3) / second_length

                # odbicie
            if abs(sin) > self.sin_1:
                self.y_velocity = -self.y_velocity
                if self.y_velocity < 5:
                    self.y_velocity += math.ceil(second_racket.y_velocity * 1.2)
                else:
                    self.y_velocity += math.ceil(second_racket.y_velocity*0.9)
            elif abs(sin) < self.sin_2:
                self.x_velocity = -self.x_velocity
                self.x_velocity += math.ceil(second_racket .x_velocity*0.9)
            else:
                racket_velocity = math.hypot(second_racket.x_velocity, second_racket.y_velocity)
                if x1 < x3 and y1 < y3:
                    sound2.play()
                    self.x_velocity = v_len * sin
                    self.y_velocity = v_len * cos
                    self.x_velocity += racket_velocity * sin
                    self.y_velocity += racket_velocity * cos
                elif y1 < y3:
                    sound1.play()
                    self.x_velocity = -v_len * sin
                    self.y_velocity = -v_len * cos
                    self.x_velocity += -racket_velocity * sin
                    self.y_velocity += -racket_velocity * cos
                elif x1 > x3 and y1 > y3:
                    sound1.play()
                    self.x_velocity = v_len * sin
                    self.y_velocity = v_len * cos
                    self.x_velocity += racket_velocity * sin
                    self.y_velocity += racket_velocity * cos

                else:
                    sound1.play()
                    self.x_velocity = -v_len * sin
                    self.y_velocity = -v_len * cos
                    self.x_velocity += -racket_velocity * sin
                    self.y_velocity += -racket_velocity * cos

                # self.x_velocity = v_len * sin
                # self.y_velocity = v_len * cos

            if not second_racket.hitting:
                new_x1 = x3 + math.ceil(115* cos)
                new_y1 = y3 + math.ceil(115* sin)

            else:
                new_x1 = x3 + math.ceil(120 * cos)
                new_y1 = y3 + math.ceil(120 * sin)

            self.rect.center = (new_x1, new_y1)
            self.collision = True
        else:
            self.collision = False

        # spowolnienie do maxymalnej prędkości
        max_velocity = 30
        if v_len > max_velocity:

            self.x_velocity = self.x_velocity * (max_velocity/v_len)
            self.y_velocity = self.y_velocity * (max_velocity/v_len)
            # self.y_velocity = math.sqrt(max_velocity**2 - x_vel**2)

        else:
            self.collision = False
        # spowolnienie do maxymalnej prędkości

        max_velocity = 30
        if v_len > max_velocity:

            self.x_velocity = self.x_velocity * (max_velocity / v_len)
            self.y_velocity = self.y_velocity * (max_velocity / v_len)
            # self.y_velocity = math.sqrt(max_velocity**2 - x_vel**2)

class CurrentRound:
    def __init__(self, screen):
        self.p1_name = "Player 1"
        self.p2_name = "Player 2"
        self.p1_score = 0
        self.p2_score = 0
        self.screen = screen
        self.name_font = pygame.font.SysFont("monospace", 30)
        self.score_font = pygame.font.SysFont("monospace", 50)
        pygame.time.set_timer(TIMEREVENT, 1000)

    def save_round(self):
        if os.path.isfile("history.csv"):
            data = pd.read_csv("history.csv")
        else:
            data = pd.DataFrame(columns=['date', 'name_1', 'name_2', 'score'])

    def new_point(self, player):
        sound3.play()
        if player == 1:
            self.p1_score += 1
        else:
            self.p2_score += 1


    def update_labels(self):
        #Player 1
        lbl_1 = self.name_font.render(f"{self.p1_name}", True, (255, 255, 255))
        screen.blit(lbl_1, (70, 30))
        lbl_2 = self.name_font.render(f"{self.p2_name}", True, (255, 255, 255))
        screen.blit(lbl_2, (70,950))
        lbl_3 = self.score_font.render(f"{self.p1_score}", True, (255, 255, 255))
        screen.blit(lbl_3, (700, 30))
        lbl_4 = self.score_font.render(f"{self.p2_score}", True, (255, 255, 255))
        screen.blit(lbl_4, (700, 950))



class InputBox:
    def __init__(self, x, y, w, h, text='', player=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = input_font.render(text, True, self.color)
        self.active = False
        self.player = player

    def hadnle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.player is not None:
                        if self.player == 1:
                            round.p1_name = self.text
                        elif self.player == 2:
                            round.p2_name = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = input_font.render(self.text, 1, self.color)
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

        pygame.draw.rect(screen, self.color, self.rect, 2)

"""
class Button:
    def __init__(self, color, x, y, w, h, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = button_font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0]:
            pass
"""
class Button():
    def __init__(self, x, y, w, h, color, text_color , action=None, text=""):
        self.rect_filled = pygame.Rect(x,y,w,h)
        self.rect_frame = pygame.Rect(x,y,w,h)
        self.color = color
        self.text_color = text_color
        self.text = text
        self.txt_surface = button_font.render(text, True, text_color)
        self.action = action


    def draw(self, screen):

        pygame.draw.rect(screen, self.color, self.rect_filled, 0)
        pygame.draw.rect(screen, white, self.rect_filled, 2)
        screen.blit(self.txt_surface, (self.rect_filled.x + (self.rect_filled.w/2 - self.txt_surface.get_width()/2), self.rect_filled.y + (self.rect_filled.h/2 - self.txt_surface.get_height()/2)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_filled.collidepoint(event.pos):
                if self.action is not None:
                    self.action()








def create_my_puck():
    puck = Puck(pygame.color.Color("blue"),(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.77))
    puck_sprite.add(puck)
    pygame.time.set_timer(PUCKEVENT_1, 0)

def create_enemy_puck():
    puck = Puck(pygame.color.Color("blue"),(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.23))
    puck_sprite.add(puck)
    pygame.time.set_timer(PUCKEVENT_2, 0)

def close():
    quit()
    global running
    running = False

def start():
    global  menu
    menu = False


def history():
    global history
    history = True


def decrease_time():
    global timer
    timer -= 1

def show_timer(screen):
    min_lbl = timer_font.render(str(math.floor(timer/60)) + ":", 1, gray)
    if timer % 60 < 10:
        sec_txt = "0"+str(timer%60)
    else:
        sec_txt = str(timer%60)
    sec_lbl = timer_font.render(sec_txt, 1, gray)
    screen.blit(min_lbl, (80,60))
    screen.blit(sec_lbl, (100,60))



#functions neeeded in while loop:

pygame.init()
#inicjalizacja fontu
my_font = pygame.font.SysFont("monospace", 15)



screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Cymbergaj")



background_image = loadImage("background_2.png")
screen.blit(background_image,(0,0))


puck_sprite = pygame.sprite.RenderClear()
puck = Puck(pygame.color.Color("blue"),(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.23))
puck_sprite.add(puck)

rackets_sprite = pygame.sprite.RenderClear()
first_racket = Racket_1((SCREEN_WIDTH / 2, 0.9 * SCREEN_HEIGHT))
second_racket = Racket_2((SCREEN_WIDTH / 2, 0.1 * SCREEN_HEIGHT))
rackets_sprite.add(first_racket)
rackets_sprite.add(second_racket)

#napisy
round = CurrentRound(screen)


#menu
menu_background = pygame.Surface(SCREEN_SIZE)
menu_background.set_alpha(160)
menu_background.fill((66,0,0))

menu_font = pygame.font.SysFont("Arial", 90)
menu_lbl = menu_font.render("MENU", 1, (255,255,255))

player_font = pygame.font.SysFont("Arial", 60)

#inputs
input_font = pygame.font.SysFont("Arial", 60)
input_box1 = InputBox(80, 380, 140, 50, player=1)
input_box2 = InputBox(600, 380, 140, 50, player=2)
input_boxes = [input_box1, input_box2]

#buttons
button_font = pygame.font.SysFont("timesnewromanboldttf", 40)
start_button = Button(338, 800, 180, 50, dark_green, white,  start, "START")
history_button = Button(90, 800, 210, 50, gray, white,  history, "HISTORIA")
close_button = Button(555, 800, 200, 50, gray, white,  close, "KONIEC")
button_boxes = [start_button, history_button, close_button]

#timer
timer = 140
timer_font = pygame.font.SysFont("timesnewromanboldttf", 25)


#sound effects
sound1 = loadSound("audio1.wav")
sound1.set_volume(0.8)
sound2 = loadSound("audio1.wav")
sound2.set_volume(0.6)
sound3 = loadSound("goal.wav")



clock = pygame.time.Clock()
menu = True
history = False
running = True
while running:
    clock.tick(40)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                running = False
            for box in input_boxes:
                box.hadnle_event(event)
            for button in button_boxes:
                button.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    menu = not menu




        player_1_label = player_font.render(f"{round.p1_name}", 1, white)
        player_2_label = player_font.render(f"{round.p2_name}", 1, white)

        for box in input_boxes:
            box.update()

        screen.blit(background_image, (0, 0))
        screen.blit(menu_background, (0,0))
        screen.blit(menu_lbl, (SCREEN_WIDTH/2-86,100))
        screen.blit(player_1_label, (100, 300))
        screen.blit(player_2_label, (620, 300))

        for box in input_boxes:
            box.draw(screen)
        for button in button_boxes:
            button.draw(screen)

        clock.tick(30)
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                first_racket.x_velocity = -8
            elif event.key == K_DOWN:
                if not first_racket.hitting:
                    first_racket.y_velocity = 8
            elif event.key == K_UP:
                if not first_racket.hitting:
                    first_racket.y_velocity = -8
            elif event.key == K_RIGHT:
                first_racket.x_velocity = 8
            elif event.key == K_RALT:
                first_racket.hit()
            elif event.key == K_w:
                second_racket.y_velocity = -8
            elif event.key == K_s:
                second_racket.y_velocity = 8
            elif event.key == K_a:
                second_racket.x_velocity = -8
            elif event.key == K_d:
                second_racket.x_velocity = 8
            elif event.key == K_SPACE:
                second_racket.hit()
            elif event.key == K_ESCAPE:
                menu = not menu


        elif event.type == KEYUP:
            if event.key == K_LEFT:
                if first_racket.x_velocity == -8:
                    first_racket.x_velocity = 0
            elif event.key == K_DOWN:
                if not first_racket.hitting and first_racket.y_velocity==8:
                    first_racket.y_velocity = 0
            elif event.key == K_UP:
                if not first_racket.hitting and first_racket.y_velocity==-8:
                    first_racket.y_velocity = 0
            elif event.key == K_RIGHT:
                if first_racket.x_velocity == 8:
                    first_racket.x_velocity = 0
            elif event.key == K_RALT:
                first_racket.back = True
            elif event.key == K_w:
                if second_racket.y_velocity ==-8:
                    second_racket.y_velocity = 0
            elif event.key == K_s:
                if second_racket.y_velocity == 8:
                    second_racket.y_velocity = 0
            elif event.key == K_a:
                if second_racket.x_velocity == -8:
                    second_racket.x_velocity = 0
            elif event.key == K_d:
                if second_racket.x_velocity == 8:
                    second_racket.x_velocity = 0
            elif event.key == K_SPACE:
                second_racket.back = True
        elif event.type == PUCKEVENT_1:
            create_my_puck()
        elif event.type == PUCKEVENT_2:
            create_enemy_puck()
        elif event.type == TIMEREVENT:
            decrease_time()

    screen.blit(background_image, (0, 0))

    puck_sprite.update()
    rackets_sprite.update()

    puck_sprite.clear(screen, background_image)
    rackets_sprite.clear(screen, background_image)

    puck_sprite.draw(screen)
    rackets_sprite.draw(screen)
    round.update_labels()

    show_timer(screen)
    pygame.display.flip()





