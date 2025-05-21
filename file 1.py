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

while True: 
    clock.tick(30)
    screen.fill(BLACK)