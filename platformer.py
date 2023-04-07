import pygame, sys, os


# ============== SETTINGS ============== #
clock = pygame.time.Clock()
FPS = 90
pygame.init()

pygame.display.set_caption('Platformer')

WINDOW_SIZE = (640,480)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((320, 240), pygame.SRCALPHA)


# ============== ASSETS LOADING ============== #
assets_files = os.listdir(os.getcwd() + "\\assets")
tile_images = [pygame.image.load(os.getcwd() + "\\assets\\" + x) for x in assets_files if 'tile' in x]
enemies = [pygame.image.load(os.getcwd() + "\\assets\\" + x) for x in assets_files if 'en' in x]
coins = [pygame.image.load(os.getcwd() + "\\assets\\" + x) for x in assets_files if 'coin' in x]
keys = [pygame.image.load(os.getcwd() + "\\assets\\" + x) for x in assets_files if 'key' in x]
doors = [pygame.image.load(os.getcwd() + "\\assets\\" + x) for x in assets_files if 'door' in x]
fakes = [pygame.image.load(os.getcwd() + "\\assets\\" + x) for x in assets_files if 'fake' in x]
decor = [pygame.image.load(os.getcwd() + "\\assets\\" + x) for x in assets_files if 'decor' in x]


# ============== MAP ============== #
def import_map(path):
    with open(path, "r") as file:
        a = file.read()
        row = a.split("\n")
        l = []
        for i in row:
            l.append(i.split(" "))
        l.pop(-1)
    return l

MAP = import_map(os.getcwd()+"\\maps\\level1.txt")
map_copy = import_map(os.getcwd()+"\\maps\\level1.txt")


# ============== PLAYER MOVEMENT AND COLLISION CHECK ============== #
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


# ============== ANIMATION ============== #
animation_frames = {}
def load_animation(path, duration):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in duration:
        animation_frame_id = animation_name + '_' + str(n)
        img_location = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_location)
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var, frame, new_val):
    if action_var != new_val:
        action_var = new_val
        frame = 0
    return action_var, frame

animation_db = {}


# ============== OTHER IMAGES ============== #
bg_img = pygame.image.load(os.getcwd()+'/bg.jpg')
key_img = pygame.image.load(os.getcwd()+'/key.png')
key_img = pygame.transform.scale(key_img, (24, 24))
coin_img = pygame.image.load(os.getcwd()+'/coin.png')
coin_img = pygame.transform.scale(coin_img, (24, 24))


# ============== COUNTER ============== #
coin_count = 0
key_count = 0
change = 0 # door change var


# ============== FONTS ============== #
win_font = pygame.font.Font(os.getcwd() + '/pixel.ttf', 50)
win_text = win_font.render('YOU WIN', True, (20, 255, 50))
font = pygame.font.Font(os.getcwd() + '/pixel.ttf', 24)


