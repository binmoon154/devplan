import pygame
import sys
import math
from settings_manager import SettingsManager

pygame.init()

BACKGROUND_COLOR = (50, 50, 70)
TITLE_COLOR = (255, 255, 255)
BUTTON_COLOR = (80, 120, 200)
BUTTON_HOVER_COLOR = (100, 140, 220)
BUTTON_TEXT_COLOR = (255, 255, 255)
SLIDER_COLOR = (120, 120, 120)
SLIDER_HANDLE_COLOR = (200, 200, 200)
SLIDER_HANDLE_HOVER = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.dragging = False
        self.handle_radius = height // 2 + 2
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_x = self.rect.x + (self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.width
            handle_pos = pygame.Rect(handle_x - self.handle_radius, self.rect.y - 2, 
                                   self.handle_radius * 2, self.rect.height + 4)
            if handle_pos.collidepoint(event.pos):
                self.dragging = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                relative_x = event.pos[0] - self.rect.x
                relative_x = max(0, min(self.rect.width, relative_x))
                self.val = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)
                return True
        return False
    
    def draw(self, surface, font):
        pygame.draw.rect(surface, SLIDER_COLOR, self.rect)
        
        handle_x = self.rect.x + (self.val - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        handle_color = SLIDER_HANDLE_HOVER if self.dragging else SLIDER_HANDLE_COLOR
        pygame.draw.circle(surface, handle_color, (int(handle_x), self.rect.centery), self.handle_radius)
        
        label_text = font.render(f"{self.label}: {self.val:.2f}", True, TEXT_COLOR)
        surface.blit(label_text, (self.rect.x, self.rect.y - 30))

class SettingsButton:
    def __init__(self, x, y, width, height, text, values, current_index=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.values = values
        self.current_index = current_index
        self.is_hovered = False
        self.corner_radius = 10
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.current_index = (self.current_index + 1) % len(self.values)
                return True
        return False
    
    def get_current_value(self):
        return self.values[self.current_index]
    
    def set_value(self, value):
        if value in self.values:
            self.current_index = self.values.index(value)
    
    def draw(self, surface, font):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=self.corner_radius)
        
        display_text = f"{self.text}: {self.values[self.current_index]}"
        text_surface = font.render(display_text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class RoundedButton:
    def __init__(self, x, y, width, height, text, icon_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon_text = icon_text
        self.is_hovered = False
        self.corner_radius = 15
        
    def draw(self, surface, font):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=self.corner_radius)
        
        if self.icon_text:
            icon_surface = font.render(self.icon_text, True, BUTTON_TEXT_COLOR)
            text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
            
            total_width = icon_surface.get_width() + text_surface.get_width() + 20
            start_x = self.rect.centerx - total_width // 2
            
            icon_y = self.rect.centery - icon_surface.get_height() // 2
            text_y = self.rect.centery - text_surface.get_height() // 2
            
            surface.blit(icon_surface, (start_x, icon_y))
            surface.blit(text_surface, (start_x + icon_surface.get_width() + 20, text_y))
        else:
            text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def run_settings_screen():
    settings_manager = SettingsManager()
    
    current_width, current_height = settings_manager.get_screen_size()
    screen = pygame.display.set_mode((current_width, current_height))
    pygame.display.set_caption("문을 열다 - 설정")
    clock = pygame.time.Clock()
    
    try:
        font_title = pygame.font.Font("NanumGothic.ttf", 60)
        font_normal = pygame.font.Font("NanumGothic.ttf", 28)
        font_button = pygame.font.Font("NanumGothic.ttf", 32)
    except:
        font_title = pygame.font.Font(None, 60)
        font_normal = pygame.font.Font(None, 28)
        font_button = pygame.font.Font(None, 32)
    
    title_text = font_title.render("설정", True, TITLE_COLOR)
    title_rect = title_text.get_rect(center=(current_width // 2, 100))
    
    screen_size_options = [
        (1280, 720),
        (1440, 1080), 
        (1920, 1080),
        (2560, 1440)
    ]
    
    screen_size_labels = ["1280x720", "1440x1080", "1920x1080", "2560x1440"]
    current_size = (current_width, current_height)
    current_index = 0 if current_size not in screen_size_options else screen_size_options.index(current_size)
    
    screen_size_button = SettingsButton(
        current_width // 2 - 200, 250, 400, 60,
        "화면 크기", screen_size_labels, current_index
    )
    
    volume_slider = Slider(
        current_width // 2 - 200, 380, 400, 20,
        0.0, 1.0, settings_manager.get_volume(), "소리 크기"
    )
    
    sound_enabled = settings_manager.is_sound_enabled()
    sound_button = SettingsButton(
        current_width // 2 - 200, 480, 400, 60,
        "소리", ["켜짐", "꺼짐"], 0 if sound_enabled else 1
    )
    
    back_button = RoundedButton(
        current_width // 2 - 100, current_height - 150, 200, 60, 
        "뒤로가기", "←"
    )
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings_manager.save_settings()
                pygame.quit()
                sys.exit()
            
            if screen_size_button.handle_event(event):
                selected_size = screen_size_options[screen_size_button.current_index]
                settings_manager.set_setting("screen_width", selected_size[0])
                settings_manager.set_setting("screen_height", selected_size[1])
                
                screen = pygame.display.set_mode(selected_size)
                current_width, current_height = selected_size
                
                title_rect = title_text.get_rect(center=(current_width // 2, 100))
                screen_size_button.rect.x = current_width // 2 - 200
                volume_slider.rect.x = current_width // 2 - 200
                sound_button.rect.x = current_width // 2 - 200
                back_button.rect.x = current_width // 2 - 100
                back_button.rect.y = current_height - 150
            
            if volume_slider.handle_event(event):
                settings_manager.set_setting("volume", volume_slider.val)
            
            if sound_button.handle_event(event):
                sound_enabled = sound_button.get_current_value() == "켜짐"
                settings_manager.set_setting("sound_enabled", sound_enabled)
            
            if back_button.handle_event(event):
                settings_manager.save_settings()
                return "main_menu"
        
        screen.fill(BACKGROUND_COLOR)
        
        screen.blit(title_text, title_rect)
        
        screen_size_button.draw(screen, font_button)
        volume_slider.draw(screen, font_normal)
        sound_button.draw(screen, font_button)
        back_button.draw(screen, font_button)
        
        pygame.display.flip()
        clock.tick(60)