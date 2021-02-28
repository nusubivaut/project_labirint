import pygame
import sys
from random import choice, randrange

RES = shirot, visot = 1202, 800
for_del = 100
_c_o_l_s, rows = shirot // for_del, visot // for_del
gameeeeeeeeee = 0


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4

    def draw(self, sc):
        x, y = self.x * for_del, self.y * for_del

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('yellow'), (x, y), (x + for_del, y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('yellow'), (x + for_del, y), (x + for_del, y + for_del), self.thickness)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('yellow'), (x + for_del, y + for_del), (x, y + for_del), self.thickness)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('yellow'), (x, y + for_del), (x, y), self.thickness)

    def get_rects(self):
        acid_rain = []
        x, y = self.x * for_del, self.y * for_del
        if self.walls['top']:
            acid_rain.append(pygame.Rect((x, y), (for_del, self.thickness)))
        if self.walls['right']:
            acid_rain.append(pygame.Rect((x + for_del, y), (self.thickness, for_del)))
        if self.walls['bottom']:
            acid_rain.append(pygame.Rect((x, y + for_del), (for_del, self.thickness)))
        if self.walls['left']:
            acid_rain.append(pygame.Rect((x, y), (self.thickness, for_del)))
        return acid_rain

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * _c_o_l_s
        if x < 0 or x > _c_o_l_s - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False


def generate_maze():
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(_c_o_l_s)]
    current_cell = grid_cells[0]
    array = []
    break_count = 1

    while break_count != len(grid_cells):
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells)
        if next_cell:
            next_cell.visited = True
            break_count += 1
            array.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif array:
            current_cell = array.pop()
    return grid_cells


spisok_zlodeev = ['darkar.png', 'cherni.png', 'diaspora.png', 'triton.png', 'trix1.png', 'valtor.png']
random_zlodei = choice(spisok_zlodeev)


class Food:
    def __init__(self):
        self.img = pygame.image.load(random_zlodei).convert_alpha()
        self.img = pygame.transform.scale(self.img, (for_del - 10, for_del - 10))
        self.rect = self.img.get_rect()
        self.set_pos()

    def set_pos(self):
        self.rect.topleft = randrange(_c_o_l_s) * for_del + 5, randrange(rows) * for_del + 5

    def draw(self):
        game_surface.blit(self.img, self.rect)


def is_collide(x, y):
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True


def eat_food():
    for food in food_list:
        if player_rect.collidepoint(food.rect.center):
            if_ono_tebya = pygame.mixer.Sound('death.wav')

            if_ono_tebya.set_volume(0.5)

            if_ono_tebya.play()
            food.set_pos()
            return True
    return False


def is_game_over():
    global time, score, record, FPS
    if time < 0:
        pygame.time.wait(700)
        player_rect.center = for_del // 2, for_del // 2
        [food.set_pos() for food in food_list]
        set_record(record, score)
        record = get_record()
        time, score, FPS = 120, 0, 60


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
            return 0


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def start_screen():
    global gameeeeeeeeee
    vstuplenie = ["                                        лабиринт только для феечек! ", " ",
                  "",
                  "",
                  ]
    nevstuplenie = [" ", "  ",
                    " "]
    # screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
    datvidania = Background('winx.png', [0, 0])
    # fon = pygame.transform.scale(image.load('images/fon.jpg'), (DISPLAY))
    surface.blit(datvidania.image, datvidania.rect)
    font = pygame.font.Font(None, 40)
    text_c = 80
    if gameeeeeeeeee == 0:
        for line in vstuplenie:
            string_rendered = font.render(line, 1, (250, 250, 250))
            o_rect = string_rendered.get_rect()
            text_c += 30
            o_rect.top = text_c
            o_rect.x = 160
            text_c += o_rect.height
            surface.blit(string_rendered, o_rect)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                # raise (SystemExit, "QUIT")
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                gameeeeeeeeee = 1

        pygame.display.flip()
    elif gameeeeeeeeee == 2:
        for line in nevstuplenie:
            string_rendered = font.render(line, 1, (0, 0, 240))
            intro_rect = string_rendered.get_rect()
            text_c += 30
            intro_rect.top = text_c
            intro_rect.x = 160
            text_c += intro_rect.height
            surface2.blit(string_rendered, intro_rect)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.flip()


FPS = 60
pygame.init()
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((shirot + 300, visot))
surface2 = pygame.display.set_mode((shirot + 300, visot))
clock = pygame.time.Clock()

