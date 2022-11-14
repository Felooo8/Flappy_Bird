import sys
import pygame
import os
from random import randint

from pygame import Rect

pygame.init()
pygame.font.init()
# pygame.mixer.init()


BG = pygame.image.load(
    os.path.join('Assets/background.png'))

WIDTH, HEIGHT = BG.get_width(), BG.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird by Felo")
programIcon = pygame.transform.scale(pygame.image.load(os.path.join('Assets/bird.png')), (64, 64))
pygame.display.set_icon(programIcon)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
VEL = 4
DISTANCE_Y = 320 + 100  ### 320 is the height of upper pipe and 2nd value is changeable distance
DISTANCE_X = 200  ### 200 is the distance between new pipes

BIRD = pygame.image.load(
    os.path.join('Assets/bird.png'))

BIRD_2 = pygame.image.load(
    os.path.join('Assets/bird_2.png'))

BIRD_3 = pygame.image.load(
    os.path.join('Assets/bird_3.png'))

BIRDS = [BIRD, BIRD_2, BIRD_3]

PIPE = pygame.image.load(
    os.path.join('Assets/pipe.png'))

PIPE_DOWN = pygame.image.load(
    os.path.join('Assets/pipe_down.png'))

PIPE_UP = pygame.image.load(
    os.path.join('Assets/pipe_up.png'))

GROUND = pygame.image.load(
    os.path.join('Assets/ground.png'))

GAME_OVER = pygame.image.load(
    os.path.join('Assets/game_over.png'))

PLAY_BUTTON = pygame.image.load(
    os.path.join('Assets/play_button.png'))

SCORE = pygame.image.load(
    os.path.join('Assets/score.png'))

NEW = pygame.image.load(
    os.path.join('Assets/new.png'))

BRONZE_MEDAL = pygame.image.load(
    os.path.join('Assets/bronze_medal.png'))

SILVER_MEDAL = pygame.image.load(
    os.path.join('Assets/silver_medal.png'))

GOLD_MEDAL = pygame.image.load(
    os.path.join('Assets/gold_medal.png'))

PLATINUM_MEDAL = pygame.image.load(
    os.path.join('Assets/platinium_medal.png'))

### images of numbers:

numbers = []

for i in range(0, 10):
    i = pygame.image.load(
        os.path.join(f'Assets/{i}.png'))
    numbers.append(i)

# images of small numbers:

small_numbers = []

for i in range(0, 10):
    if i == 1:
        small_numbers.append(pygame.transform.scale(
            numbers[i], (10, 20)))
    else:
        small_numbers.append(pygame.transform.scale(
            numbers[i], (14, 20)))

### numbers manual:

ZERO = pygame.image.load(
    os.path.join('Assets/0.png'))

ONE = pygame.image.load(
    os.path.join('Assets/1.png'))

TWO = pygame.image.load(
    os.path.join('Assets/2.png'))

THREE = pygame.image.load(
    os.path.join('Assets/3.png'))

FOUR = pygame.image.load(
    os.path.join('Assets/4.png'))

FIVE = pygame.image.load(
    os.path.join('Assets/5.png'))

SIX = pygame.image.load(
    os.path.join('Assets/6.png'))

SEVEN = pygame.image.load(
    os.path.join('Assets/7.png'))

EIGHT = pygame.image.load(
    os.path.join('Assets/8.png'))

NINE = pygame.image.load(
    os.path.join('Assets/9.png'))

SCORE_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)

END = pygame.USEREVENT + 1


