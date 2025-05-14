import pygame # 1. pygame 선언
 
pygame.init() # 2. pygame 초기화
 
# 3. pygame에 사용되는 전역변수 선언
 
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
 
clock= pygame.time.Clock()
 
# 4. pygame 무한루프
 
def runGame():
    global done
    while not done:
        clock.tick(10)
        screen.fill(WHITE)
 
runGame()
pygame.quit()

