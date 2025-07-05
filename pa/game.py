from background import Background 
from  player import Player
import image
import os
import sys 
import pygame


pygame.init()
screen_width, screen_height = 1440, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("탐정 걷기 게임")
clock = pygame.time.Clock()

n = input('이름 입력 필요:')
width, height = idle_img.get_width(), idle_img.get_height()        
searcher = Player(n, width, height)

# 탐정 고정 위치
searcher.detective_x = screen_width // 2 - idle_img.get_width() // 2
searcher.detective_y = 400
searcher.last_direction = "right"
searcher.current_img = idle_img

