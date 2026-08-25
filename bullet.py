import pygame
import math

weaponTypes = {"basic" : {"name": "Pistol", "energycost" : 5, "damage" : 3, "bulletsize" : 20}, 
               "sniper" : {"name": "Sniper","energycost" : 20, "damage": 30, "bulletsize" : 64},
               "machine" : {"name": "Machine Gun","energycost" : 2, "damage": 4, "bulletsize" : 10}}

enemyBulletTypes = {
    "archer": {
        "width": 20,
        "height": 8,
        "colour": (150, 75, 0), #brown
        "shape": "rectangle"
    },
    "mage": {
        "width": 32,
        "height": 32,
        "colour": (138, 43, 226), #purple
        "shape": "circle"
    },
    "king": { #boss enemy
        "width": 48,
        "height": 48,
        "colour": (255,255,0), #yellow
        "shape": "circle"
    }
}

class Bullet:
    def __init__(self, weaponType, nx, ny, ndx, ndy, isEnemyBullet=False, enemyType=None):
        self.x = nx
        self.y = ny
        self.dx = ndx
        self.dy = ndy
        
        self.isEnemyBullet = isEnemyBullet
        
        if isEnemyBullet and enemyType:  
            #if the enemytype is passed, it updates the bullet to suit that enemy
            self.enemyType = enemyType
            bulletData = enemyBulletTypes[enemyType] #grabs the data stored in the dictionary
            self.width = bulletData["width"]
            self.height = bulletData["height"]
            self.bulletcolour = bulletData["colour"]
            self.shape = bulletData["shape"] 
            self.energyrequirement = 0 #enemies have no energy requirement
            self.weapon = None #theres no weapon
        else:
            #the bullet is the player bullet, data is grabbed from the weapon dictionary
            self.weaponType = weaponType
            self.weapon = weaponTypes[self.weaponType]
            self.energyrequirement = self.weapon["energycost"]
            self.width = self.weapon["bulletsize"]
            #makes it look like a rectangle
            self.height = (self.weapon["bulletsize"]) * 0.4 
            self.bulletcolour = (255, 255, 0)
            self.shape = "rectangle"
        
        # Calculate angle for rotation
        self.angle = math.degrees(math.atan2(-ndy, ndx))

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def getrect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def draw(self, surface, camx, camy):
        screenX = self.x - camx
        screenY = self.y - camy
        
        if self.shape == "circle":
            #if the shape is circle (mage bullet) if adds this
            radius = self.width / 2 #calculates the radius
            pygame.draw.circle(surface, self.bulletcolour, (int(screenX + radius), 
                int(screenY + radius)), radius) #draws a circle for the bullet
        else:
            #make sure the bullet rotates towards the players direction
            bullet_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(bullet_surface, self.bulletcolour, (0, 0, self.width, self.height))
            
            rotatedSurface = pygame.transform.rotate(bullet_surface, self.angle)
            rotatedRect = rotatedSurface.get_rect(center=(int(screenX  + self.width/2), int(screenY + self.height/2)))
            surface.blit(rotatedSurface, rotatedRect)
    
    def getWeaponData(self):
        return weaponTypes

