import pygame as pg
import random
#Initialize pygame
pg.init()
#Set Display Surface

WINDOW_WIDTH=1000
WINDOW_HEIGHT=400
display_surface = pg.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pg.display.set_caption('FEED THE DRAGON')
#Set FPS and clock
FPS=60
clock=pg.time.Clock()
#Set game values
PLAYER_STARTING_LIVES=100
PLAYER_VELOCITY=5
COIN_STARTING_VELOCITY=5
COIN_ACCELERATING_VELOCITY=2
BUFFER_DISTANCE=100
score=0
player_lives=PLAYER_STARTING_LIVES
coin_velocity=COIN_STARTING_VELOCITY
#Set colours
GREEN=(0,255,0)
DARKGREEN=(10,50,10)
WHITE=(255,255,255)
BLACK=(0,0,0)
#Set Fonts
font=pg.font.Font('AttackGraffiti.ttf',32)
#Set text
score_text=font.render("Score: "+str(score),True,GREEN,DARKGREEN)
score_rect=score_text.get_rect()
score_rect.topleft=(10,10)

title_text=font.render("Feed the Dragon",True,GREEN,WHITE)
title_rect=title_text.get_rect()
title_rect.centerx=WINDOW_WIDTH/2
title_rect.y=10

lives_text=font.render("Lives: "+str(player_lives),True,GREEN,DARKGREEN)
lives_rect=lives_text.get_rect()
lives_rect.topright=(WINDOW_WIDTH-10,10)

game_over_text=font.render("GAMEOVER",True,GREEN,DARKGREEN)
game_over_rect=game_over_text.get_rect()
game_over_rect.center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2)

continue_text=font.render("Press any key to play again",True,GREEN<DARKGREEN)
continue_rect=continue_text.get_rect()
continue_rect.center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2 + 32)
#Set sounds and music
coin_sound=pg.mixer.Sound('coin_sound.wav')
miss_sound=pg.mixer.Sound("miss_sound.wav")
miss_sound.set_volume(0.1)
pg.mixer.music.load("ftd_background_music.wav")
#Set images
player_image=pg.image.load("dragon_right.png")
player_rect=player_image.get_rect()
player_rect.left=32
player_rect.centery=WINDOW_HEIGHT/2

coin_image=pg.image.load("coin.png")
coin_rect=coin_image.get_rect()
coin_rect.x=WINDOW_WIDTH+BUFFER_DISTANCE
coin_rect.y=random.randint(64,WINDOW_HEIGHT-32)
#The main game loop
pg.mixer.music.play(-1,0.0)
running=True
while running:
    #Does user want to Quit
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=False
    #Check to see if the user wants to move
    keys=pg.key.get_pressed()
    if keys[pg.K_UP] and player_rect.top>64:
        player_rect.y-=PLAYER_VELOCITY
    if keys[pg.K_DOWN] and player_rect.bottom<WINDOW_HEIGHT:
        player_rect.y+=PLAYER_VELOCITY
    #Move the coin
    if coin_rect.x<0:
        player_lives-=1
        miss_sound.play()
        coin_rect.x=WINDOW_WIDTH+BUFFER_DISTANCE
        coin_rect.y=random.randint(64,WINDOW_HEIGHT-32)
    else:
        #Move the coin
        coin_rect.x-=coin_velocity
    #Check for Collision
    if player_rect.colliderect(coin_rect):
        score+=1
        coin_sound.play()
        if coin_velocity<60:
            coin_velocity+=COIN_ACCELERATING_VELOCITY
        coin_rect.x=WINDOW_WIDTH+BUFFER_DISTANCE
        coin_rect.y=random.randint(64,WINDOW_HEIGHT-32)
    #Update HUD
    score_text=font.render("Scores: "+str(score),True,GREEN,DARKGREEN)
    lives_text=font.render("Lives: "+str(player_lives),True,GREEN,DARKGREEN)
    #Check for game over
    if player_lives==0:
        display_surface.blit(game_over_text,game_over_rect)
        display_surface.blit(continue_text,continue_rect)
        pg.display.update()
    #Pause the game until player presses a key,then reset the game
        pg.mixer.stop()
        is_paused=True
        while is_paused:
            for event in pg.event.get():
                #The player wants to play again
                if event.type==pg.KEYDOWN:
                    score=0
                    player_lives= PLAYER_STARTING_LIVES
                    player_rect.y=WINDOW_HEIGHT/2
                    coin_velocity=COIN_STARTING_VELOCITY
                    pg.mixer.music.play(-1,0.0)
                    is_paused=False
                #The player wants to quit
                if event.type==pg.QUIT:
                    is_paused=False
                    running=False
    #Fill the display
    display_surface.fill((0,0,0))
    #Blit the HUD to screen
    display_surface.blit(score_text,score_rect)
    display_surface.blit(title_text,title_rect)
    display_surface.blit(lives_text,lives_rect)
    pg.draw.line(display_surface,WHITE,(0,64),(WINDOW_WIDTH,64),2)

    #Blit the assets to screen
    display_surface.blit(player_image,player_rect)
    display_surface.blit(coin_image,coin_rect)
    
    #Update display and tick the clock
    pg.display.update()
    clock.tick(FPS)
pg.quit()