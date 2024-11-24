# Example file showing a basic pygame "game loop"
import pygame
from random import randint, seed
import time
from math import floor

# game setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
seed(time.time())
font = pygame.font.SysFont(None, 36)
# pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

sec_counter = 0

zone_num = 0
zone_init = True

loose_items = []
loose_items_pos = []

enemies = []
enemies_pos = []
enemies_modes = []
enemy_img = ":)"
enemy2_x = True
enemy2_y = True
enemies_timeout = []

player_x = 10
player_y = 500
player_size = 100
player_img = pygame.image.load(f"assets/player0.png")
player_box = pygame.Rect(player_x, player_y, player_size, player_size)
player_health = 20
player_health_rem = 20
player_atk = 4
player_speed = 2
player_attacking = False
# print(randint(5, 20))
bloop = 0
bot_piece_pos = (0,0)
bot_piece_img = ":("

flame_imgs = [pygame.image.load(f"assets/flame/flame0.png"), pygame.image.load(f"assets/flame/flame1.png"), pygame.image.load(f"assets/flame/flame2.png"), pygame.image.load(f"assets/flame/flame3.png"), pygame.image.load(f"assets/flame/flame4.png"), pygame.image.load(f"assets/flame/flame5.png"), pygame.image.load(f"assets/flame/flame6.png"), pygame.image.load(f"assets/flame/flame7.png"), pygame.image.load(f"assets/flame/flame8.png"), pygame.image.load(f"assets/flame/flame9.png"), pygame.image.load(f"assets/flame/flame10.png"), pygame.image.load(f"assets/flame/flame11.png"), pygame.image.load(f"assets/flame/flame12.png"), pygame.image.load(f"assets/flame/flame13.png"), pygame.image.load(f"assets/flame/flame14.png"), ]
for i in range(len(flame_imgs)):
    flame_imgs[i] = pygame.transform.scale(flame_imgs[i], (player_size+100, player_size+100))

