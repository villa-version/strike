import pygame, sys, math, time


#WIDTH, HEIGHT = 1024, 680

player = None
enemies = []
bullets = []
mouse_pressed = False
intime = 0.07
update_time = time.time()
cells = []
map = [
    'wwwwwwwwwwwwwwwwwwwwww',
    'w  w              w  w',
    'w  w              w  w',
    'w     w   w  w       w',
    'w                    w',
    'w     w       w      w',
    'w                    w',
    'w  w      w      w   w',
    'w  w             w   w',
    'wwwwwwwwwwwwwwwwwwwwww'
]
CELL_SIZE = 50
CELLS_NUMB_X = len(map[0])
CELLS_NUMB_Y = len(map)
WIDTH, HEIGHT = CELL_SIZE*CELLS_NUMB_X, CELL_SIZE*CELLS_NUMB_Y
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


class Player:

    def __init__(self, x, y, speed, r):
        self.x = x
        self.y = y
        self.speed = speed
        self.r = r

    def draw(self):
        pygame.draw.circle(SCREEN, (0, 0, 0), (self.x, self.y), self.r)


class Bullet:

    def __init__(self, x, y, r, m_pos, p_pos):
        self.x = x
        self.y = y
        self.r = r
        self.mouse_x, self.mouse_y = m_pos
        self.player_x, self.player_y = p_pos
        self.speed_x, self.speed_y = self.calculate_speeds()

    def draw(self):
        pygame.draw.circle(SCREEN, (0, 0, 0), (self.x, self.y), self.r)

    def calculate_speeds(self):
        dx = self.mouse_x - self.player_x
        dy = self.mouse_y - self.player_y
        dc = math.sqrt(dx**2+dy**2)
        try:
            cos = dx/dc
            #print(cos)
        except ZeroDivisionError:
            cos = 0
        try:
            sin = dy/dc
            #print(sin)
        except ZeroDivisionError:
            sin = 0

        return cos*2, sin*2


def setup():
    global player
    build_map()
    player = Player(WIDTH // 2, HEIGHT // 2, 1 / 3.5, 15)


def build_map():
    global cells
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] in 'w':
                cells.append((x*CELL_SIZE, y*CELL_SIZE))


def update():
    move_player()
    move_bullet()
    destroy_bullets()
    shoot()
    draw_objects()
    #for cell in cells:
    #    collision_with_wall(cell[0])


def draw_objects():
    player.draw()
    for bullet in bullets:
        bullet.draw()
    for cell in cells:
        pygame.draw.rect(SCREEN, (139, 69, 19), pygame.Rect(cell[0], cell[1], CELL_SIZE, CELL_SIZE))


def collision_with_wall(x):
    if abs(player.x - x-CELL_SIZE/2) <= player.speed:
        print(1)
        #player.x = x-CELL_SIZE_X/2-0.1


def shoot():
    global bullets, mouse_pressed, update_time
    if mouse_pressed:
        if time.time() - update_time >= intime:
            update_time = time.time()
            bullets.append(Bullet(player.x, player.y, 2, pygame.mouse.get_pos(), (player.x, player.y)))


def move_bullet():
    global bullets
    for bullet in bullets:
        bullet.x += bullet.speed_x
        bullet.y += bullet.speed_y


def destroy_bullets():
    global bullets
    for bullet in bullets[:]:
        if 0 > bullet.x or WIDTH < bullet.x:
            bullets.remove(bullet)
        elif 0 > bullet.y or HEIGHT < bullet.y:
            bullets.remove(bullet)


def move_player():
    global player
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player.y -= player.speed
    if key[pygame.K_s]:
        player.y += player.speed
    if key[pygame.K_a]:
        player.x -= player.speed
    if key[pygame.K_d]:
        player.x += player.speed


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

            SCREEN.fill((255, 222, 178))
            update()
            pygame.display.flip()

    except KeyboardInterrupt:
        sys.exit()
        pygame.quit()


if __name__ == '__main__':
    main()
