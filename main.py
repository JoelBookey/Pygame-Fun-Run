import sys
import time
import pygame
import random


class State_Machine():

    def __init__(self):
        global dead
        global has_won

        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 900
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.BG_COLOUR = (255, 255, 255)

        self.player = Player(50, 450,
                             {
                                'right_1': pygame.image.load('assets/run_right1.png').convert_alpha(),
                                'right_2': pygame.image.load('assets/run_right2.png').convert_alpha(),
                                'left_1': pygame.image.load('assets/run_left1.png').convert_alpha(),
                                'left_2': pygame.image.load('assets/run_left2.png').convert_alpha(),
                                'stand': pygame.image.load('assets/standstill.png').convert_alpha(),
                                'death': pygame.image.load('assets/death.png').convert_alpha(),
                                'win_right': pygame.image.load('assets/win_right.png').convert_alpha(),
                                'win_left': pygame.image.load('assets/win_left.png').convert_alpha()
                             },
                             self.SCREEN_WIDTH, self.SCREEN_HEIGHT
                             )

        self.ball_images = [pygame.image.load('assets/ball_4.png').convert_alpha(),
                            pygame.image.load('assets/ball_3.png').convert_alpha(),
                            pygame.image.load('assets/ball_2.png').convert_alpha(),
                            pygame.image.load('assets/ball_1.png').convert_alpha()]

        self.bird_images = [pygame.image.load('assets/bird_1.png').convert_alpha(),
                            pygame.image.load('assets/bird_2.png').convert_alpha(),
                            pygame.image.load('assets/bird_3.png').convert_alpha()]

        self.font = pygame.font.Font(None, 36)
        self.fail_text = self.font.render('Game Over!', True, (0, 0, 0))
        self.win_text = self.font.render('You Win!', True, (0, 0, 0))
        pygame.display.set_caption('RUN!!!!!')
        pygame.display.set_icon(pygame.image.load('assets/icon.ico'))

        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.enemy_group = pygame.sprite.Group()
        self.player.y = 450
        self.player.x = 50

        self.mode = ''
        self.timed_button = Button(self.SCREEN_WIDTH * 0.25, self.SCREEN_HEIGHT / 2, 100, 75, 'Timed', (0, 0, 0), 36,
                              (255, 255, 255))
        self.survive_button = Button(self.SCREEN_WIDTH * 0.75, self.SCREEN_HEIGHT / 2, 100, 75, 'Survive', (0, 0, 0), 36,
                                (255, 255, 255))
        while self.mode == '':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.timed_button.rect.collidepoint(pos):
                            self.mode = 'timed'
                        elif self.survive_button.rect.collidepoint(pos):
                            self.mode = 'survive'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.mode = 'timed'
                    if event.key == pygame.K_2:
                        self.mode = 'survive'

            self.screen.fill(self.BG_COLOUR)
            self.timed_button.draw(self.screen)
            self.survive_button.draw(self.screen)
            pygame.display.update()

        self.enemy_choices = ['wacky bird', 'bird', 'ball', 'ball']                                           
        self.number = 0
        self.og_enemies = []
        if self.mode == 'survive':
            self.number = 0
            for i in range(35):
                enemy = (random.choice(self.enemy_choices), random.randint(3, 5), self.number, random.randint(1, 3))
                self.number += random.randint(1, 4)
                self.og_enemies.append(enemy)
                self.enemies = self.enemy_generate()

        elif self.mode == 'timed':
            self.enemies = []
            for i in range(5):
                enemy = (random.choice(self.enemy_choices), random.randint(3, 5), self.number, random.randint(1, 3))
                self.number += random.randint(1, 4)
                self.enemies.append(enemy)

        self.player_x_speed = 0
        self.player_Y_speed = 0
        self.player_y_acc = 0
        self.start_time = time.time()
        self.left_pressed = False
        self.right_pressed = False
        self.win_done = False
        self.jumping = False
        self.jumping_queue = False
        self.jumping_clock = 0
        self.dead_done = False
        self.survive_time = 0
        dead = False
        has_won = False

    def reset(self):
        global dead
        global has_won

        self.player.y = 450
        self.player.x = 50
        self.enemy_group.empty()

        self.mode = ''
        while self.mode == '':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.timed_button.rect.collidepoint(pos):
                            self.mode = 'timed'
                        elif self.survive_button.rect.collidepoint(pos):
                            self.mode = 'survive'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.mode = 'timed'
                    if event.key == pygame.K_2:
                        self.mode = 'survive'

            self.screen.fill(self.BG_COLOUR)
            self.timed_button.draw(self.screen)
            self.survive_button.draw(self.screen)
            pygame.display.update()

        self.enemy_choices = ['wacky bird', 'bird', 'ball', 'ball']
        self.number = 0
        if self.mode == 'survive':
            self.og_enemies = []
            for i in range(35):
                enemy = (random.choice(self.enemy_choices), random.randint(3, 5), self.number, random.randint(1, 3))
                self.number += random.randint(1, 4)
                self.og_enemies.append(enemy)
                self.enemies = self.enemy_generate()

        elif self.mode == 'timed':
            self.enemies = []
            for i in range(5):
                enemy = (random.choice(self.enemy_choices), random.randint(3, 5), self.number, random.randint(1, 3))
                self.number += random.randint(1, 4)
                self.enemies.append(enemy)

        self.player_x_speed = 0
        self.player_Y_speed = 0
        self.player_y_acc = 0
        self.start_time = time.time()
        self.left_pressed = False
        self.right_pressed = False
        dead = False
        self.jumping = False
        self.jumping_queue = False
        self.jumping_clock = 0
        self.dead_done = False
        has_won = False
        self.win_done = False
        self.survive_time = 0

    def normal(self):
        global dead
        global has_won

        if self.mode == 'timed' and len(self.enemies) < 5:
            self.enemies.append((random.choice(self.enemy_choices), random.randint(3, 5), self.number, random.randint(1, 3)))
            self.number += random.randint(1, 4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    self.player_x_speed = 4
                    self.right_pressed = True
                if event.key == pygame.K_LEFT:
                    self.player_x_speed = -4
                    self.left_pressed = True

                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if not self.jumping:
                        self.jumping_clock = pygame.time.get_ticks()
                        self. jumping = True
                        self.player_y_acc = -2
                    elif not self.jumping_queue and self.jumping and (pygame.time.get_ticks() - self.jumping_clock) / 1000 >= 0.75:
                        self.jumping_queue = True

                if event.key == pygame.K_F1 and self.mode == 'survive':
                    self.enemy_group.empty()
                    has_won = True

                if event.key == pygame.K_ESCAPE:
                    self.reset()
                    return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_pressed = False
                if event.key == pygame.K_RIGHT:
                    self.right_pressed = False
                if event.key == pygame.K_RIGHT and not self.left_pressed:
                    self.player_x_speed = 0
                if event.key == pygame.K_RIGHT and self.left_pressed:
                    self.player_x_speed = -4
                if event.key == pygame.K_LEFT and not self.right_pressed:
                    self.player_x_speed = 0
                if event.key == pygame.K_LEFT and self.right_pressed:
                    self.player_x_speed = 4

        self.enemy_spawn()
        if self.jumping:
            if self.player.y <= 350:
                self.player_Y_speed += 1
            elif self.player.y >= 450 and self.player_Y_speed:
                self.player.y = 450
                self.player_Y_speed = 0
                self.player_y_acc = 0
                self.jumping = False
                if self.jumping_queue:
                    self.player_y_acc = -2
            else:
                self.player_Y_speed += self.player_y_acc

        elif self.jumping_queue:
            if self.player.y <= 350:
                self.player_Y_speed += 1
            elif self.player.y >= 450 and self.player_Y_speed:
                self.player.y = 450
                self.player_Y_speed = 0
                self.player_y_acc = 0
                self.jumping_queue = False
            else:
                self.player_Y_speed += self.player_y_acc

        self.player.move(self.player_x_speed, self.player_Y_speed)
        self.enemy_group.update()
        self.screen.fill(self.BG_COLOUR)
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 549, 1200, 450))
        self.enemy_group.draw(self.screen)
        self.player_group.draw(self.screen)

        if self.mode == 'timed':
            self.survive_time = self.font.render(str(round(time.time() - self.start_time, 2)), True, (0, 0, 0))
            self.screen.blit(self.survive_time, (50, 50))

        if self.collision_check():
            dead = True
            self.jumping = False
            self.jumping_queue = False
            self.jumping_clock = 0
            self.left_pressed = False
            self.right_pressed = False
            self.enemy_group.empty()
            self.player_x_speed = 0
            self.player_Y_speed = 0
            self.player_y_acc = 0
            self.player.image = self.player.images['death']
            return

        if not self.enemy_group.sprites():
            has_won = True
            self.jumping = False
            self.jumping_queue = False
            self.jumping_queue = 0
            self.left_pressed = False
            self.right_pressed = False
            self.enemy_group.empty()
            self.player_x_speed = 0
            self.player_Y_speed = 0
            self.player_y_acc = 0
            self.player.image = self.player.images['win_left']

    def game_over(self):
        global dead
        global has_won

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.reset()
                    return
                elif self.dead_done:
                    self.enemies = []
                    dead = False
                    self.dead_done = False
                    if self.mode == 'survive':
                        self.enemies = self.enemy_generate()
                    else:
                        self.number = 0
                        for i in range(5):
                            enemy = (random.choice(self.enemy_choices), random.randint(3, 5), self.number, random.randint(1, 3))
                            self.number += random.randint(1, 4)
                            self.enemies.append(enemy)

                    self.player.x = 50
                    self.player.y = 450
                    self.start_time = time.time()
                    return

        self.screen.fill(self.BG_COLOUR)
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 549, 1200, 450))
        if self.mode == 'timed':
            self.screen.blit(self.survive_time, (50, 50))
        if self.player.DieNowYes():
            self.screen.blit(self.fail_text, (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 - 200))
            self.dead_done = True
        self.player_group.draw(self.screen)

    def win(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and self.win_done:
                self.reset()
                return

        self.screen.fill(self.BG_COLOUR)
        if self.player.win():
            self.win_done = True
            self.screen.blit(self.win_text, (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 - 200))
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 549, 1200, 450))
        self.player_group.draw(self.screen)

    def collision_check(self):
        if pygame.sprite.spritecollide(self.player_group.sprite, self.enemy_group, False):
            if pygame.sprite.spritecollide(self.player_group.sprite, self.enemy_group, False, pygame.sprite.collide_mask):
                return True

    def enemy_spawn(self):

        for enemy in self.enemies:
            if enemy[2] <= time.time() - self.start_time:
                if enemy[0] == 'ball':
                    self.enemy_group.add(Ball(self.SCREEN_WIDTH - 20, 505, self.ball_images, enemy[1] - 1))
                if enemy[0] == 'bird':
                    self.enemy_group.add(Bird(self.SCREEN_WIDTH - 20, 100, self.bird_images, enemy[1] - 1))
                if enemy[0] == 'wacky bird':
                    self.enemy_group.add(
                        WackyBird(self.SCREEN_WIDTH - 20, 10, self.bird_images, enemy[1], enemy[3], random.randint(200, 400)))
                self.enemies.remove(enemy)
            else:
                break

    def enemy_generate(self):
        return self. og_enemies * 1

