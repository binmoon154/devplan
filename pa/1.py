import pygame
import sys

# 게임 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Class로 만든 캐릭터")
clock = pygame.time.Clock()

# 색깔
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# 캐릭터 클래스 만들기
class Player:
    def __init__(self, x, y):
        self.x = x  # 캐릭터의 x 위치
        self.y = y  # 캐릭터의 y 위치
        self.width = 50
        self.height = 50
        self.color = BLUE
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()  # 키보드 입력 확인
        if keys[pygame.K_RIGHT]:  # 오른쪽 화살표 키
            self.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Player 클래스 사용해서 캐릭터 만들기
player = Player(100, 300)

# 게임 루프
running = True
while running:
    screen.fill(WHITE)  # 화면 흰색으로 지우기
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move()  # 캐릭터 움직임
    player.draw(screen)  # 캐릭터 그리기

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
