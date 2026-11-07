import random, pygame, data
from data import asteroid_images, screen_width, brain, screen, player_list, size, bullets

pause = 1
game_over = 0
new_game = 1

def rot_center(image, rect, angle):
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


def check_intersection(a, b, c, d):
    top = (d[0] - c[0]) * (a[1] - c[1]) - (d[1] - c[1]) * (a[0] - c[0])
    utop = (c[1]-a[1]) * (a[0]-b[0]) - (c[0]-a[0]) * (a[1]-b[1])
    bottom = (d[1] - c[1]) * (b[0] - a[0]) - (d[0] - c[0]) * (b[1] - a[1])
    t = -1
    u = -1
    if bottom:
        t = top / bottom
        u = utop / bottom
    return [t, 0 <= t <= 1 and 0 <= u <= 1]


def check_collision(obj1_pos, obj1_size, obj2_pos, obj2_size):
    edges = [
        [obj1_pos[0], obj1_pos[1]],
        [obj1_pos[0] + obj1_size[0], obj1_pos[1]],
        [obj1_pos[0], obj1_pos[1] + obj1_size[1]],
        [obj1_pos[0] + obj1_size[0], obj1_pos[1] + obj1_size[1]]
    ]

    obj_edges = [
        [obj2_pos[0], obj2_pos[1]],
        [obj2_pos[0] + obj2_size[0], obj2_pos[1]],
        [obj2_pos[0], obj2_pos[1] + obj2_size[1]],
        [obj2_pos[0] + obj2_size[0], obj2_pos[1] + obj2_size[1]]
    ]

    for edge in edges:
        if obj2_pos[0] <= edge[0] <= obj2_pos[0] + obj2_size[0] and obj2_pos[1] <= edge[1] <= obj2_pos[1] + obj2_size[1]:
            return True

    for edge in obj_edges:
        if obj1_pos[0] <= edge[0] <= obj1_pos[0] + obj1_size[0] and obj1_pos[1] <= edge[1] <= obj1_pos[1] + obj1_size[1]:
            return True


class Asteroid:
    def __init__(self):
        self.number = random.randint(0, len(asteroid_images) - 1)
        self.img = asteroid_images[self.number]
        self.img = pygame.transform.scale(self.img, [self.img.get_width() * 4, self.img.get_height() * 4])
        self.size = [self.img.get_width(), self.img.get_height()]

        self.rotation = 0
        self.rotation_speed = 0.4 * random.random() - 0.2
        # random.randint(80, screen_width - 80)
        self.pos = [random.randint(-70, screen_width + 70), -200] if brain != "AI" else [random.randint(-80, screen_width + 80), -200]
        self.speed_y = random.random() * 0.8 + 0.4
        self.speed_x = random.random() * 0.4 - 0.2

    def control(self):
        self.pos[1] += self.speed_y
        self.pos[0] += self.speed_x
        self.rotation += self.rotation_speed

        return self.checkCollisions()

    def drawAsteroid(self):
        rect = self.img.get_rect(
            center=(self.img.get_width() // 2 + self.pos[0], self.img.get_height() // 2 + self.pos[1]))
        obj, r = rot_center(self.img, rect, self.rotation)

        screen.blit(obj, r)

    def checkCollisions(self):
        global pause
        global game_over
        if data.brain == "AI":
            for p1 in player_list:
                if p1.pos[0]-self.size[0] <= self.pos[0] <= p1.pos[0]+size[0] and check_collision(self.pos, self.size, p1.pos, [size[0], size[1] - 30]):
                    p1.active = 0
                    p1.obj.set_alpha(90)
        else:
            if check_collision(self.pos, self.size, data.player_position, [size[0], size[1] - 30]):
                pause = 1
                game_over = 1

        for bullet in bullets:
            i = 0
            while i < len(bullet.poses):
                if check_collision(self.pos, self.size, bullet.poses[i], bullet.size):
                    del bullet.poses[i]
                    if self.number > 1:
                        return True
                i += 1