# -----------------------------------
class Button:
    def __init__(self, x, y, width, height, text, color, font_size, font_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.font_color = font_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text = self.font.render(self.text, True, self.font_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)


class Player(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, images, screen_width, screen_height):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.images = images
        self.image = self.images['stand']
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
        self.anime_forward = 0
        self.anime_backward = 0
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, x_move, y_move):

        if x_move or y_move:
            if x_move and 0 <= self.x + x_move <= self.screen_width:
                self.x += x_move
                if x_move > 0:
                    self.anime_backward = 0
                    self.anime_forward += 0.5
                    if self.anime_forward > 10:
                        self.anime_forward = 0
                    if self.anime_forward <= 5:
                        self.image = self.images['right_1']
                        self.mask = pygame.mask.from_surface(self.image)
                    if self.anime_forward > 5:
                        self.image = self.images['right_2']
                        self.mask = pygame.mask.from_surface(self.image)

                if x_move < 0:
                    self.anime_forward = 0
                    self.anime_backward += 0.5
                    if self.anime_backward > 10:
                        self.anime_backward = 0
                    if self.anime_backward <= 5:
                        self.image = self.images['left_1']
                        self.mask = pygame.mask.from_surface(self.image)
                    if self.anime_backward > 5:
                        self.image = self.images['left_2']
                        self.mask = pygame.mask.from_surface(self.image)

            if y_move:
                self.y += y_move

        else:
            self.anime_backward = 0
            self.anime_forward = 0
            self.image = self.images['stand']
            self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

    def DieNowYes(self):

        # die.
        if round(self.x, 1) != round(self.screen_width / 2, 1) or round(self.y, 1) != round(self.screen_height / 2 + 100, 1):
            x_displace = (self.screen_width / 2) - self.x
            self.x += x_displace / 10
            y_displace = (self.screen_height / 2) + 100 - self.y
            self.y += y_displace / 10
            self.rect.center = [self.x, self.y]
            return False

        return True

    def win(self):

        if round(self.x, 1) != round(self.screen_width / 2, 1) or round(self.y, 1) != round(self.screen_height / 2, 1):
            x_displace = (self.screen_width / 2) - self.x
            self.x += x_displace / 10
            y_displace = (self.screen_height / 2) - self.y
            self.y += y_displace / 10
            if x_displace < 0:
                self.image = self.images['win_left']
            if x_displace > 0:
                self.image = self.images['win_right']
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = [self.x, self.y]
            return False

        return True


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, images, speed):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.x_speed = speed
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
        self.mask = pygame.mask.from_surface(self.image)
        self.image_num = 0


