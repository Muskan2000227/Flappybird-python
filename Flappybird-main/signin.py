#Signup,Login,random players,background change,display score,display high score,
#Pause or Resume
from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import cx_Oracle
import pygame
from pygame.locals import *
import pygame.font  

# Define a function to start the game
def start_game():
    LoginPage.destroy()
    
    # random player colors,display score,pause or resume,change background
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


swap_count = 0


#Signup page
def Signup():

    def clear():
        emailEntry.delete(0, END)
        UsernameEntry.delete(0, END)
        PasswordEntry.delete(0, END)
        confirmpasswordEntry.delete(0, END)
        check.set(0)

    def login_page():
        Signup.destroy()
        Login()

    def connect_database():
        if emailEntry.get() == '' or UsernameEntry.get() == '' or PasswordEntry.get() == '' or confirmpasswordEntry.get() == '':
            messagebox.showerror('Error', 'All Fields are Required')
        elif PasswordEntry.get() != confirmpasswordEntry.get():
            messagebox.showerror('Error', 'Password mismatch')
        elif '@' and '.com' not in emailEntry.get():
            messagebox.showinfo('Error', 'Enter valid email\n For example-abc@gmail.com,abc@yahoo.com')
        elif check.get() == 0:
            messagebox.showerror('Error', 'Please accept our terms and services')
        else:
            conn = cx_Oracle.connect(user='airline', password='mmmk')
            cur = conn.cursor()
            # if user already exists
            query = f"select * from data where username=:1"
            cur.execute(query, (UsernameEntry.get(),))
            row = cur.fetchone()
            if row != None:
                messagebox.showerror('Error', 'User already exists,Please change your username')
            else:
                # to insert new user
                a = f"insert into data(email,username,password) values('{emailEntry.get()}','{UsernameEntry.get()}','{PasswordEntry.get()}')"
                cur.execute(a)
                conn.commit()
                cur.close()
                conn.close()
                messagebox.showinfo('Success', 'You have successfully registered')
                clear()
                Signup.destroy()
                Login()
                #import signin

    # GUI part
    Signup = Tk()
    global swap_count
    swap_count += 1
    if swap_count > 10:
        Signup.destroy()
        return
    Signup.geometry("900x600+240+100")
    Signup.resizable(False, False)
    Signup.title("Signup Page")

    # Adding Image
    bgimg = ImageTk.PhotoImage(file='flog.png')
    bgLabel = Label(Signup, image=bgimg)
    bgLabel.place(x=0, y=0)

    # adding frame
    Frame_login = Frame(Signup, bg="white", highlightbackground='dark turquoise', highlightthickness=2, )
    Frame_login.place(x=490, y=60, height=500, width=350)
    # Adding labels and Entry fields for email
    # heading=Label(Signup,text='CREATE AN ACCOUNT',font=("Impact",28,"bold"),bg='deeppink',fg='grey1')
    heading = Label(Signup, text='SIGNUP', font=("Open Sans", 25, 'bold'), bg='white', fg='black')
    heading.place(x=600, y=100)

    # adding label and entry fiel for email
    emailEntry = StringVar()
    email = Label(Signup, text="Email", font=("RBNO2 Light Light", 12, 'bold'), fg="dark turquoise", bg="white")
    email.place(x=510, y=160)
    emailEntry = Entry(Signup, width=27, font=('Monotype', 11), bd=2, fg='black', bg="white", )
    emailEntry.place(x=540, y=190)

    # adding label and entry fiel for username
    UsernameEntry = StringVar()
    Username = Label(Signup, text="Username", font=("Open sans", 12, 'bold'), fg="dark turquoise", bg="white")
    Username.place(x=510, y=230)
    UsernameEntry = Entry(Signup, width=27, font=('Monotype', 11), bd=2, fg='black', bg="white")
    UsernameEntry.place(x=540, y=255)

    # aading label and entry fiel for Password
    PasswordEntry = StringVar()
    Password = Label(Signup, text="Password", font=("Open sans", 12, 'bold'), fg="dark turquoise", bg="white")
    Password.place(x=510, y=290)
    PasswordEntry = Entry(Signup, width=27, font=('Monotype', 11), bd=2, fg='black', bg="white", show='*')
    PasswordEntry.place(x=540, y=315)

    # aading label and entry fiel for confirmPassword
    confirmpassword = Label(Signup, text="ConfirmPassword", font=("Open sans", 12, 'bold'), fg="dark turquoise",
                            bg="white")
    confirmpassword.place(x=510, y=350)
    confirmpasswordEntry = Entry(Signup, width=27, font=('Monotype', 11), bd=2, fg='black', bg="white", show='*')
    confirmpasswordEntry.place(x=540, y=380)

    # check Button
    check = IntVar()
    terms = Checkbutton(Signup, text='I agree to the Terms and Conditions',
                        font=('Microsoft Yahei UI Light', 11, 'bold'), fg='red',
                        bg='white', activebackground="white", activeforeground="red", cursor='hand2', variable=check)
    terms.place(x=500, y=410)

    # SignUp Button
    signupbutton = Button(Signup, text="Sign Up", font=('Microsoft Yahei UI Light', 12, 'bold'), bd=0, width=25,
                          fg="white", bg="dark turquoise",
                          activebackground="dark turquoise", activeforeground="white", cursor='hand2',
                          command=connect_database)
    signupbutton.place(x=520, y=460)

    # label and login button
    alreadyaccount = Label(Signup, text="Already Have an account?", font=("Open Sans", 11, "bold"), bg='white',
                           fg='red')
    alreadyaccount.place(x=520, y=520)
    Loginbutton = Button(Signup, text='Login', font=('Open Sans', 9, 'bold underline'), bd=0, fg='blue', bg='white',
                         activeforeground='blue',
                         activebackground='white', cursor='hand2', width=10, command=login_page)
    Loginbutton.place(x=720, y=520)

    Signup.mainloop()

