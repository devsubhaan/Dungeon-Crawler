#Imports
import tkinter as tk
import sqlite3 as sql
import hashlib as hl
import pygame


#Class Imports
from game import Game 

#Main
maintitle = "2D dungeon crawler" #The name of the game (displayed on the window tab)
userData = None #This is where the users data would be stored so it can be accessed by the program.

GAMEWIDTH = 800 #Initialises both the height and width of the game screens
GAMEHEIGHT = 600

MAINWIDTH = 800   #Initialises both the height and width of the main menu screen
MAINHEIGHT = 800

volume = 50
move_up = "w"
move_down = "s"
move_left = "a"
move_right = "d"

def maingame():
    maingame = Game(GAMEWIDTH,GAMEHEIGHT, move_up, move_down, move_right, move_left, volume, userData) #The game file is a class, so it has to be initialised for it to work
    maingame.run() #The game is run

    mainmenu() #When the loop of the game is terminated (the program is exited) the main menu reappears.
    #To exit the program you must click 'exit' or the 'X' button on the window in the main menu.

def mainmenu():
    #Tkinter Initialisation
    root = tk.Tk()

    def toggleFullscreen():
        root.attributes("-fullscreen", not root.attributes("-fullscreen"))

    #binds f11 key to toggle full screen
    root.bind("<F11>", lambda e: toggleFullscreen()) 
    root.geometry(str(MAINWIDTH)+"x"+str(MAINHEIGHT)) 
    #Tkinter requires the window dimensions to be a string like (500x500), converting the dimensions to a string allows it to be dassed through
    root.title(maintitle) #Puts the maintitle (the name of the game) on the window tab.



    pygame.mixer.init()
    pygame.mixer.music.load(r"Assets\Sounds\MainMenuMusic.mp3")
    pygame.mixer.music.set_volume(volume / 100)  # Use your volume variable
    pygame.mixer.music.play(-1)

    uiclicksound = pygame.mixer.Sound(r"Assets\Sounds\UIClick.wav")
    uiclicksound.set_volume(volume / 100)


    def create_frame():
        frame = tk.Frame(root, bg = "black")
        frame.place(relwidth=1, relheight=1)
        
        ##bgImage = tk.PhotoImage(file=r"Assets\Main Menu\background.png")
        #bg_label = tk.Label(frame, image=bgImage, bg = "black")
        #bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        #bg_label.image = bgImage

        return frame
    
    #Frames
    #each one of these initialises the frames for each section of the main menu
    #Using tk.raise() puts the wanted frame on top and hides the others which is how you can traverse through menus.
    mainmenuframe = create_frame()  
    loginframe = create_frame()  
    signupframe = create_frame()  
    settingsframe = create_frame() 
    validationframe = create_frame() 
    controlframe = create_frame()
    objectiveframe = create_frame()

    #Menu button images
    #These are the images created in a wireframe. 
    #Each is assigned to a variable and is used later on to replace the buttons.
    welcomeimage = tk.PhotoImage(file= r"Assets\Main Menu\Welcome.png") 
    loginimage = tk.PhotoImage(file= r"Assets\Main Menu\Log in.png")
    signupimage = tk.PhotoImage(file= r"Assets\Main Menu\Sign up.png")
    settingsimage = tk.PhotoImage(file= r"Assets\Main Menu\Settings.png")
    playimage = tk.PhotoImage(file= r"Assets\Main Menu\Play.png")
    exitimage = tk.PhotoImage(file= r"Assets\Main Menu\Exit.png")

    #Login/Signup images
    #Images are also used here for the same purpose as above.
    logintextimage = tk.PhotoImage(file= r"Assets\Main Menu\LoginText.png")
    reenterpassword = tk.PhotoImage(file= r"Assets\Main Menu\reenterpassword.png")
    submitpassword = tk.PhotoImage(file= r"Assets\Main Menu\Submit.png")
    enterpassword = tk.PhotoImage(file= r"Assets\Main Menu\EnterPassword.png")   
    enterusername = tk.PhotoImage(file= r"Assets\Main Menu\EnterUsername.png")   
    signuptext = tk.PhotoImage(file= r"Assets\Main Menu\Signuptext.png")   
    returntomain = tk.PhotoImage(file= r"Assets\Main Menu\Return.png")     

    #Validation images
    validationTitle = tk.PhotoImage(file= r"Assets\Main Menu\ValidationTitle.png")   
    validationText  = tk.PhotoImage(file= r"Assets\Main Menu\SignUpValidation.png")  
    validationButton = tk.PhotoImage(file= r"Assets\Main Menu\ValidationButton.png")  

    #Settings menu images
    settings_title_image = tk.PhotoImage(file= r"Assets\Main Menu\settingstext.png")  

    #Controls screen images
    controlsTitle = tk.PhotoImage(file= r"Assets\Main Menu\ControlsTitle.png")
    controlsText = tk.PhotoImage(file= r"Assets\Main Menu\GameControls.png")
    controlsButtonImage = tk.PhotoImage(file= r"Assets\Main Menu\EnterControlsButton.png")

    #Objectives screen images
    objectivesTitle = tk.PhotoImage(file= r"Assets\Main Menu\ObjectivesTitle.png")
    objectivesText = tk.PhotoImage(file= r"Assets\Main Menu\GameObjectives.png")
    objectivesButtonImage = tk.PhotoImage(file= r"Assets\Main Menu\EnterObjectivesButton.png")
       

    #-Procedures

    #--Menu Traversal
    #These procedures (play() to exit()) are fired when their respective button is clicked
    def play():     
        uiclicksound.play()
        root.destroy() #Terminates the main menu screen and loads up the actual game.
        maingame()
    
    def login():
        uiclicksound.play()
        loginframe.tkraise() #Raises the login frame so that it is displayed to the user.

    def signup():
        uiclicksound.play()
        signupframe.tkraise() #Raises the signup frame so that it is displayed to the user.

    def settings():
        uiclicksound.play()
        settingsframe.tkraise() #Raises the settings frame so that it is displayed to the user.

    def exit():
        uiclicksound.play()
        root.destroy() #Terminates the main menu screen and doesnt load up the game. (Program exited)
    
    def validationScreen():
        uiclicksound.play()
        #raises frame
        validationframe.tkraise()
    
    def controlsScreen():
        uiclicksound.play()
        #raises frame
        controlframe.tkraise()
    
    def objectiveScreen():
        uiclicksound.play()
        #raises frame
        objectiveframe.tkraise()
    
    def returnToMainMenu():
        uiclicksound.play()
        mainmenuframe.tkraise()
    
    def returnToSettings():
        uiclicksound.play()
        settingsframe.tkraise()
    
    
        
    
    #--Database
    def submitsignin():
        uiclicksound.play()
        if signpassword.get() == signpassword2.get(): #Checks if both of the entered passwords are the same (this is a requirement)

            usernametext = signusername.get() #Assigns the given username and given password to a variable
            passwordtext = signpassword.get()

            #Initialises variables relevant to which criteria the password meets.
            hasNum = False  #True if there is a number
            hasSChar = False #True if theres a special character
            hasCapital = False #True if there is a capital
            isLong = False #True if the password is longer than 5 characters
            usernameSupport = False

            if not len(passwordtext) < 5: #Checks if the length of the password is not less than five (bigger than five)
                isLong = True #If the password is bigger than 5 characters in length, isLong becomes true

            for chr in passwordtext:
                if chr in ["1","2","3","4","5","6","7","8","9","0"]: #States all valid numbers to be used in the password
                    hasNum = True #The above statement also checks if theres a number in the list in the password
                    break   #hasNum becomes true if it has a number, it exits out of the loop if theres a number

            for chr in passwordtext:
                if not chr.isalnum():      #The method .isalnum() returns True if all characters are letters/numbers
                    hasSChar = True        #In the case that there is no special character, this will return false
                    break                  #Therefore the hasSChar variable will be false

            if not passwordtext == passwordtext.lower(): #Checks whether theres a capital letter 
                hasCapital = True #This is done by comparing the password to a form where its all non capital letters
            #If this statement is true, we know that it has a capital letter, so the variable becomes true
            if not isLong: #Fires if the password is not long enough.
                signerror.config(text="Password must be more than 5 characters.")
            elif not hasCapital: #Fires if the password does not have a capital letter
                signerror.config(text="Password must contain at least one uppercase letter.")
            elif not hasNum: #Fires if the password does not have a number
                signerror.config(text="Password must contain at least one number.")
            elif not hasSChar: #Fires if the password does not have a special character
                signerror.config(text="Password must contain at least one symbol\n(!, #, *, %, @, etc.).")
            
            for chr in usernametext:
                if not (chr.isalnum() or chr == "_"):  # accepts letters, numbers and underscores
                    usernameSupport = False
                    break

            # Or more concisely using all()
            usernameSupport = all(chr.isalnum() or chr == "_" for chr in usernametext)

            #Checks if all criteria are met
            if hasSChar and hasCapital and isLong and hasNum: 
            #If it has a special character, capital letter, >5 characters and has a number it will continue.
                if usernameSupport:
                    if len(usernametext) <=8 and len(usernametext) >=3: #These are the requirements for the username (has to be between or equal to 3 and 8)
                        connection = sql.connect("Assets\Database\mainDatabase.db") #Connects to the database (this is required in sqllite)
                        cursor = connection.cursor()

                        cursor.execute("SELECT * FROM player WHERE Username = ?", (usernametext,)) # Executes code which checks if the entered username is already taken
                        result = cursor.fetchone()

                        if result is None: #No result, meaning the username doesnt exist so it passes the unique username validation.
                            passencode = passwordtext.encode() #These three lines of code hash the password using the sha256 algorithm.
                            passobject = hl.sha256(passencode)
                            hashedpassword = passobject.hexdigest()

                            cursor.execute("""
                                INSERT INTO player (Username, Password) VALUES (?, ?)
                            """, (usernametext, hashedpassword))    #The variables are put in the places of the question marks (?)
                            #Executes the SQL code above, SQL injection is prevent with the use of (?)

                            connection.commit() #Makes changes to the SQLlite database

                            signusername.delete(0, tk.END) #Removes the text within the Tkinter field boxes
                            signpassword.delete(0, tk.END)  #This makes it so that upon pressing submit, field data is lost.
                            signpassword2.delete(0, tk.END)

                            connection.close() #closes the connection, this is neccessary for every database.

                            signerror.config(text=f"Successfully created account as {usernametext}\nYou can now log in!",fg="lime green") 
                            #Changes the displayed text to let the user know they have logged in
                        else:
                            #If result is not 'None' there is a same username in the database already
                            signerror.config(text=f"This username has already been taken!",fg="red") #It sends an error message to the user, letting them know.
                            connection.close() #The connection closes in the previous branch and not in this one, so we have to close it again.
                    else:
                        #If username length validation fails, it prints out the corresponding error message.
                        #The database was never defined before this statement so we do not need 'connection.close()'
                        signerror.config(text="Username between 3 and 8 characters!",fg="red")
                else:
                    signerror.config(text="Username must only include numbers\nunderscores and letters",fg="red")
            

        else:
            #Fires if both passwords arent the same, which is a validation requirement.
            signerror.config(text="Passwords are not the same!",fg="red")
    
    def submitlogin(): #Fired when the submit button is pressed on the login screen
        uiclicksound.play()
        global userData 
        #The userdata in the main program can only be changed on a global scope, this is a local scope so we have to define it as a global variable
        connection = sql.connect("Assets\Database\mainDatabase.db") #Connects to the database
        cursor = connection.cursor()

        usernametext = username.get() #Gets both usernames and passwords
        passwordtext = password.get()
        
        passencode = passwordtext.encode() #Converts the password into a byte sequence so it can be hashed.
        passobject = hl.sha256(passencode) #Uses sha256 hashing algorithm to hash the password
        hashedpassword = passobject.hexdigest() #Returns the hashed password as a variable.

        cursor.execute("""                                              
            SELECT * FROM player WHERE Username = ? AND Password = ?
        """, (usernametext, hashedpassword))   #Executes this SQL code
        #The variables stated at the end are replaced with the ?, this prevents SQL Injection
        
        result = cursor.fetchone() #Fetches the result of the SQL code
        
        if result:
            userData = result #Stores the result as its own variable, allowing access to user data

            loginerror.config(text=f"You have successfully logged in as {usernametext}",fg="lime green") #Additional text shows login is successful
            
            signupbutton.pack_forget() #Upon logining in there's no need for signup and login buttons, so they are removed.
            loginbutton.pack_forget()
            playbutton.pack(pady=12, before=settingsbutton) #Show the play button after successful login
        else:
            loginerror.config(text="Your password or username is incorrect!",fg="red") #Changes the additional message into a designated error message and displays it
        
        username.delete(0, tk.END) #Deletes the username and password upon login or incorrect credentials
        password.delete(0, tk.END)

        connection.close()

    
    #Set the background color of each frame
    mainmenuframe.configure(bg="black") 
    loginframe.configure(bg="black")
    signupframe.configure(bg="black")
    settingsframe.configure(bg="black")
    controlframe.configure(bg="black")
    objectiveframe.configure(bg="black")

    

    #MAIN MENU SCREEN
    #For each button/label, text refers to what will appear on the object, image is destination of the wireframe images I defined earlier.
    #'fg' and 'bg' refer to the foreground and background of the images. 'font' refers to the font style, size and the type, e.g. bold, italic.
    #'bd' refers to the border width, it is zero so theres no border. Active background refers to what the colour of the background is when clicking the button.
    screentitle = tk.Label(mainmenuframe, text="Welcome!", image = welcomeimage, fg="lime green", bg="black", font=("Courier", 20, "bold"), bd = 0)
    playbutton = tk.Button(mainmenuframe, text="Play", image = playimage, command=play, fg="lime green", bg="black", bd = 0, activebackground="Black")
    loginbutton = tk.Button(mainmenuframe, text="Login", image = loginimage, command=login, fg="lime green", bg="black", bd = 0, activebackground="Black")
    signupbutton = tk.Button(mainmenuframe, text="Sign-up", image = signupimage, command=signup, fg="lime green", bg="black", bd = 0, activebackground="Black")
    settingsbutton = tk.Button(mainmenuframe, text="Settings", image = settingsimage, command=settings, fg="lime green", bg="black", bd = 0, activebackground="Black")
    exitbutton = tk.Button(mainmenuframe, text="Exit", image = exitimage, command=exit, fg="lime green", bg="black", bd = 0, activebackground="Black")

    screentitle.pack(pady=40) #In order to display each label and
    #Only show play button if user is logged in, otherwise show login/signup buttons
    if userData is not None:
        playbutton.pack(pady=12)
        username_display = userData[1]  # index 1 is the Username
        screentitle.config(text=f"Welcome {username_display}!")
    else:
        loginbutton.pack(pady=12)
        signupbutton.pack(pady=12)

    settingsbutton.pack(pady=12)
    exitbutton.pack(pady=12)

    mainmenuframe.tkraise()

    # LOGIN SCREEN

    logintitle = tk.Label(loginframe, text="Login", fg="lime green", image = logintextimage, bg="black", font=("Courier", 16, "bold"), bd = 0)
    userlabel = tk.Label(loginframe, text="Username:", image = enterusername, fg="lime green", bg="black", bd = 0, activebackground="Black")
    userframe = tk.Frame(loginframe, background="#8FE229", borderwidth= 3)
    username = tk.Entry(userframe,fg = "#8FE229",  bg="black", font=("Courier", 16, "bold"), bd = 0)

    passlabel = tk.Label(loginframe, text="Password:", image = enterpassword, fg="lime green", bg="black", bd = 0, activebackground="Black")
    passframe = tk.Frame(loginframe, background="#8FE229", borderwidth= 3)
    password = tk.Entry(passframe, show="*",fg = "#8FE229",  bg="black", font=("Courier", 16, "bold"), bd = 0)

    loginerror = tk.Label(loginframe, text="", fg="red", bg="black", bd = 0, activebackground="Black",font=("Courier", 16, "bold"))
    loginsubmit = tk.Button(loginframe, text="Submit", image = submitpassword, command=submitlogin, fg="lime green", bg="black", bd = 0, activebackground="Black")
    loginexit = tk.Button(loginframe, text="Return", image = returntomain, command=returnToMainMenu, fg="lime green", bg="black", bd = 0, activebackground="Black")

    logintitle.pack(pady=20)

    userlabel.pack()
    userframe.pack(pady=15)
    username.pack(pady=1, padx=1)
    
    passlabel.pack()
    passframe.pack(pady=15)
    password.pack(pady=1, padx=1)

    loginerror.pack(pady=15)
    loginsubmit.pack(pady=10)
    loginexit.pack(pady=10)

    # SIGN UP SCREEN
    #For each button/label, text refers to what will appear on the object, image is destination of the wireframe images I defined earlier.
    #'fg' and 'bg' refer to the foreground and background of the images. 'font' refers to the font style, size and the type, e.g. bold, italic.
    #'bd' refers to the border width, it is zero so theres no border. Active background refers to what the colour of the background is when clicking the button.
    signuptitle = tk.Label(signupframe, text="Signup", image = signuptext,fg="#8FE229", bg="black", font=("Courier", 16, "bold"), bd = 0, activebackground="Black")

    signuserlabel = tk.Label(signupframe, text="Username:", image = enterusername, fg="#8FE229", bg="black", bd = 0, activebackground="Black")
    signuserframe = tk.Frame(signupframe, background="#8FE229", borderwidth= 3)
    signusername = tk.Entry(signuserframe,fg = "#8FE229",  bg="black", font=("Courier", 16, "bold"), bd = 0)

    signpasslabel = tk.Label(signupframe, text="Password:", image = enterpassword, fg="#8FE229", bg="black", bd = 0, activebackground="Black")
    signpassframe = tk.Frame(signupframe, background="#8FE229", borderwidth= 3)
    signpassword = tk.Entry(signpassframe, show = "*", fg = "#8FE229",  bg="black", font=("Courier", 16, "bold"), bd = 0)

    signpasslabel2 = tk.Label(signupframe, text="Re-enter Password:", image = reenterpassword,fg="#8FE229", bg="black", bd = 0, activebackground="Black")
    signpassframe2 = tk.Frame(signupframe, background="#8FE229", borderwidth= 3)
    signpassword2 = tk.Entry(signpassframe2, show = "*", fg = "#8FE229",  bg="black", font=("Courier", 16, "bold"), bd = 0)

    signerror = tk.Label(signupframe, text="", fg="red", bg="black",font=("Courier", 16, "bold"))
    signsubmit = tk.Button(signupframe, text="Submit", image = submitpassword, command=submitsignin, fg="#8FE229", bg="black", bd = 0, activebackground="Black")
    signupvalidation = tk.Button(signupframe, image = validationButton, command=validationScreen, fg="#8FE229", bg="black", bd = 0, activebackground="Black")
    signupexit = tk.Button(signupframe, text="Return", image = exitimage, command=returnToMainMenu, fg="#8FE229", bg="black", bd = 0, activebackground="Black")

    signuptitle.pack(pady=20)

    signuserlabel.pack()
    signuserframe.pack(pady=10)
    signusername.pack(padx=1,pady=1)

    signpasslabel.pack()
    signpassframe.pack(pady=10)
    signpassword.pack(padx=1,pady=1)

    signpasslabel2.pack()
    signpassframe2.pack(pady=10)
    signpassword2.pack(padx=1,pady=1)

    signerror.pack(pady=15)
    signsubmit.pack(pady=5)
    signupvalidation.pack(pady=5)
    signupexit.pack(pady=5)

    #VALIDATION SCREEN
    validationscreentitle = tk.Label(validationframe, image = validationTitle,fg="#8FE229", bg="black", font=("Courier", 16, "bold"), bd = 0, activebackground="Black")
    validationinfo = tk.Label(validationframe, image = validationText,fg="#8FE229", bg="black", font=("Courier", 16, "bold"), bd = 0, activebackground="Black")
    validationexit = tk.Button(validationframe, image = exitimage, command=signup, fg="#8FE229", bg="black", bd = 0, activebackground="Black")

    validationscreentitle.pack(pady=20)
    validationinfo.pack(pady=5)
    validationexit.pack(pady=10)

    # SETTINGS SCREEN
    #This appears on the main menu
    settings_title = tk.Label(settingsframe, image = settings_title_image ,fg="#8FE229", bg="black", 
                              font=("Courier", 16, "bold"), bd = 0, activebackground="Black")
    settings_title.pack(pady=20)

    volumelabel = tk.Label(settingsframe, text=f"Volume: {volume}%", fg="#8FE229", bg="black", font=("Courier", 18, "bold"))
    volumelabel.pack(pady=10)

    fullscreenlabel = tk.Label(settingsframe, text="Press F11 to toggle fullscreen!", fg="#8FE229", bg="black", font=("Courier", 18, "bold"))

    def change_volume(v):
        global volume #global variables can be accessed through the whole program
        volume = int(v) #converts the new volume to an integer since its a string
        volumelabel.config(text=f"Volume: {volume}%") #changes slider text to show current volume
        pygame.mixer.music.set_volume(volume / 100)
        uiclicksound.set_volume(volume / 100)

    #Parameters: from_ and to indicate the minimum and maximum values the slider can be too
    #orient is the positioning of the scale.
    #length is the visible length of the scale across the screen
    volume_slider = tk.Scale(settingsframe, from_=0, to=100, orient=tk.HORIZONTAL, 
                            bg="black", fg="#8FE229", font=("Courier", 16, "bold"), length=100, command=change_volume,
                            troughcolor="#8FE229", highlightthickness=2, highlightbackground="#8FE229",
                            highlightcolor="#8FE229", activebackground="#8FE229", bd=0)
    

    
    volume_slider.set(volume) #sets td volume to the indicated volume
    volume_slider.pack(pady=10)

    #keybind changing
    tk.Label(settingsframe, text="KEYBINDS", fg="#8FE229", bg="black", font=("Courier", 18, "bold")).pack(pady=20)

    keys_frame = tk.Frame(settingsframe, bg="black")
    keys_frame.pack()

    #the grid method in pygame puts text in a grid like format on a screen, this is efficient for showing keybinds in my game
    upkey = tk.Label(keys_frame, text=f"Up: {move_up}", fg="#8FE229", bg="black", font=("Courier", 16, "bold"))
    upkey.grid(row=0, column=0, padx=20, pady=5)
    downkey = tk.Label(keys_frame, text=f"Down: {move_down}", fg="#8FE229", bg="black", font=("Courier", 16, "bold"))
    downkey.grid(row=0, column=1, padx=20, pady=5)
    leftkey = tk.Label(keys_frame, text=f"Left: {move_left}", fg="#8FE229", bg="black", font=("Courier", 16, "bold"))
    leftkey.grid(row=1, column=0, padx=20, pady=5)
    rightkey = tk.Label(keys_frame, text=f"Right: {move_right}", fg="#8FE229", bg="black", font=("Courier", 16, "bold"))
    rightkey.grid(row=1, column=1, padx=20, pady=5)

    #Procedure that switches key binds
    def toggle_keys():
        uiclicksound.play()
        #Global so these variables can be accessed throughout the program
        global move_up, move_down, move_left, move_right 
        if move_up == "w":
            #When the button is pressed it is switched between arrow keys and WASD
            #the text for each arrow key is capitalised since this is how it must appear in pygame
            move_up = "UP"
            move_down = "DOWN"
            move_left = "LEFT"
            move_right = "RIGHT"
            togglebutton.config(text="Switch to WASD") #Text changed to inform the user
        else:
            #Keys switched to WASD
            move_up = "w"
            move_down = "s"
            move_left = "a"
            move_right = "d"
            togglebutton.config(text="Switch to Arrow Keys") #Text changed to inform the user
        
        # Update labels
        upkey.config(text=f"Up: {move_up.upper()}")
        downkey.config(text=f"Down: {move_down.upper()}")
        leftkey.config(text=f"Left: {move_left.upper()}")
        rightkey.config(text=f"Right: {move_right.upper()}")

    togglebutton = tk.Button(settingsframe, text="Switch to Arrow Keys", command=toggle_keys,
                            fg="#8FE229", bg="black", font=("Courier", 18, "bold"),
                            bd=2, relief="solid", activebackground="#8FE229", activeforeground="black")
    togglebutton.pack(pady=15)
    fullscreenlabel.pack(pady = 10)
    
    controlButton = tk.Button(settingsframe, image = controlsButtonImage, command=controlsScreen, fg="#8FE229", bg="black", bd = 0, activebackground="Black")
    objectivesButton = tk.Button(settingsframe, image = objectivesButtonImage, command=objectiveScreen, fg="#8FE229", bg="black", bd = 0, activebackground="Black")

    settingsexit = tk.Button(settingsframe, text="Return", image = returntomain, command=returnToMainMenu, 
                             fg="lime green", bg="black", bd = 0, activebackground="Black")
    controlButton.pack(pady=5)
    objectivesButton.pack(pady=5)
    settingsexit.pack(pady=10)

    

    #CONTROLS SCREEN
    controlsscreentitle = tk.Label(controlframe, image = controlsTitle, fg="#8FE229", bg="black", font=("Courier", 16, "bold"), bd = 0, activebackground="Black")
    controlsinfo = tk.Label(controlframe, image = controlsText, fg="#8FE229", bg="black", font=("Courier", 16, "bold"), bd = 0, activebackground="Black")
    controlsexit = tk.Button(controlframe, image = returntomain, command=returnToSettings, fg="#8FE229", bg="black", bd = 0, activebackground="Black")

    controlsscreentitle.pack(pady=20)
    controlsinfo.pack(pady=5)
    controlsexit.pack(pady=10)

    #OBJECTIVES SCREEN
    objectivesscreentitle = tk.Label(objectiveframe, image = objectivesTitle, fg="#8FE229", bg="black", font=("Courier", 16, "bold"), bd = 0, activebackground="Black")
    objectivesinfo = tk.Label(objectiveframe, image = objectivesText, fg="#8FE229", bg="black", font=("Courier", 16, "bold"), bd = 0, activebackground="Black")
    objectivesexit = tk.Button(objectiveframe, image = returntomain, command=returnToSettings, fg="#8FE229", bg="black", bd = 0, activebackground="Black")

    objectivesscreentitle.pack(pady=20)
    objectivesinfo.pack(pady=5)
    objectivesexit.pack(pady=10)



    #Extras
    if userData is not None:
        username = userData[1]  # index 1 is the Username
        screentitle.config(text=f"Welcome {username}!")
        
        signupbutton.pack_forget()
        loginbutton.pack_forget()
    else:
        screentitle.config(text="Welcome!")

    root.mainloop()

mainmenu()

