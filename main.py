import pygame, sys, serial, time,io
from pygame.locals import *
from reportlab.pdfgen import canvas
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')


# UART  
ser = serial.Serial('COM14', 115200, timeout=1)

# PDF
def save_result_pdf(winner):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"game_result_{now}.pdf"
    c = canvas.Canvas(filename)
    c.setFont("Helvetica", 20)
    c.drawString(100, 750, f"🏆 Game Winner: {winner}")
    c.drawString(100, 720, f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.save()
    print(f"✔ PDF saved as {filename}")

# Init()
pygame.init()
width, height = 400, 300
white = (255, 255, 255)
black = (0, 0, 0)
fps = 30

displaysurf = pygame.display.set_mode((width, height))
pygame.display.set_caption("Serial Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont('galmuri11regular', 24)
status_text = "Waiting for players..."

def draw_screen(text):
    displaysurf.fill(white)
    rendered = font.render(text, True, black)
    rect = rendered.get_rect(center=(width/2, height/2))
    displaysurf.blit(rendered, rect)
    pygame.display.update()

# 메인 
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            ser.close()
            pygame.quit()
            sys.exit()

    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        print(f"📥Received: {line}")    
        if line == "Player_1":
            status_text = "Player 1 Wins!"
            save_result_pdf("Player 1")
        elif line == "Player_2":
            status_text = "Player 2 Wins!"
            save_result_pdf("Player 2")
    
    draw_screen(status_text)
    clock.tick(fps)