#Login function
def Login():

 def clear():
    usernameEntry.delete(0,END)
    password.delete(0,END)


 def Login_user():
    if usernameEntry.get()=='' or password.get()=='':
        messagebox.showerror('Error','All fields are required')
    elif usernameEntry.get()=='Username' or password.get()=='Password':
        messagebox.showerror('Error', 'All fields are required')
    else:
        conn=cx_Oracle.connect(user='airline',password='mmmk')
        cur=conn.cursor()
        query="select * from data where username=:1 and password=:2"
        cur.execute(query,(usernameEntry.get(),password.get()))

        row=cur.fetchone()
        if row==None:
            messagebox.showerror('Error', 'Invalid Username or Password')
            clear()
        else:
            messagebox.showinfo('Success', 'Login Successful')
            start_game()



 def on_userentry(event):
    if usernameEntry.get()=='Username':
        usernameEntry.delete(0,END)
 def on_passentry(event):
    if password.get()=='Password':
        password.delete(0,END)
 def hide():
    openeye.config(file='m.png')
    password.config(show='*')
    eyeButton.config(command=show)

 def show():
    openeye.config(file='mm.png')
    password.config(show='')
    eyeButton.config(command=hide)

 def signup_page():
     LoginPage.destroy()
     Signup()


#GUI Part
 global LoginPage
 LoginPage=Tk()
 global swap_count
 swap_count += 1
 if swap_count > 10:
     LoginPage.destroy()
     return
 LoginPage.geometry("900x600+240+100")
 LoginPage.resizable(False,False)
 LoginPage.title("Login Page")
 p1=PhotoImage(file="login.png")    #icon
 LoginPage.iconphoto(False,p1)

#Placing Image
 bgImage=ImageTk.PhotoImage(file="flog.png")
 bgLabel=Label(LoginPage,image=bgImage)
 bgLabel.place(x=0,y=0)

#Adding Frame
 Frame_login=Frame(LoginPage,bg="white",highlightbackground='dark turquoise',highlightthickness=2)
 Frame_login.place(x=490,y=70,height=470,width=350)
#Adding Label
 heading=Label(LoginPage,text='LOGIN PAGE',font=("Impact",30),bg='white',fg='black')
 heading.place(x=550,y=100)

#Entry Field for username
 usernameEntry=Entry(LoginPage,width=27,font=('Microsoft Yahei UI Light',11,'bold'),bd=0,fg='dark turquoise')
 usernameEntry.place(x=530,y=200)
 usernameEntry.insert(0,'Username')
#frame for line
 usernameEntry.bind('<FocusIn>',on_userentry)
 Frame(LoginPage,width=250,height=2,bg='dark turquoise').place(x=530,y=222)

#Entry field for password
 password=Entry(LoginPage,width=27,font=('Microsoft Yahei UI Light',11,'bold'),bd=0,fg='dark turquoise')
 password.place(x=530,y=280)
 password.insert(0,'Password')
 password.bind('<FocusIn>',on_passentry)
 Frame(LoginPage,width=250,height=2,bg='dark turquoise').place(x=530,y=305)

#Eye Button
 openeye=PhotoImage(file='mm.png')
 eyeButton=Button(LoginPage,image=openeye,bd=0,bg='white',activebackground='white',cursor='hand2',command=hide)
 eyeButton.place(x=750,y=280)

#Forget Button
#ForgetButton=Button(LoginPage,text='Forgot Password?',bd=0,bg='white',fg='red',font=('Microsoft Yahei UI Light',9,'bold underline'),activebackground='white',activeforeground='red',cursor='hand2')
#ForgetButton.place(x=700,y=320)

#Login Button
 LoginButton=Button(LoginPage,text='Login',font=('Open Sans',16,'bold'),bd=0,fg='white',bg='dark turquoise',activeforeground='white',
                   activebackground='dark turquoise',cursor='hand2',width=19,command=Login_user)
 LoginButton.place(x=540,y=385)

#Signup
 signuplabel=Label(LoginPage,text="Don't have an Account?",font=("Open Sans",11,"bold"),bg='white',fg='red')
 signuplabel.place(x=520,y=480)
 newaccountbutton=Button(LoginPage,text='Create new Account',font=('Open Sans',9,'bold underline'),bd=0,fg='blue',bg='white',activeforeground='blue',
                   activebackground='white',cursor='hand2',width=19,command=signup_page)
 newaccountbutton.place(x=690,y=480)

 LoginPage.mainloop()


Signup()
#Login()



