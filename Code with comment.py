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

paused = False

def runGame():
    paused = False
    
    #게임 상태 및 변수상태 초기화
    score = 0                   #벽돌 깬 횟수 기록 (게임 점수)
    missed = 0                  #공을 놓친 횟수 (3번 놓치면 게임 오버)
    SUCCESS = 1                 #게임 성공을 나타내는 상태값
    FAILURE = 2                 #게임 실패를 나타내는 상태값
    game_over = 0               #게임 현재상태 (0이면 실행중)

    #벽돌 생성
    bricks = []
    COLUMN_COUNT = 8
    ROW_COUNT = 7               #8열 7행의 벽돌 생성
    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT):
            brick = pygame.Rect(column_index * (60 + 10) + 35, row_index * (16 + 5) + 35, 60, 16)           #벽돌의 크기 : 60 * 16 / 벽돌사이 간격 : 가로 10 세로 5 / 열간격 : (60 + 10) / 행간격 : (16 + 5) /  시작좌표 : (35, 35)
            bricks.append(brick)                                                                            #bricks 배열에 추가

    #공과 패들 초기 설정
    ball = pygame.Rect(screen_width // 2 - 16 // 2, screen_height // 2 - 16 // 2, 16, 16)                   #공 크기 :16 * 16, 화면 정 중앙에 위치
    ball_dx = 5                                                                                             #ball_dx : 공 x축 속도
    ball_dy = -5                                                                                            #ball_dy : 공 y축 속도

    paddle = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 16, 80, 16)                           #패들 크기 : 80 * 16 / 화면 아래쪽에 위치 시킴
    paddle_dx = 0                                                                                           #패들 좌우 이동속도 (키 입력에 따라 변경)

    #메인루프 시작
    while True: 
        delta_time = clock.tick(30)                                                                         #FPS 30으로 설정 : 게임속도 고정
        screen.fill(BLACK)                                                                                  #이전 프레임의 내용을 지우고 새로 그림

    #이벤트 처리 (키 입력)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle_dx = -5
                elif event.key == pygame.K_RIGHT:
                    paddle_dx = 5
                elif event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_p:
                    paused = not paused
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    paddle_dx = 0
                elif event.key == pygame.K_RIGHT:
                    paddle_dx = 0


        if not paused and game_over == 0:
        #객체 위치 업데이트
            paddle.left += paddle_dx

            ball.left += ball_dx
            ball.top  += ball_dy

        #공의 벽 충돌 처리
            ##공이 좌우 벽에 닿으면 반사 (방향 반전)
            if ball.left <= 0:
                ball.left = 0
                ball_dx = -ball_dx
            elif ball.left >= screen_width - ball.width: 
                ball.left = screen_width - ball.width
                ball_dx = -ball_dx

            ##공이 천장에 닿으면 위아래 방향 반전
            if ball.top < 0:
                ball.top = 0
                ball_dy = -ball_dy

            ##공이 화면 아래로 떨어지면 missed += 1 (놓친 횟수 증가)
            ##공을 다시 중앙에 위치시키고 방향만 반대로
            elif ball.top >= screen_height:
                missed += 1
                ball.left = screen_width // 2 - ball.width // 2
                ball.top = screen_height // 2 - ball.width // 2
                ball_dy = -ball_dy 

        #게임 오버 조건 검사
            if missed >= 3:
                game_over = FAILURE                                         #공을 3번 놓치면 게임 실패 처리

        #패들의 화면 경계 제한 (패들이 화면 밖으로 나가지 않게 함)
            if paddle.left < 0:
                paddle.left = 0
            elif paddle.left > screen_width - paddle.width:
                paddle.left = screen_width - paddle.width
        
        #공과 벽돌 충돌 처리
            for brick in bricks:
                if ball.colliderect(brick):
                    bricks.remove(brick)                                    #해당 벽돌 제거
                    ball_dy = -ball_dy                                      #공 반사
                    score += 1                                              #점수 1점 증가
                    break
        
        #공과 패들 충돌처리
            if ball.colliderect(paddle):
                ball_dy = -ball_dy                                                  #공이 패들과 부딪히면 위로 반사
                if ball.centerx <= paddle.left or ball.centerx > paddle.right:      #만약 공이 패들의 가장자리에 닿았으면 X축 방향도 반사
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


        if paused:
            pause_text = large_font.render("PAUSED", True, WHITE)
            screen.blit(pause_text, pause_text.get_rect(centerx=screen_width // 2, centery=screen_height // 2))

        pygame.display.update()

runGame()
pygame.quit()

