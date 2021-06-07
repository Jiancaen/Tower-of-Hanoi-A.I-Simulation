import pygame

# Initialize
pygame.init()

# Screen
screen = pygame.display.set_mode((800, 550))
pygame.time.set_timer(pygame.USEREVENT, 100)
bg = pygame.image.load('bg.jpg')
bg2 = pygame.transform.scale(bg, (800, 550))
font = pygame.font.SysFont(None, 30)
font2 = pygame.font.SysFont(None, 100)
pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.set_volume(.3)
pygame.mixer.music.play(-1)
sound_on = pygame.image.load('sound_on.png')
sound_off = pygame.image.load('sound_off.png')
inc = pygame.image.load('next.png')
inc2 = pygame.transform.scale(inc, (30, 40))
dec = pygame.image.load('prev.png')
dec2 = pygame.transform.scale(dec, (30, 40))
rst_btn = pygame.image.load('rst_btn.png')

# Info
pygame.display.set_caption("Towers of Hanoi")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Classes

class Disk(pygame.Rect):
    moving = False
    stationary = False
    on_spot = False

    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)

    def change_state(self):
        if self.moving is False:
            self.moving = True
        else:
            self.moving = False


class Tower:
    def __init__(self, x, origin, destination, auxiliary):
        self.x = x
        self.origin = origin
        self.destination = destination
        self.auxiliary = auxiliary


# initial variables
global btn, default, done, current, count, disc_list, moves, counter, gravity_on, busy, \
    ground, tower1, tower2, tower3, \
    disk1, disk2, disk3, disk4, disk5, disk6, disk7

running = True
__move_set = []
goal = 7  # Goal of Initial Disc Number -> 3


def main(disc_count):
    global default, done, current, count, disc_list, moves, counter, gravity_on, busy, \
        ground, tower1, tower2, tower3, \
        disk1, disk2, disk3, disk4, disk5, disk6, disk7

    count = disc_count
    disc_list = []
    moves = []
    counter = 1
    gravity_on = True
    busy = False
    current = None
    done = False
    default = sound_on

    ground = pygame.Rect(0, 475, 800, 75)

    tower1 = pygame.Rect(168, 175, 10, 350)
    tower2 = pygame.Rect(400, 175, 10, 350)
    tower3 = pygame.Rect(632, 175, 10, 350)

    disk1 = Disk(135, 100, 75, 25)
    disk2 = Disk(120, 150, 100, 25)
    disc_list.append(disk1)
    disc_list.append(disk2)

    if disc_count >= 3:
        disk3 = Disk(105, 200, 125, 25)
        disc_list.append(disk3)
    if disc_count >= 4:
        disk4 = Disk(90, 250, 150, 25)
        disc_list.append(disk4)
    if disc_count >= 5:
        disk5 = Disk(85, 300, 175, 25)
        disc_list.append(disk5)
    if disc_count >= 6:
        disk6 = Disk(60, 350, 200, 25)
        disc_list.append(disk6)
    if disc_count >= 7:
        disk7 = Disk(45, 400, 225, 25)
        disc_list.append(disk7)

    while running:
        run(disc_count)


def __move_disks(tower):
    if not tower.x == 1:
        __move_disks(Tower(tower.x - 1, tower.origin, tower.auxiliary, tower.destination))
        __move_set.append((tower.x, tower.destination))
        __move_disks(Tower(tower.x - 1, tower.auxiliary, tower.destination, tower.origin))
        return
    __move_set.append((tower.x, tower.destination))


def solve(number_of_disks):
    __move_disks(Tower(number_of_disks, 1, 3, 2))
    return __move_set


def placeable(top_disc, bottom_disc):
    global current, counter

    if top_disc.colliderect(bottom_disc) & (not top_disc.__eq__(bottom_disc)):
        top_disc.bottom = bottom_disc.top
        top_disc.stationary = True

        if top_disc.stationary:
            if busy:
                top_disc.on_spot = False

                if top_disc == current:
                    current = None


def fall(this_disc):
    global current
    this_disc.y += 1

    if this_disc.colliderect(ground):
        if ground.top - this_disc.bottom < 0:
            this_disc.bottom = ground.top
            this_disc.stationary = True

        if this_disc.stationary:
            if this_disc.centerx == tower1.centerx:
                if busy:
                    this_disc.on_spot = False
                    if this_disc == current:
                        current = None

            elif this_disc.centerx == tower2.centerx:
                if busy:
                    this_disc.on_spot = False
                    if this_disc == current:
                        current = None

            elif this_disc.centerx == tower3.centerx:
                if busy:
                    this_disc.on_spot = False
                    if this_disc == current:
                        current = None

    placeable(this_disc, disk1)
    placeable(this_disc, disk2)

    if count >= 3:
        placeable(this_disc, disk3)
    if count >= 4:
        placeable(this_disc, disk4)
    if count >= 5:
        placeable(this_disc, disk5)
    if count >= 6:
        placeable(this_disc, disk6)
    if count >= 7:
        placeable(this_disc, disk7)


def draw(disk_count):
    pygame.draw.rect(screen, (68, 77, 163), disk1, border_radius=20)
    pygame.draw.rect(screen, (91, 196, 191), disk2, border_radius=20)
    pygame.draw.rect(screen, (3, 166, 82), disk3, border_radius=20)
    if disk_count >= 4:
        pygame.draw.rect(screen, (253, 175, 22), disk4, border_radius=20)
    if disk_count >= 5:
        pygame.draw.rect(screen, (242, 88, 34), disk5, border_radius=20)
    if disk_count >= 6:
        pygame.draw.rect(screen, (216, 25, 32), disk6, border_radius=20)
    if disk_count >= 7:
        pygame.draw.rect(screen, (51, 51, 51), disk7, border_radius=20)


