#,random players,background change,display score,display high score,
#Pause or Resume
from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import cx_Oracle
import pygame
from pygame.locals import *
import pygame.font  
import random  # generating random pipes
import sys  # will use sys.exit
import pygame
import pygame.locals  
#from pygame import *
import cx_Oracle
conn = cx_Oracle.connect("airline/mmmk")
cur = conn.cursor()
print(conn.version)
"""try:
        cur.execute('''CREATE TABLE scor (
                            score NUMBER
                        )''')
        conn.commit()
        print("Scores table created successfully.")
except cx_Oracle.Error as e:
        print("Error creating scores table:", e)"""

# GLobal Variables for game
FPS = 32  # (frames per second)
SCREENWIDTH = 500
SCREENHEIGHT = 500
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))  # make display surface(initialize screen)
GROUNDY = SCREENHEIGHT * 0.8  # 80% of screen to ground
GAME_SPRITES = {}  # Images
GAME_SOUNDS = {}  # Sounds
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'
GAME_SPRITES['gameover'] = pygame.image.load('gallery/sprites/bird.png').convert_alpha()
BIRD_COLORS = ['red', 'blue', 'green', 'yellow']  # Add more colors as needed
    

def welcomeScreen():
        '''
        Shows welcome images on the screen
        '''
        playerx = int(SCREENWIDTH / 5)
        playery = float((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 1.5)
        messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
        messagey = int(SCREENHEIGHT * 0.13)
        basex = 0
        while True:
            for event in pygame.event.get():
                # Press cross button to close the game
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                # press space or up key to start the game
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    return
                else:
                    SCREEN.blit(GAME_SPRITES['background'], (0, 0))  # blit means place image on screen
                    SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                    SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                    SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)

   

def gameOverScreen(score):
        gameoverx = int(SCREENWIDTH / 8)
        gameovery = int(SCREENHEIGHT / 3)
        scorex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width() / 5))
        scorey = int(SCREENHEIGHT * 0.4)

        font = pygame.font.Font(None, 50)  # None uses the default font, and 50 is the font size
        text = font.render("Your Score is:", True, (0, 0, 255))  # Render the score as text
        text_rect = text.get_rect()
        text_rect.center = (250, 250)
        insert_score(score)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    return

            # Display game over message and background
            SCREEN.blit(GAME_SPRITES['background'], (0, 0))
            SCREEN.blit(GAME_SPRITES['gameover'], (gameoverx, gameovery))

            # Blit the text onto the screen
            SCREEN.blit(text, text_rect)

            # Display final score
            score_str = str(score)
            score_width = len(score_str) * GAME_SPRITES['numbers'][0].get_width()
            score_x = (SCREENWIDTH - score_width) / 1.2
            for digit_char in score_str:
                digit = int(digit_char)
                score_display = GAME_SPRITES['numbers'][digit]
                SCREEN.blit(score_display, (score_x, scorey + text.get_height()))
                score_x += GAME_SPRITES['numbers'][0].get_width()

            # Create and render the "GAME OVER" message
            additional_text = font.render("GAME OVER", True, (255, 0, 0))

            # Position the additional line of text on the screen
            additional_text_rect = additional_text.get_rect()
            additional_text_rect.center = (SCREENWIDTH // 2, SCREENHEIGHT * 0.2)  # Adjust the position as needed

            # Blit the additional line of text onto the screen
            SCREEN.blit(additional_text, additional_text_rect)

            font1 = pygame.font.Font(None, 36)
            additional_text = font1.render("Restart by pressing tab or uparrow key", True, (255, 0, 0))

            # Position the additional line of text on the screen
            additional_text_rect = additional_text.get_rect()
            additional_text_rect.center = (SCREENWIDTH // 2, SCREENHEIGHT * 0.9)  # Adjust the position as needed

            # Blit the additional line of text onto the screen
            SCREEN.blit(additional_text, additional_text_rect)

            # Calculate the high score
            high_score = getHighScore()
            # Display the high score on the screen
            displayHighScore(high_score)
            pygame.display.update()

            FPSCLOCK.tick(FPS)

def insert_score(score):
        try:
            cur.execute("INSERT INTO scor (score) VALUES (:score)", {"score": score})
            conn.commit()
            print("Score inserted successfully.")
        except cx_Oracle.Error as e:
            print("Error inserting score:", e)

def getHighScore():
        try:
            cur.execute("SELECT MAX(score) FROM scor")
            result = cur.fetchone()
            if result:
                return result[0]
        except cx_Oracle.Error as e:
            print("Error fetching high score:", e)
        return 0  # Return 0 if there's an error or no high score found

def displayHighScore(high_score):
        font = pygame.font.Font(None, 36)
        high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 255))
        high_score_rect = high_score_text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT * 0.8))
        SCREEN.blit(high_score_text, high_score_rect)

