
import pygame
import math
import random

enemyTypes = {
    "basic": {
        "max_health": 5,
        "speed": 3,
        "damage": 1,
        "colour": (255, 0, 0),
        "attackrange": 70,  # Melee range
        "attackcooldown": 60,  # Attack every second
    },
    "tank": {
        "max_health": 10,
        "speed": 1,
        "damage": 1,
        "colour": (150, 0, 0),
        "attackrange": 80,
        "attackcooldown": 90,  # Slower attacks
    },
    "knight": {
        "max_health": 7,
        "speed": 2,
        "damage": 1,
        "colour": (150, 0, 0),
        "attackrange": 80,
        "attackcooldown": 60,  # Slower attacks
    },
    "archer": {
        "max_health": 4,
        "speed": 1,
        "damage": 1,
        "colour": (100, 255, 100),
        "shootrange": 400,
        "stoprange": 350,
        "shootcooldown": 60,
        "bulletspeed": 8,
    },
    "mage": {
        "max_health": 4,
        "speed": 1,
        "damage": 2,
        "colour": (255,255,255),
        "shootrange": 400,
        "stoprange": 350,
        "shootcooldown": 60,
        "bulletspeed": 2,
    }
}

class Enemy:
    x = 0
    y = 0
    def __init__(self, nx, ny):
        self.x = nx
        self.y = ny
        self.speed = 3
        self.width = 60
        self.height = 90
        self.rect = pygame.Rect(self.x, self.y, self.width,self.height)

        
        #random.choices selects a random item from a list with a weighted probability, the weights define the probability of one being chosen.
        #k=1 refers to the amount of lists to be chosen (1). this method returns a list, [0] extracts the value
        self.selectedEnemy = random.choices(population=["basic", "tank", "knight","archer","mage"], weights=[50, 25, 15, 20, 10], k=1)[0]
        
        self.animationframes = []
        #loops through all 4 frames
        for i in range(1, 5):  #i starts at 1 ends at 4
            #loads the image using formatting for simplicity
            frame = pygame.image.load(rf"Assets\Enemies\zombie {self.selectedEnemy}\images\zombie {self.selectedEnemy}_0{i}.png").convert_alpha() 
            #scales to the correct width/height so they don't appear squashed
            frame = pygame.transform.scale(frame, (self.width, self.height))
            #adds to animation frame so it can be stored and retrieved as its not a variable
            self.animationframes.append(frame) 

        
        # Animation variables
        self.currentframe = 0
        self.animationspeed = 0.15
        self.animationtimer = 0
        self.facingleft = False

        enemyStats = enemyTypes[self.selectedEnemy]

        self.isranged = "shootrange" in enemyStats
        self.ismelee = "attackrange" in enemyStats


        self.max_health = enemyStats["max_health"]
        self.health = self.max_health
        self.speed = enemyStats["speed"]
        self.damage = enemyStats["damage"]
        self.colour = enemyStats["colour"]

        if self.isranged:
            self.shootrange = enemyStats["shootrange"]
            self.stoprange = enemyStats["stoprange"]
            self.shootcooldown = enemyStats["shootcooldown"]
            self.bulletspeed = enemyStats["bulletspeed"]
            self.attacktimer = enemyStats["shootcooldown"]
        elif self.ismelee:
            self.attackrange = enemyStats["attackrange"]
            self.attackcooldown = enemyStats["attackcooldown"]
            self.attacktimer = enemyStats["attackcooldown"]

        self.alive = True

        print(f"Created the enemy {self.selectedEnemy}: Speed: {self.speed} Max Health: {self.max_health} Damage: {self.damage}")

        print("Dictionary values for " + 
             self.selectedEnemy +" : Speed: " + 
              str(enemyStats["speed"]) +
              " Health: " + str(enemyStats["max_health"]) +
              " Damage: " + str(enemyStats["damage"]))


    def draw(self, screen, offsetx=0, offsety=0):
        
        adjustedx = self.x - offsetx
        adjustedy = self.y - offsety

        #gets the current enemy sprite to be printed to the screen
        currentsprite = self.animationframes[self.currentframe]
        
        #if the enemy sprite is facing left, its flipped
        if self.facingleft:
            currentsprite = pygame.transform.flip(currentsprite, True, False)
        
        #the enemy is then drawn
        screen.blit(currentsprite, (int(adjustedx), int(adjustedy)))
        

        # Health bar
        health_bar_width = self.width #how wide the bar is (same width as enemy)
        health_bar_height = 6 #how tall the bar is in pixels
        #max picks the highest value from 0, and the ratio of health to max health (prevents negative errors)
        health_percentage = max(0, self.health / self.max_health) 
        
        health_bg_x = int(adjustedx)
        health_bg_y = int(adjustedy) - 12 #appears 12 pixels ABOVE the enemy
        pygame.draw.rect(screen, (50, 0, 0), (health_bg_x, health_bg_y, health_bar_width, health_bar_height)) #draws health bar background
        
        #colour of bar changes depending on how much health is left
        if health_percentage > 0.5:
            bar_colour = (0, 255, 0)
        elif health_percentage > 0.25:
            bar_colour = (255, 255, 0)
        else:
            bar_colour = (255, 0, 0)
        
        #draws the actual health bar, this decreases relative to the health percentage
        pygame.draw.rect(screen, bar_colour,(health_bg_x, health_bg_y, int(health_bar_width * health_percentage), health_bar_height))
    
    def getrect(self):
        return self.rect
    
    def takedamage(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.health = 0
            self.alive = False
            return True  #enemy has died
        return False  #enemy is still alive
    
    def update(self, playerworldx, playerworldy, walls):
        enemy_center_x = self.x + self.width // 2
        enemy_center_y = self.y + self.height // 2
        
        dx = playerworldx - enemy_center_x
        dy = playerworldy - enemy_center_y
        distance = math.hypot(dx, dy)
        
        # Decrease attack timer
        if hasattr(self, 'attacktimer') and self.attacktimer > 0:
            self.attacktimer -= 1
        
        #if the enemy is ranged
        if self.isranged:
            #if the enemy is further than the shooting range 
            if distance > self.shootrange: 
                #it wont attack, it will simply move to the player
                self.movetoplayer(playerworldx, playerworldy, walls)
                return None, False
            elif distance > self.stoprange:
                #if the enemy is at the stop range it moves and shoots at the same time
                self.movetoplayer(playerworldx, playerworldy, walls)
                if self.attacktimer == 0: #adds a shoot cooldown
                    #if the cooldown is over it shoots
                    bullet = self.shoot(playerworldx, playerworldy)
                    self.attacktimer = self.shootcooldown
                    return bullet, False #returns the bullet to be added to the enemy bullet array
            else:
                if self.attacktimer == 0: #if the enemy is at the stop range
                    #it stands still and shoots so it does not get too close 
                    bullet = self.shoot(playerworldx, playerworldy)
                    self.attacktimer = self.shootcooldown
                    return bullet, False
            return None, False
        
        #melee enemy, so it goes close to the player before attacking
        if self.ismelee:
            if distance > self.attackrange:
                #the enemy is out of range so it moves to the player
                self.movetoplayer(playerworldx, playerworldy, walls)
                return None, False
            else:
                #the enemy is in range, so it checks if its attack cooldown is gone 
                #if theres no attack cooldown it attacks
                if self.attacktimer == 0:
                    self.attacktimer = self.attackcooldown
                    return None, True  #attacks health reduction are handled in the game file (to get the player object)
                return None, False

    
    def shoot(self, playerworldx, playerworldy):
        ecenterx = self.x + self.width // 2
        ecentery = self.y + self.height // 2
        
        dx = playerworldx - ecenterx
        dy = playerworldy - ecentery
        
        #use pythagerous to find the direction to aim at 
        length = math.hypot(dx, dy)
        if length > 0: #prevents dividing by zero
            dx = (dx / length) * self.bulletspeed
            dy = (dy / length) * self.bulletspeed
        
        #sends it back to the game file to add to the enemy bullet array
        from bullet import Bullet
        return Bullet("basic", ecenterx, ecentery, dx, dy, True, self.selectedEnemy) 


    def movetoplayer(self, playerworldx, playerworldy, walls):
        #find direction to player
        dx = playerworldx - self.x
        dy = playerworldy - self.y

        #find distance to player
        distance = math.hypot(dx, dy)

        #if enemy is close enough, stop moving and reset animation
        if distance <= 5:
            self.currentframe = 0
            self.animationtimer = 0
            return

        #updates facing direction based on horizontal movement
        if abs(dx) > 1: #gets the magnitude of dx (could be negative)
            self.facingleft = dx < 0

        #normalise direction and apply speed
        dx = (dx / distance) * self.speed
        dy = (dy / distance) * self.speed

        #handles animation while moving
        self.animationtimer += self.animationspeed
        if self.animationtimer >= 1:
            self.animationtimer = 0 #resets animation time
            # % (modulus) makes it a positive integer in range
            #the frame is then moved on to the next one (incremented)
            self.currentframe = (self.currentframe + 1) % len(self.animationframes) 

        #checks for x axis collision
        old_x = self.x
        self.x += dx
        self.rect.x = int(self.x)

        for wall in walls:
            if self.rect.colliderect(wall): #if theres a collision bring the enemy back
                self.x = old_x
                self.rect.x = int(old_x) #updates hitbox back aswell
                break

        #checks for y axis collisions
        old_y = self.y
        self.y += dy
        self.rect.y = int(self.y)

        for wall in walls:
            if self.rect.colliderect(wall): #if theres a collision bring the enemy back
                self.y = old_y
                self.rect.y = int(old_y) #updates hitbox back aswell
                break
                        