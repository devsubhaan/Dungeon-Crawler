import pygame

weaponSizes = {
    "basic": {
        "width": 16,
        "height": 8,
    },
    "machine": {
        "width": 44,
        "height": 10,
    },
    "sniper": {
        "width": 37,
        "height": 9,
    },
}

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 8 #This is the players movement speed
        self.width = 32
        self.height = 32

        self.weapon_slots = ["basic", None]   #maximum of two slots
        self.active_slot = 0 
        self.weaponScale = 3

        self.weaponImage = pygame.image.load(f"Assets\Weapons\{self.weapon_slots[self.active_slot]}.png").convert_alpha()
        self.weaponSizeW = weaponSizes[self.weapon_slots[self.active_slot]]["width"] * self.weaponScale
        self.weaponSizeH = weaponSizes[self.weapon_slots[self.active_slot]]["height"] * self.weaponScale

        #Heart statistics
        self.max_health = 5
        self.health = self.max_health
        #Heart image objects
        self.heartfull = pygame.image.load("Assets\heartv2.png").convert() #images that need loading
        self.heartfull.set_colorkey((0,0,0))

        self.recoveringenergy = False
        self.maxenergy = 100 #Max energy the player can hold
        self.energy = self.maxenergy #Ammunition, each shot fired reduces this number by the energy cost.
        self.energyrate = 5
        self.energytimer = 0

        self.score = 0



    def get_rect(self):
        
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys, up, down, left, right):
        upkey = getattr(pygame, f'K_{up}') #getattr converts a string into a pygame key
        downkey = getattr(pygame, f'K_{down}') #so i can directly insert the variables
        leftkey = getattr(pygame, f'K_{left}')
        rightkey = getattr(pygame, f'K_{right}')
        
        if keys[upkey]: #allows for the movement of the player depending on the key
            self.y -= self.speed #changes coordinate values based on speed
        if keys[downkey]:
            self.y += self.speed
        if keys[leftkey]:
            self.x -= self.speed
        if keys[rightkey]:
            self.x += self.speed
        
        return self.x, self.y #returns the new x and y values so the player updates position

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.get_rect())

        self.drawHUD(surface, "Hearts", None, None)
        self.drawHUD(surface, "Energy", "basic", None)
        self.drawHUD(surface, "Score", None, None)

    def equip_weapon(self, weapon_type):
        #checks if theres no weapons in the weapon slot
        if None in self.weapon_slots:
            #Finds the index where there is no weapon (instead of manually searching for one)
            index = self.weapon_slots.index(None)
            self.weapon_slots[index] = weapon_type #grabs that index and places the weapon inside it
        else:
            #Replaces the weapon with the one on the ground if theres no free slots
            self.weapon_slots[self.active_slot] = weapon_type

    def switch_weapon(self): 
        self.active_slot = 1 - self.active_slot
        if self.weapon_slots[self.active_slot] != None:
            self.weaponImage = pygame.image.load(f"Assets\Weapons\{self.weapon_slots[self.active_slot]}.png").convert_alpha()
            self.weaponSizeW = weaponSizes[self.weapon_slots[self.active_slot]]["width"] * self.weaponScale
            self.weaponSizeH = weaponSizes[self.weapon_slots[self.active_slot]]["height"] * self.weaponScale


    def get_current_weapon(self): #gets the currently equipped weapon and returns it
        return self.weapon_slots[self.active_slot]



    def drawHUD(self, surface, HUDToUpdate, currentWeapon, weaponTypes):
        #Heart system HUD
        if HUDToUpdate == "Hearts": #Checks if the UI that needs updating is the the health
            heartsize = 32 #32x32

            for heartnumber in range(self.max_health):
                #The x and y positions of the hearts on the screen
                x = 20 + heartnumber * (heartsize + 5) #Each heart is placed 5 pixels to the right of each other heart
                y = 20
                if heartnumber < self.health: #checks if the heart counter is less than the players current health
                    surface.blit(self.heartfull, (x, y)) #If it is, the player has that heart so its displayed

        #Energy system HUD
        elif HUDToUpdate == "Energy": #Checks if the UI that needs updating is the energy
            x = 20 #The x and y positions of the energy text on the screen
            y = 60
            energyFont = pygame.font.Font(None, 48) #Initialises the text with a font size of 48
            #Renders this text, showing the current energy
            text = energyFont.render(str(self.energy) + "/" + str(self.maxenergy), True, (255, 255, 255))
            surface.blit(text, (x,y)) #Outputs the white rendered text onto the screen where the user can see it

        #current weapon and energy cost HUD
        if currentWeapon != None and weaponTypes != None:
            x = 20
            y = 100
            weaponFont = pygame.font.Font(None, 48)
            costFont = pygame.font.Font(None, 30)
            energycost = (weaponTypes[currentWeapon]["energycost"])

            text = weaponFont.render("Weapon: " + weaponTypes[currentWeapon]["name"], True, (255, 255, 255))
            subtext = costFont.render("Cost: " + str(energycost), True, (255, 255, 255))

            surface.blit(text, (x,y))
            surface.blit(subtext, (x,y + 35))
        
        #Score system HUD
        if HUDToUpdate == "Score": #Checks if the UI that needs updating is the score
            currentScore = self.score #Assigns the attribute score to a variable
            if currentScore < 0: #If its less than zero it becomes zero.
                currentScore = 0 #This prevents negative values
            scoreTextX = 350 #The x position of the score text on the screen
            scoreTextY = 20 #The y position of the score text on the screen
            scoreFont = pygame.font.Font(None, 32) #Initialises the text with a font size of 48
            text = scoreFont.render("Score: " + str(currentScore), True, (255, 255, 255)) #Renders this text, showing the current score.
            surface.blit(text, (scoreTextX,scoreTextY)) #Outputs the white rendered text onto the screen where the user can see it.
        

    def recoverenergy(self):
        #starts recovering energy, this procedure is called 60 times per second
        if self.energy < self.maxenergy:
            self.energytimer += 1  # after 1 second, energytimer = 60

            #checks if it's been 60 frames
            if self.energytimer >= 60:
                self.energytimer = 0
                self.energy += self.energyrate

                #prevents energy exceeding max
                if self.energy > self.maxenergy:
                    self.energy = self.maxenergy






        
        
            