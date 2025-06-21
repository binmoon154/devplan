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

# 탐정 상태
detective_x = 400
detective_y = 400
detective_speed = 5
last_direction = "right" #초기 방향
current_img = idle_img

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
    #print(f"keys:{keys}")
    
    if keys[pygame.K_a]:
        #keys[pygame.K_a] = 1
        last_direction = "left"
        #print(f"pygame.K_a:{keys[pygame.K_a]}")
        if keys[pygame.K_LSHIFT]:
            detective_x -= detective_speed * 1.4
            current_img = run_left_img
        else  : 
            detective_x -= detective_speed
            current_img = walk_left_img
    elif keys[pygame.K_d]:
        #keys[pygame.K_d] = 0
        last_direction = "right"
        #print(f"pygame.K_d:{keys[pygame.K_d]}")
        if keys[pygame.K_LSHIFT]:
            detective_x += detective_speed * 1.4
            current_img = run_right_img
        else  : 
            detective_x += detective_speed
            current_img = walk_right_img
    else:
        if last_direction == "right":
            current_img = idle_img  # 아무 키도 안 눌렀을 때 서있는 이미지
        else :
            current_img = back_idle_img

    # 캐릭터 그리기
    screen.blit(current_img, (detective_x, detective_y))

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