class StraightEnemy(Enemy):
    def __init__(self, pos_x, pos_y, images, speed):
        super().__init__(pos_x, pos_y, images, speed)

    def update(self):
        self.x -= self.x_speed
        self.image_num += 0.1
        if self.image_num > len(self.images):
            self.image_num = 0
        self.image = self.images[int(self.image_num)]
        self.mask = pygame.mask.from_surface(self.image)
        if self.x < 0:
            self.kill()
        self.rect.center = [self.x, self.y]


class Ball(StraightEnemy):
    def __init__(self, pos_x, pos_y, images, speed):
        super().__init__(pos_x, pos_y, images, speed)


class Bird(StraightEnemy):
    def __init__(self, pos_x, pos_y, images, speed):
        super().__init__(pos_x, pos_y, images, speed)


class WackyBird(Enemy):
    def __init__(self, pos_x, pos_y, images, x_speed, y_speed, y_barrier):
        super().__init__(pos_x, pos_y, images, x_speed)
        self.y_speed = y_speed
        self.y_barrier = y_barrier
        self.starting_y = pos_y

    def update(self):
        self.x -= self.x_speed
        if self.y > self.y_barrier or self.y < self.starting_y:
            self.y_speed *= -1
        self.y -= self.y_speed
        self.image_num += 0.1
        if self.image_num > len(self.images):
            self.image_num = 0
        self.image = self.images[int(self.image_num)]
        self.mask = pygame.mask.from_surface(self.image)
        if self.x < 0:
            self.kill()
        self.rect.center = [self.x, self.y]


pygame.init()

clock = pygame.time.Clock()

state = State_Machine()


while True:
    if not dead and not has_won:
        state.normal()
    elif dead:
        state.game_over()
    elif has_won:
        state.win()
    pygame.display.update()
    clock.tick(60)

