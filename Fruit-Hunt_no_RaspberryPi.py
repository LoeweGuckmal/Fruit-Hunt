import time
import random
import pygame
from colorama import Fore

debug = False


#Game
pygame.init()


# Bildschirm-Einstellungen
screen_width = 1280
screen_height = 734
#screen_height = 600 #debug height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fruit-Hunt")


# Farben
bg = (200, 255, 200)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 150, 0)
yellow = (255, 200, 0)
bombC = (180, 0, 180)


# Spieler (Quadrate)
player_size = 50
player1_x = screen_width // 2 - player_size // 2
player1_y = screen_height - player_size - 20
player2_x = screen_width // 2 - player_size // 2
player2_y = screen_height - player_size - 20
player1_speed = 4
player1_temp = 0
player2_speed = 4
player2_temp = 0


# Äpfel (Kreise)
apple_radius = 15
apples = []
num_apples = 19
banana_radius = 25
bananas = []
bomb_radius = 20
bombs = []
egg_radius = 30
eggs = []
eggI = 0
speeds = []
speed_size = 20

# anderes
score1 = 0
score2 = 0
clock = pygame.time.Clock()
running = True
startCountdown = 6
sound = 0
s_timer = 0
f_timer = 0
bIsOn = False


for _ in range(num_apples):
    apple_x = random.randint(0, screen_width - 2 * apple_radius)
    apple_y = random.randint(0, screen_height - 2 * apple_radius)
    apples.append((apple_x, apple_y))
banana_x = random.randint(0, screen_width - 2 * banana_radius)
banana_y = random.randint(0, screen_height - 2 * banana_radius)
bananas.append((banana_x, banana_y))

o = 0

