import pygame, sys, os
from platformer import game_loop


# ============== SETTINGS ============== #
clock = pygame.time.Clock()
FPS = 90
pygame.init()

pygame.display.set_caption('Platformer')

WINDOW_SIZE = (640,480)
display = pygame.display.set_mode(WINDOW_SIZE,0,32)


# ============== PLAYERS PATHS ============== #
img_paths = [os.getcwd() + '/player_animations/MiniNobelMan', os.getcwd() + '/player_animations/MiniNobelWoMan',
             os.getcwd() + '/player_animations/MiniOldMan', os.getcwd() + '/player_animations/MiniOldWoman',
             os.getcwd() + '/player_animations/MiniPeasant', os.getcwd() + '/player_animations/MiniPrincess',
             os.getcwd() + '/player_animations/MiniQueen', os.getcwd() + '/player_animations/MiniVillagerMan',
             os.getcwd() + '/player_animations/MiniVillagerWoman', os.getcwd() + '/player_animations/MiniWorker']
img_path = img_paths[0]


bg_img = pygame.image.load(os.getcwd()+'/menu_bg.jpg')


class Button:

    def __init__(self, x, y, text:str):
        self.x = x
        self.y = y
        self.font = pygame.font.Font(os.getcwd() + '/pixel.ttf', 50)
        self.rendered_text = self.font.render(text, True, (255, 255, 255))
        self.rect = pygame.Rect(x - 20, y - 20, self.rendered_text.get_width() + 40, self.rendered_text.get_height() + 40)

    def draw(self):
        display.blit(self.rendered_text, (self.x, self.y))

    def draw_rama(self):
        pygame.draw.rect(display, (255, 255, 255), self.rect, 5)


class Hero:

    def __init__(self, x, y, path):
        self.x = x
        self.y = y
        self.path = path
        img = pygame.image.load(path + '/idle/idle_0.png')
        self.img = pygame.transform.scale(img,(32, 34))
        self.rect = pygame.Rect(x - 20, y - 20, self.img.get_width() + 40, self.img.get_height() + 40)

    def draw(self):
        display.blit(self.img, (self.x, self.y))

    def draw_rama(self):
        pygame.draw.rect(display, (255, 255, 255), self.rect, 5)


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

animation_db = {}
player_frame = 0


# ============== HERO CHANGE ACTION ============== #
def choose_hero():
    global hero
    global img_path
    flag = True
    hero_bg = pygame.image.load(os.getcwd() + '/hero_bg.png')
    while flag:

        display.blit(hero_bg, (0, 0))

        # ============== EVENTS ============== #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    flag = False
                if event.key == pygame.K_DOWN and hero < 5:
                    hero += 5
                elif event.key == pygame.K_DOWN and hero >= 5:
                    hero -= 5
                elif event.key == pygame.K_UP and hero > 5:
                    hero -= 5
                elif event.key == pygame.K_UP and hero <= 5:
                    hero += 5
                if event.key == pygame.K_RIGHT:
                    hero += 1
                elif event.key == pygame.K_LEFT:
                    hero -= 1


        if hero == 10:
            hero = 0
        elif hero == -1:
            hero = 9

        for i in heroes:
            i.draw()

        heroes[hero].draw_rama()
        img_path = img_paths[hero]


        # ============== DISPLAY UPDATE ============== #
        pygame.display.update()
        clock.tick(FPS)


# ============== BUTTONS ============== #
B1 = Button(440, 100, 'Play')
B2 = Button(415, 200, 'Heroes')
B3 = Button(440, 300, 'Exit')
buttons = [B1, B2, B3]
btn = 0


# ============== HEROES ============== #
H1 = Hero(100, 100, img_paths[0])
H2 = Hero(200, 100, img_paths[1])
H3 = Hero(300, 100, img_paths[2])
H4 = Hero(400, 100, img_paths[3])
H5 = Hero(500, 100, img_paths[4])
H6 = Hero(100, 200, img_paths[5])
H7 = Hero(200, 200, img_paths[6])
H8 = Hero(300, 200, img_paths[7])
H9 = Hero(400, 200, img_paths[8])
H10 = Hero(500, 200, img_paths[9])
heroes = [H1, H2, H3, H4, H5, H6, H7, H8, H9, H10]
hero = 0


# ============== MAIN LOOP ============== #
while True:


    display.blit(bg_img, (0, 0))

    animation_db['idle'] = load_animation(img_path + '/idle', [7, 15, 7, 9])


    # ============== EVENTS ============== #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                btn += 1
            elif event.key == pygame.K_UP:
                btn -= 1
            elif event.key == pygame.K_SPACE and btn == 0:
                game_loop(img_path)
            elif event.key == pygame.K_SPACE and btn == 1:
                choose_hero()
            elif event.key == pygame.K_SPACE and btn == 2:
                pygame.quit()
                sys.exit()


    if btn == 3:
        btn = 0
    elif btn == -1:
        btn = 2

    for i in buttons:
        i.draw()

    buttons[btn].draw_rama()


    # ============== MENU PLAYER ANIMATION ============== #
    player_frame += 1
    if player_frame > len(animation_db['idle']) - 1:
        player_frame = 0
    player_image_id = animation_db['idle'][player_frame]
    player_image = animation_frames[player_image_id]
    player_image = pygame.transform.scale(player_image, (64, 64))
    display.blit(player_image,  (150, 245))


    # ============== DISPLAY UPDATE ============== #
    pygame.display.update()
    clock.tick(FPS)
