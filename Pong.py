#imports pygame and random and mixer for sounds
import pygame
import random
from pygame import mixer
#initializes pygame
pygame.init()

#makes width and heights and sets screen size
width = 1200
height = 800
screen = pygame.display.set_mode((width, height))

#sets up sounds
mixer.init()
pygame.mixer.Channel(0).play(pygame.mixer.Sound('background.mp3'), -1)

#gets the clock so it can limit to 60
clock = pygame.time.Clock()

#define rects for the game
ball = pygame.Rect(585, 385, 30, 30)
player = pygame.Rect(1160, 320, 20, 160)
opponent = pygame.Rect(20, 320, 20, 160)

#different speeds and difficulties
xSpeed = 15
ySpeed = 0
maxY = 15
minY = -15

playerSpeed = 10
difficulty1 = 10
difficulty2 = 12
difficulty3 = 15
opponentSpeed = 0

#scores
playerScore = 0
opponentScore = 0

#fonts
font = pygame.font.SysFont(None, 80)


#difficulty level (1-3)
difficulty = 1

#variables to see if game started, to see if up and down are being pressed or not
playing = True

up = False
down = False

started = False

#main loop while playing
while (playing):
    
    #KEY INPUTS
    for event in pygame.event.get():
        #quits game
        if (event.type == pygame.QUIT):
            playing = False
        #if up or down is pressed, updates variables
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_UP):
                up = True
            if (event.key == pygame.K_DOWN):
                down = True
            if (event.key == 13):
                #if pressed enter, start game
                if (started == False):
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound('click.mp3'))
                    started = True
        if (event.type == pygame.KEYUP):
            if (event.key == pygame.K_UP):
                up = False
            if (event.key == pygame.K_DOWN):
                down = False
        # gets mouse button down to see if arrows to change diffiiculty are pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            #gets mouse position
            pos = pygame.mouse.get_pos()
            #if position is within arrow keys, increase/decrease difficulty level
            if (pos[1] > 184 and pos[1] < 224):
                if (pos[0] > 831 and pos[0] < 877 and difficulty < 3):
                    difficulty += 1
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound('click.mp3'))
                if (pos[0] > 309 and pos[0] < 354 and difficulty > 1):
                    difficulty -= 1
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound('click.mp3'))

                    
    #if down/up is held, move player by player speed and limit to screen            
    if (down and player.bottom < 790):
        player.y += playerSpeed
    if (up and player.top > 10):
        player.y -= playerSpeed
        
    #if the round started
    if (started):
        #moves the ball
        ball.x += xSpeed
        ball.y += ySpeed
        #makes speed negative if it bounces
        if (ball.top <= 0 or ball.bottom >= 800):
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('bounce.mp3'))
            ySpeed *= -1
      
        #if it collides with player, changes speed and makes it negative
        if (ball.colliderect(player) or ball.colliderect(opponent)):
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('bounce.mp3'))
            ySpeed = random.randint(minY, maxY)
            xSpeed *= -1

    #adds score and resets up game if ball goes off screen and plays sounds
    if (ball.left > 1200):
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('score.mp3'))
        opponentScore += 1
        started = False
        ball.x = 585
        ball.y = 385
        ySpeed = 0
        xSpeed = 15
        player.y = 320
    if (ball.right < 0):
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('score.mp3'))
        playerScore += 1
        started = False
        ball.x = 585
        ball.y = 385
        ySpeed = 0
        xSpeed = 15
        player.y = 320
           
           
    #changes opponent speeds based on difficulty selected
    if (difficulty == 3):
        opponentSpeed = difficulty3   
    elif (difficulty == 2):
        opponentSpeed = difficulty2
    elif (difficulty == 1):
        opponentSpeed = difficulty1

    #moves opponent in direction of ball by checking the balls y position and moving accordingly
    wantedY = ball.y - 65
    if (opponent.y > (wantedY + 70)):
        opponent.y -= opponentSpeed
    elif (opponent.y < (wantedY - 70)):
        opponent.y += opponentSpeed
    if (opponent.bottom > 790):
        opponent.bottom = 790
    if (opponent.top < 10):
        opponent.top = 10
    
    #fill screen orange
    screen.fill((255, 165, 0))
    
    #draws all the lines, balls, players
    pygame.draw.line(screen, (0, 0, 0), (600, 0), (600, 800))
    pygame.draw.ellipse(screen, (0, 0, 0), ball)
    pygame.draw.rect(screen, (0, 0, 0), player)
    pygame.draw.rect(screen, (0, 0, 0), opponent)
    
    #draws scores
    score1 = font.render(str(playerScore), True, (0,0,0))
    screen.blit(score1, (1150, 750))
    score2 = font.render(str(opponentScore), True, (0,0,0))
    screen.blit(score2, (20, 750))

    
    #draws instructions + difficulties after round ends
    if (started == False):
        txt1 = font.render('PRESS ENTER TO RELEASE THE BALL', True, (0,0,0))
        screen.blit(txt1, (50, 20))
        txt2 = font.render('USE ARROW KEYS TO MOVE PADDLE', True, (0,0,0))
        screen.blit(txt2, (65, 100))
        txt3 = font.render('DIFFICULTY: %d'%difficulty, True, (0,0,0))
        screen.blit(txt3, (400, 180))
        #draws arrows using polygons
        pygame.draw.polygon(screen, (0, 0, 0), ((841, 224), (867, 224), (867, 198), (877, 198), (854, 184), (831, 198), (841, 198)))
        pygame.draw.polygon(screen, (0, 0, 0), ((319, 184), (344, 184), (344, 210), (354, 210), (332, 224), (309, 210), (319, 210)))

    
    #updates display
    pygame.display.flip()
    
    #limits to 60
    clock.tick(60)

#quit pygame
pygame.quit()

