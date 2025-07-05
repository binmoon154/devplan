import pygame
import sys
import os

# 초기화
pygame.init()
screen_width, screen_height = 1440, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("탐정 걷기 게임")
clock = pygame.time.Clock()

# 이미지 경로
img_dir = r"game-image"
bg_path = os.path.join(img_dir, "home.png")
idle_path = os.path.join(img_dir, "stop.png")
walk_right_path = os.path.join(img_dir, "walk.png")
walk_left_path = os.path.join(img_dir, "back_walk.png")
run_right_path = os.path.join(img_dir, "run.png")
run_left_path = os.path.join(img_dir, "back_run.png")
stop_left_path = os.path.join(img_dir, "back_stop.png")

# 이미지 로드
bg_img = pygame.image.load(bg_path).convert()
idle_img = pygame.image.load(idle_path).convert_alpha()
back_idle_img = pygame.image.load(stop_left_path).convert_alpha()
walk_right_img = pygame.image.load(walk_right_path).convert_alpha()
walk_left_img = pygame.image.load(walk_left_path).convert_alpha()
run_right_img = pygame.image.load(run_right_path).convert_alpha()
run_left_img = pygame.image.load(run_left_path).convert_alpha()

# 상태 초기화
scroll_x = 0
scroll_speed = 5
last_direction = "right"
current_img = idle_img

# 탐정 고정 위치
detective_x = screen_width // 2 - idle_img.get_width() // 2
detective_y = 400
last_direction = "right"
current_img = idle_img
detective_width = idle_img.get_width()
detective_height = idle_img.get_height()

# 가상의 충돌 오브젝트 예시 (예: 책상)
# background의 실제 위치 기준으로 좌표 설정 (예: 맵 내 x=1000)
#obstacle_rect = pygame.Rect(1700, 420, 120, 60)  # x, y, width, height
# 충돌 오브젝트 목록 (배경 기준 좌표)
obstacle_list = [
    {"rect": pygame.Rect(1000, 420, 120, 60), "name": "책상"},
    {"rect": pygame.Rect(1600, 420, 80, 80), "name": "서랍"},
    {"rect": pygame.Rect(500, 420, 100, 100), "name": "문"},
]

# 배경색
bg_color = (230, 230, 230)

# 게임 루프
running = True
while running:
    screen.fill(bg_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()

    # 가상 위치 갱신 (scroll_x는 배경이 이동한 만큼)
    detective_world_rect = pygame.Rect(-scroll_x + detective_x, detective_y, detective_width, detective_height)
    
    if keys[pygame.K_a]:
        last_direction = "left"
        next_rect = detective_world_rect.move(-scroll_speed, 0)
        if not any(next_rect.colliderect(obj["rect"]) for obj in obstacle_list):
            if keys[pygame.K_LSHIFT]:
                scroll_x += scroll_speed * 1.4
                current_img = run_left_img
            else  : 
                scroll_x += scroll_speed  # 왼쪽으로 가면 배경은 오른쪽으로 이동
                current_img = walk_left_img
        else:
            current_img = back_idle_img
    elif keys[pygame.K_d]:
        last_direction = "right"
        next_rect = detective_world_rect.move(scroll_speed, 0)
        if not any(next_rect.colliderect(obj["rect"]) for obj in obstacle_list):
            if keys[pygame.K_LSHIFT]:
                scroll_x -= scroll_speed * 1.4
                current_img = run_right_img
            else  : 
                scroll_x -= scroll_speed  # 오른쪽으로 가면 배경은 왼쪽으로 이동
                current_img = walk_right_img
        else: 
            current_img = idle_img
    else:
        if last_direction == "right":
            current_img = idle_img  # 아무 키도 안 눌렀을 때 서있는 이미지
        else :
            current_img = back_idle_img

    # 배경 그리기 (스크롤)
    #screen.blit(bg_img, (scroll_x, 0))

    # 추가: 배경을 반복하고 싶다면 두 배경 이어 붙이기
    #screen.blit(bg_img, (scroll_x + bg_img.get_width(), 0))
    #screen.blit(bg_img, (scroll_x - bg_img.get_width(), 0))

    # 캐릭터 그리기
    screen.blit(current_img, (detective_x, detective_y))

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
