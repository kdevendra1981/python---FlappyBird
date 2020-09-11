import pygame
import sys
import random

def drawFloor():
    screen.blit(base, (baseX, int(SCREEN_HEIGHT * .75)))
    screen.blit(base, (baseX+SCREEN_WIDTH, int(SCREEN_HEIGHT * .75)))

def create_pipe():
    randomPipeHeight = random.choice(pipe_height)
    bottomPipe = pipe_surface.get_rect(midtop = (405,randomPipeHeight))
    topPipe = pipe_surface.get_rect(midbottom = (405,randomPipeHeight-150))
    return bottomPipe,topPipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -=3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom > 500:
            screen.blit(pipe_surface, pipe)
        else:
            flipPipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flipPipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            pygame.mixer.music.load(hit)
            pygame.mixer.music.play()
            return False
    if bird_rect.top  <= -62 or bird_rect.bottom > int(SCREEN_HEIGHT * .75):
        pygame.mixer.music.load(die)
        pygame.mixer.music.play()
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-birdMovement*3,1)
    return  new_bird

def score_display(gameState):
    if gameState == 'Main_Game':
        score_surface =gamefont.render('Score: '+str(int(score)),True,(255,0,0),None)
        lastscore = 0
        score_rect = score_surface.get_rect(topleft = (10,10))
        screen.blit(score_surface,score_rect)
    elif gameState == 'Game_Over':
        score_surface =gamefont.render('Score: '+str(int(score)),True,(255,0,0),None)
        score_rect = score_surface.get_rect(topleft = (10,10))
        screen.blit(score_surface,score_rect)

        highscore_surface = gamefont.render('Highscore: '+str(int(highscore)), True, (255, 0, 255), None)
        highscore_rect = highscore_surface.get_rect(topleft=(10, 50))
        screen.blit(highscore_surface, highscore_rect)

def update_score(score):
    global highscore
    if highscore < score:
        highscore= score
    return highscore
pygame.init()
pygame.mixer.pre_init(frequency=44100,size=16,channels=1,buffer=256)
highscore = 0
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
gamefont = pygame.font.Font('gallery/sprites/04B_19.ttf',40)
#game variables
gravity = 0.15
birdMovement = 0
game_active = True
score = 0
point_score = 1




background = pygame.image.load('gallery/sprites/background.jpg')
background = pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))

base = pygame.image.load('gallery/sprites/base.png')
base = pygame.transform.scale2x(base)
baseX =0

bird = pygame.image.load('gallery/sprites/aircraft.png')
bird_rect = bird.get_rect(center = (50,300))

pipe_surface = pygame.image.load('gallery/sprites/slimPipe.png')

pipelist = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 2000)
pipe_height=[200,300,400]

gameover_surface = pygame.image.load('gallery/sprites/gameover.png')
gameover_surface = pygame.transform.scale(gameover_surface,(SCREEN_WIDTH,SCREEN_HEIGHT))
gameover_rect = gameover_surface.get_rect(topleft = (0,0))

#sounds
flap = 'gallery/sounds/flap.mp3'
hit = 'gallery/sounds/hit.mp3'
point = 'gallery/sounds/point.mp3'
swoosh = 'gallery/sounds/swoosh.mp3'
die = 'gallery/sounds/die.mp3'


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and game_active:
                birdMovement = 0
                birdMovement -= 5
                pygame.mixer.music.load(swoosh)
                pygame.mixer.music.play()
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and game_active == False:
                game_active = True
                score = 0
                point_score=1
                pipelist =[]
                birdMovement = 0
                bird_rect.center = (50  ,250)

        if event.type == SPAWNPIPE:
            pipelist.extend(create_pipe())


    #background

    screen.blit(background,(0,0))

    if game_active:
        #bird movement
        birdMovement +=gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery +=birdMovement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipelist)

        # pipes
        pipelist = move_pipes(pipelist)
        draw_pipes(pipelist)
        score += 0.01
        if score>point_score:
            pygame.mixer.music.load(point)
            pygame.mixer.music.play()
            point_score+=1

        score_display('Main_Game')



        # base floor
        baseX -= 2
        drawFloor()
        if baseX <= -SCREEN_WIDTH:
            baseX = 0
    else:
        update_score(score)
        screen.blit(gameover_surface, gameover_rect)
        score_display('Game_Over')

    pygame.display.update()
    clock.tick(120)