# images
fone_it = pygame.image.load(r'C:\Users\iraka\PycharmProjects\pythonProject\project\general_fone.png').convert()
starssssss = pygame.image.load(r'C:\Users\iraka\PycharmProjects\pythonProject\project\stars.png').convert()

# get maze
maze = generate_maze()
feechki = ['blum.png', 'roxi.png', 'muza.png', 'stella.png', 'techna.png', 'leila.png', 'daphna.png', 'flora.png']
spisok_feechek = choice(feechki)
# player settings
player_speed = 6
player_img = pygame.image.load(spisok_feechek).convert_alpha()
player_img = pygame.transform.scale(player_img, (for_del - 2 * maze[0].thickness, for_del - 2 * maze[0].thickness))
player_rect = player_img.get_rect()
player_rect.center = for_del // 2, for_del // 2
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
direction = (0, 0)

# food settings
food_list = [Food() for i in range(10)]

# collision list
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

# timer, score, record
pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 120
score = 0
record = get_record()

# fonts
font = pygame.font.SysFont('Impact', 150)
text_font = pygame.font.SysFont('Impact', 80)

spisok_pesen = ['да, а что вы хотели.wav', 'Billie Eilish-Therefore I Am-kissvk.com.wav',
                'Bo-i-Bro-Щекоти кота-kissvk.com.wav',
                'Chuang 2020-Miss Freak  HD Audio - Xu Yiyangs Team--kissvk.com.wav',
                'KEΛEVRA-Остановись-kissvk.com.wav', 'Laura Marling-What He Wrote-kissvk.com.wav',
                'Pain Of Salvation-Sisters-kissvk.com.wav', 'Theodor Bastard-Шуми-kissvk.com.wav',
                'Агата Кристи-Секрет-kissvk.com.wav', 'Гр. Пурген-2. Австралопитеки идут-kissvk.com.wav',
                'Женя Тихомирова-Мотылёк-kissvk.com.wav', 'Йорш-Панк никогда не умрёт-kissvk.com.wav',
                'Канцлер Ги-Версковый Мед-kissvk.com.wav', 'Кукрыниксы-Шторм-kissvk.com.wav',
                'Лакмус-Человек человеку-kissvk.com.wav', 'Порнофильмы-Звёздочка-kissvk.com.wav',
                'Порнофильмы-Ритуалы-kissvk.com.wav', 'Рок-опера Орфей-Власть-kissvk.com.wav',
                'Сразу Май-Хірасімы-kissvk.com.wav', 'Тараканы--Я смотрю на них-kissvk.com.wav']
spisok_for_random = choice(spisok_pesen)
pesenki = pygame.mixer.Sound(spisok_for_random)
pesenki.set_volume(0.1)

pesenki.play()
while True:

    [cell.draw(game_surface) for cell in maze]
    if gameeeeeeeeee == 0:
        start_screen()
    elif gameeeeeeeeee == 1:
        surface.blit(starssssss, (shirot, 0))
        surface.blit(game_surface, (0, 0))
        game_surface.blit(fone_it, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                time -= 1

        # controls and movement
        pressed_key = pygame.key.get_pressed()
        for key, key_value in keys.items():
            if pressed_key[key_value] and not is_collide(*directions[key]):
                direction = directions[key]
                break
        if not is_collide(*direction):
            player_rect.move_ip(direction)

        # gameplay
        if eat_food():
            FPS += 10
            score += 1
        is_game_over()

        # draw player
        game_surface.blit(player_img, player_rect)

        # draw food
        [food.draw() for food in food_list]

        # draw stats
        surface.blit(text_font.render('TIME', True, pygame.Color('cyan'), True), (shirot + 70, 20))
        surface.blit(font.render(f'{time}', True, pygame.Color('cyan')), (shirot + 70, 100))
        surface.blit(text_font.render('score:', True, pygame.Color('forestgreen'), True), (shirot + 50, 290))
        surface.blit(font.render(f'{score}', True, pygame.Color('forestgreen')), (shirot + 70, 370))
        surface.blit(text_font.render('record:', True, pygame.Color('magenta'), True), (shirot + 30, 550))
        surface.blit(font.render(f'{record}', True, pygame.Color('magenta')), (shirot + 70, 630))

        # print(clock.get_fps())
        pygame.display.flip()
        clock.tick(FPS)
