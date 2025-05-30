import pygame, sys, serial, random

# 초기화
pygame.init()
ser = serial.Serial('COM14', 115200, timeout=1)

# 화면, 색상 설정
WHITE = (255, 255, 255)
size = (480, 640)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("UART Game")
clock = pygame.time.Clock()

# 이미지 불러오기
airplane = pygame.image.load('C:/projectWorkspace/2playerGame/images/plane.png')
character = pygame.image.load('C:/projectWorkspace/2playerGame/images/player.png')
background = pygame.image.load('C:/projectWorkspace/2playerGame/images/back.png')
flame = pygame.image.load('C:/projectWorkspace/2playerGame/images/flame.png')

# 이미지 크기 조절
airplane = pygame.transform.scale(airplane, (200, 100))
flame = pygame.transform.scale(flame, (40, 40))

# 폰트
font = pygame.font.SysFont("galmuri11regular", 25)

def start_menu():
    while True:
        screen.fill((0, 0, 50))
        title_text = font.render("🚀 UART Game", True, (255, 255, 255))
        start_text = font.render("▶ 시작하기 (Click here)", True, (255, 255, 0))
        quit_text = font.render("⛔ 종료하기 (Click here)", True, (255, 0, 0))

        screen.blit(title_text, (size[0]//2 - 80, 150))
        screen.blit(start_text, (size[0]//2 - 100, 300))
        screen.blit(quit_text, (size[0]//2 - 100, 350))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if size[0]//2 - 100 <= mouse_pos[0] <= size[0]//2 + 100:
                    if 300 <= mouse_pos[1] <= 330:
                        return "START"
                    elif 350 <= mouse_pos[1] <= 380:
                        pygame.quit()
                        sys.exit()

def runGame():
    x = 130
    y = 500
    flame_x = random.randint(0, size[0] - 40)
    flame_y = -40
    flame_speed = 7
    score = 0

    while True:
        clock.tick(30)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # UART 입력 처리
        try:
            data = ser.readline().decode().strip()
            if data == 'L':
                x -= 10
            elif data == 'R':
                x += 10
        except:
            pass

        x = max(0, min(x, size[0] - 200))

        # 불 이동
        flame_y += flame_speed
        if flame_y > size[1]:
            flame_y = -40
            flame_x = random.randint(0, size[0] - 40)
            score += 1

        # 충돌 판정
        airplane_rect = pygame.Rect(x, y, 200, 100)
        flame_rect = pygame.Rect(flame_x, flame_y, 40, 40)
        if airplane_rect.colliderect(flame_rect):
            return  # 게임 종료 후 menu로!

        # 화면 그리기
        screen.blit(background, (0, 0))
        screen.blit(airplane, (x, y))
        screen.blit(character, (180, 0))
        screen.blit(flame, (flame_x, flame_y))

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.update()


def game_over_menu():
    while True:
        screen.fill((0, 0, 0))
        game_over_text = font.render("🔥 Game Over", True, (255, 0, 0))
        regame_text = font.render("▶ 다시하기 (Click here)", True, (255, 255, 255))
        quit_text = font.render("⛔ 종료하기 (Click here)", True, (255, 255, 255))

        screen.blit(game_over_text, (size[0]//2 - 80, 150))
        screen.blit(regame_text, (size[0]//2 - 100, 300))
        screen.blit(quit_text, (size[0]//2 - 100, 350))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if size[0]//2 - 100 <= mouse_pos[0] <= size[0]//2 + 100:
                    if 300 <= mouse_pos[1] <= 330:
                        return "RESTART"
                    elif 350 <= mouse_pos[1] <= 380:
                        pygame.quit()
                        sys.exit()

start_menu()
# 🎮 메인 루프
while True:
    runGame()
    result = game_over_menu()
    if result != "RESTART":
        break
