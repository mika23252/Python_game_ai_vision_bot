import time
import math

import asteroid
from asteroid import check_intersection
from network import *
import data
from data import *
from bullet import *

pygame.init()

clock = pygame.time.Clock()
t = time.monotonic()
global_score = 0

pause_time = pause_click_time

controls = [0, 0, 0]  # [left, right, fire]

asteroid_time = asteroid_generation_time
asteroids = []

bullet_time = bullets_generation_time

N = 1
best_score_human = ''
best_score_AI = ''
with open('leaderboard.txt') as f:
    data2 = [a.split(' ') for a in f.readlines()]
    best_score_human = int(data2[0][1])
    best_score_AI = int(data2[1][1])


class Player:
    def __init__(self):
        self.bullet_time = bullets_generation_time
        self.rays = []
        self.pos = []
        self.center = []
        self.score = 0
        self.active = 1
        for el1, el2 in zip(player_position, size):
            self.pos.append(el1)
            self.center.append(el1 + el2 // 2)

        self.controls = [0, 0, 0]
        self.brain = Network([rays_number, 6, 3])

        self.obj = pygame.transform.scale(player_images[player_img_number // 20], size)
        self.weapon_lvl = weapon_level

    def move(self):
        self.obj = pygame.transform.scale(player_images[player_img_number // 20], size)

        if self.controls[0] and not self.controls[1]:
            self.pos[0] -= player_speed

            if self.pos[0] < 0 - size[0] // 2:
                self.pos[0] = screen_width - size[0] // 2

            self.center[0] = self.pos[0] + size[0] // 2

        if self.controls[1] and not self.controls[0]:
            self.pos[0] += player_speed

            if self.pos[0] > screen_width - size[0] // 2:
                self.pos[0] = 0 - size[0] // 2

            self.center[0] = self.pos[0] + size[0] // 2

        if self.controls[2]:
            if self.bullet_time == bullets_generation_time:
                bullets.append(Bullets(self.pos))
                self.bullet_time = 0
            else:
                self.bullet_time += 1
        self.controls = [0, 0, 0]
        self.score = global_score

    def calc_ray(self, ang=90):
        length = ray_max_length
        angle = -ang * math.pi / 180
        start_point = [self.center[0], self.pos[1] + size[1] - 30]
        end_point = [self.center[0] + math.cos(angle) * ray_max_length,
                     self.pos[1] + size[1] - 30 + math.sin(angle) * ray_max_length]

        if ang == 90:
            for asteroid in asteroids:
                if end_point[0] - asteroid.size[0] <= asteroid.pos[0] <= start_point[0] and end_point[1] - asteroid.size[1] <= asteroid.pos[1] <= start_point[1]:
                    res = check_intersection(end_point, start_point,
                                             [asteroid.pos[0], asteroid.pos[1] + asteroid.size[1]],
                                             [asteroid.pos[0] + asteroid.size[0], asteroid.pos[1] + asteroid.size[1]])

                    if res[1] and start_point[1] - lerp(end_point[1], start_point[1], res[0]) <= length:
                        length = start_point[1] - lerp(end_point[1], start_point[1], res[0])
                        end_point[0] = lerp(end_point[0], start_point[0], res[0])
                        end_point[1] = lerp(end_point[1], start_point[1], res[0])

        if ang == 180:
            for asteroid in asteroids:
                if end_point[0] - asteroid.size[0] <= asteroid.pos[0] <= start_point[0] and end_point[1] - asteroid.size[1] <= asteroid.pos[1] <= start_point[1]:
                    res = check_intersection(end_point, start_point,
                                             [asteroid.pos[0] + asteroid.size[0], asteroid.pos[1]],
                                             [asteroid.pos[0] + asteroid.size[0], asteroid.pos[1] + asteroid.size[1]])

                    if res[1] and start_point[0] - lerp(end_point[0], start_point[0], res[0]) <= length:
                        length = start_point[0] - lerp(end_point[0], start_point[0], res[0])
                        end_point[0] = lerp(end_point[0], start_point[0], res[0])
                        end_point[1] = lerp(end_point[1], start_point[1], res[0])

        if ang == 0:
            for asteroid in asteroids:
                if end_point[0] >= asteroid.pos[0] >= start_point[0] and end_point[1] - asteroid.size[1] <= asteroid.pos[1] <= start_point[1]:
                    res = check_intersection(end_point, start_point, [asteroid.pos[0], asteroid.pos[1]],
                                             [asteroid.pos[0], asteroid.pos[1] + asteroid.size[1]])

                    if res[1] and lerp(end_point[0], start_point[0], res[0]) - start_point[0] <= length:
                        length = lerp(end_point[0], start_point[0], res[0]) - start_point[0]
                        end_point[0] = lerp(end_point[0], start_point[0], res[0])
                        end_point[1] = lerp(end_point[1], start_point[1], res[0])

        if 180 > ang > 90:
            for asteroid in asteroids:
                if end_point[0] - asteroid.size[0] <= asteroid.pos[0] < start_point[0] and end_point[1] - asteroid.size[1] <= asteroid.pos[1] <= start_point[1]:
                    res1 = check_intersection(end_point, start_point,
                                              [asteroid.pos[0], asteroid.pos[1] + asteroid.size[1]],
                                              [asteroid.pos[0] + asteroid.size[0], asteroid.pos[1] + asteroid.size[1]])
                    res2 = check_intersection(end_point, start_point,
                                              [asteroid.pos[0] + asteroid.size[0], asteroid.pos[1]],
                                              [asteroid.pos[0] + asteroid.size[0], asteroid.pos[1] + asteroid.size[1]])

                    if res1[1] and (start_point[0] - (lerp(end_point[0], start_point[0], res1[0]))) / math.cos(
                            -math.pi + angle) <= length:
                        length = (start_point[0] - (lerp(end_point[0], start_point[0], res1[0]))) / math.cos(
                            -math.pi + angle)
                        end_point[0] = lerp(end_point[0], start_point[0], res1[0])
                        end_point[1] = lerp(end_point[1], start_point[1], res1[0])
                    elif res2[1] and (start_point[0] - (lerp(end_point[0], start_point[0], res2[0]))) / math.cos(
                            -math.pi + angle) <= length:
                        length = (start_point[0] - (lerp(end_point[0], start_point[0], res2[0]))) / math.cos(
                            -math.pi + angle)
                        end_point[0] = lerp(end_point[0], start_point[0], res2[0])
                        end_point[1] = lerp(end_point[1], start_point[1], res2[0])

        if 0 < ang < 90:
            for asteroid in asteroids:
                if end_point[0] >= asteroid.pos[0] > start_point[0] - asteroid.size[0] and end_point[1] - asteroid.size[1] <= asteroid.pos[1] <= start_point[1]:
                    res1 = check_intersection(start_point, end_point, [asteroid.pos[0], asteroid.pos[1]],
                                              [asteroid.pos[0], asteroid.pos[1] + asteroid.size[1]])
                    res2 = check_intersection(start_point, end_point,
                                              [asteroid.pos[0], asteroid.pos[1] + asteroid.size[1]],
                                              [asteroid.pos[0] + asteroid.size[0], asteroid.pos[1] + asteroid.size[1]])

                    if res1[1] and (lerp(start_point[0], end_point[0], res1[0]) - start_point[0]) / math.cos(
                            angle) <= length:
                        length = (lerp(start_point[0], end_point[0], res1[0]) - start_point[0]) / math.cos(angle)
                        end_point[0] = lerp(start_point[0], end_point[0], res1[0])
                        end_point[1] = lerp(start_point[1], end_point[1], res1[0])

                    elif res2[1] and (lerp(start_point[0], end_point[0], res2[0]) - start_point[0]) / math.cos(
                            angle) <= length:
                        length = (lerp(start_point[0], end_point[0], res2[0]) - start_point[0]) / math.cos(angle)
                        end_point[0] = lerp(start_point[0], end_point[0], res2[0])
                        end_point[1] = lerp(start_point[1], end_point[1], res2[0])

        self.rays.append(length)
        pygame.draw.line(screen, (225, 225, 0), start_point, end_point)


best_brain = None

dead_players = []

with open('best_brain.pkl', 'rb') as f:
    best_brain = Player()
    best_brain.brain = pickle.load(f)
for i in range(N):
    newP1 = Player()
    newP1.brain = mutate(best_brain.brain, 0)
    player_list.append(newP1)


def restart_game(brain):
    import data
    from data import player_list
    global asteroids, asteroid_time, bullet_time, global_score, pause_time, best_score_AI, best_score_human, dead_players, best_brain

    with open('leaderboard.txt', "r+") as f:
        data1 = [a.split(' ') for a in f.read().split('\n')]
        data1[0][1] = str(max(global_score, int(data1[0][1])))
        f.seek(0)
        f.write('\n'.join([' '.join(a) for a in data1]))
        f.truncate()

    player_position[0] = player_position_default[0]
    player_position[1] = player_position_default[1]
    asteroids = []
    data.brain = brain
    data.bullets = []
    data.player_list = []
    asteroid_time = asteroid_generation_time
    bullet_time = bullets_generation_time
    global_score = 0
    pause_time = pause_click_time
    data.player_img_number = 0
    with open('leaderboard.txt') as f:
        data2 = [a.split(' ') for a in f.readlines()]
        best_score_human = int(data2[0][1])
        best_score_AI = int(data2[1][1])
    best_brain = None

    dead_players = []

    with open('best_brain.pkl', 'rb') as f:
        best_brain = Player()
        best_brain.brain = pickle.load(f)
    for i in range(N):
        newP1 = Player()
        newP1.brain = mutate(best_brain.brain, 0)
        data.player_list.append(newP1)


def draw():
    global player_img_number

    screen.fill(background)

    for i in range(len(asteroids)):
        asteroids[i].drawAsteroid()

    for i in range(len(bullets)):
        bullets[i].draw_bullets()

    if not asteroid.pause:
        player_img_number += 1
        if player_img_number > 79:
            player_img_number = 0

    if data.brain == "AI":
        for p1 in player_list:
            screen.blit(p1.obj, p1.pos)
            angle = fow / (rays_number - 1)
            if p1.active:
                p1.rays = []
                for i in range(rays_number):
                    p1.calc_ray((180 - fow) // 2 + i * angle)
            else:
                dead_players.append(p1)
                player_list.pop(player_list.index(p1))
        for p1 in dead_players:
            screen.blit(p1.obj, p1.pos)

    else:
        score = pygame.font.Font(None, 42).render(f'СЧЕТ: {global_score}', 1, (255, 255, 255))
        best_score = pygame.font.Font(None, 30).render(f'ЛУЧШИЙ СЧЕТ: {best_score_human}', 1, (255, 255, 255))
        best_score_neuro = pygame.font.Font(None, 30).render(f'ЛУЧШИЙ СЧЕТ (ИИ): {best_score_AI}', 1, (255, 255, 255))
        screen.blit(player, player_position)

        screen.blit(score, (10, 10))
        screen.blit(best_score, (10, 42))
        screen.blit(best_score_neuro, (10, 74))

    if asteroid.game_over or asteroid.new_game:
        screen.fill(background)
        player_position[0] = player_position_default[0]
        player_position[1] = player_position_default[1]
        screen.blit(player, player_position)

    if asteroid.pause:
        pause_bg = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA, 32)
        pause_bg.fill((0, 0, 0))
        pause_bg.set_alpha(80)
        screen.blit(pause_bg, (0, 0))


def control():
    global controls
    global pause_time
    key = pygame.key.get_pressed()
    if not asteroid.pause:
        if key[pygame.K_a] and not key[pygame.K_d]:
            controls[0] = 1

        if key[pygame.K_d] and not key[pygame.K_a]:
            controls[1] = 1

        if key[pygame.K_SPACE]:
            controls[2] = 1
    if asteroid.new_game:
        if key[pygame.K_1]:
            asteroid.new_game = 0
            asteroid.pause = 0
            restart_game("AI")
        if key[pygame.K_2]:
            asteroid.new_game = 0
            asteroid.pause = 0
            restart_game("HUMAN")
    elif key[pygame.K_ESCAPE]:
        if pause_time >= pause_click_time and not asteroid.game_over:
            asteroid.pause = 0 if asteroid.pause else 1
            pause_time = 0
    pause_time += 1

    if asteroid.game_over:
        if key[pygame.K_RETURN]:
            asteroid.pause = 1
            asteroid.game_over = 0
            asteroid.new_game = 1


def move():
    global controls
    global player
    global bullet_time
    player = pygame.transform.scale(player_images[player_img_number // 20], size)

    if controls[0] and not controls[1]:
        player_position[0] -= player_speed
        if player_position[0] < 0 - size[0] // 2:
            player_position[0] = screen_width - size[0] // 2

    if controls[1] and not controls[0]:
        player_position[0] += player_speed

        if player_position[0] > screen_width - size[0] // 2:
            player_position[0] = 0 - size[0] // 2

    if controls[2]:
        if bullet_time >= bullets_generation_time:
            bullets.append(Bullets(player_position))
            bullet_time = 0
    bullet_time += 1
    controls = [0, 0, 0]


def generation():
    global asteroid_time
    if asteroid_time >= asteroid_generation_time:
        asteroids.append(asteroid.Asteroid())
        asteroid_time = 0
    else:
        asteroid_time += 1


def update():
    global asteroids

    if data.brain == "AI":
        for p1 in player_list:
            offsets = [1 - el / ray_max_length for el in p1.rays]
            offsets.reverse()
            p1.controls = p1.brain.feedForward(offsets, p1.brain)
            if p1.active:
                p1.move()
    else:
        control()

    if not asteroid.pause:
        move()

        generation()

        i = 0
        while i < len(asteroids):
            hit = asteroids[i].control()
            if asteroids[i].pos[1] > screen_height or hit:
                del asteroids[i]
                i -= 1
            i += 1

        i = 0
        while i < len(bullets):
            bullets[i].update_bullets()
            if len(bullets[i].poses) == 0:
                del bullets[i]
                i -= 1
            i += 1


run = True

while run:
    if time.monotonic() - t >= 1 and not asteroid.pause:
        t = time.monotonic()
        global_score += 1
    if data.brain == "AI":
        draw()
        update()
        for p1 in player_list:
            if p1.active:
                p1.score = global_score
    else:
        update()
        draw()

    if asteroid.pause:
        if asteroid.new_game:
            data.brain = "HUMAN"
            pause_text = pygame.font.Font(None, 72).render('ВЫБЕРИТЕ РЕЖИМ', 1, (255, 255, 255))
            pause_text_rect = pause_text.get_rect(center=(screen_width / 2, screen_height / 2.5))
            screen.blit(pause_text, pause_text_rect)

            one_button = pygame.font.Font(None, 36).render('1 - БОТ', 1, (255, 255, 255))
            one_rect = one_button.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(one_button, one_rect)

            two_button = pygame.font.Font(None, 36).render('2 - ИГРОК', 1, (255, 255, 255))
            two_rect = one_button.get_rect(center=(screen_width / 2, screen_height / 1.8))
            screen.blit(two_button, two_rect)
        elif asteroid.game_over:
            data.brain = "HUMAN"
            game_over_text = pygame.font.Font(None, 72).render('КОНЕЦ ИГРЫ', 1, (255, 255, 255))
            game_over_text_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 2.5))
            screen.blit(game_over_text, game_over_text_rect)

            score = pygame.font.Font(None, 36).render(f'СЧЕТ: {global_score}', 1, (255, 255, 255))
            score_rect = score.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(score, score_rect)

            restart_button = pygame.font.Font(None, 36).render('ENTER - НОВАЯ ИГРА', 1, (255, 255, 255))
            restart_rect = restart_button.get_rect(center=(screen_width / 2, screen_height / 1.5))
            screen.blit(restart_button, restart_rect)
        else:
            pause_text = pygame.font.Font(None, 72).render('ПАУЗА', 1, (255, 255, 255))
            pause_text_rect = pause_text.get_rect(center=(screen_width / 2, screen_height / 2.5))
            screen.blit(pause_text, pause_text_rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    clock.tick(300)

pygame.quit()
print(global_score)

with open('leaderboard.txt', "r+") as f:
    data1 = [a.split(' ') for a in f.read().split('\n')]
    data1[0][1] = str(max(global_score, int(data1[0][1])))
    f.seek(0)
    f.write('\n'.join([' '.join(a) for a in data1]))
    f.truncate()

if data.brain == "AI":
    if len(dead_players) != 0:
        print(dead_players[-1].score)
    else:
        dead_players.append(player_list[-1])
        print(dead_players[-1].score)
    with open('leaderboard.txt', "r+") as f:
        data = [a.split(' ') for a in f.read().split('\n')]
        data[1][1] = str(max(dead_players[-1].score, int(data[1][1])))
        f.seek(0)
        f.write('\n'.join([' '.join(a) for a in data]))
        f.truncate()
    a = input('какой?')
    if a:
        a = int(a)
        if len(dead_players) != 0:
            save(dead_players[a].brain)
        else:
            save(player_list[a].brain)