import pygame
import os

pygame.init()

Screen_width = 800
Screen_Height = 600

screen = pygame.display.set_mode((Screen_width, Screen_Height))
pygame.display.set_caption("EVIL GANG EVIL GANG EVIL GANG")

# limiting frame rate:
clock = pygame.time.Clock()
FPS = 60

# Loading images

bullet_img = pygame.image.load(f'img/bullet/0.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (int(bullet_img.get_width() * 2.5), int(bullet_img.get_height() * 2.5)))


# game variables:

GRAVITY = 0.75

###############

# player action variables
#######################
moving_left = False
moving_right = False
shoot = False
########################

BG = (144, 201, 120)
Red = (255, 0, 0)


def background():
    screen.fill(BG)
    pygame.draw.line(screen, Red, (0, 400), (Screen_width, 400))


class character(pygame.sprite.Sprite):
    def __init__(self, type_of_char, x, y, scale,ammo, speed):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True
        self.type_of_char = type_of_char
        self.direction = 1  # this specififies the right direction
        self.flip = False
        self.jump = False
        self.ammo = ammo
        self.staring_ammo = ammo
        self.in_air = True
        self.shoot_cool_down = 0
        self.animation_list = []
        self.index = 0  # this is to get next element of the animation list
        self.update_time = pygame.time.get_ticks()
        self.speed = speed
        self.vertical_velcoity = 0
        self.action = 0
        temp_list = []

        # LOADING ALL POSIBLE ANIMATION FOLDER
        animation_types = ["idle", "run", "jump", "death", "crouch", "death"]

        for animation in animation_types:
            # restinng  the list
            temp_list = []
            # couting number of frames
            num_of_frames = len(os.listdir(f'img/{self.type_of_char}/{animation}'))

            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.type_of_char}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.character_standing = self.animation_list[self.action][self.index]
        self.rect = self.character_standing.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()

        if self.shoot_cool_down > 0:
            self.shoot_cool_down -= 1





    def movement(self, moving_left, moving_right):
        # movement variables
        x = 0
        y = 0

        if moving_left:
            x = -self.speed
            self.flip = True
            self.direction = -1

        if moving_right:
            x = self.speed
            self.flip = False
            self.direction = 1

        if self.jump == True and self.in_air is False:
            self.vertical_velcoity = -11
            self.jump = False
            self.in_air = True

        self.vertical_velcoity += GRAVITY
        if self.vertical_velcoity > 10:
            self.vertical_velcoity = 10
        y += self.vertical_velcoity

        # checking colision
        if self.rect.bottom + y > 410:
            y = 410 - self.rect.bottom
            self.in_air = False

        # updating rectanlge position

        self.rect.x += x
        self.rect.y += y

    def shoot(self):
        #we can only shoot if we have ammo and the cooldown has worn off
        if self.shoot_cool_down == 0 and self.ammo >0:
            bullet = Bullet(self.rect.centerx + (0.55 * self.rect.size[0] * self.direction),
                            self.rect.centery + (-0.05 * self.rect.size[1]), self.direction)
            bullet_group.add(bullet)
            self.shoot_cool_down =20
            self.ammo -=1

    def update_animation(self):
        # update amimation
        Animation_Cooldown = 100
        # check if enough time has passed untill last update
        self.character_standing = self.animation_list[self.action][self.index]
        if pygame.time.get_ticks() - self.update_time > Animation_Cooldown:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        # if the index for the animated list gets out of bound we get error so i will try to remove this issue
        if self.index >= len(self.animation_list[self.action]):
            self.index = 0

    def uptate_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.character_standing, self.flip, False), self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self): #this is the bullet class update method
        # this moves the bullets around
        self.rect.x += (self.direction * self.speed)
        # check if bullet needs to be deleted

        if self.rect.right < 0 or self.rect.left > Screen_width:
            self.kill()

            # object collision will be handled below

        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:  # dont want bullets going through dead bodies
                self.kill()

        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:  # dont want bullets going through dead bodies
                self.kill()


# creating sprite groups
bullet_group = pygame.sprite.Group()

player = character('player', 200, 200, 1,3000, 5)
enemy = character('enemy',200,385,1,20,5)

RUN = True

while RUN:

    clock.tick(FPS)
    background()

    player.update()
    player.draw()
    enemy.update()
    enemy.draw()

    # update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)
    # see what actions the player is performing !
    if player.alive == True:

        if shoot:
            player.shoot()

        if player.in_air:
            player.uptate_action(2)  # 2 means jump


        elif moving_left or moving_right:
            player.uptate_action(1)  # 1 means run
        else:
            player.uptate_action(0)  # 0 means idle

    # update player actions
    if moving_left or moving_right:
        player.uptate_action(1)  # 1 means run
    else:
        player.uptate_action(0)  # 0 means idle
    player.movement(moving_left, moving_right)




    # code is to close the game when we want to close it
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
            # above code is to close the game when we want to close it

        # detects when to iniitate movement by pression keydown
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True

            if event.key == pygame.K_d:
                moving_right = True

            if event.key == pygame.K_w and player.alive == True:
                player.jump = True

            if event.key == pygame.K_SPACE:
                shoot = True

        # detects when to stop movement when key is not being pressed aka key up

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False

            if event.key == pygame.K_d:
                moving_right = False

            if event.key == pygame.K_SPACE:
                shoot = False

    pygame.display.update()
pygame.quit()
