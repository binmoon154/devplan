# Update(game\prac3.py)
#  ⎿  Updated game\prac3.py with 184 additions and 29 removals
        33    # --- 폰트 설정 ---
        34    # ✅ 한글 폰트 설정 - NanumGothic 사용
        35    font_path = './zzz/NanumGothic.ttf'  # 파일 경로
        36 -  font = pygame.font.SysFont(None, 36)
        36 +  font = pygame.font.Font(font_path, 36)
        37    
        38    camera_offset = 0
        39    
        40 +  # --- 아이템 클래스 ---
        41 +  class Item:
        42 +      def __init__(self, x, y, name):
        43 +          self.rect = pygame.Rect(x, y, 30, 30)
        44 +          self.name = name
        45 +          self.picked_up = False
        46 +  
        47 +      def draw(self, screen, offset_x):
        48 +          if not self.picked_up:
        49 +              draw_rect = self.rect.move(-offset_x, 0)
        50 +              pygame.draw.rect(screen, BLUE, draw_rect)
        51 +  
        52 +  # --- 인벤토리 클래스 ---
        53 +  class Inventory:
        54 +      def __init__(self):
        55 +          self.items = []
        56 +          self.max_items = 5
        57 +          self.is_open = False
        58 +          self.item_pickup_text = ""
        59 +          self.pickup_text_timer = 0
        60 +          self.pickup_text_duration = 2000  # 2초
        61 +  
        62 +      def add_item(self, item):
        63 +          if len(self.items) < self.max_items:
        64 +              self.items.append(item)
        65 +              self.item_pickup_text = item.name
        66 +              self.pickup_text_timer = pygame.time.get_ticks()
        67 +              return True
        68 +          return False
        69 +  
        70 +      def toggle(self):
        71 +          self.is_open = not self.is_open
        72 +  
        73 +      def draw(self, screen, player_pos):
        74 +          # 아이템 획득 텍스트 표시
        75 +          if self.item_pickup_text:
        76 +              current_time = pygame.time.get_ticks()
        77 +              if current_time - self.pickup_text_timer < self.pickup_text_duration:
        78 +                  text = font.render(self.item_pickup_text, True, BLACK)
        79 +                  text_x = player_pos[0] - text.get_width() // 2
        80 +                  text_y = player_pos[1] - 60
        81 +
        82 +                  # 텍스트 배경 사각형
        83 +                  text_width, text_height = text.get_size()
        84 +                  padding = 10
        85 +                  bg_rect = pygame.Rect(
        86 +                      text_x - padding // 2,
        87 +                      text_y - padding // 2,
        88 +                      text_width + padding,
        89 +                      text_height + padding
        90 +                  )
        91 +
        92 +                  # 반투명 배경
        93 +                  bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
        94 +                  bg_surface.set_alpha(160)
        95 +                  bg_surface.fill((255, 255, 255))
        96 +
        97 +                  screen.blit(bg_surface, (bg_rect.x, bg_rect.y))
        98 +                  screen.blit(text, (text_x, text_y))
        99 +              else:
       100 +                  self.item_pickup_text = ""
       101 +
       102 +          # 인벤토리 UI 표시
       103 +          if self.is_open:
       104 +              # 인벤토리 배경
       105 +              inv_width = 250
       106 +              inv_height = 100
       107 +              inv_x = screen.get_width() // 2 - inv_width // 2
       108 +              inv_y = 50
       109 +
       110 +              # 반투명 배경
       111 +              inv_bg = pygame.Surface((inv_width, inv_height))
       112 +              inv_bg.set_alpha(200)
       113 +              inv_bg.fill((50, 50, 50))
       114 +              screen.blit(inv_bg, (inv_x, inv_y))
       115 +
       116 +              # 테두리
       117 +              pygame.draw.rect(screen, WHITE, (inv_x, inv_y, inv_width, inv_height), 2)
       118 +
       119 +              # 제목
       120 +              title_text = font.render("인벤토리", True, WHITE)
       121 +              screen.blit(title_text, (inv_x + 10, inv_y + 10))
       122 +
       123 +              # 아이템 슬롯 그리기
       124 +              slot_size = 30
       125 +              slot_margin = 5
       126 +              start_x = inv_x + 10
       127 +              start_y = inv_y + 50
       128 +
       129 +              for i in range(self.max_items):
       130 +                  slot_x = start_x + (slot_size + slot_margin) * i
       131 +                  slot_rect = pygame.Rect(slot_x, start_y, slot_size, slot_size)
       132 +
       133 +                  # 슬롯 배경
       134 +                  pygame.draw.rect(screen, GRAY, slot_rect)
       135 +                  pygame.draw.rect(screen, WHITE, slot_rect, 1)
       136 +
       137 +                  # 아이템이 있으면 표시
       138 +                  if i < len(self.items):
       139 +                      pygame.draw.rect(screen, BLUE, slot_rect.inflate(-4, -4))
       140 +  
       141    # --- Player 클래스 ---
       142    class Player:
       143        def __init__(self, x, y):
     ...
       46            self.direction = "right"
       47            self.is_running = False
       48            self.is_moving = False
       49 +          self.inventory = Inventory()
       50    
       51        def move(self):
       52            global camera_offset  # offset을 전역 변수로 접근
     ...
       120        Door(1400, 260, 300),   # 세 번째 문은 300 이동
       121    ]
       122    
       123 +  # 아이템 생성
       124 +  items = [
       125 +      Item(800, 350, "파란색 네모"),
       126 +      Item(1200, 350, "파란색 네모"),
       127 +      Item(1600, 350, "파란색 네모")
       128 +  ]
       129    
       130 +  
       131    # --- 게임 루프 ---
       132    running = True
       133    while running:
     ...
       129        for event in pygame.event.get():
       130            if event.type == pygame.QUIT:
       131                running = False
       132 +          elif event.type == pygame.KEYDOWN:
       133 +              if event.key == pygame.K_m:
       134 +                  player.inventory.toggle()
       135    
       136        player.move()
       137        screen.fill(WHITE)
     ...
       136        for door in doors:
       137            door.update()
       138            door.draw(screen, camera_offset)
       139 +      
       140 +      # 아이템 그리기
       141 +      for item in items:
       142 +          item.draw(screen, camera_offset)
       143    
       144        # 문과의 충돌 검사 및 열기
       145        keys = pygame.key.get_pressed()
       146        # 문 위치를 카메라 기준으로 보정해서 충돌 검사
       147 +      near_any_door = False
       148        for door in doors:
       149            door_rect_with_offset = door.closed_rect.move(-camera_offset, 0)
       150            near_door = player.rect.colliderect(door_rect_with_offset)
       151 -  
       152 -          if near_door and keys[pygame.K_e] and not door.opened:
       153 -              door.open()
       154 -              camera_offset -= 50   # 화면을 이동시켜 플레이어가 이동한 것처럼 보임
       151 
       152 -          # 텍스트 표시
       153 -          if near_door and not door.opened:
       154 -              text = font.render("E", True, BLACK)
       155 -              text_x = player.rect.x - 40
       156 -              text_y = player.rect.y - 40
       152 +          if near_door:
       153 +              near_any_door = True
       154 +              if keys[pygame.K_e] and not door.opened:
       155 +                  door.open()
       156 +                  camera_offset -= 50   # 화면을 이동시켜 플레이어가 이동한 것처럼 보임
       157 +
       158 +              # 텍스트 표시
       159 +              if not door.opened:
       160 +                  text = font.render("E", True, BLACK)
       161 +                  text_x = player.rect.x - 40
       162 +                  text_y = player.rect.y - 40
       163    
       164 -              #텍스트 배경 사각형 크기 계산
       165 -              text_width, text_height = text.get_size()
       166 -              padding = 10
       167 -              bg_rect = pygame.Rect(
       168 -                  text_x - padding // 2,
       169 -                  text_y - padding // 2,
       170 -                  text_width + padding,
       171 -                  text_height + padding
       172 -              )
       164 +                  #텍스트 배경 사각형 크기 계산
       165 +                  text_width, text_height = text.get_size()
       166 +                  padding = 10
       167 +                  bg_rect = pygame.Rect(
       168 +                      text_x - padding // 2,
       169 +                      text_y - padding // 2,
       170 +                      text_width + padding,
       171 +                      text_height + padding
       172 +                  )
       173    
       174 -              # 반투명 배경 Surface 만들기
       175 -              bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
       176 -              bg_surface.set_alpha(160)  # 0=완전투명, 255=불투명
       177 -              bg_surface.fill((255, 255, 255))  # 흰색 반투명 배경
       174 +                  # 반투명 배경 Surface 만들기
       175 +                  bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
       176 +                  bg_surface.set_alpha(160)  # 0=완전투명, 255=불투명
       177 +                  bg_surface.fill((255, 255, 255))  # 흰색 반투명 배경
       178 +
       179 +                  # 배경 먼저 그리기
       180 +                  screen.blit(bg_surface, (bg_rect.x + 40 , bg_rect.y + 30))
       181 +                  # 텍스트는 위에 그리기
       182 +                  screen.blit(text, (player.rect.x, player.rect.y - 10))
       183 +      
       184 +      # 아이템과의 충돌 검사 및 줍기
       185 +      if not near_any_door:  # 문 근처가 아닐 때만 아이템 줍기 가능
       186 +          for item in items:
       187 +              if not item.picked_up:
       188 +                  item_rect_with_offset = item.rect.move(-camera_offset, 0)
       189 +                  near_item = player.rect.colliderect(item_rect_with_offset)
       190 +
       191 +                  if near_item:
       192 +                      if keys[pygame.K_e]:
       193 +                          if player.inventory.add_item(item):
       194 +                              item.picked_up = True
       195 +
       196 +                      # E키 힌트 표시
       197 +                      text = font.render("E", True, BLACK)
       198 +                      text_x = player.rect.x - 40
       199 +                      text_y = player.rect.y - 40
       200    
       201 -  # 그리기 순서: 문 먼저, 플레이어 나중에!
       201 +                      text_width, text_height = text.get_size()
       202 +                      padding = 10
       203 +                      bg_rect = pygame.Rect(
       204 +                          text_x - padding // 2,
       205 +                          text_y - padding // 2,
       206 +                          text_width + padding,
       207 +                          text_height + padding
       208 +                      )
       209 +  
       210 +                      bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
       211 +                      bg_surface.set_alpha(160)
       212 +                      bg_surface.fill((255, 255, 255))
       213 +
       214 +                      screen.blit(bg_surface, (bg_rect.x + 40 , bg_rect.y + 30))
       215 +                      screen.blit(text, (player.rect.x, player.rect.y - 10))
       216 +                      break  # 하나의 아이템만 상호작용
       217 +  
       218 +      # 그리기 순서: 문 먼저, 플레이어 나중에!
       219        player.draw(screen)
       220        
       221 -       # 배경 먼저 그리기
       222 -      screen.blit(bg_surface, (bg_rect.x + 40 , bg_rect.y + 30))
       221 +      # 인벤토리 UI 그리기
       222 +      player.inventory.draw(screen, (player.rect.x, player.rect.y))
       223    
       224 -      # 텍스트는 위에 그리기
       225 -      screen.blit(text, (player.rect.x, player.rect.y - 10))   
       226 -  
       224        pygame.display.update()
       225        clock.tick(60)