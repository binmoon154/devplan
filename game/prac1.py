import pygame
import sys
import os

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("문 상호작용")
clock = pygame.time.Clock()

# 이미지 경로
img_dir = r"game-image"
idle_path = os.path.join(img_dir, "stop.png")
walk_right_path = os.path.join(img_dir, "walk.png")
walk_left_path = os.path.join(img_dir, "back_walk.png")
run_right_path = os.path.join(img_dir, "run.png")
run_left_path = os.path.join(img_dir, "back_run.png")
stop_left_path = os.path.join(img_dir, "back_stop.png")

# 이미지 로드
idle_img = pygame.image.load(idle_path).convert_alpha()
back_idle_img = pygame.image.load(stop_left_path).convert_alpha()
walk_right_img = pygame.image.load(walk_right_path).convert_alpha()
walk_left_img = pygame.image.load(walk_left_path).convert_alpha()
run_right_img = pygame.image.load(run_right_path).convert_alpha()
run_left_img = pygame.image.load(run_left_path).convert_alpha()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)

# --- 폰트 설정 ---
# ✅ 한글 폰트 설정 - NanumGothic 사용
font_path = './zzz/NanumGothic.ttf'  # 파일 경로
font = pygame.font.SysFont(None, 36)

# --- Player 클래스 ---
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = 5
        self.image = idle_img     # 기본 이미지는 idle
        self.direction = "right"  # 방향 기억 (오른쪽/왼쪽)
        self.is_running = False   # Shift 누르고 있나?
        self.is_moving = False    # 이동 중인지?

    def move(self):
        keys = pygame.key.get_pressed()
        self.is_moving = False
        self.is_running = False

        # ← 방향 이동
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction = "left"
            self.is_moving = True
            if keys[pygame.K_LSHIFT]:
                self.rect.x -= self.speed * 1.4
                self.is_running = True
            else:
                self.rect.x -= self.speed

        # → 방향 이동
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction = "right"
            self.is_moving = True
            if keys[pygame.K_LSHIFT]:
                self.rect.x += self.speed * 1.4
                self.is_running = True
            else:
                self.rect.x += self.speed

        # 이동 상태에 따라 이미지 선택
        if self.is_moving:
            if self.is_running:
                if self.direction == "right":
                    self.image = run_right_img
                else:
                    self.image = run_left_img
            else:
                if self.direction == "right":
                    self.image = walk_right_img
                else:
                    self.image = walk_left_img
        else:
            if self.direction == "right":
                self.image = idle_img
            else:
                self.image = back_idle_img

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# --- Door 클래스 ---
class Door:
    def __init__(self, x, y):
        self.closed_rect = pygame.Rect(x, y, 150, 240)
        self.opened = False
        self.open_time = 0         # 문이 열린 시각 (ms)
        self.cooldown = 2000       # 문이 열린 상태 유지 시간 (2초)

    def open(self):
        self.opened = True
        self.open_time = pygame.time.get_ticks()

    def update(self):
        if self.opened:
            current_time = pygame.time.get_ticks()
            if current_time - self.open_time > self.cooldown:
                self.opened = False  # 시간 지나면 다시 닫힘

    def draw(self, screen):
        if self.opened:
            pygame.draw.rect(screen, GRAY, self.closed_rect)
        else:
            pygame.draw.rect(screen, BROWN, self.closed_rect)

# 객체 생성
player = Player(100, 300)
door = Door(600, 260)

# --- 게임 루프 ---
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move()

    # 문 상태 업데이트
    door.update()

    near_door = player.rect.colliderect(door.closed_rect)

    # 문 열기
    keys = pygame.key.get_pressed()
    if near_door and keys[pygame.K_e] and not door.opened:
        door.open()
        player.rect.x -= 50  # 플레이어 왼쪽으로 이동

# 그리기 순서: 문 먼저, 플레이어 나중에!
    door.draw(screen)
    player.draw(screen)

    # 텍스트 표시
    if near_door and not door.opened:
        text = font.render("E", True, BLACK)
        text_x = player.rect.x - 40
        text_y = player.rect.y - 40

    #텍스트 배경 사각형 크기 계산
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
        screen.blit(bg_surface, (bg_rect.x + 40 , bg_rect.y + 30))

        # 텍스트는 위에 그리기
        screen.blit(text, (player.rect.x, player.rect.y - 10))


    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
