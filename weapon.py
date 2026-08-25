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

class Weapon:
    def __init__(self, x, y, weapon_type):
        self.x = x
        self.y = y
        self.weapon_type = weapon_type




        self.weaponScale = 3
        #gets the weapon image from the assets folder
        self.image = pygame.image.load(f"Assets\\Weapons\\{weapon_type}.png").convert_alpha() 
        #scales it based on the weapon scale factor
        self.image = pygame.transform.scale(self.image, (weaponSizes[weapon_type]["width"] * self.weaponScale, weaponSizes[weapon_type]["height"] * self.weaponScale))
                
        self.rect = pygame.Rect(self.x, self.y, 32, 32)

    def update_rect(self):
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface, camx, camy):
        drawx = self.x - camx
        drawy = self.y - camy
        surface.blit(self.image, (drawx, drawy))