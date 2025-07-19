class Animation:
    def __init__(self, images, frame_speed=6, loop=True):
        self.images = images              # 이미지 리스트
        self.frame_speed = frame_speed    # 프레임 간격 (작을수록 빠름)
        self.loop = loop                  # 반복 여부
        self.index = 0
        self.timer = 0
        self.finished = False

    def update(self):
        if self.finished:
            return self.images[-1]

        self.timer += 1
        if self.timer >= self.frame_speed:
            self.timer = 0
            self.index += 1
            if self.index >= len(self.images):
                if self.loop:
                    self.index = 0
                else:
                    self.index = len(self.images) - 1
                    self.finished = True
        return self.images[self.index]

    def reset(self):
        self.index = 0
        self.timer = 0
        self.finished = False

    def get_image(self):
        return self.images[self.index]


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
