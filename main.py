#import section
import pygame
import random
import os

#init section
pygame.init ()

FPS = pygame.time.Clock()   # Frame per Seconds declare

#Constants
WIDTH = 1200
HEIGHT = 800

FONT = pygame.font.SysFont('Verdana', 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 127, 0)

# Create the graphical window
main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = 'goose'
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

#Create the Player
player_size = (180, 70)
# player = pygame.image.load('player.png').convert_alpha()
player = pygame.transform.scale(pygame.image.load('player.png').convert_alpha(), player_size)
# player_rect = player.get_rect()
player_rect = pygame.Rect(0, (HEIGHT - player_size[0]) // 2, *player_size)
player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [4, 0]
player_move_left = [-4, 0]

# Enemies section
def create_enemy():
    enemy_size = (200, 70)
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), enemy_size)
    enemy_rect = pygame.Rect(WIDTH, random.randint(50, HEIGHT-enemy_size[1]-100), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

# Bonus section
def create_bonus():
    bonus_size = (90, 150)
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), bonus_size)
    bonus_rect = pygame.Rect(random.randint(100, WIDTH - 100), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

#Main Loop
enemies = []
bonuses = []

score = 0

image_index = 0
image_index_step = 1

playing = True

while playing:
    FPS.tick(120)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            # image_index += 1
            # if image_index >= len(PLAYER_IMAGES):
            #     image_index = 0
            image_index += image_index_step
            if image_index >= len(PLAYER_IMAGES)-1:
                image_index_step = -1
            elif image_index <= 0:
                image_index_step = 1

    # main_display.fill(COLOR_BLACK)

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN] and player_rect.bottom <= HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[pygame.K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_up)

    if keys[pygame.K_RIGHT] and player_rect.right <= WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[pygame.K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(player_move_left)
    
    # [0] - enemy; [1] - enemy_rect; [2] - enemy_move
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])
    
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    # Wipe out the enemies that flew to the left border 
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            playing = False

    # Wipe out the bonuses that flew to the bottom border 
    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
        
        if player_rect.colliderect(bonus[1]):
            score += bonus[2][1] // 2
            bonuses.pop(bonuses.index(bonus))
            
print("Bye!")
