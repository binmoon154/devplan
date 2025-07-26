import pygame
import sys
import os
from animation import Animation

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

# 걷기 애니메이션 이미지 불러오기
walk_right_imgs = [pygame.image.load(os.path.join(img_dir, f"walk{i}.png")).convert_alpha() for i in range(1, 5)]
walk_left_imgs = [pygame.image.load(os.path.join(img_dir, f"back_walk{i}.png")).convert_alpha() for i in range(1, 5)]
# 뛰기 이미지들
run_right_imgs = [pygame.image.load(os.path.join(img_dir, f"run{i}.png")).convert_alpha() for i in range(1, 5)]
run_left_imgs = [pygame.image.load(os.path.join(img_dir, f"back_run{i}.png")).convert_alpha() for i in range(1, 5)]


# 애니메이션 인스턴스 만들기
walk_right_anim = Animation(walk_right_imgs)
walk_left_anim = Animation(walk_left_imgs)
run_right_anim = Animation(run_right_imgs)
run_left_anim = Animation(run_left_imgs)


# --- Player 클래스 ---
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = 5
        self.image = idle_img
        self.direction = "right"
        self.is_running = False
        self.is_moving = False

        # 애니메이션 객체 연결
        self.walk_right_anim = walk_right_anim
        self.walk_left_anim = walk_left_anim

    def move(self):
        keys = pygame.key.get_pressed()
        self.is_moving = False
        self.is_running = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction = "left"
            self.is_moving = True
            if keys[pygame.K_LSHIFT]:
                self.rect.x -= self.speed * 1.4
                self.is_running = True
            else:
                self.rect.x -= self.speed

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction = "right"
            self.is_moving = True
            if keys[pygame.K_LSHIFT]:
                self.rect.x += self.speed * 1.4
                self.is_running = True
            else:
                self.rect.x += self.speed

        # 애니메이션 갱신
        if self.is_moving:
            if self.direction == "right":
                self.image = self.walk_right_anim.update()
            else:
                self.image = self.walk_left_anim.update()
        else:
            self.walk_right_anim.reset()
            self.walk_left_anim.reset()
            if self.direction == "right":
                self.image = idle_img
            else:
                self.image = back_idle_img

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# --- Door 클래스 ---
class Door:
    def __init__(self, x, y):
        self.closed_rect = pygame.Rect(x, y, 50, 80)
        self.opened = False

    def open(self):
        self.opened = True

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
        screen.blit(bg_surface, (bg_rect.x + 20 , bg_rect.y))

        # 텍스트는 위에 그리기
        screen.blit(text, (player.rect.x - 20, player.rect.y - 40))


    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
