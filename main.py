import pygame, sys, math, time

# WIDTH, HEIGHT = 1024, 680

player = None
enemies = []
bullets = []
mouse_pressed = False
intime = 0.07
update_time = time.time()
map = [
    'wwwwwwwwwwwwwwwwwwwwww',
    'w                    w',
    'w                    w',
    'w                    w',
    'w                    w',
    'w         w          w',
    'w                    w',
    'w                    w',
    'w                    w',
    'wwwwwwwwwwwwwwwwwwwwww'
]
cells = []
for _ in range(len(map)):
    cells.append([])
CELL_SIZE = 50
CELLS_NUMB_X = len(map[0])
CELLS_NUMB_Y = len(map)
WIDTH, HEIGHT = CELL_SIZE * CELLS_NUMB_X, CELL_SIZE * CELLS_NUMB_Y
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


class Player:

    def __init__(self, x, y, speed_x, speed_y, r, status, cell_x, cell_y, nearest_cells):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.status = status
        self.r = r
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.nearest_cells = nearest_cells

    def draw(self):
        pygame.draw.circle(SCREEN, (0, 0, 0), (self.x, self.y), self.r)


class Cell:
    def __init__(self, x, y, fill, status):
        self.x = x
        self.y = y
        self.fill = fill
        self.status = status

    def draw(self):
        pygame.draw.rect(SCREEN, self.fill, pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE))


class Bullet:

    def __init__(self, x, y, r, status, m_pos, p_pos, nearest_cells, cell_x, cell_y):
        self.x = x
        self.y = y
        self.r = r
        self.status = status
        self.mouse_x, self.mouse_y = m_pos
        self.player_x, self.player_y = p_pos
        self.speed_x, self.speed_y = self.calculate_speeds()
        self.nearest_cells = nearest_cells
        self.cell_x = cell_x
        self.cell_y = cell_y

    def draw(self):
        pygame.draw.circle(SCREEN, (0, 0, 0), (self.x, self.y), self.r)

    def calculate_speeds(self):
        dx = self.mouse_x - self.player_x
        dy = self.mouse_y - self.player_y
        dc = math.sqrt(dx ** 2 + dy ** 2)
        try:
            cos = dx / dc
            # print(cos)
        except ZeroDivisionError:
            cos = 0
        try:
            sin = dy / dc
            # print(sin)
        except ZeroDivisionError:
            sin = 0

        return cos * 2, sin * 2


def setup():
    global player
    build_map()
    player = Player(WIDTH // 2, HEIGHT // 2, 1 / 3.5, 1 / 3.5, 15, 'player', 0, 0, [])


def build_map():
    global cells
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] in 'w':
                cells[y].append(Cell(x * CELL_SIZE, y * CELL_SIZE, (139, 69, 19), 'block'))
            else:
                cells[y].append(Cell(x * CELL_SIZE, y * CELL_SIZE, (255, 222, 178), 'air'))


def update():
    global player
    move_player()
    move_bullet()
    shoot()
    draw_objects()
    find_out_cell_pos()
    check_nearest_сells(player)
    for bullet in bullets[:]:
        check_nearest_сells(bullet)
        for block in bullet.nearest_cells:
            collision(block, bullet)
        bullet.nearest_cells.clear()
    for block in player.nearest_cells:
        collision(block, player)
    player.nearest_cells.clear()


def draw_objects():
    for row in cells:
        for cell in row:
            cell.draw()
    for bullet in bullets:
        bullet.draw()
    player.draw()


def find_out_cell_pos():
    global player
    player.cell_x, player.cell_y = player.x // CELL_SIZE, player.y // CELL_SIZE


def check_nearest_сells(main_obj):
    starting_point = (main_obj.cell_x - 1, main_obj.cell_y - 1)
    x = 0
    while x < 3:
        y = 0
        while y < 3:
            bx, by = int(starting_point[0] + x), int(starting_point[1] + y)
            try:
                if cells[by][bx].status in 'block':
                    main_obj.nearest_cells.append(cells[by][bx])
            except IndexError:
                pass
            y += 1
        x += 1


def check_stay_in_place_y(main_obj, obj):
    if main_obj.y <= obj.y - obj.r <= main_obj.y + CELL_SIZE:
        return True
    elif main_obj.y <= obj.y + obj.r <= main_obj.y + CELL_SIZE:
        return True


def check_stay_in_place_x(main_obj, obj):
    if main_obj.x <= obj.x - obj.r <= main_obj.x + CELL_SIZE:
        return True
    elif main_obj.x <= obj.x + obj.r <= main_obj.x + CELL_SIZE:
        return True


def collision(block, obj):
    dx, dy = block.x - obj.x, block.y - obj.y

    d_left_side = obj.speed_x >= dx - obj.r >= 0
    d_right_side = obj.speed_x >= -dx - obj.r - CELL_SIZE >= 0
    d_up_side = obj.speed_y >= dy - obj.r >= 0
    d_down_side = obj.speed_y >= -dy - obj.r - CELL_SIZE >= 0

    if check_stay_in_place_y(block, obj):
        if d_left_side:
            if obj.status in 'player':
                obj.x = block.x - obj.r - obj.speed_x
            else:
                print('collide')
        if d_right_side:
            if obj.status in 'player':
                obj.x = block.x + CELL_SIZE + obj.r + obj.speed_x
            else:
                print('collide')
    if check_stay_in_place_x(block, obj):
        if d_up_side:
            if obj.status in 'player':
                obj.y = block.y - obj.r - obj.speed_y
            else:
                print('collide')
        if d_down_side:
            if obj.status in 'player':
                obj.y = block.y + CELL_SIZE + obj.r + obj.speed_y
            else:
                print('collide')


def shoot():
    global bullets, mouse_pressed, update_time
    if mouse_pressed:
        if time.time() - update_time >= intime:
            update_time = time.time()
            bullets.append(Bullet(player.x, player.y, 2, 'bullet', pygame.mouse.get_pos(), (player.x, player.y), [], 0, 0))


def move_bullet():
    global bullets
    for bullet in bullets:
        bullet.x += bullet.speed_x
        bullet.y += bullet.speed_y


def move_player():
    global player
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.y -= player.speed_y
    if key[pygame.K_s]:
        player.y += player.speed_y
    if key[pygame.K_a]:
        player.x -= player.speed_x
    if key[pygame.K_d]:
        player.x += player.speed_x


def main():
    global mouse_pressed

    setup()

    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pressed = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pressed = False

            SCREEN.fill((0, 0, 0))
            update()
            pygame.display.flip()

    except KeyboardInterrupt:
        sys.exit()
        pygame.quit()


if __name__ == '__main__':
    main()
