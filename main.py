# Himanish
import pygame
import time
import sys
import os
# Initialize Pygame
pygame.init()
# Initialize the mixer for audio
pygame.mixer.init()
# Resolution + Header
WIDTH, HEIGHT = 1280, 780  # 1600 x 900 OR 1980 x 1080 too
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter!")
# Constants
FPS = 60
BLACK = (0, 0, 0)
GREEN = (0, 255,0)
RED = (255, 0, 0)
WHITE_BG = (255, 255, 255)
VLS = 7.5
VLR = 3.0
SHIPWIDTH, SHIPHEIGHT = 82, 70
MAXLAZERS = 220
# Assets
LSHIPL = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("SpaceshipL1.png"), (SHIPWIDTH, SHIPHEIGHT)), 180)
RSHIPR = pygame.transform.scale(pygame.image.load("SpaceshipR1.png"), (SHIPWIDTH, SHIPHEIGHT))
BG = pygame.transform.scale(pygame.image.load("BG.png"), (WIDTH, HEIGHT))
CENTREB = pygame.Rect(0, HEIGHT // 2 - 5, WIDTH, 2.5)
CENTREBCOLOR = (231, 76, 60)
iconimg = pygame.image.load("PygameIcon.png")
pygame.display.set_icon(iconimg)

# Health Images
TOP_HP_IMAGES = [
    pygame.image.load("100HP.png"),
    pygame.image.load("80HP.png"),
    pygame.image.load("60HP.png"),
    pygame.image.load("40HP.png"),
    pygame.image.load("20HP.png"),
    pygame.image.load("0HP.png")
]


BOT_HP_IMAGES = [
    pygame.image.load("100HP.png"),
    pygame.image.load("80HP.png"),
    pygame.image.load("60HP.png"),
    pygame.image.load("40HP.png"),
    pygame.image.load("20HP.png"),
    pygame.image.load("0HP.png")
]


# Win Images
BlueWin = pygame.image.load("BlueW.png")
PinkWin = pygame.image.load("PinkW.png")

 

# Sounds
SHOOT = pygame.mixer.Sound("Shoot2.wav")

 

# Event Types
LHIT = pygame.USEREVENT + 1
RHIT = pygame.USEREVENT + 2

 


def draw_window(R1, L1, RLazer, LLazer, TOP_HP, BOT_HP):
    # Default
    WIN.fill(WHITE_BG)

 

    # Background
    WIN.blit(BG, (0, 0))

 

    # Border
    pygame.draw.rect(WIN, CENTREBCOLOR, CENTREB)

 

    # Top Ship
    WIN.blit(LSHIPL, (L1.x, L1.y))

 

    # Bottom Ship
    WIN.blit(RSHIPR, (R1.x, R1.y))

 

    # Hearts
    WIN.blit(TOP_HP_IMAGES[TOP_HP // 20], (0, 0))
    WIN.blit(BOT_HP_IMAGES[BOT_HP // 20], (0, HEIGHT - BOT_HP_IMAGES[0].get_height()))

 

    # Drawing Lazers
    for Lazer in RLazer:
        pygame.draw.rect(WIN, RED, Lazer)

 

    for Lazer in LLazer:
        pygame.draw.rect(WIN, GREEN, Lazer)

 

    pygame.display.update()

 


def winner(win):
    win = pygame.transform.scale(win, (600, 600))
    WIN.blit(win, (WIDTH // 2 - win.get_width() // 2, HEIGHT // 2 - win.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)
    launcher()

 


def top_move(L1):
    keys_pressed = pygame.key.get_pressed()

 

    if keys_pressed[pygame.K_a] and L1.x - VLS > 0:  # Left
        L1.x -= VLS
    if keys_pressed[pygame.K_d] and L1.x + VLS + L1.width < WIDTH:  # Right
        L1.x += VLS
    if keys_pressed[pygame.K_w] and L1.y - VLS > 0:  # Forward
        L1.y -= VLS
    if keys_pressed[pygame.K_s] and L1.y + VLS + L1.height < CENTREB.y:  # Back
        L1.y += VLS

 


def bottom_move(R1):
    keys_pressed = pygame.key.get_pressed()

 

    if keys_pressed[pygame.K_LEFT] and R1.x - VLS > 0:  # Left
        R1.x -= VLS
    if keys_pressed[pygame.K_RIGHT] and R1.x + VLS + R1.width < WIDTH:  # Right
        R1.x += VLS
    if keys_pressed[pygame.K_DOWN] and R1.y + VLS + SHIPHEIGHT < HEIGHT:  # Back
        R1.y += VLS
    if keys_pressed[pygame.K_UP] and R1.y - VLS + 8.2 > CENTREB.y:  # Forward
        R1.y -= VLS

 


def manage_lazers(l_lazer, r_lazer, LShip, RShip):
    for Lazer in l_lazer:
        Lazer.y += VLR
        if Lazer.colliderect(RShip):
            pygame.event.post(pygame.event.Event(RHIT))
            l_lazer.remove(Lazer)
        elif Lazer.y < 0:
            l_lazer.remove(Lazer)

 

    for Lazer in r_lazer:
        Lazer.y -= VLR
        if Lazer.colliderect(LShip):
            pygame.event.post(pygame.event.Event(LHIT))
            r_lazer.remove(Lazer)
        elif Lazer.y > HEIGHT:
            r_lazer.remove(Lazer)

 


def launcher():
    R1 = pygame.Rect(550, 600, SHIPWIDTH, SHIPHEIGHT)
    L1 = pygame.Rect(850, 100, SHIPWIDTH, SHIPHEIGHT)

 

    TOP_HP = 100
    BOT_HP = 100
    RLazer = []
    LLazer = []

 

    clock = pygame.time.Clock()

 

    run = True
    while run:
        clock.tick(FPS)

 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and len(LLazer) < MAXLAZERS:
                    Lazer = pygame.Rect(L1.x + L1.width // 2 - 5, L1.y + L1.height, 10, 5)
                    pygame.mixer.Sound.play(SHOOT)
                    LLazer.append(Lazer)
                if event.key == pygame.K_PAGEDOWN and len(RLazer) < MAXLAZERS:
                    Lazer = pygame.Rect(R1.x + R1.width // 2 - 5, R1.y - R1.height, 10, 5)
                    RLazer.append(Lazer)
                    pygame.mixer.Sound.play(SHOOT)

 

            if event.type == LHIT:
                TOP_HP -= 20
                if TOP_HP < 0:
                    TOP_HP = 0
                    break

 

            if event.type == RHIT:
                BOT_HP -= 20
                if BOT_HP < 0:
                    BOT_HP = 0
                    break

 

        top_move(L1)
        bottom_move(R1)
        for Lazer in RLazer:
            Lazer.y -= VLR
            if Lazer.bottom > HEIGHT:
                RLazer.remove(Lazer)

 

        for Lazer in LLazer:
            Lazer.y += VLR
            if Lazer.top < 0:
                LLazer.remove(Lazer)

 

        manage_lazers(LLazer, RLazer, L1, R1)
        draw_window(R1, L1, LLazer, RLazer, TOP_HP, BOT_HP)

 

        if BOT_HP <= 0:
            winner(BlueWin)

 

        if TOP_HP <= 0:
            winner(PinkWin)

 

    pygame.quit()

 


if __name__ == "__main__":
    launcher()
    print("\033c")
    print("Thanks For Playing!")
