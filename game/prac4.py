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

# 전역 문 열기 쿨다운
global_door_cooldown = 0
GLOBAL_COOLDOWN_TIME = 1000  # 1초

# --- Player 클래스 ---
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = 5
        self.image = idle_img
        self.direction = "right"
        self.is_running = False
        self.is_moving = False

    def move(self, walls):
        global camera_offset  # offset을 전역 변수로 접근
        keys = pygame.key.get_pressed()
        self.is_moving = False
        self.is_running = False
        
        # 이동 전 카메라 오프셋 저장
        old_offset = camera_offset

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

        # 벽과의 충돌 검사
        for wall in walls:
            wall_rect_with_offset = wall.rect.move(-camera_offset, 0)
            if self.rect.colliderect(wall_rect_with_offset):
                # 충돌 시 이전 위치로 되돌림
                camera_offset = old_offset
                self.is_moving = False
                break

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


# --- Wall 클래스 ---
class Wall:
    def __init__(self, x, y, width, height, color=(BLACK)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen, offset_x):
        # 카메라 위치 보정
        draw_rect = self.rect.move(-offset_x, 0)
        pygame.draw.rect(screen, self.color, draw_rect)

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
    Door(600, 260, -800),    # 첫 번째 문은 100 이동
    Door(1000, 260, -1000),   # 두 번째 문은 200 이동
    Door(1400, 260, 800),   # 세 번째 문은 300 이동
    Door(2000, 260, 1000)
]

# 벽 만들기 (방의 경계)
walls = [
    Wall(0, 0, 50, 1000, (BLACK)),           # 왼쪽 벽
    Wall(2500, 0, 50, 1000, (BLACK)),        # 오른쪽 벽
    Wall(0, 0, 2550, 50, (BLACK)),           # 위쪽 벽
    Wall(0, 950, 2550, 50, (BLACK)),         # 아래쪽 벽
]


# --- 게임 루프 ---
running = True
e_key_pressed = False  # E키 눌림 상태 추적

while running:
    screen.fill(WHITE)
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                e_key_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                e_key_pressed = False

    player.move(walls)
    screen.fill(WHITE)
    
    # 벽 그리기
    for wall in walls:
        wall.draw(screen, camera_offset)
    
    # 문 상태 업데이트
    for door in doors:
        door.update()
        door.draw(screen, camera_offset)

    # 전역 쿨다운 업데이트
    current_time = pygame.time.get_ticks()
    can_open_door = current_time > global_door_cooldown

    # 문과의 충돌 검사 및 열기 (E키가 방금 눌렸을 때만)
    if e_key_pressed and can_open_door:
        for door in doors:
            door_rect_with_offset = door.closed_rect.move(-camera_offset, 0)
            near_door = player.rect.colliderect(door_rect_with_offset)

            if near_door and not door.opened:
                # 현재 문 열기
                door.open()
                camera_offset -= door.move_distance   # 각 문마다 다른 거리로 화면 이동
                
                # x - move_distance가 다른 문의 x와 같은 문들도 열기
                opened_door_target_x = door.closed_rect.x - door.move_distance
                for other_door in doors:
                    if other_door != door and other_door.closed_rect.x == opened_door_target_x:
                        other_door.open()
                
                global_door_cooldown = current_time + GLOBAL_COOLDOWN_TIME  # 전역 쿨다운 설정
                e_key_pressed = False  # E키 처리 완료 후 False로 설정
                break  # 한 번에 하나의 문만 열기
    
    # 텍스트 표시 (문 근처에 있을 때)
    for door in doors:
        door_rect_with_offset = door.closed_rect.move(-camera_offset, 0)
        near_door = player.rect.colliderect(door_rect_with_offset)
        
        if near_door and not door.opened:
            text = font.render("E", True, (255, 0, 0))
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