def spawnFruit():
    global apple_radius
    global apples
    global banana_radius
    global bananas
    global bomb_radius
    global bombs
    global speeds
    global speed_size
    
        
    if random.randint(1,25) == 1 and len(speeds)==0:
        speeds.append(((player1_x + player_size + player2_x)//2, (player1_y + player_size  + player2_y)//2))
    if random.randint(1,20) == 1:
        banana_x = random.randint(0, screen_width - 2 * banana_radius)
        banana_y = random.randint(0, screen_height - 2 * banana_radius)
        bananas.append((banana_x, banana_y))
    elif random.randint(1,10) == 1 and len(bombs)<=9:
        bomb_x = random.randint(0, screen_width - 2 * bomb_radius)
        bomb_y = random.randint(0, screen_height - 2 * bomb_radius)
        bombs.append((bomb_x, bomb_y))
    elif random.randint(1,700) == 1 and len(eggs)<=1:
        egg_x = random.randint(0, screen_width - 2 * egg_radius)
        egg_y = random.randint(0, screen_height - 2 * egg_radius)
        eggs.append((egg_x, egg_y))
    else:
        apple_x = random.randint(0, screen_width - 2 * apple_radius)
        apple_y = random.randint(0, screen_height - 2 * apple_radius)
        apples.append((apple_x, apple_y))
def coll(fruits, fruit_radius, color, player1_x, player1_y, player2_x, player2_y, player_size, value):
    global score1
    global score2
    global sound
    
    player1_rect = pygame.Rect(player1_x, player1_y, player_size, player_size)
    player2_rect = pygame.Rect(player2_x, player2_y, player_size, player_size)
    # Zeichnen der Früchte und Kollisionserkennung
    for fruit in fruits[:]:  # Loop über Kopie der Liste, um sie während der Iteration zu ändern
        fruit_rect = pygame.Rect(fruit[0], fruit[1], 2 * fruit_radius, 2 * fruit_radius)
        pygame.draw.circle(screen, color, fruit_rect.center, fruit_radius)
 

        # Kollisionserkennung
        if player1_rect.colliderect(fruit_rect):
            fruits.remove(fruit)
            score1 += value
            if score1 < 0:
                score1 = 0
            spawnFruit()
            sound = 3
        elif player2_rect.colliderect(fruit_rect):
            fruits.remove(fruit)
            score2 += value
            if score2 < 0:
                score2 = 0
            spawnFruit()
            sound = 2
def move_player(keys, key_left, key_right, key_up, key_down, x, y, speed, width, height):
    if keys[key_left] and x > 0:
        x -= speed
    if keys[key_right] and x < width - player_size:
        x += speed
    if keys[key_up] and y > 0:
        y -= speed
    if keys[key_down] and y < height - player_size:
        y += speed
    return x, y



# Spiel-Loop

try:
    print(Fore.YELLOW + "Bananen: +7")
    print(Fore.RED + "Äpfel: +1")
    print(Fore.MAGENTA + "Bomben: -5")
    print(Fore.CYAN + "Speedboost: +50% Speed")
    if debug:
        startCountdown = 0
    while startCountdown > 3:
        screen.fill(bg)
        size = 130
        font = pygame.font.Font(None, size)
        text = font.render("Banane: +7", True, yellow)
        screen.blit(text, (20,20+0*size))
        text = font.render("Apfel: +1", True, red)
        screen.blit(text, (20,20+1*size))
        text = font.render("Bombe: -5", True, bombC)
        screen.blit(text, (20,20+2*size))
        text = font.render("Speedboost: +50% Speed", True, (150, 150, 255))
        screen.blit(text, (20,20+3*size))
        startCountdown -= 1
        pygame.display.flip()
        time.sleep(1)
    while startCountdown > 0:
        screen.fill(bg)
        font = pygame.font.Font(None, 300)
        text = font.render(f"{startCountdown}", True, green)
        screen.blit(text, (screen_width // 2 - 50, screen_height // 2 - 100))
        startCountdown -= 1
        pygame.display.flip()
        time.sleep(1)
    while running:
        eggI += 2
        screen.fill(bg)


        # Event-Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Spielerbewegung    
        keys = pygame.key.get_pressed()
        # Verwendung der Funktion für Spieler 1
        player1_x, player1_y = move_player(keys, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, player1_x, player1_y, player1_speed, screen_width, screen_height)
        # Verwendung der Funktion für Spieler 2
        player2_x, player2_y = move_player(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, player2_x, player2_y, player2_speed, screen_width, screen_height)


        player1_rect = pygame.Rect(player1_x, player1_y, player_size, player_size)
        player2_rect = pygame.Rect(player2_x, player2_y, player_size, player_size)
        # Speeditem
        for speed in speeds[:]:  # Loop über Kopie der Liste, um sie während der Iteration zu ändern
            speed_rect = pygame.Rect(speed[0], speed[1], 3*speed_size, 2*speed_size)
            pygame.draw.polygon(screen, (150, 150, 255), [(speed_rect.centerx+speed_size-12, speed_rect.centery-speed_size), (speed_rect.centerx-12, speed_rect.centery+2*speed_size-speed_size), (speed_rect.centerx+2*speed_size-12, speed_rect.centery +2*speed_size-speed_size)])


            # Kollisionserkennung
            if player1_rect.colliderect(speed_rect):
                speeds.remove(speed)
                player1_speed += 1
                player1_temp = score1
                sound = 1
            elif player2_rect.colliderect(speed_rect):
                speeds.remove(speed)
                player2_speed += 1
                player2_temp = score2
                sound = 1
        if score1 - player1_temp >= 10:
            player1_speed = 5
        if score2 - player2_temp >= 10:
            player2_speed = 5
        
        coll(apples, apple_radius, red, player1_x, player1_y, player2_x, player2_y, player_size, 1)
        coll(bananas, banana_radius, yellow, player1_x, player1_y, player2_x, player2_y, player_size, 7)
        coll(bombs, bomb_radius, bombC, player1_x, player1_y, player2_x, player2_y, player_size, -5)
        coll(eggs, egg_radius, ((40+eggI)%255, (120+eggI)%255, (200+eggI)%255), player1_x, player1_y, player2_x, player2_y, player_size, 20)

        # Zeichnen des Spielers
        pygame.draw.rect(screen, green, (player1_x, player1_y, player_size, player_size))
        pygame.draw.rect(screen, blue, (player2_x, player2_y, player_size, player_size))

                    

        font = pygame.font.Font(None, 36)
        text = font.render(f"Punkte: {score1}", True, green)
        screen.blit(text, (10, 10))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Punkte: {score2}", True, blue)
        screen.blit(text, (1150, 10))
        
        pygame.display.flip()
        clock.tick(120)  # Begrenzung auf 120 Frames pro Sekunde 

        
        counter=10000+int(str(score1)+str(score2).zfill(2))
        if score1>=100 or score2>=100:
            if score1 == 42 or score2 == 42:
                screen.fill(bg)
                font = pygame.font.Font(None, 300)
                text = font.render(f"42", True, green)
                screen.blit(text, (screen_width // 2 - 110, screen_height // 2 - 100))
                pygame.display.flip()
            
            running = False
            pygame.quit()
except KeyboardInterrupt:
    print("fertig")
finally:
    pygame.quit()
