import pygame
import math
import random

from enemy import Enemy
from bullet import Bullet

bossTypes = {
    "king": {
        "name": "Undead King",
        "maxhealth": 200,
        "speed": 1,
        "damage": 1,
        "colour": (255,255,51),
        "shootrange": 400,
        "stoprange": 100,
        "shootcooldown": 40,
        "bulletspeed": 3,
        "bulletsize": 2,
        "specialattackcd": 180
    },
    "knight": {
        "name": "Undead Knight",
        "maxhealth": 250,
        "speed": 3,
        "damage": 3,
        "colour": (160,160,160),
        "attackrange": 125,
        "attackcooldown": 50,
        "specialattackcd": 240
    },
}

class Boss(Enemy):
    def __init__(self, nx, ny):
        
        self.x = nx #boss spawn position
        self.y = ny
        self.width = 180 #boss width and height
        self.height = 270
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) #boss object
        
        #boss stats
        #this chooses a random boss with weighted probability
        self.selectedBoss = random.choices(population=["king", "knight"], weights=[50, 50], k=1)[0] 
        self.selectedEnemy = self.selectedBoss
        #extracts the data from the chosen boss
        self.bossStats = bossTypes[self.selectedBoss]

        #these get the actual data within the bossType data for that chosen boss
        self.bossName = self.bossStats["name"]
        self.maxhealth = self.bossStats["maxhealth"]
        self.health = self.maxhealth
        self.speed = self.bossStats["speed"]
        self.damage = self.bossStats["damage"]
        self.colour = self.bossStats["colour"]
        
        #checks if its a soley ranged or melee boss
        self.isranged = "shootrange" in self.bossStats
        self.ismelee = "attackrange" in self.bossStats
        self.attacktimer = 0

        #if the boss is ranged
        if self.isranged:
            #all the range related stats are extracted
            self.shootrange = self.bossStats["shootrange"]
            self.stoprange = self.bossStats["stoprange"]
            self.shootcooldown = self.bossStats["shootcooldown"]
            self.bulletspeed = self.bossStats["bulletspeed"]
            self.specialattackcooldown = self.bossStats["specialattackcd"]
            self.specialtimer = 0
    
        #if the boss is melee, it has no bullets so only the melee stats are extracted
        elif self.ismelee:
            self.attackrange = self.bossStats["attackrange"]
            self.attackcooldown = self.bossStats["attackcooldown"]
            self.specialattackcooldown = self.bossStats["specialattackcd"]
            self.specialtimer = 0
            self.dashing = False
            self.dashtimer = 30  
        
        #changes boss properties during a second phase
        self.phase = 1
        
        #gets the animations (same code as enemy and player animations)
        self.animationframes = []
        try:
            for i in range(1, 5):
                frame = pygame.image.load(rf"Assets\Enemies\Bosses\{self.selectedBoss}boss\{self.selectedBoss}boss_0{i}.png").convert_alpha()
                frame = pygame.transform.scale(frame, (self.width, self.height))
                self.animationframes.append(frame)
        except:
            #fallback to colored squares if images not found
            for i in range(4):
                frame = pygame.Surface((self.width, self.height))
                frame.fill(self.colour)
                self.animationframes.append(frame)
        
        self.currentframe = 0
        self.animationspeed = 0.15
        self.animationtimer = 0
        self.facingleft = False
        
        self.alive = True
    
    def update(self, playerworldx, playerworldy, walls):
        """Boss AI with phase system"""
        enemycenterx = self.x + self.width // 2
        enemycentery = self.y + self.height // 2
        
        dx = playerworldx - enemycenterx
        dy = playerworldy - enemycentery
        distance = math.hypot(dx, dy)
        
        # Update timers
        if self.attacktimer > 0:
            self.attacktimer -= 1
        if self.specialtimer > 0:
            self.specialtimer -= 1
        
        #checks if the health is below half, if so it goes to the next phase
        if self.health < self.maxhealth // 2 and self.phase == 1:
            self.phase = 2
            self.speed *= 1.3  #30% extra speed
            if self.isranged:
                self.shootcooldown = int(self.shootcooldown * 0.7)  #30% less cooldown
            else:
                self.attackcooldown = int(self.attackcooldown * 0.7)  #30% faster attacks
            self.colour = (255, 0, 255)  #purple in phase 2
            print(f"{self.bossName} entered phase 2!")
        
        #RANGED BOSS BEHAVIOR
        if self.isranged:
            # Special attack - spread shot
            if self.specialtimer == 0 and distance < self.shootrange:
                bullets = self.specialAttack(playerworldx, playerworldy)
                self.specialtimer = self.specialattackcooldown
                return bullets, False
            
            # Normal ranged behavior
            if distance > self.shootrange:
                self.movetoplayer(playerworldx, playerworldy, walls)
                return [], False
            elif distance > self.stoprange:
                self.movetoplayer(playerworldx, playerworldy, walls)
                if self.attacktimer == 0:
                    bullet = self.shoot(playerworldx, playerworldy)
                    self.attacktimer = self.shootcooldown
                    return [bullet], False
            else:
                #in shoot range - stop and shoot
                if self.attacktimer == 0:
                    bullet = self.shoot(playerworldx, playerworldy)
                    self.attacktimer = self.shootcooldown
                    return [bullet], False
            return [], False
        
        #MELEE BOSS BEHAVIOR
        elif self.ismelee:
            # Special attack - dash towards player
            if self.dashing:
                self.specialDash()

            # Start dash
            elif self.specialtimer == 0 and distance < 300 and distance > self.attackrange:
                self.specialDash()
                self.specialtimer = self.specialattackcooldown
                print(f"{self.bossName} DASH ATTACK!")
            
            # Normal melee behavior
            if distance > self.attackrange:
                #too far - chase player
                self.movetoplayer(playerworldx, playerworldy, walls)
                return [], False
            else:
                #melee range - attack
                if self.attacktimer == 0:
                    self.attacktimer = self.attackcooldown
                    return [], True  #melee hit
                return [], False
        
        return [], False
    
    def specialAttack(self, playerworldx, playerworldy):
        #boss special attacks
        #gets the center of the enemy. the bullet is fired from here
        enemycenterx = self.x + self.width // 2 
        enemycentery = self.y + self.height // 2
        
        #finds the direction relative to the player and enemy position
        dx = playerworldx - enemycenterx
        dy = playerworldy - enemycentery
        
        baseangle = math.atan2(dy, dx) #gets the angle to the player
        bullets = [] #adds a new bullet list
        
        #spread count changes based on phase
        spreadcount = 20 if self.phase == 2 else 10
        spreadangle = 0.4 if self.phase == 2 else 0.3
        
        #determine angle offsets based on spread count
        angleoffsets = []
        if spreadcount == 3:
            angleoffsets = [-spreadangle, 0, spreadangle]
        else:
            angleoffsets = [-spreadangle*2, -spreadangle, 0, spreadangle, spreadangle*2]
        
        #bullets are spread separated by angles
        for angleoffset in angleoffsets:  #the math function needs radians so we use it here
            angle = baseangle + angleoffset #base angle is the angle it is being currently fired at with no change
            bulletdx = math.cos(angle) * self.bulletspeed #updates bullets new velocity
            bulletdy = math.sin(angle) * self.bulletspeed
            
            #passes on the enemies center position, the bullets velocity and if its a enemy bullet
            bullet = Bullet("basic", enemycenterx, enemycentery, bulletdx, bulletdy, True, self.selectedBoss) 
            #adds to the bullet list
            bullets.append(bullet)
        
        print(f"{self.bossName} special attack - {spreadcount} shot spread!")
        return bullets #returns the new list with the bullets
    
    def specialDash(self):
        if not self.dashing: #checks if the boss isnt already dashing
            self.dashing = True #its now dashing
            self.dashtimer = 30 #resets dashtimer
            self.speed = 10 #doubles speed for 30 frames
            return

        #reduce dash timer by 1 every frame
        self.dashtimer -= 1

        if self.dashtimer <= 0: #if the timer reaches zero
            self.speed = self.bossStats["speed"]
            self.dashing = False #it stops dashing

    def draw(self, screen, offsetx=0, offsety=0):
        adjustedx = self.x - offsetx
        adjustedy = self.y - offsety
        
        # Get current sprite
        currentsprite = self.animationframes[self.currentframe]
        if self.facingleft:
            currentsprite = pygame.transform.flip(currentsprite, True, False)
        
        screen.blit(currentsprite, (int(adjustedx), int(adjustedy)))

    def drawHealthBar(self, screen, screenwidth, screenheight):
        barwidth = 50 #define the height and width of the health bar
        barheight = 300
        barx = screenwidth - barwidth - 20  #define the position of the bar (x and y values)
        bary = (screenheight - barheight) / 2  
        
        pygame.draw.rect(screen, (0, 0, 0), (barx, bary, barwidth, barheight)) #adds the health bar background
        
        healthpercentage = max(0, self.health / self.maxhealth) #gets health percentage
        healthheight = int(barheight * healthpercentage) #calculates how full the bar should be, initialises at full
        
        #depending on how much health is left, the bar colour changes
        if healthpercentage > 0.5: #50%
            barcolour = (0, 255, 0) #green
        elif healthpercentage > 0.25: #25%
            barcolour = (255, 255, 0) #yellow
        else:
            barcolour = (255, 0, 0) #red
        
        #draws health bar so that it goes downwards when health decreases
        pygame.draw.rect(screen, barcolour, (barx, bary + barheight - healthheight, barwidth, healthheight))
        
        #adds a dark green border to the health bar to make it stand out more
        pygame.draw.rect(screen, (0,102,0) , (barx, bary, barwidth, barheight), 2)
        
        #adds the boss name on the side of the bar (vertically)
        font = pygame.font.Font(None, 32)
        nametext = font.render(self.bossName, True, self.colour) #gets the bossname, and the colour defined in the bossTypes
        
        #this rotates the bar vertically 
        rotatedtext = pygame.transform.rotate(nametext, 90)
        screen.blit(rotatedtext, (barx - 30, bary + barheight / 2 - rotatedtext.get_height() / 2)) #adds to the screen
        
        #adds a green health text to show the health remaining in numerical form
        healthtext = font.render(f"{int(self.health)}/{self.maxhealth}", True, (102,204,0)) 
        screen.blit(healthtext, (barx - healthtext.get_width() / 2 + barwidth / 2, bary - 25))
    
    
    def getrect(self):
        return self.rect