import pygame
pygame.init()

win = pygame.display.set_mode((630, 368))

pygame.display.set_caption('My Game')

screenWidth = 630
screenHeight = 368

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
backgrounds = [pygame.image.load('bg.jpg'), pygame.image.load('bg2.jpg')]
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()
bg = 0

# Sounds not working for some reason
# bulletSound = pygame.mixer.Sound('bullet.wav')
# hitSound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score = 0


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y + 13, 24, 48)
        self.health = 200
        self.alive = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            else:
                win.blit(walkRight[0], (self.x, self.y))
        self.hitbox = (self.x + 20, self.y + 13, 24, 48)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0, 150, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (.25 * (200 - self.health)), 10))

    def hit(self):
        if self.health > 0:
            self.health -= 10
        else:
            self.alive = False

    def death(self):
        self.x = 30
        self.y = screenHeight - 70
        self.walkCount = 0
        self.health = 210
        self.alive = True
        fontDeath = pygame.font.SysFont('ariel', 100, True, True)
        text = fontDeath.render('YOU DIED', 1, (255, 0, 0))
        win.blit(text, (screenWidth/2 - (text.get_width()/2), screenHeight/2))
        pygame.display.update()
        pygame.time.delay(3000)


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Enemy(object):
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.vel = -3
        self.hitbox = (self.x + 20, self.y + 13, 24, 48)
        self.health = 200
        self.visible = True
        self.jay = pygame.image.load('L1E.png')

    def draw(self, win):
        self.move()
        if self.visible:
            win.blit(self.jay, (self.x, self.y))
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 150, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (.25*(200-self.health)), 10))
            self.hitbox = (self.x, self.y, 50, 60)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):  # logic for how the enemy moves
        if self.vel > 0:  # if enemy is facing right
            if self.x + self.vel < 800:  # right side of the screen
                if man.x < self.x - 75:  # checking if man is left of enemy if enemy is moving right
                    self.vel = self.vel * -1
                    self.walkCount = 0
                    self.x += self.vel  # the actual moving
                else:
                    self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0  # walkCount = what position in the animation
        else:  # if enemy is facing left
            if self.x - self.vel > 0:  # left side of the screen
                if man.x > self.x + 75:
                    self.vel = self.vel * -1
                    self.walkCount = 0
                    self.x += self.vel  # the actual moving
                else:
                    self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 10
        else:
            self.visible = False


def nextLevel():
    global bg, goblin
    bg += 1
    man.x = 40
    goblin = Enemy(450, screenHeight - 70, 64, 64, 70)
    goblin.visible = True


def redrawGameWindow():
    win.blit(backgrounds[bg], (0, 0))
    text = font.render('Score: {}'.format(score), 1, (0, 0, 0))
    win.blit(text, (390, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


# Main loop
font = pygame.font.SysFont('ariel', 30, True)
man = Player(30, screenHeight - 70, 64, 64)
goblin = Enemy(450, screenHeight - 70, 64, 64, 70)
bullets = []
shootLoop = 0
run = True
while run:
    clock.tick(27)

    if man.hitbox[0] + man.hitbox[2] >= screenWidth - 30 and goblin.visible is False and bg < 1:
        nextLevel()

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 5:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if not man.alive:
        score -= 100
        man.death()

    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            if goblin.visible:
                man.hit()

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                if goblin.visible:
                    goblin.hit()
                    score += 10
                    bullets.pop(bullets.index(bullet))
        if 0 < bullet.x < screenWidth:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 10:
            bullets.append(Projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0, 0, 0,), facing))
        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x - man.vel >= 0:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x + man.width + man.vel <= screenWidth:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if keys[pygame.K_UP]:
            man.isJump = True
            man.walkCount = 0
    if man.jumpCount >= -7 and man.isJump:
        neg = 1
        if man.jumpCount < 0:
            neg = -1
        man.y -= (abs(man.jumpCount) ** 2) * neg
        man.jumpCount -= 1
    else:
        man.isJump = False
        man.jumpCount = 7

    redrawGameWindow()


pygame.quit()
