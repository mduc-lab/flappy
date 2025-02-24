import pygame
import sys
import random

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()

game_font = pygame.font.Font('flappy/04B_19.TTF',40)
score = 0
high_score = 0
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
gravity = 0.25
bird_movement = 0
bg=pygame.image.load('C:/Users/nmd14/Python/flappy/assets/background-night.png')
bg=pygame.transform.scale(bg,(432,768))
#tao floor
floor = pygame.image.load('C:/Users/nmd14/Python/flappy/assets/floor.png')
floor = pygame.transform.scale(floor,(432,168))
floor_x_pos = 0
#tao chim
bird = pygame.image.load('flappy/assets/yellowbird-midflap.png')
bird = pygame.transform.scale(bird,(50,50))
bird_rect = bird.get_rect(center = (100,384))

#tao ong
pipe_list = []
pipe_height = [200,300,400,500,600]
game_active = True

flap_sound = pygame.mixer.Sound('flappy/sound/sfx_wing.wav')
colision_sound = pygame.mixer.Sound('flappy/sound/sfx_hit.wav')

#ham tao ong
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe.get_rect(midtop=(500,random_pipe_pos))
    top_pipe = pipe.get_rect(midbottom=(500,random_pipe_pos-200))
    return top_pipe, bottom_pipe

#ham di chuyen ong
def move_pipe(pipes):
    for pipe in pipes:
        pipe[0].centerx -= 5
        pipe[1].centerx -= 5
    return pipes

#ham va cham
def check_colision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
            #print("va cham")
            colision_sound.play()
            return False
        if bird_rect.top <= -100 or bird_rect.bottom >= 600:
            #print("ra ngoai")
            colision_sound.play()
            return False

    return True

def score_display(score):
    score_surface = game_font.render(f"Score: {score}",True,(255,255,255))
    score_rect = score_surface.get_rect(center = (216,50))
    screen.blit(score_surface,score_rect)

pipe = pygame.image.load('flappy/assets/pipe-green.png')
pipe = pygame.transform.scale(pipe,(100,600))  # chieu cao ong

#tao man hinh ket thuc
game_over_surface = pygame.image.load('C:/Users/nmd14/Python/flappy/assets/gameover.png')
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (216,384))


#tao timer
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe,1200) # 1200ms = 1.2s tao ra ong moi



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_movement = 0
        if event.type == spawn_pipe:
            pipe_list.append(create_pipe())
    #hinh nen
    screen.blit(bg,(0,0))

    if game_active:
        #chim
        bird_movement += gravity
        bird_rect.centery += bird_movement

        bird_rotated = pygame.transform.rotozoom(bird,-bird_movement*3,1)

        screen.blit(bird_rotated,bird_rect)

        game_active = check_colision(pipe_list)

        #ong        
        pipe_list = move_pipe(pipe_list)
        for x in pipe_list:
                screen.blit(pipe,x[1])
                flip_pipe = pygame.transform.flip(pipe,False,True)
                screen.blit(flip_pipe,x[0])
        score = len(pipe_list)
    else:
        screen.blit(game_over_surface,game_over_rect)
    
    score_display(score)
    #floor
    if floor_x_pos <= -432:
        floor_x_pos = 0
    floor_x_pos -= 1
    screen.blit(floor,(floor_x_pos,600))
    screen.blit(floor,(floor_x_pos+432,600))

    pygame.display.update()
    clock.tick(50)
