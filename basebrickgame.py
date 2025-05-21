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
    
    #게임 상태 및 변수상태 초기화
    score = 0                   #벽돌 깬 횟수 기록 (게임 점수)
    missed = 0                  #공을 놓친 횟수 (3번 놓치면 게임 오버)
    SUCCESS = 1                 #게임 성공을 나타내는 상태값
    FAILURE = 2                 #게임 실패를 나타내는 상태값
    game_over = 0               #게임 현재상태 (0이면 실행중)

    #벽돌 생성
    bricks = []
    COLUMN_COUNT = 8
    ROW_COUNT = 7
    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT):
            brick = pygame.Rect(column_index * (60 + 10) + 35, row_index * (16 + 5) + 35, 60, 16)
            bricks.append(brick)      

    #공과 패들 초기 설정
    ball = pygame.Rect(screen_width // 2 - 16 // 2, screen_height // 2 - 16 // 2, 16, 16)
    ball_dx = 5
    ball_dy = -5

    paddle = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 16, 80, 16)
    paddle_dx = 0

    #메인루프 시작
    while True: 
        clock.tick(30)
        screen.fill(BLACK) 

    #이벤트 처리 (키 입력)
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
    #객체 위치 업데이트
        paddle.left += paddle_dx

        ball.left += ball_dx
        ball.top  += ball_dy

    #공의 벽 충돌 처리
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

    #게임 오버 조건 검사
        if missed >= 3:
            game_over = FAILURE 

    #패들의 화면 경계 제한
        if paddle.left < 0:
            paddle.left = 0
        elif paddle.left > screen_width - paddle.width:
            paddle.left = screen_width - paddle.width
    
    #공과 벽돌 충돌 처리
        for brick in bricks:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_dy = -ball_dy
                score += 1
                break
    
    #공과 패들 충돌처리
        if ball.colliderect(paddle):
            ball_dy = -ball_dy
            if ball.centerx <= paddle.left or ball.centerx > paddle.right:
                ball_dx = ball_dx * -1

    #게임 성공 조건 (남은 벽돌이 없으면 게임 성공)
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

