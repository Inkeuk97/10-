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
    score = 0
    missed = 0
    SUCCESS = 1
    FAILURE = 2
    game_over = 0

    bricks = []
    COLUMN_COUNT = 8
    ROW_COUNT = 7
    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT):
            brick = pygame.Rect(column_index * (60 + 10) + 35, row_index * (16 + 5) + 35, 60, 16)
            bricks.append(brick)      

    ball = pygame.Rect(screen_width // 2 - 16 // 2, screen_height // 2 - 16 // 2, 16, 16)
    ball_dx = 5
    ball_dy = -5

    paddle = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 16, 80, 16)
    paddle_dx = 0
    
    bomb_blocks = []  # 폭탄 블록 리스트
    BOMB_SIZE = 24
    last_bomb_time = pygame.time.get_ticks()
    BOMB_INTERVAL = 10000  # 10초마다 폭탄 생성

    def explode_bomb(bomb):
        nonlocal bricks, score
        # 폭탄 주변에 있는 블록들을 제거
        explosion_radius = BOMB_SIZE * 2  # 폭탄 영향 범위
        destroyed = []
        for brick in bricks:
            # 폭탄 중심과 블록 중심 사이 거리 체크
            dist_x = abs(bomb.centerx - brick.centerx)
            dist_y = abs(bomb.centery - brick.centery)
            if dist_x <= explosion_radius and dist_y <= explosion_radius:
                destroyed.append(brick)
        for d in destroyed:
            bricks.remove(d)
            score += 1

    while True: 
        clock.tick(30)
        screen.fill(BLACK) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle_dx = -5
                elif event.key == pygame.K_RIGHT:
                    paddle_dx = 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    paddle_dx = 0
                elif event.key == pygame.K_RIGHT:
                    paddle_dx = 0        

        paddle.left += paddle_dx

        ball.left += ball_dx
        ball.top  += ball_dy

        if ball.left <= 0:
            ball.left = 0
            ball_dx = -ball_dx
        elif ball.left >= screen_width - ball.width: 
            ball.left = screen_width - ball.width
            ball_dx = -ball_dx
        if ball.top < 0:
            ball.top = 0
            ball_dy = -ball_dy
        elif ball.top >= screen_height:
            missed += 1
            ball.left = screen_width // 2 - ball.width // 2
            ball.top = screen_height // 2 - ball.width // 2
            ball_dy = -ball_dy 

        if missed >= 3:
            game_over = FAILURE 

        if paddle.left < 0:
            paddle.left = 0
        elif paddle.left > screen_width - paddle.width:
            paddle.left = screen_width - paddle.width

        for brick in bricks:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_dy = -ball_dy
                score += 1
                break

        # 폭탄 블록과 충돌
        bomb_to_remove = None
        for bomb in bomb_blocks:
            if ball.colliderect(bomb):
                bomb_to_remove = bomb
                ball_dy = -ball_dy
                explode_bomb(bomb)
                break
        if bomb_to_remove:
            bomb_blocks.remove(bomb_to_remove)

        if ball.colliderect(paddle):
            ball_dy = -ball_dy
            if ball.centerx <= paddle.left or ball.centerx > paddle.right:
                ball_dx = ball_dx * -1

        if len(bricks) == 0:
            print('success')
            game_over = SUCCESS

        #화면 그리기

        for brick in bricks:
            pygame.draw.rect(screen, GREEN, brick)

        if game_over == 0:
            pygame.draw.circle(screen, WHITE, (ball.centerx, ball.centery), ball.width // 2)

        pygame.draw.rect(screen, BLUE, paddle)

        score_image = small_font.render('Point {}'.format(score), True, YELLOW)
        screen.blit(score_image, (10, 10))

        missed_image = small_font.render('Missed {}'.format(missed), True, YELLOW)
        screen.blit(missed_image, missed_image.get_rect(right=screen_width - 10, top=10))

        if game_over > 0:
            if game_over == SUCCESS:
                success_image = large_font.render('성공', True, RED)
                screen.blit(success_image, success_image.get_rect(centerx=screen_width // 2, centery=screen_height // 2))
            elif game_over == FAILURE:
                failure_image = large_font.render('실패', True, RED)
                screen.blit(failure_image, failure_image.get_rect(centerx=screen_width // 2, centery=screen_height // 2))

        pygame.display.update()

runGame()
pygame.quit()