# ============== GAME LOOP ============== #
def game_loop(img_path):
    global animation_db
    global coin_count
    global key_count
    global change
    global MAP

    img_for_rect = pygame.image.load(img_path + '/idle/idle_0.png')
    player_rect = pygame.Rect(230, 100, img_for_rect.get_width(), img_for_rect.get_height())

    moving_right = False
    moving_left = False

    player_y_momentum = 0
    air_timer = 0

    true_scroll = [0, 0]
    camera_speed = 20

    animation_db['run'] = load_animation(img_path + '/run', [7, 7, 7, 7, 7, 7])
    animation_db['idle'] = load_animation(img_path + '/idle', [7, 15, 7, 9])
    player_action = 'idle'
    player_frame = 0
    flip = False

    flag = True
    win = False

    while flag:


        # ============== SCROLL ============== #
        true_scroll[0] += (player_rect.x - true_scroll[0] - 167)/camera_speed
        true_scroll[1] += (player_rect.y - true_scroll[1] - 127)/camera_speed*2
        # true scroll - дробное число, отлично подходит для камеры, для создания нужного эффекта,
        # НО, т.к. компьютер не может нормально вычислять float значения, все будет криво, из-за чего используется
        # scroll со значением int
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])


        # ============== BACKGROUND BLIT ============== #
        display.blit(bg_img, (0 - scroll[0]/2, 0- scroll[1]/3))


        # ============== DOORS CHANGE ============== #
        if key_count == 3 and change == 0:
            doors[0], doors[1] = doors[1], doors[0]
            change += 1


        # ============== PLACEMENT OF BLOCKS ============== #
        tile_rects = []
        enemies_rects = []
        coins_rects = []
        keys_rects =[]
        door_rect = []
        y = 0
        for row in MAP:
            x = 0
            for tile in row:

                if tile != '0' and int(tile) < 51:
                    display.blit(tile_images[int(tile) - 1], (x * 16 - scroll[0], y * 16 - scroll[1]))
                    tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))

                elif tile != '0' and 101 > int(tile) > 50:
                    display.blit(enemies[int(tile) - 51], (x * 16 - scroll[0], y * 16 - scroll[1]))
                    enemies_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))

                elif tile != '0' and 151 > int(tile) > 100:
                    display.blit(coins[int(tile) - 101], (x * 16 - scroll[0], y * 16 - scroll[1]))
                    coins_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))

                elif tile != '0' and 201 > int(tile) > 150:
                    display.blit(keys[int(tile) - 151], (x * 16 - scroll[0], y * 16 - scroll[1]))
                    keys_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))

                elif tile != '0' and 251 > int(tile) > 200:
                    display.blit(doors[int(tile) - 201], (x * 16 - scroll[0], y * 16 - scroll[1]))
                    door_rect.append(pygame.Rect(x * 16, y * 16, 16, 32))

                elif tile != '0' and 351 > int(tile) > 300:
                    display.blit(decor[int(tile) - 301], (x * 16 - scroll[0], y * 16 - scroll[1]))

                x += 1
            y += 1


        # ============== PLAYER MOVEMENT ============== #
        player_movement = [0, 0]
        if moving_right:
            player_movement[0] += 2
        elif moving_left:
            player_movement[0] -= 2
        player_movement[1] += player_y_momentum
        player_y_momentum += 0.2
        if player_y_momentum > 5:
            player_y_momentum = 5


        # ============== ANIMATION ACTION CHANGE ============== #
        if player_movement[0] > 0:
            player_action, player_frame = change_action(player_action, player_frame, 'run')
            flip = False
        elif player_movement[0] < 0:
            player_action, player_frame = change_action(player_action, player_frame, 'run')
            flip = True
        elif player_movement[0] == 0:
            player_action, player_frame = change_action(player_action, player_frame, 'idle')


        player_rect, collisions = move(player_rect, player_movement, tile_rects) #  player move


        # ============== FOR JUMP ============== #
        if collisions['bottom']:
            player_y_momentum = 0
            air_timer = 0
        else:
            air_timer += 1

        if collisions['top']:
            player_y_momentum = 0


        # ============== ENEMIES COLLISION CHECK AND CORDS CHANGE ============== #
        if player_rect.collidelistall(enemies_rects):
            player_rect.x = 180
            player_rect.y = 140


        # ============== ANIMATION CHANGE ============== #
        player_frame += 1
        if player_frame > len(animation_db[player_action])-1:
            player_frame = 0
        player_image_id = animation_db[player_action][player_frame]
        player_image = animation_frames[player_image_id]

        if player_movement[1] < 0:
            player_image = pygame.image.load(img_path + '/jump/jump_0.png')
        elif player_movement[1] > 2 and not collisions['bottom']:
            player_image = pygame.image.load(img_path + '/jump/jump_1.png')


        # ============== KEYS AND COINS COLLISION ============== #
        for coin in range(len(coins_rects)):
            if player_rect.colliderect(coins_rects[coin]):
                MAP[int(coins_rects[coin].y/16)][int(coins_rects[coin].x/16)] = '0'
                coin_count += 1

        for key in range(len(keys_rects)):
            if player_rect.colliderect(keys_rects[key]):
                MAP[int(keys_rects[key].y/16)][int(keys_rects[key].x/16)] = '0'
                key_count += 1


        # ============== EVENTS ============== #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and not win:
                    moving_right = True
                if event.key == pygame.K_LEFT and not win:
                    moving_left = True
                if event.key == pygame.K_UP and not win:
                    if air_timer < 6:
                        player_y_momentum = -6
                elif event.key == pygame.K_ESCAPE and not win:
                    flag = False
                elif event.key == pygame.K_ESCAPE and win:
                    flag = False
                    MAP = map_copy
                    coin_count = 0
                    key_count = 0
                    win = False
                    change = 0
                    doors[0], doors[1] = doors[1], doors[0]
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    moving_right = False
                if event.key == pygame.K_LEFT:
                    moving_left = False


        # ============== DRAW PLAYER ============== #
        display.blit(pygame.transform.flip(player_image, flip, False),(player_rect.x - scroll[0], player_rect.y - scroll[1]))


        # ============== PLACEMENT OF FAKE BLOCKS ============== #
        y = 0
        for row in MAP:
            x = 0
            for tile in row:
                if tile != '0' and 301 > int(tile) > 250:
                    display.blit(fakes[int(tile) - 251], (x * 16 - scroll[0], y * 16 - scroll[1]))
                x += 1
            y += 1


        # ============== KEYS AND COINS INDICATOR ============== #
        coin_text = font.render(str(coin_count), True, (255, 255, 255))
        key_text = font.render(str(key_count), True, (255, 255, 255))
        display.blit(coin_img, (0, 0))
        display.blit(coin_text, (30, 0))
        display.blit(key_img, (0, 24))
        display.blit(key_text, (30, 24))


        # ============== WIN ============== #
        if player_rect.colliderect(door_rect[0]) and change == 1:
            win = True
            display.blit(win_text, (160 - win_text.get_width()/2, 120 - win_text.get_height()/2))


        # ============== DISPLAY UPDATE ============== #
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


