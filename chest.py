import pygame
import random

class Chest:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.opened = False
        
        #loads the chest images
        self.closedImage = pygame.image.load(r"Assets\Chests\closedChest.png").convert_alpha()
        self.openImage = pygame.image.load(r"Assets\Chests\chestOpen.png").convert_alpha() 
        #scales these chests to the tile size (64x64)
        self.closedImage = pygame.transform.scale(self.closedImage, (64, 64))
        self.openImage = pygame.transform.scale(self.openImage, (64, 64))
        
        #adds the chest hitbox, as the same size as chests
        self.rect = pygame.Rect(self.x, self.y, 64, 64)
        
        #chooses a random reward from these
        self.rewardType = random.choice(["weapon", "health", "energy"])
        
        #if the weapon is the reward, it chooses a random one from these
        if self.rewardType == "weapon":
            self.weapon_type = random.choice(["basic", "sniper", "machine"])
    
    def open(self, player, dropped_weapons):
        if self.opened:
            return
        #if the chest is already opened it exits
        
        self.opened = True
        
        if self.rewardType == "health":
            #if the reward is health, it choses a random health amount (1 to 3)
            healthAmount = random.randint(1, 3)
             #gives this health with a cap of the players max health
            player.health = min(player.health + healthAmount, player.max_health)
        
        elif self.rewardType == "energy":
            #gives the player a random amount of energy (20 to 50)
            energyAmount = random.randint(20, 50)
            #adds this energy with a cap of 100 
            player.energy = min(player.energy + energyAmount, 100)
        
        elif self.rewardType == "weapon":
            #drops a weapon near the chest for the player to pick it up
            from weapon import Weapon
            #adds a larger hitbox to the weapon
            dropped_weapon = Weapon(self.x + 80, self.y + 80, self.weapon_type)  
            dropped_weapons.append(dropped_weapon)
    
    def draw(self, surface, camx, camy):
        #draws the chest on the screen relative to the player camera
        drawx = self.x - camx
        drawy = self.y - camy
        
        #textures changes when chest opens
        if self.opened:
            surface.blit(self.openImage, (drawx, drawy))
        else:
            surface.blit(self.closedImage, (drawx, drawy))

    
    def update_rect(self):
        #updates the hitbox position
        self.rect.topleft = (self.x, self.y)