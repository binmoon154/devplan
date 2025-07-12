import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("카메라 따라다니기")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 36)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = 5
        self.inventory = []

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if keys[pygame.K_LSHIFT]:
                self.rect.x -= self.speed * 1.4
            else:
                self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if keys[pygame.K_LSHIFT]:
                self.rect.x += self.speed * 1.4
            else:
                self.rect.x += self.speed

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.rect(screen, BLUE, (self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height))

class Door:
    def __init__(self, screen_x, screen_y):  # 화면 좌표로 고정
        self.screen_rect = pygame.Rect(screen_x, screen_y, 50, 80)
        self.opened = False

    def open(self):
        self.opened = True

    def draw(self, screen):
        color = GRAY if self.opened else BROWN
        pygame.draw.rect(screen, color, self.screen_rect)

    def is_player_near(self, player_rect, camera_x, camera_y):
        # 화면 좌표의 문 위치와 월드 좌표의 플레이어 충돌 확인
        screen_player_rect = pygame.Rect(
            player_rect.x - camera_x,
            player_rect.y - camera_y,
            player_rect.width,
            player_rect.height
        )
        return self.screen_rect.colliderect(screen_player_rect)

player = Player(100, 300)
# 문 생성
door = Door(600, 400)  # 화면 우측 고정

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move()

    # 카메라 위치 계산 (플레이어 중심으로)
    camera_x = player.rect.centerx - screen.get_width() // 2
    camera_y = player.rect.centery - screen.get_height() // 2

    # 충돌 검사
    near_door = door.is_player_near(player.rect, camera_x, camera_y)

    # 문 열기
    if near_door and keys[pygame.K_e] and not door.opened:
        door.open()
        player.rect.x -= 200  # 플레이어 왼쪽으로 이동

    # 문-플레이어 순서 (겹침 방지)

    door.draw(screen)
    player.draw(screen, camera_x, camera_y)


    # 텍스트 (화면상 좌표로 변환해서 그려야 함)
    if near_door and not door.opened:
        text = font.render("E", True, BLACK)
        text_x = player.rect.x - camera_x - 20
        text_y = player.rect.y - camera_y - 40
        
        # 텍스트 배경 사각형 크기 계산
        text_width, text_height = text.get_size()
        padding = 10
        bg_rect = pygame.Rect(
            text_x - padding // 2,
            text_y - padding // 2,
            text_width + padding,
            text_height + padding
        )

        # 반투명 배경 Surface 만들기
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
        bg_surface.set_alpha(160)  # 0=완전투명, 255=불투명
        bg_surface.fill((255, 255, 255))  # 흰색 반투명 배경

        # 배경 먼저 그리기
        screen.blit(bg_surface, (bg_rect.x + 20 , bg_rect.y))

        # 텍스트는 위에 그리기
        screen.blit(text, (text_x + 20, text_y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