class Flappy_Bird:

    bird: Rect

    def __init__(self, record):

        init_pipe_x = 300

        init_pipe_y_up = -100

        init_pipe_y_down = init_pipe_y_up + DISTANCE_Y

        self.bird = pygame.Rect(1 / 5 * WIDTH, 1 / 3 * HEIGHT, BIRD.get_width(), BIRD.get_height())

        self.pipe_up = pygame.Rect(init_pipe_x, init_pipe_y_up, PIPE_UP.get_width(), PIPE_UP.get_height())

        self.pipe_down = pygame.Rect(init_pipe_x, init_pipe_y_down, PIPE_DOWN.get_width(), PIPE_DOWN.get_height())

        self.ground = pygame.Rect(0, HEIGHT - GROUND.get_height(), GROUND.get_width(), GROUND.get_height())

        self.current_bird = 0
        self.current_bird_change = 0

        self.score = 0  #### score === pipes passed

        self.record = record

        self.acc = 0  ### acceleration

        self.generate = 0  ### not to create too many pipes

        self.current_pipe = 0  ### pipe that bird is going to pass now

        self.pipes = [(self.pipe_up, self.pipe_down)]
        self.pipes_up = [self.pipe_up]
        self.pipes_down = [self.pipe_down]

        self.grounds = [self.ground]

        self.clock = pygame.time.Clock()
        self.run = True
        while self.run:
            self.clock.tick(FPS)
            self.if_key_was_pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.run = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.if_key_was_pressed:
                            self.fly()  ###jump
                            self.if_key_was_pressed = True
                        else:
                            pass
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.if_key_was_pressed:
                        self.fly()  ###jump
                        self.if_key_was_pressed = True
                    else:
                        pass





            #### generates new pipe only once in a time (now once a second)
            self.generate += 1
            if self.generate < 2:
                self.generate_objects()
            elif self.generate > 60:  ### generate new pipe once a x fps
                self.generate = 0
            else:
                pass



            self.handle_collisions()

            for event in pygame.event.get():
                if event.type == END:
                    self.end_game()

            self.move_objects()
            self.draw_window()


    def fly(self):
        self.acc = -64

    def handle_collisions(self):

        for pipe_up, pipe_down in self.pipes:  ### if bird touches pipes
            if pipe_up.colliderect(self.bird) or pipe_down.colliderect(self.bird):
                pygame.event.post(pygame.event.Event(END))

        if self.bird.y < 0 or self.bird.y + BIRD.get_height() > self.ground.y:  ### if bird flies too high or to low
            pygame.event.post(pygame.event.Event(END))

        if self.bird.x > ((self.pipes[self.current_pipe][0]).x + PIPE_DOWN.get_width()):  #### if bird passes the pipe
            self.score += 1
            self.current_pipe += 1


    def draw_window(self):

        WIN.blit(BG, (0, 0))
        WIN.blit(BIRDS[self.current_bird], (self.bird.x + 1, self.bird.y))

        #### so that it changes less often
        self.current_bird_change += 1
        if self.current_bird_change > 6: ### the higher the slower it changes
            self.current_bird_change = 0
            self.current_bird += 1
            if self.current_bird > 2:
                self.current_bird = 0

        for i, pipe in enumerate(self.pipes):
            WIN.blit(PIPE_UP, (self.pipes[i][0].x, self.pipes[i][0].y))

        for i, pipe in enumerate(self.pipes):
            WIN.blit(PIPE_DOWN, (self.pipes[i][1].x, self.pipes[i][1].y))

        for i, ground in enumerate(self.grounds):
            WIN.blit(GROUND, (self.grounds[i].x, self.grounds[i].y))

        ### draw score

        self.height_of_score = BG.get_height() / 10

        if self.score // 10 == 0:
            WIN.blit(numbers[self.score], (BG.get_width() / 2 - numbers[self.score].get_width() / 2, self.height_of_score))
        elif 0 < self.score // 10 < 10:
            WIN.blit(numbers[int(str(self.score)[0])],
                     (BG.get_width() / 2 - (numbers[int(str(self.score)[0])].get_width() + numbers[int(str(self.score)[1])].get_width()) / 2, self.height_of_score))

            WIN.blit(numbers[int(str(self.score)[1])], (BG.get_width() / 2 - (- numbers[int(str(self.score)[0])].get_width() + numbers[int(str(self.score)[1])].get_width()) / 2, self.height_of_score))
        else:
            WIN.blit(numbers[int(str(self.score)[0])], (
                BG.get_width() / 2 - (numbers[int(str(self.score)[0])].get_width() + numbers[int(str(self.score)[1])].get_width() + numbers[int(str(self.score)[2])].get_width()) / 2, self.height_of_score))

            WIN.blit(numbers[int(str(self.score)[1])],
                     (BG.get_width() / 2 - ( - numbers[int(str(self.score)[0])].get_width() + numbers[int(str(self.score)[1])].get_width() + numbers[int(str(self.score)[2])].get_width()) / 2, self.height_of_score))

            WIN.blit(numbers[int(str(self.score)[2])], (BG.get_width() / 2 - ( - numbers[int(str(self.score)[0])].get_width() - numbers[int(str(self.score)[1])].get_width() + numbers[int(str(self.score)[2])].get_width()) / 2, self.height_of_score))

        pygame.display.update()

    def generate_objects(self):
        new_pipe_x = self.pipes[len(self.pipes) - 1][0].x + DISTANCE_X
        new_pipe_y = randint(-280, -80)
        self.pipe_up = pygame.Rect(new_pipe_x, new_pipe_y, PIPE_UP.get_width(), PIPE_UP.get_height())
        self.pipe_down = pygame.Rect(new_pipe_x, new_pipe_y + DISTANCE_Y, PIPE_DOWN.get_width(), PIPE_DOWN.get_height())
        self.pipes.append((self.pipe_up, self.pipe_down))

        ### so that it moves and is always on the screen
        new_ground_x = self.grounds[len(self.grounds) - 1].x + GROUND.get_width()
        self.ground = pygame.Rect(new_ground_x, HEIGHT - GROUND.get_height(), GROUND.get_width(), GROUND.get_height())
        self.grounds.append(self.ground)

    def move_objects(self):

        #### if acc > 0 then its going down (y is increasing), the higher acc the hugher speed)
        if self.acc < -32:
            self.bird.y -= VEL
            self.acc += VEL
        elif self.acc < 0:
            self.bird.y -= VEL / 2
            self.acc += VEL / 2
        else:
            if self.acc > 48:
                self.bird.y += VEL + 1
                self.acc += VEL + 1
            elif self.acc > 32:
                self.bird.y += VEL
                self.acc += VEL
            else:
                self.bird.y += VEL / 2
                self.acc += VEL / 2

        for i, pipe in enumerate(self.pipes):
            self.pipes[i][0].x -= 2
            self.pipes[i][1].x -= 2

        for i, ground in enumerate(self.grounds):
            self.grounds[i].x -= 1
            self.grounds[i].x -= 1

    def end_game(self):

        WIN.blit(GAME_OVER, (BG.get_width() / 2 - GAME_OVER.get_width() / 2, BG.get_height() / 4 - 20))

        b = WIN.blit(PLAY_BUTTON, (BG.get_width() / 2 - PLAY_BUTTON.get_width() / 2, BG.get_height() / 2 + 50))

        #b = WIN.blit(PLAY_BUTTON, (BG.get_width() / 2 - PLAY_BUTTON.get_width() / 2, BG.get_height() / 2 + 50))

        self.draw_score()

        pygame.display.update()

        run = True
        while run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if b.collidepoint(pos):
                        Flappy_Bird(self.record)
                        run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Flappy_Bird(self.record)
                        run = False
                        break

        # pygame.time.delay(5000)
        # Flappy_Bird(self.record)

    def draw_score(self):

        self.height_of_small_numbers = BG.get_height() / 3 + 32  ### 32 is the distance between SCORE and postiion of numbers

        SCORE_X, SCORE_Y = BG.get_width() / 2 - SCORE.get_width() / 2, self.height_of_small_numbers - 32

        WIN.blit(SCORE, (SCORE_X, SCORE_Y))

        self.width_of_small_numbers = 221

        if self.score // 10 == 0:
            WIN.blit(small_numbers[self.score], (self.width_of_small_numbers,
                                                 self.height_of_small_numbers))
        elif 0 < self.score // 10 < 10:
            WIN.blit(small_numbers[int(str(self.score)[0])],
                     (self.width_of_small_numbers - small_numbers[int(str(self.score)[0])].get_width(),
                      self.height_of_small_numbers))

            WIN.blit(small_numbers[int(str(self.score)[1])],
                     (self.width_of_small_numbers, self.height_of_small_numbers))
        else:
            WIN.blit(small_numbers[int(str(self.score)[0])], (
                self.width_of_small_numbers - small_numbers[int(str(self.score)[1])].get_width()
                - small_numbers[int(str(self.score)[0])].get_width(), self.height_of_small_numbers))

            WIN.blit(small_numbers[int(str(self.score)[1])],
                     (self.width_of_small_numbers - small_numbers[int(str(self.score)[1])].get_width(),
                      self.height_of_small_numbers))

            WIN.blit(small_numbers[int(str(self.score)[2])],
                     (self.width_of_small_numbers, self.height_of_small_numbers))

        if self.score > self.record:
            self.record = self.score
            WIN.blit(NEW, (BG.get_width() / 2 - SCORE.get_width() / 2 + 136, BG.get_height() / 3 + 59))

        if self.score > 100:
            WIN.blit(PLATINUM_MEDAL, (SCORE_X + 26, SCORE_Y + 42))
        elif self.score > 50:
            WIN.blit(GOLD_MEDAL, (SCORE_X + 26, SCORE_Y + 42))
        elif self.score > 20:
            WIN.blit(SILVER_MEDAL, (SCORE_X + 26, SCORE_Y + 42))
        elif self.score > 10:
            WIN.blit(BRONZE_MEDAL, (SCORE_X + 26, SCORE_Y + 42))

        self.height_of_record = BG.get_height() / 3 + 32 + 42  ### 42 is the difference between score and record on image
        self.width_of_record = self.width_of_small_numbers

        if self.record // 10 == 0:
            WIN.blit(small_numbers[self.record], (self.width_of_record,
                                                  self.height_of_record))
        elif 0 < self.record // 10 < 10:
            WIN.blit(small_numbers[int(str(self.record)[0])],
                     (self.width_of_record - small_numbers[int(str(self.record)[0])].get_width(),
                      self.height_of_record))

            WIN.blit(small_numbers[int(str(self.record)[1])],
                     (self.width_of_record, self.height_of_record))
        else:
            WIN.blit(small_numbers[int(str(self.record)[0])], (
                self.width_of_record - small_numbers[int(str(self.record)[1])].get_width() - small_numbers[
                    int(str(self.record)[0])].get_width(), self.height_of_record))

            WIN.blit(small_numbers[int(str(self.record)[1])],
                     (self.width_of_record - small_numbers[int(str(self.record)[1])].get_width(),
                      self.height_of_record))

            WIN.blit(small_numbers[int(str(self.record)[2])],
                     (self.width_of_record, self.height_of_record))


if __name__ == "__main__":
    record = 0
    Flappy_Bird(record)