def mainGame():

        score = 0
        playerx = int(SCREENWIDTH / 5)
        playery = int(SCREENWIDTH / 2)
        basex = 0
        game_paused = False
        

        bird_colors = ['red', 'blue', 'green', 'yellow']
        bird_color = random.choice(bird_colors)
        # change background
        current_background = 'gallery/sprites/background.png'  # Initialize the background
        # background_change_score = 7
        # Create 2 pipes for blitting on the screen
        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()

        # my List of upper pipes
        upperPipes = [
            {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]
        # my List of lower pipes
        lowerPipes = [
            {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        pipeVelX = -4 

        playerVelY = -9
        playerMaxVelY = 10
        playerMinVelY = -8
        playerAccY = 1

        playerFlapAccv = -8  # velocity while flapping
        playerFlapped = False  # It is true only when the bird is flapping

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE or event.key == K_UP:
                        if playery > 0 and not game_paused:
                            playerVelY = playerFlapAccv
                            playerFlapped = True
                            GAME_SOUNDS['wing'].play()
                    elif event.key == K_p:  # Press "P" to pause/resume the game
                        game_paused = not game_paused  # Toggle the pause state

            if not game_paused:

                crashTest = isCollide(playerx, playery, upperPipes,
                                      lowerPipes)  # This function will return true if the player is crashed
                if crashTest:
                    gameOverScreen(score)
                    return

                    # check for score
                playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
                for pipe in upperPipes:
                    pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
                    if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                        score += 1
                        #print(f"Your score is {score}")
                        GAME_SOUNDS['point'].play()

                if playerVelY < playerMaxVelY and not playerFlapped:
                    playerVelY += playerAccY

                if playerFlapped:
                    playerFlapped = False
                playerHeight = GAME_SPRITES['player'].get_height()
                playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

                # move pipes to the left
                for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                    upperPipe['x'] += pipeVelX
                    lowerPipe['x'] += pipeVelX

                # Add a new pipe when the first is about to cross the leftmost part of the screen
                if 0 < upperPipes[0]['x'] < 5:
                    newpipe = getRandomPipe()
                    upperPipes.append(newpipe[0])
                    lowerPipes.append(newpipe[1])

                # if the pipe is out of the screen, remove it
                if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
                    upperPipes.pop(0)
                    lowerPipes.pop(0)
                
                # Lets blit our sprites now
                # Update the background based on the player's score
                if score > 10 and score < 20:
                    current_background = 'gallery/sprites/back.png'  # Change to the next background

                elif score > 20:
                    current_background = 'gallery/sprites/save3.png'
                    # Load and blit the background image
                background_image = pygame.image.load(current_background).convert()
                SCREEN.blit(background_image, (0, 0))
                for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                    SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                    SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                SCREEN.blit(GAME_SPRITES[f'player_{bird_color}'], (playerx, playery))

                myDigits = [int(x) for x in list(str(score))]
                width = 0
                for digit in myDigits:
                    width += GAME_SPRITES['numbers'][digit].get_width()
                Xoffset = (SCREENWIDTH - width) / 2

                for digit in myDigits:
                    SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
                    Xoffset += GAME_SPRITES['numbers'][digit].get_width()
                font1 = pygame.font.Font(None, 36)
                additional_text = font1.render("PRESS 'P' to Pause or Resume", True, 'blue')

                # Position the additional line of text on the screen
                additional_text_rect = additional_text.get_rect()
                additional_text_rect.center = (SCREENWIDTH // 2, SCREENHEIGHT * 0.9)  # Adjust the position as needed

                # Blit the additional line of text onto the screen
                SCREEN.blit(additional_text, additional_text_rect)
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
        if playery > GROUNDY - 25 or playery < 0:
            GAME_SOUNDS['hit'].play()
            return True

        for pipe in upperPipes:
            pipeHeight = GAME_SPRITES['pipe'][0].get_height()
            if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
                GAME_SOUNDS['hit'].play()
                return True

        for pipe in lowerPipes:
            if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < \
                    GAME_SPRITES['pipe'][0].get_width():
                GAME_SOUNDS['hit'].play()
                return True

        return False

def getRandomPipe():
        """
        Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
        """
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        offset = SCREENHEIGHT / 3
        y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
        pipeX = SCREENWIDTH + 10
        y1 = pipeHeight - y2 + offset
        pipe = [
            {'x': pipeX, 'y': -y1},  # upper Pipe
            {'x': pipeX, 'y': y2}  # lower Pipe
        ]
        return pipe

if __name__ == "__main__":
        # this will be main function where game will start
        pygame.init()  # initialize pygame modules
        FPSCLOCK = pygame.time.Clock()  # control fps
        pygame.display.set_caption('FLAPPY BIRD GAME')
        GAME_SPRITES['player_red'] = pygame.image.load('gallery/sprites/player_red.png').convert_alpha()
        GAME_SPRITES['player_blue'] = pygame.image.load('gallery/sprites/player_blue.png').convert_alpha()
        GAME_SPRITES['player_green'] = pygame.image.load('gallery/sprites/player_green.png').convert_alpha()
        GAME_SPRITES['player_yellow'] = pygame.image.load('gallery/sprites/player_yellow.png').convert_alpha()
        GAME_SPRITES['numbers'] = (
            pygame.image.load('gallery/sprites/0.png').convert_alpha(),
            pygame.image.load('gallery/sprites/1.png').convert_alpha(),
            pygame.image.load('gallery/sprites/2.png').convert_alpha(),
            pygame.image.load('gallery/sprites/3.png').convert_alpha(),
            pygame.image.load('gallery/sprites/4.png').convert_alpha(),
            pygame.image.load('gallery/sprites/5.png').convert_alpha(),
            pygame.image.load('gallery/sprites/6.png').convert_alpha(),
            pygame.image.load('gallery/sprites/7.png').convert_alpha(),
            pygame.image.load('gallery/sprites/8.png').convert_alpha(),
            pygame.image.load('gallery/sprites/9.png').convert_alpha(),
        )

        GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/flapp.png').convert_alpha()
        GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
        GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                                pygame.image.load(PIPE).convert_alpha()
                                )

        GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
        GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
        GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
        GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
        GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

        GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
        GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

        while True:
            welcomeScreen()  # shows welcome screen until button is pressed
            mainGame()  # this is main game function




