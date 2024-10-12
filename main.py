import pygame
import sys
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE1 = (16,78,139)
BLUE2 = (24,116,205)
BLUE3 = (0,154,205)
BLUE4 = (0,191,255)
BLUE5 = (151,255,255)
BLUE6 = (32,178,170)

class Paddle:
    def __init__(self, screen):
        self.screen = screen
        self.speed = 0
        self.xpos = 350
        self.rect = pygame.Rect(self.xpos, 570, 100, 15)

    def update(self):
        self.xpos += self.speed
        if self.xpos > 700:
            self.xpos = 700
        if self.xpos < 0:
            self.xpos = 0

    def draw(self):
        pygame.draw.rect(self.screen, BLUE6, self.rect)

class Ball:
    def __init__(self, screen):
        self.screen = screen
        self.xspeed = -.3
        self.yspeed = -.3
        self.rspeed = math.sqrt(self.xspeed ** 2 + self.yspeed ** 2)
        self.bx = 400
        self.by = 300
        self.rect = pygame.Rect(self.bx, self.by, 30, 30)

    def update(self):
        self.bx += self.xspeed
        self.by += self.yspeed

        if self.bx > SCREEN_WIDTH or self.bx < 0:
            self.xspeed *= -1
        if self.by > SCREEN_HEIGHT:
            if self.by > SCREEN_HEIGHT:
                sys.exit()
        if self.by < 0:
            self.yspeed *= -1

    def draw(self):
        pygame.draw.ellipse(self.screen, BLUE5, self.rect)


class Brick:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.rect = pygame.Rect(x, y, 77, 12)

    def draw(self):
        pygame.draw.rect(self.screen, self.rect)


class BreakoutGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Breakout Game')

        self.paddle = Paddle(self.screen)
        self.ball = Ball(self.screen)
        self.bricks = self.create_bricks()

        self.score = 0
        self.winning_score = 80
        self.font = pygame.font.SysFont('comic sans', size=25)

        self.start_screen = True

    def create_bricks(self):
        bricks = []
        for i in range(8):
            for j in range(10):
                brick_x = j * 81 + 1
                brick_y = i * 15
                brick = Brick(self.screen, brick_x, brick_y)
                bricks.append(brick)
        return bricks

    def display_scores(self):
        text = self.font.render(f"Breakout Game|Score: {self.score}|", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 138))
        self.screen.blit(text, text_rect)

    def display_bricks(self):
        for brick in self.bricks:
            if brick.rect.y == 0 or brick.rect.y == 15:
                colour = BLUE1
            if brick.rect.y == 30 or brick.rect.y == 45:
                colour = BLUE2
            if brick.rect.y == 60 or brick.rect.y == 75:
                colour = BLUE3
            if brick.rect.y == 90 or brick.rect.y == 105:
                colour = BLUE4
            pygame.draw.rect(self.screen, colour, brick.rect)

    def game_over(self):
        if self.score == self.winning_score:
            self.screen.fill((0,0,0))
            font = pygame.font.SysFont('comic sans', 50)
            text3 = font.render(f"GAME OVER, You Win!", True, WHITE, None)
            text3_rect = text3.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            self.screen.blit(text3, text3_rect)

    def run(self):
        while self.start_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start_screen = False
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    self.start_screen = False

            self.screen.fill((0, 0, 0))
            font = pygame.font.SysFont('comic sans', size=30)
            start_text = font.render("Press Any Key To Start", True, WHITE)
            start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, 340))
            self.screen.blit(start_text, start_text_rect)
            font2 = pygame.font.SysFont('comic sans', size=60)
            start_text2 = font2.render("Breakout Game", True, WHITE)
            start_text_rect2 = start_text2.get_rect(center=(SCREEN_WIDTH / 2, 250))
            self.screen.blit(start_text2, start_text_rect2)
            font3 = pygame.font.SysFont('comic sans', size=18)
            start_text3 = font3.render("Created By Natasha", True, WHITE)
            start_text_rect3 = start_text3.get_rect(center=(705, 580))
            self.screen.blit(start_text3, start_text_rect3)
            pygame.display.update()

        game_on = True

        while game_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.paddle.speed += .7
                    if event.key == pygame.K_LEFT:
                        self.paddle.speed -= .7
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.paddle.speed -= .7
                    if event.key == pygame.K_LEFT:
                        self.paddle.speed += .7

            self.paddle.update()
            self.ball.update()

            if self.ball.rect.colliderect(self.paddle.rect):
                distance = (self.ball.bx + 7.5) - (self.paddle.xpos + 50)
                self.ball.xspeed = distance / 80 * self.ball.rspeed
                self.ball.yspeed = math.sqrt(self.ball.rspeed ** 2 - self.ball.xspeed ** 2)
                self.ball.yspeed *= -1
                self.ball.by -= 10

            for brick in self.bricks:
                if self.ball.rect.colliderect(brick.rect):
                    self.bricks.remove(brick)
                    self.ball.yspeed *= -1
                    self.ball.by += 1
                    self.score += 1

            self.screen.fill((0, 0, 0))
            self.paddle.rect = pygame.Rect(self.paddle.xpos, 570, 100, 15)
            self.paddle.draw()
            self.ball.rect = pygame.Rect(self.ball.bx, self.ball.by, 20, 20)
            self.ball.draw()
            self.display_bricks()
            self.display_scores()
            self.game_over()
            pygame.display.update()


game = BreakoutGame()
game.run()
