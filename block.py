import pygame
import random
import time

pygame.init()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

def runGame():
    Level = 1
    paused = False
    score = 0
    Life = 3
    SUCCESS = 1
    FAILURE = 2
    game_over = 0

    bricks = []
    COLUMN_COUNT = 8
    ROW_COUNT = 3
    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT):
            brick = pygame.Rect(column_index * (60 + 10) + 35, row_index * (16 + 5) + 80, 60, 16)
            bricks.append(brick)

    # 폭탄 관련 변수
    bomb_bricks = []
    last_bomb_time = time.time()
    bomb_interval = 5

    def spawn_bomb_block():
        empty_spaces = [brick for brick in bricks if brick not in bomb_bricks]
        if empty_spaces:
            new_bomb = random.choice(empty_spaces)
            bomb_bricks.append(new_bomb)

    ball = pygame.Rect(screen_width // 2 - 16 // 2, screen_height // 2 - 16 // 2, 16, 16)
    ball_dx = 5.0
    ball_dy = -5.0

    paddle = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 16, 100, 16)
    paddle_dx = 0

    while True:
        delta_time = clock.tick(60) / 10000
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle_dx = -5.0
                elif event.key == pygame.K_RIGHT:
                    paddle_dx = 5.0
                elif event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_p:
                    paused = not paused
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    paddle_dx = 0

        if not paused and game_over == 0:
            paddle.left += paddle_dx
            ball.left += ball_dx
            ball.top += ball_dy

            if ball.left <= 0 or ball.left >= screen_width - ball.width:
                ball_dx = -ball_dx
            if ball.top < 0:
                ball_dy = -ball_dy
            elif ball.top >= screen_height:
                Life -= 1
                ball.left = screen_width // 2 - ball.width // 2
                ball.top = screen_height // 2 - ball.width // 2
                ball_dy = -ball_dy

            if Life <= 0:
                game_over = FAILURE

            if paddle.left < 0:
                paddle.left = 0
            elif paddle.left > screen_width - paddle.width:
                paddle.left = screen_width - paddle.width

            # 폭탄 생성 타이머
            current_time = time.time()
            if current_time - last_bomb_time > bomb_interval:
                spawn_bomb_block()
                last_bomb_time = current_time

            # 공과 벽돌 충돌 처리
            for brick in bricks:
                if ball.colliderect(brick):
                    if brick in bomb_bricks:
                        bomb_bricks.remove(brick)
                        bx, by = brick.center
                        removed = []
                        for b in bricks:
                            if abs(b.centerx - bx) <= 70 and abs(b.centery - by) <= 25:
                                removed.append(b)
                        for b in removed:
                            if b in bricks:
                                bricks.remove(b)
                                if b in bomb_bricks:
                                    bomb_bricks.remove(b)
                                score += 1
                    else:
                        bricks.remove(brick)
                        score += 1
                    ball_dy = -ball_dy
                    break

        if ball.colliderect(paddle):
            ball_dy = -ball_dy
            if ball.centerx <= paddle.left or ball.centerx > paddle.right:
                ball_dx = ball_dx * -1

        if len(bricks) == 0:
            Level += 1
            Life += 1
            ball_dx = float(ball_dx * 1.3) if ball_dx > 0 else float(ball_dx * 1.3)
            ball_dy = float(ball_dy * 1.3) if ball_dy > 0 else float(ball_dy * 1.3)
            bricks = []
            bomb_bricks = []
            COLUMN_COUNT = 8
            ROW_COUNT = min(3 + Level, 6)
            for column_index in range(COLUMN_COUNT):
                for row_index in range(ROW_COUNT):
                    brick = pygame.Rect(column_index * (60 + 10) + 35, row_index * (16 + 5) + 80, 60, 16)
                    bricks.append(brick)
            ball.left = screen_width // 2 - ball.width // 2
            ball.top = screen_height // 2 - ball.height // 2
            ball_dy = -abs(ball_dy)

        # 화면 그리기
        for brick in bricks:
            if brick in bomb_bricks:
                pygame.draw.rect(screen, RED, brick)
            else:
                pygame.draw.rect(screen, GREEN, brick)

        if game_over == 0:
            pygame.draw.circle(screen, WHITE, (ball.centerx, ball.centery), ball.width // 2)

        pygame.draw.rect(screen, BLUE, paddle)

        score_image = small_font.render('Point {}'.format(score), True, YELLOW)
        screen.blit(score_image, (10, 10))

        Life_image = small_font.render('Life {}'.format(Life), True, YELLOW)
        screen.blit(Life_image, Life_image.get_rect(right=screen_width - 10, top=10))

        level_image = small_font.render('Level {}'.format(Level), True, YELLOW)
        screen.blit(level_image, (10, 40))

        if game_over == FAILURE:
            failure_image = large_font.render('Game Over', True, RED)
            screen.blit(failure_image, failure_image.get_rect(centerx=screen_width // 2, centery=screen_height // 2))

        if paused:
            pause_text = large_font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, pause_text.get_rect(centerx=screen_width // 2, centery=screen_height // 2))

        pygame.display.update()

runGame()
pygame.quit()
