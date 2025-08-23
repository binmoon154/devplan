import pygame
import sys
import os
from settings_manager import SettingsManager
from settings_screen import run_settings_screen

pygame.init()

BACKGROUND_COLOR = (50, 50, 70)
TITLE_COLOR = (255, 255, 255)
BUTTON_COLOR = (80, 120, 200)
BUTTON_HOVER_COLOR = (100, 140, 220)
BUTTON_TEXT_COLOR = (255, 255, 255)

settings_manager = SettingsManager()
SCREEN_WIDTH, SCREEN_HEIGHT = settings_manager.get_screen_size()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("문을 열다 - 메인 메뉴")
clock = pygame.time.Clock()

try:
    font_large = pygame.font.Font("NanumGothic.ttf", 80)
    font_button = pygame.font.Font("NanumGothic.ttf", 36)
except:
    font_large = pygame.font.Font(None, 80)
    font_button = pygame.font.Font(None, 36)

class RoundedButton:
    def __init__(self, x, y, width, height, text, icon_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon_text = icon_text
        self.is_hovered = False
        self.corner_radius = 15
        
    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=self.corner_radius)
        
        icon_surface = font_button.render(self.icon_text, True, BUTTON_TEXT_COLOR)
        text_surface = font_button.render(self.text, True, BUTTON_TEXT_COLOR)
        
        total_width = icon_surface.get_width() + text_surface.get_width() + 20
        start_x = self.rect.centerx - total_width // 2
        
        icon_y = self.rect.centery - icon_surface.get_height() // 2
        text_y = self.rect.centery - text_surface.get_height() // 2
        
        surface.blit(icon_surface, (start_x, icon_y))
        surface.blit(text_surface, (start_x + icon_surface.get_width() + 20, text_y))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def run_main_menu():
    global settings_manager, SCREEN_WIDTH, SCREEN_HEIGHT, screen
    title_text = font_large.render("문을 열다", True, TITLE_COLOR)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
    
    settings_button = RoundedButton(
        SCREEN_WIDTH // 2 - 200, 500, 400, 80, "설정", "⚙"
    )
    
    gameplay_button = RoundedButton(
        SCREEN_WIDTH // 2 - 200, 620, 400, 80, "게임플레이", "🏃"
    )
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if settings_button.handle_event(event):
                result = run_settings_screen()
                if result == "main_menu":
                    settings_manager = SettingsManager()
                    SCREEN_WIDTH, SCREEN_HEIGHT = settings_manager.get_screen_size()
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
                    settings_button.rect.x = SCREEN_WIDTH // 2 - 200
                    gameplay_button.rect.x = SCREEN_WIDTH // 2 - 200
            
            if gameplay_button.handle_event(event):
                print("게임플레이 버튼 클릭됨")
                return "start_game"
        
        screen.fill(BACKGROUND_COLOR)
        
        screen.blit(title_text, title_rect)
        
        settings_button.draw(screen)
        gameplay_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

def run_game():
    pygame.quit()
    import subprocess
    import sys
    import os
    
    # 현재 스크립트의 디렉토리를 기준으로 prac3.py 실행
    current_dir = os.path.dirname(os.path.abspath(__file__))
    game_script = os.path.join(current_dir, "game", "prac3.py")
    
    # Python path에 현재 디렉토리 추가
    env = os.environ.copy()
    if 'PYTHONPATH' in env:
        env['PYTHONPATH'] = current_dir + os.pathsep + env['PYTHONPATH']
    else:
        env['PYTHONPATH'] = current_dir
    
    subprocess.run([sys.executable, game_script], cwd=current_dir, env=env)

if __name__ == "__main__":
    result = run_main_menu()
    if result == "start_game":
        run_game()