def shoot(disc, tower):
    disc.centerx = tower.centerx


def touch(disc):
    if disc.colliderect(tower1):
        shoot(disc, tower1)
    elif disc.colliderect(tower2):
        shoot(disc, tower2)
    elif disc.colliderect(tower3):
        shoot(disc, tower3)


def gravity():
    if not disk1.moving:
        touch(disk1)
        fall(disk1)
    if not disk2.moving:
        touch(disk2)
        fall(disk2)
    if not disk3.moving:
        touch(disk3)
        fall(disk3)
    if count >= 4:
        if not disk4.moving:
            touch(disk4)
            fall(disk4)
    if count >= 5:
        if not disk5.moving:
            touch(disk5)
            fall(disk5)
    if count >= 6:
        if not disk6.moving:
            touch(disk6)
            fall(disk6)
    if count >= 7:
        if not disk7.moving:
            touch(disk7)
            fall(disk7)


def auto_move(disc, tower):
    if not disc.on_spot:
        if disc.centery != 100:
            disc.y += -1

    if (disc.centery == 100) & (tower.centerx != disc.centerx):

        if disc.centerx < tower.centerx:
            disc.x += 1
        elif disc.centerx > tower.centerx:
            disc.x -= 1

    if tower.centerx == disc.centerx:
        disc.on_spot = True
        touch(disc)
        fall(disc)


def simulate(i):
    global current, disc_list, moves
    tower = [tower1, tower2, tower3]

    if busy:
        current = disc_list[moves[i - 1][0] - 1]
        disc_list[moves[i - 1][0] - 1].change_state()
        auto_move(disc_list[moves[i - 1][0] - 1], tower[moves[i - 1][1] - 1])
        # print(moves[i-1], counter)


def run(disc_count):
    global btn, default, goal, done, __move_set, moves, current, busy, counter, gravity_on, running, count
    screen.fill((181, 194, 199))

    # Event listeners
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if default.get_rect(topleft=(730, 485)).collidepoint(event.pos):
                    if default is sound_on:
                        default = sound_off
                        pygame.mixer.music.pause()
                    elif default is sound_off:
                        default = sound_on
                        pygame.mixer.music.unpause()
                if rst_btn.get_rect(topleft=(20, 492)).collidepoint(event.pos):
                    __move_set = []
                    main(disc_count)
                if btn.collidepoint(event.pos):
                    if not done:
                        if not busy:
                            busy = True
                            gravity_on = False
                            moves = solve(disc_count)

                if dec2.get_rect(topleft=(260, 492)).collidepoint(event.pos):

                    if disc_count == 3:
                        disc_count = 3
                        goal = (2 ** disc_count) - 1
                        __move_set = []
                        main(disc_count)
                    else:
                        disc_count -= 1
                        goal = (2 ** disc_count) - 1
                        __move_set = []
                        main(disc_count)
                if inc2.get_rect(topleft=(330, 492)).collidepoint(event.pos):

                    if disc_count == 7:
                        disc_count = 7
                        goal = (2 ** disc_count) - 1
                        __move_set = []
                        main(disc_count)
                    else:
                        disc_count += 1
                        goal = (2 ** disc_count) - 1
                        __move_set = []
                        main(disc_count)

        if busy & (current is None):
            if event.type == pygame.USEREVENT:
                counter += 1

    # Static objects
    screen.blit(bg2, (0, 0))
    pygame.draw.rect(screen, (236, 204, 180), tower1, border_radius=21)
    pygame.draw.rect(screen, (236, 204, 180), tower2, border_radius=21)
    pygame.draw.rect(screen, (236, 204, 180), tower3, border_radius=21)
    pygame.draw.rect(screen, (145, 104, 74), ground)
    draw(disc_count)

    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(260, 492, 100, 40))
    screen.blit(dec2, (260, 492))
    screen.blit(inc2, (330, 492))

    disc_adj = font.render(str(disc_count), True, (31, 29, 8))
    screen.blit(disc_adj, (305, 502))

    move_count = font.render('MOVES: ' + str(counter - 1), True, (31, 29, 8))
    screen.blit(move_count, (20, 20))
    goal_des = font.render('GOAL: ' + str(goal) + ' MOVES', True, (31, 29, 8))
    screen.blit(goal_des, (600, 20))
    finish = font2.render("DONE!", True, (31, 29, 8))
    disc_num = font.render('NO. OF DISC: '+str(disc_count), True, (31, 29, 8))
    screen.blit(disc_num, (400, 20))
    screen.blit(rst_btn, (20, 492))
    screen.blit(default, (730, 488))

    sim = font.render('SIMULATE', True, (255, 255, 255))
    btn = pygame.draw.rect(screen, (34, 39, 44), pygame.Rect(80, 492, 150, 40), border_radius=21)
    screen.blit(sim, (100, 502))

    if busy:
        if counter > len(moves):
            done = True
            busy = False

    if done:
        screen.blit(finish, (292, 250))

    simulate(counter)

    gravity()

    pygame.display.update()
    # print(counter-1)


main(3)
