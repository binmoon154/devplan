import pygame
import sys
import os

# 상위 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings_manager import SettingsManager

pygame.init()

settings_manager = SettingsManager()
SCREEN_WIDTH, SCREEN_HEIGHT = settings_manager.get_screen_size()
VOLUME = settings_manager.get_volume()
SOUND_ENABLED = settings_manager.is_sound_enabled()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("문 상호작용")
clock = pygame.time.Clock()

pygame.mixer.init()
if SOUND_ENABLED:
    pygame.mixer.set_num_channels(8)
    master_volume = VOLUME
else:
    master_volume = 0.0

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
font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'NanumGothic.ttf')
try:
    font = pygame.font.Font(font_path, 36)
except:
    font = pygame.font.Font(None, 36)  # 폴백 폰트

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


# --- Timer 클래스 ---
class Timer:
    def __init__(self, x, y, initial_time=90, font_size=48):
        self.x = x
        self.y = y
        self.current_time = initial_time
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.SysFont(None, font_size)
        self.is_running = True
        
    def update(self):
        if self.is_running:
            current_ticks = pygame.time.get_ticks()
            elapsed_time = (current_ticks - self.start_time) // 1000
            
            if elapsed_time >= 1:  # 1초가 지났으면
                self.current_time = max(0, self.current_time - elapsed_time)
                self.start_time = current_ticks
                
                if self.current_time <= 0:
                    self.is_running = False
    
    def add_time(self, seconds):
        self.current_time += seconds
        
    def subtract_time(self, seconds):
        self.current_time = max(0, self.current_time - seconds)
        
    def draw(self, screen):
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        time_text = f"{minutes:02d}:{seconds:02d}"
        
        # 시간이 적으면 빨간색, 많으면 흰색
        color = (255, 0, 0) if self.current_time <= 30 else WHITE
        
        text_surface = self.font.render(time_text, True, color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        
        # 배경 사각형
        bg_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(screen, BLACK, bg_rect)
        pygame.draw.rect(screen, WHITE, bg_rect, 2)
        
        screen.blit(text_surface, text_rect)
        
    def is_time_up(self):
        return self.current_time <= 0

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

# --- 표지판/편지 클래스 ---
class Readable:
    def __init__(self, x, y, width, height, text, title="", readable_type="sign"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.title = title
        self.type = readable_type  # "sign" (표지판) 또는 "letter" (편지)
        self.color = (101, 67, 33) if readable_type == "sign" else (240, 240, 220)  # 갈색 또는 연한 황색
        self.border_color = (60, 40, 20) if readable_type == "sign" else (200, 200, 180)
        
    def draw(self, screen, offset_x):
        # 카메라 위치 보정
        draw_rect = self.rect.move(-offset_x, 0)
        
        # 메인 배경
        pygame.draw.rect(screen, self.color, draw_rect)
        pygame.draw.rect(screen, self.border_color, draw_rect, 3)
        
        # 타입별 시각적 구분
        if self.type == "sign":
            # 표지판 - 나무 기둥 표현
            pole_rect = pygame.Rect(draw_rect.centerx - 5, draw_rect.bottom, 10, 30)
            pygame.draw.rect(screen, (101, 67, 33), pole_rect)
        else:
            # 편지 - 접힌 모서리 표현
            corner_size = 15
            corner_points = [
                (draw_rect.right - corner_size, draw_rect.top),
                (draw_rect.right, draw_rect.top + corner_size),
                (draw_rect.right - corner_size, draw_rect.top + corner_size)
            ]
            pygame.draw.polygon(screen, self.border_color, corner_points)

# --- 텍스트 읽기 모드 클래스 ---
class TextReader:
    def __init__(self):
        self.is_reading = False
        self.current_readable = None
        self.font_title = None
        self.font_text = None
        try:
            font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'NanumGothic.ttf')
            self.font_title = pygame.font.Font(font_path, 48)
            self.font_text = pygame.font.Font(font_path, 24)
        except:
            self.font_title = pygame.font.Font(None, 48)
            self.font_text = pygame.font.Font(None, 24)
    
    def start_reading(self, readable):
        self.is_reading = True
        self.current_readable = readable
    
    def stop_reading(self):
        self.is_reading = False
        self.current_readable = None
    
    def draw(self, screen):
        if not self.is_reading or not self.current_readable:
            return
        
        # 반투명 배경
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # 텍스트 배경 박스
        box_width = SCREEN_WIDTH - 200
        box_height = SCREEN_HEIGHT - 200
        box_x = 100
        box_y = 100
        
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, (240, 235, 220), box_rect)
        pygame.draw.rect(screen, (100, 100, 100), box_rect, 5)
        
        # 제목 표시
        if self.current_readable.title:
            title_surface = self.font_title.render(self.current_readable.title, True, (50, 50, 50))
            title_rect = title_surface.get_rect(centerx=box_x + box_width // 2, y=box_y + 30)
            screen.blit(title_surface, title_rect)
            text_start_y = box_y + 100
        else:
            text_start_y = box_y + 50
        
        # 텍스트 줄바꿈 처리
        words = self.current_readable.text.split()
        lines = []
        current_line = []
        max_width = box_width - 60
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            text_surface = self.font_text.render(test_line, True, (50, 50, 50))
            if text_surface.get_width() > max_width and current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # 텍스트 표시
        for i, line in enumerate(lines):
            if text_start_y + (i * 35) > box_y + box_height - 80:
                break  # 박스를 벗어나면 중단
            text_surface = self.font_text.render(line, True, (50, 50, 50))
            screen.blit(text_surface, (box_x + 30, text_start_y + (i * 35)))
        
        # 하단 안내 메시지
        instruction = self.font_text.render("E키를 눌러 나가기", True, (100, 100, 100))
        instruction_rect = instruction.get_rect(centerx=box_x + box_width // 2, y=box_y + box_height - 40)
        screen.blit(instruction, instruction_rect)


# 객체 생성
player = Player(SCREEN_WIDTH // 2 - 25, 300)

# 여러 개의 문 만들기
doors = [
    Door(600, 260, -800),    # 첫 번째 문은 100 이동
    Door(1000, 260, -1000),   # 두 번째 문은 200 이동
    Door(1400, 260, 800),   # 세 번째 문은 300 이동
    Door(2000, 260, 1000)
]

# 벽 만들기 (방의 경계)
walls = [
    Wall(0, 0, 50, SCREEN_HEIGHT, (BLACK)),           # 왼쪽 벽
    Wall(2500, 0, 50, SCREEN_HEIGHT, (BLACK)),        # 오른쪽 벽
    Wall(0, 0, 2550, 50, (BLACK)),           # 위쪽 벽
    Wall(0, SCREEN_HEIGHT - 50, 2550, 50, (BLACK)),         # 아래쪽 벽
]

# 타이머 생성 (화면 상단 중앙에 위치, 90초로 시작)
timer = Timer(SCREEN_WIDTH // 2, 100, initial_time=90)

# 표지판/편지 만들기
readables = [
    Readable(800, 300, 80, 120, 
             "여기는 탈출 게임입니다. 문을 열어 탈출하세요! E키를 눌러 문과 상호작용할 수 있습니다. 시간이 부족하니 서둘러야 합니다.",
             "게임 안내", "sign"),
    Readable(1800, 280, 80, 120,
             "출구까지 거의 다 왔습니다! 마지막 문을 열면 탈출할 수 있습니다. 지금까지 수고하셨습니다.",
             "출구 안내", "sign"),
]

# 텍스트 읽기 시스템
text_reader = TextReader()

# --- 게임 오버 화면 클래스 ---
class GameOverScreen:
    def __init__(self):
        self.font_title = None
        self.font_text = None
        try:
            font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'NanumGothic.ttf')
            self.font_title = pygame.font.Font(font_path, 72)
            self.font_text = pygame.font.Font(font_path, 36)
        except:
            self.font_title = pygame.font.Font(None, 72)
            self.font_text = pygame.font.Font(None, 36)
    
    def draw(self, screen):
        # 반투명 배경
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # 게임 오버 텍스트
        game_over_text = self.font_title.render("게임 오버", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(game_over_text, game_over_rect)
        
        # 시간 초과 메시지
        time_up_text = self.font_text.render("시간이 다 지났습니다!", True, (255, 255, 255))
        time_up_rect = time_up_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        screen.blit(time_up_text, time_up_rect)
        
        # 안내 메시지
        instruction_text = self.font_text.render("3초 후 메인 메뉴로 돌아갑니다...", True, (200, 200, 200))
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(instruction_text, instruction_rect)

# 게임 오버 스크린 초기화
game_over_screen = GameOverScreen()
game_over_start_time = None
game_state = "playing"  # "playing", "game_over", "returning"

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
            if event.key == pygame.K_e and game_state == "playing":
                if text_reader.is_reading:
                    # 텍스트 읽기 모드에서 나가기
                    text_reader.stop_reading()
                else:
                    e_key_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_e and not text_reader.is_reading and game_state == "playing":
                e_key_pressed = False

    # 게임 상태별 처리
    if game_state == "playing":
        player.move(walls)
        screen.fill(WHITE)
        
        # 타이머 업데이트
        timer.update()
        
        # 타이머 만료 체크
        if timer.is_time_up():
            game_state = "game_over"
            game_over_start_time = pygame.time.get_ticks()
    
    elif game_state == "game_over":
        # 게임 오버 상태에서 3초 후 메인 메뉴로 돌아가기
        current_time = pygame.time.get_ticks()
        if current_time - game_over_start_time > 3000:  # 3초 후
            pygame.quit()
            import subprocess
            import sys
            subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main_menu.py")])
            sys.exit()
    
    # 게임 플레이 화면 그리기 (게임 오버 상태가 아닐 때만)
    if game_state == "playing":
        # 벽 그리기
        for wall in walls:
            wall.draw(screen, camera_offset)
        
        # 문 상태 업데이트
        for door in doors:
            door.update()
            door.draw(screen, camera_offset)
        
        # 타이머 그리기 (항상 고정 위치)
        timer.draw(screen)

        # 전역 쿨다운 업데이트
        current_time = pygame.time.get_ticks()
        can_open_door = current_time > global_door_cooldown

        # 상호작용 시스템 (E키 처리)
        if e_key_pressed and can_open_door and not text_reader.is_reading:
            interaction_handled = False
            
            # 표지판/편지와의 상호작용 확인
            for readable in readables:
                readable_rect_with_offset = readable.rect.move(-camera_offset, 0)
                near_readable = player.rect.colliderect(readable_rect_with_offset)
                
                if near_readable:
                    text_reader.start_reading(readable)
                    e_key_pressed = False
                    interaction_handled = True
                    break
            
            # 문과의 상호작용 확인 (표지판 상호작용이 없을 때만)
            if not interaction_handled:
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
    
        # 표지판/편지 그리기
        for readable in readables:
            readable.draw(screen, camera_offset)
        
        # 상호작용 가능한 오브젝트 근처에서 E키 안내 표시
        if not text_reader.is_reading:
            # 문 근처에서 E키 표시
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
                    break
        
            # 표지판/편지 근처에서 E키 표시
            for readable in readables:
                readable_rect_with_offset = readable.rect.move(-camera_offset, 0)
                near_readable = player.rect.colliderect(readable_rect_with_offset)
                
                if near_readable:
                    text = font.render("E", True, (0, 150, 0))
                    text_x = player.rect.x - 40
                    text_y = player.rect.y - 60

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
                    bg_surface.set_alpha(160)
                    bg_surface.fill((255, 255, 255))

                    # 배경 먼저 그리기
                    screen.blit(bg_surface, (bg_rect.x + 40 , bg_rect.y + 30))

                    # 텍스트는 위에 그리기
                    screen.blit(text, (player.rect.x, player.rect.y - 30))
                    break

        # 그리기 순서: 문 먼저, 플레이어 나중에!
        player.draw(screen)
        
        # 텍스트 읽기 UI (가장 마지막에 그리기)
        text_reader.draw(screen)
    
    # 게임 오버 화면 그리기
    elif game_state == "game_over":
        game_over_screen.draw(screen)
     
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
