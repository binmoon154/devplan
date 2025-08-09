import pygame
import sys
import os

pygame.init()
screen = pygame.display.set_mode((1440, 1000))
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

camera_offset = 0

# --- Player 클래스 ---
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = 5
        self.image = idle_img
        self.direction = "right"
        self.is_running = False
        self.is_moving = False

    def move(self):
        global camera_offset  # offset을 전역 변수로 접근
        keys = pygame.key.get_pressed()
        self.is_moving = False
        self.is_running = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction = "left"
            self.is_moving = True
            if keys[pygame.K_LSHIFT]:
                camera_offset -= self.speed * 1.4
                self.is_running = True
            else:
                camera_offset -= self.speed

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction = "right"
            self.is_moving = True
            if keys[pygame.K_LSHIFT]:
                camera_offset += self.speed * 1.4
                self.is_running = True
            else:
                camera_offset += self.speed

        # 이미지 설정은 그대로
        if self.is_moving:
            if self.is_running:
                self.image = run_right_img if self.direction == "right" else run_left_img
            else:
                self.image = walk_right_img if self.direction == "right" else walk_left_img
        else:
            self.image = idle_img if self.direction == "right" else back_idle_img

    def draw(self, screen):
        # 항상 중앙에 그리기
        screen.blit(self.image, self.rect)


# --- Door 클래스 ---
class Door:
    def __init__(self, x, y, move_distance):
        self.closed_rect = pygame.Rect(x, y, 150, 240)
        self.opened = False
        self.open_time = 0
        self.cooldown = 2000
        self.move_distance = move_distance  # 문마다 이동 거리 다르게 설정

    def open(self):
        self.opened = True
        self.open_time = pygame.time.get_ticks()

    def update(self):
        if self.opened:
            current_time = pygame.time.get_ticks()
            if current_time - self.open_time > self.cooldown:
                self.opened = False

    def draw(self, screen, offset_x):
        # 카메라 위치 보정
        draw_rect = self.closed_rect.move(-offset_x, 0)
        color = GRAY if self.opened else BROWN
        pygame.draw.rect(screen, color, draw_rect)


# 객체 생성
player = Player(1440 // 2 - 25, 300)
# 여러 개의 문 만들기
doors = [
    Door(600, 260, 100),    # 첫 번째 문은 100 이동
    Door(1000, 260, 200),   # 두 번째 문은 200 이동
    Door(1400, 260, 300),   # 세 번째 문은 300 이동
]


# --- 게임 루프 ---
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move()
    screen.fill(WHITE)
    # 문 상태 업데이트
    for door in doors:
        door.update()
        door.draw(screen, camera_offset)

    # 문과의 충돌 검사 및 열기
    keys = pygame.key.get_pressed()
    # 문 위치를 카메라 기준으로 보정해서 충돌 검사
    for door in doors:
        door_rect_with_offset = door.closed_rect.move(-camera_offset, 0)
        near_door = player.rect.colliderect(door_rect_with_offset)

        if near_door and keys[pygame.K_e] and not door.opened:
            door.open()
            camera_offset -= 50   # 화면을 이동시켜 플레이어가 이동한 것처럼 보임
        
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

# 그리기 순서: 문 먼저, 플레이어 나중에!
    player.draw(screen)
     
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