bg_img = pygame.image.load(f"assets/bg.png").convert()
bg_img = pygame.transform.scale(bg_img, (1280, 720))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            sec_counter += 1

    # player movement
    if pygame.key.get_pressed()[pygame.K_w]:
        player_y -= player_speed
        # print("key w pressed")
    if pygame.key.get_pressed()[pygame.K_a]:
        player_x -= player_speed
        # print("key w pressed")
    if pygame.key.get_pressed()[pygame.K_s]:
        player_y += player_speed
        # print("key w pressed")
    if pygame.key.get_pressed()[pygame.K_d]:
        player_x += player_speed
        # print("key w pressed")

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    
    screen.blit(bg_img, (0, 0))

    if zone_init:
        # init items each zone
        loose_items.clear()
        loose_items_pos.clear()
        if zone_num < 6:
            for i in range(randint(1,4)):
                loose_items.append(randint(0,3))
                loose_items_pos.append((randint(50, 1230), randint(50, 690)))
        
        # init enemies each zone
        enemies.clear()
        enemies_pos.clear()
        enemies_modes.clear()
        if zone_num < 6:
            for i in range(randint(3, 5)):
                enemies.append(randint(0,2))
                enemies_pos.append((randint(250, 1030), randint(250, 470)))
                enemies_modes.append(randint(0,2))
                enemies_timeout.append(0)            
        zone_num += 1
        if zone_num == 1:
            bot_piece_img = pygame.image.load(f"assets/bot-arm.png")
        elif zone_num == 2:
            bot_piece_img = pygame.image.load(f"assets/bot-arm.png")
            bot_piece_img = pygame.transform.flip(bot_piece_img, True, False)
        elif zone_num == 3:
            bot_piece_img = pygame.image.load(f"assets/bot-leg.png")
        elif zone_num == 4:
            bot_piece_img = pygame.image.load(f"assets/bot-leg.png")
            bot_piece_img = pygame.transform.flip(bot_piece_img, True, False)
        elif zone_num == 5:
            bot_piece_img = pygame.image.load(f"assets/bot-head.png")
        elif zone_num == 6:
            bot_pos = (20, 20)
            bot_img = pygame.image.load(f"assets/big-bot.png")
            bot_img = pygame.transform.scale(bot_img, (300, 300))
        bot_piece_img = pygame.transform.scale(bot_piece_img, (80, 80))
        bot_lives = 5
        bot_piece_pos = (randint(50, 1230), randint(50, 670))
        player_health_rem = player_health
        zone_init = False
        bot_piece_collected = False

    # RENDER YOUR GAME HERE
    player_box = pygame.Rect(player_x, player_y, player_size, player_size)
    # pygame.draw.rect(screen, "black", player_box)
    player_img = pygame.transform.scale(player_img, (player_size, player_size))
    screen.blit(player_img, (player_x, player_y))

    # item renderer
    for i in range(len(loose_items)):
        if loose_items[i] == 0:
            pygame.draw.rect(screen, "orange", pygame.Rect(loose_items_pos[i][0], loose_items_pos[i][1], 20, 20))
        elif loose_items[i] == 1:
            pygame.draw.rect(screen, "blue", pygame.Rect(loose_items_pos[i][0], loose_items_pos[i][1], 20, 20))
        elif loose_items[i] == 2:
            pygame.draw.rect(screen, "red", pygame.Rect(loose_items_pos[i][0], loose_items_pos[i][1], 20, 20))
        elif loose_items[i] == 3:
            pygame.draw.rect(screen, "red", pygame.Rect(loose_items_pos[i][0], loose_items_pos[i][1], 20, 20))
            pygame.draw.rect(screen, "orange", pygame.Rect(loose_items_pos[i][0]+4, loose_items_pos[i][1]+4, 12, 12))
            pygame.draw.rect(screen, "blue", pygame.Rect(loose_items_pos[i][0]+7, loose_items_pos[i][1]+7, 6, 6))

    # player/pellet collision
    for i in range(len(loose_items)):
        if player_x <= loose_items_pos[i][0] + 20 and player_x + player_size >= loose_items_pos[i][0]:
            if player_y <= loose_items_pos[i][1] + 20 and player_y + player_size >= loose_items_pos[i][1]:
                if loose_items[i] == 0:
                    bloop = player_health_rem / player_health
                    player_health += randint(5,10)
                    player_health_rem = int(floor(bloop)*player_health)
                    loose_items[i] = 4
                elif loose_items[i] == 1:
                    player_speed += 1
                    loose_items[i] = 4
                elif loose_items[i] == 2:
                    player_atk += randint(2, 4)
                    loose_items[i] = 4
                elif loose_items[i] == 3:
                    match randint(0,2):
                        case 0:
                            bloop = player_health_rem / player_health
                            player_health += randint(5,10)
                            player_health_rem = int(floor(bloop)*player_health)
                        case 1:
                            player_speed += 1
                        case 2:
                            player_atk += randint(2, 4)
                    loose_items[i] = 4

    # stats gui
    pygame.draw.rect(screen, "black", pygame.Rect(15, 675, 110, 30))
    pygame.draw.rect(screen, "white", pygame.Rect(20, 680, 100, 20))
    pygame.draw.rect(screen, "orange", pygame.Rect(20, 680, int((player_health_rem/player_health)*100), 20))

    # enemy renderer
    for i in range(len(enemies)):
        if enemies_modes[i] == 0:
            enemy_img = pygame.image.load(f"assets/blem0.png")
            enemy_img = pygame.transform.scale(enemy_img, (player_size-40, player_size-40))
            screen.blit(enemy_img, (enemies_pos[i][0], enemies_pos[i][1]))
        if enemies_modes[i] == 1:
            enemy_img = pygame.image.load(f"assets/glorg0.png")
            enemy_img = pygame.transform.scale(enemy_img, (player_size-60, player_size-60))
            screen.blit(enemy_img, (enemies_pos[i][0], enemies_pos[i][1]))
        if enemies_modes[i] == 2:
            enemy_img = pygame.image.load(f"assets/zeep0.png")
            enemy_img = pygame.transform.scale(enemy_img, (player_size-50, player_size-50))
            screen.blit(enemy_img, (enemies_pos[i][0], enemies_pos[i][1]))

    # enemy movement
    for i in range(len(enemies)):
        if enemies_modes[i] == 0 and enemies_timeout[i] == 0:
            if enemies_pos[i][0] - player_x > 0:
                enemies_pos[i] = (enemies_pos[i][0]-int(player_speed/2), enemies_pos[i][1])
            elif enemies_pos[i][0] - player_x < 0:
                enemies_pos[i] = (enemies_pos[i][0]+int(player_speed/2), enemies_pos[i][1])
            if enemies_pos[i][1] - player_y > 0:
                enemies_pos[i] = (enemies_pos[i][0], enemies_pos[i][1]-int(player_speed/2))
            elif enemies_pos[i][1] - player_y < 0:
                enemies_pos[i] = (enemies_pos[i][0], enemies_pos[i][1]+int(player_speed/2))
            if player_x <= enemies_pos[i][0] + 50 and player_x + player_size >= enemies_pos[i][0]:
                if player_y <= enemies_pos[i][1] + 50 and player_y + player_size >= enemies_pos[i][1]:
                    player_health_rem -= zone_num * 2
                    # print("blob")
                    # sec_counter = pygame.time.get_ticks()
                    enemies_timeout[i] = 100
            if player_x-50 <= enemies_pos[i][0] + 50 and player_x + player_size+50 >= enemies_pos[i][0] and player_attacking > 0:
                if player_y-50 <= enemies_pos[i][1] + 50 and player_y + player_size+50 >= enemies_pos[i][1]:
                    # player_attacking = 63
                    enemies_modes[i] = 5
        elif enemies_modes[i] == 1 and enemies_timeout[i] == 0:
            if enemies_pos[i][0] - player_x > 0:
                enemies_pos[i] = (enemies_pos[i][0]+int(player_speed/2), enemies_pos[i][1])
            elif enemies_pos[i][0] - player_x < 0:
                enemies_pos[i] = (enemies_pos[i][0]-int(player_speed/2), enemies_pos[i][1])
            if enemies_pos[i][1] - player_y > 0:
                enemies_pos[i] = (enemies_pos[i][0], enemies_pos[i][1]+int(player_speed/2))
            elif enemies_pos[i][1] - player_y < 0:
                enemies_pos[i] = (enemies_pos[i][0], enemies_pos[i][1]-int(player_speed/2))
            if enemies_pos[i][0] > 1280-player_size+60:
                enemies_pos[i] = (enemies_pos[i][0]-int(player_speed/2), enemies_pos[i][1])
            if enemies_pos[i][0] < 0:
                enemies_pos[i] = (enemies_pos[i][0]+int(player_speed/2), enemies_pos[i][1])
            if enemies_pos[i][1] > 720-player_size+60:
                enemies_pos[i] = (enemies_pos[i][0], enemies_pos[i][1]-int(player_speed/2))
            if enemies_pos[i][1] < 0:
                enemies_pos[i] = (enemies_pos[i][0], enemies_pos[i][1]+int(player_speed/2))
            if player_x <= enemies_pos[i][0] + 50 and player_x + player_size >= enemies_pos[i][0]:
                if player_y <= enemies_pos[i][1] + 50 and player_y + player_size >= enemies_pos[i][1]:
                    player_health_rem -= zone_num * 2
                    # print("blob")
                    # sec_counter = pygame.time.get_ticks()
                    enemies_timeout[i] = 100
            if player_x-50 <= enemies_pos[i][0] + 50 and player_x + player_size+50 >= enemies_pos[i][0] and player_attacking > 0:
                if player_y-50 <= enemies_pos[i][1] + 50 and player_y + player_size+50 >= enemies_pos[i][1]:
                    # player_attacking = 63
                    enemies_modes[i] = 5
        elif enemies_modes[i] == 2 and enemies_timeout[i] == 0:
            if enemy2_x:
                enemies_pos[i] = (enemies_pos[i][0]+int(player_speed/2), enemies_pos[i][0])
            else:
                enemies_pos[i] = (enemies_pos[i][0]-int(player_speed/2), enemies_pos[i][0])
            if enemy2_y:
                enemies_pos[i] = (enemies_pos[i][0], enemies_pos[i][0]+int(player_speed/2))
            else:
                enemies_pos[i] = (enemies_pos[i][0], enemies_pos[i][0]+int(player_speed/2))
            if enemies_pos[i][0] > 1280-player_size+50:
                enemy2_x = False
            if enemies_pos[i][0] < 0:
                enemy2_x = True
            if enemies_pos[i][1] > 720-player_size+50:
                enemy2_x = False
            if enemies_pos[i][1] < 0:
                enemy2_x = True
        
            if player_x <= enemies_pos[i][0] + 50 and player_x + player_size >= enemies_pos[i][0]:
                if player_y <= enemies_pos[i][1] + 50 and player_y + player_size >= enemies_pos[i][1]:
                    player_health_rem -= zone_num * 2
                    # print("blob")
                    # sec_counter = pygame.time.get_ticks()
                    enemies_timeout[i] = 100
            if player_x-50 <= enemies_pos[i][0] + 50 and player_x + player_size+50 >= enemies_pos[i][0] and player_attacking > 0:
                if player_y-50 <= enemies_pos[i][1] + 50 and player_y + player_size+50 >= enemies_pos[i][1]:
                    # player_attacking = 63
                    enemies_modes[i] = 5
        if enemies_timeout[i] > 0:
            enemies_timeout[i] -= 1
            # print(enemies_timeout[i])
        
    if not 0 in enemies_modes and not 1 in enemies_modes and not 2 in enemies_modes and bot_piece_collected:
        zone_init = True

    # player attack
    if pygame.key.get_pressed()[pygame.K_SPACE] and player_attacking == 0:
        player_attacking = 63
    
    if player_attacking > 0:
        player_attacking -= 1
        if player_attacking >= 4 and player_attacking <= 7:
            screen.blit(flame_imgs[14], (player_x-50, player_y-50))
        elif player_attacking >= 8 and player_attacking <= 11:
            screen.blit(flame_imgs[13], (player_x-50, player_y-50))
        elif player_attacking >= 12 and player_attacking <= 15:
            screen.blit(flame_imgs[12], (player_x-50, player_y-50))
        elif player_attacking >= 16 and player_attacking <= 19:
            screen.blit(flame_imgs[11], (player_x-50, player_y-50))
        elif player_attacking >= 20 and player_attacking <= 23:
            screen.blit(flame_imgs[10], (player_x-50, player_y-50))
        elif player_attacking >= 24 and player_attacking <= 27:
            screen.blit(flame_imgs[9], (player_x-50, player_y-50))
        elif player_attacking >= 28 and player_attacking <= 31:
            screen.blit(flame_imgs[8], (player_x-50, player_y-50))
        elif player_attacking >= 32 and player_attacking <= 35:
            screen.blit(flame_imgs[7], (player_x-50, player_y-50))
        elif player_attacking >= 36 and player_attacking <= 39:
            screen.blit(flame_imgs[6], (player_x-50, player_y-50))
        elif player_attacking >= 40 and player_attacking <= 43:
            screen.blit(flame_imgs[5], (player_x-50, player_y-50))
        elif player_attacking >= 44 and player_attacking <= 47:
            screen.blit(flame_imgs[4], (player_x-50, player_y-50))
        elif player_attacking >= 48 and player_attacking <= 51:
            screen.blit(flame_imgs[3], (player_x-50, player_y-50))
        elif player_attacking >= 52 and player_attacking <= 55:
            screen.blit(flame_imgs[2], (player_x-50, player_y-50))
        elif player_attacking >= 56 and player_attacking <= 59:
            screen.blit(flame_imgs[1], (player_x-50, player_y-50))
        elif player_attacking >= 60 and player_attacking <= 63:
            screen.blit(flame_imgs[0], (player_x-50, player_y-50))

    if not bot_piece_collected and zone_num < 6:
        screen.blit(bot_piece_img, bot_piece_pos)
    elif zone_num == 6:
        if bot_pos[0] - player_x > 0:
            bot_pos = (bot_pos[0]-player_speed +2, bot_pos[1])
        elif bot_pos[0] - player_x < 0:
            bot_pos = (bot_pos[0]+player_speed - 2, bot_pos[1])
        if bot_pos[1] - player_y > 0:
            bot_pos = (bot_pos[0], bot_pos[1]-player_speed +2)
        elif bot_pos[1] - player_y < 0:
            bot_pos = (bot_pos[0], bot_pos[1]+player_speed - 2)
        if bot_pos[0] > 1280-player_size+60:
            bot_pos = (bot_pos[0]+player_speed - 2, bot_pos[1])
        if bot_pos[0] < 0:
            bot_pos = (bot_pos[0]-player_speed +2, bot_pos[1])
        if bot_pos[1] > 720-player_size+60:
            bot_pos = (bot_pos[0], bot_pos[1]+player_speed - 2)
        if bot_pos[1] < 0:
            bot_pos = (bot_pos[0], bot_pos[1]-player_speed +2)
        if player_x <= bot_pos[0]+300 and player_x + player_size >= bot_pos[0]:
            if player_y <= bot_pos[1]+300 and player_y + player_size >= bot_pos[1]:
                player_health_rem -= 10
        screen.blit(bot_img, bot_pos)
        if player_x-50 <= bot_pos[0] + 300 and player_x + player_size+50 >= bot_pos[0] and player_attacking == 0:
            if player_y-50 <= bot_pos[1] + 300 and player_y + player_size+50 >= bot_pos[1]:
                bot_lives -= 1


    if player_x <= bot_piece_pos[0]+70 and player_x + player_size >= bot_piece_pos[0]:
        if player_y <= bot_piece_pos[1]+70 and player_y + player_size >= bot_piece_pos[1]:
            bot_piece_collected = True
    
    if player_health_rem <= 0 or bot_lives == 0:
        pygame.quit()
        
    stats_txt = font.render("HLT: "+ str(player_health_rem) + "     ATK: " + str(player_atk) + "     SPD: " + str(player_speed), True, (255, 255, 255))
    screen.blit(stats_txt, (130, 680))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()