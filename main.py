import pygame

pygame.init()

Screen_width = 800
Screen_Height = 600

screen = pygame.display.set_mode((Screen_width, Screen_Height))
pygame.display.set_caption("EVIL GANG EVIL GANG EVIL GANG")

#limiting frame rate:
clock = pygame.time.Clock()
FPS = 60




#player action variables
#######################
moving_left = False
moving_right = False
########################

BG =(144,201,120)

def background():
    screen.fill(BG)

class character(pygame.sprite.Sprite):
    def __init__(self, type_of_char ,x,y,scale,speed):
        pygame.sprite.Sprite.__init__(self)

        self.type_of_char = type_of_char
        self.direction = 1 #this specififies the right direction
        self.flip = False
        self.speed = speed
        img = pygame.image.load(f'{self.type_of_char}/ff.png')
        self.character_standing = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.character_standing.get_rect()
        self.rect.center = (x, y)


    def movement(self,moving_left,moving_right):
        #movement variables
        x = 0
        y = 0

        if moving_left:
            x = -self.speed
            self.flip = True
            self.direction = -1

        if moving_right:
            x = self.speed
            self.flip = False
            self.direction =1

        #updating rectanlge position

        self.rect.x += x
        self.rect.y += y

    def draw(self):
        screen.blit(pygame.transform.flip(self.character_standing,self.flip,False), self.rect)


player = character('protag1',200,200,1,5)
enemy = character('enemy',400,200,0.2,5)

RUN = True



while RUN:

    clock.tick(FPS)
    background()


    player.draw()
    player.movement(moving_left,moving_right)

    enemy.draw()

    #code is to close the game when we want to close it
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
            # above code is to close the game when we want to close it

    #detects when to iniitate movement by pression keydown
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True

            if event.key == pygame.K_d:
                moving_right = True



    #detects when to stop movement when key is not being pressed aka key up

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left= False

            if event.key == pygame.K_d:
                moving_right = False


    pygame.display.update()
pygame.quit()
