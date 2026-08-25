import pygame
import math
import pytmx
import random

from bullet import Bullet
from enemy import Enemy
from player import Player
from weapon import Weapon
from boss import Boss
from leaderboard import Leaderboard
from chest import Chest
from weapon import weaponSizes

class Game:
    x,y = 0,0
    speed = 10

    def __init__(self,width,height, up, down, right, left, volume, userData):
        self.width = width
        self.height = height
        self.running = True

        self.userData = userData
        #refers to the what the keybind of each key is 
        self.up = up 
        self.down = down
        self.right = right
        self.left = left

        #refers to the master volume of the game
        self.volume = volume

        self.alphahit = 0  #the transparency of the damage indicator
        #0 = invisible, 255 is fully visible
        self.flashspeed = 5  #how fast the damage indicator fades

        self.boss = None
        self.bossSpawned = False

        self.gameEnd = False

        self.starttime = 0  # Track game start time
        self.leaderboardshown = False  # Track if leaderboard was shown

        self.leaderboardTitleImage = None
        self.leaderboardRowImage = None
        self.exitImage = None
        self.rankHeaderImage = None
        self.playerHeaderImage = None
        self.scoreHeaderImage = None
        self.timeHeaderImage = None

        self.chest_message = None
        self.chest_message_timer = 0
        self.CHEST_MESSAGE_DURATION = 180



    
    def drawLeaderboard(self, screen, playerscore, userdata):
        #procedure draws the leaderboard at the end of the game 
        leaderboard = Leaderboard() #initialises leaderboard object
        topPlayers = leaderboard.getTopPlayers(5) #gets the top 5 players to be on the leaderboard

        #title image
        screen.blit(self.leaderboardTitleImage, (self.width/2 - self.leaderboardTitleImage.get_width()/2, 60))

        #player rows which show player data
        rowFont = pygame.font.Font(None, 40) #how big the font text is 
        rowHeight = self.leaderboardRowImage.get_height()  #gets how big the row is based on the image
        startY = 180 #where the player stats row starts relative to the screen

        for i, player in enumerate(topPlayers): #loops through all top players
            if player['rank'] != None and player['score'] != None and player['time'] != None:
                ypos = startY + (i * rowHeight) #gets the y position
                rowColour = (143, 226, 41) #green colour matching screen title

                #header and text x positions
                #self.width is the width of the window
                headerY = 140
                rankX = self.width/2 - 260
                usernameX = self.width/2 - 150
                scoreX = self.width/2 + 60
                timeX = self.width/2 + 190
                textY = ypos + rowHeight/4  

                #rank player data
                #renders font and prints to screen
                ranktext = rowFont.render(f"#{player['rank']}", True, rowColour)
                screen.blit(ranktext, (rankX, textY))

                #username player data
                #renders font and prints to screen
                username = player['username']
                usernametext = rowFont.render(username, True, rowColour) 
                screen.blit(usernametext, (usernameX, textY))

                #score player data
                #renders font and prints to screen
                scoretext = rowFont.render(str(player['score']), True, rowColour)
                screen.blit(scoretext, (scoreX, textY)) 

                #time taken player data
                #renders font and prints to screen
                timestr = f"{player['time']:.2f}s" #rounds to 2 decimal places
                timetext = rowFont.render(timestr, True, rowColour) 
                screen.blit(timetext, (timeX, textY))

                #adds all the headers, (rank, username, score, time) to the screen
                screen.blit(self.rankHeaderImage, (rankX, headerY))
                screen.blit(self.playerHeaderImage, (usernameX, headerY))
                screen.blit(self.scoreHeaderImage, (scoreX, headerY))
                screen.blit(self.timeHeaderImage, (timeX, headerY))

        #Exit information image displayed at end
        screen.blit(self.exitImage, (self.width/2 - self.exitImage.get_width()/2, 530))



    def run(self):
        pygame.init() #initialses pygame
        pygame.mixer.init() #initialses sound system for pygame
        
        #SCALED scales the game to the devices resolution
        screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED)
        pygame.display.set_caption("2D Dungeon Crawler")
        
        def toggleFullscreen():
            nonlocal screen
            currentFlags = screen.get_flags() #gets current screen flags
            #if theres a current flag and the game is in full screen
            if currentFlags and pygame.FULLSCREEN: 
                #full screen is exited
                screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED)
            else:
                #full screen is entered
                screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.SCALED)
                
        tmx_data = pytmx.load_pygame("TMX map\dungeon map.tmx")

        #game music
        pygame.mixer.music.load(r"Assets\Sounds\GameMusic.mp3")
        pygame.mixer.music.set_volume(self.volume / 100)  #volume setting indicated in main menu
        pygame.mixer.music.play(-1) 

        #initialise all sounds used
        shootsound = pygame.mixer.Sound(r"Assets\Sounds\GunFire.mp3")
        enemydeathsound = pygame.mixer.Sound(r"Assets\Sounds\EnemyDeath.mp3")
        playerfootstep = pygame.mixer.Sound(r"Assets\Sounds\PlayerFootstep.mp3")
        meleeattack = pygame.mixer.Sound(r"Assets\Sounds\MeleeAttack.mp3")
        winsound = pygame.mixer.Sound(r"Assets\Sounds\WinSound.mp3")
        losesound = pygame.mixer.Sound(r"Assets\Sounds\LoseSound.mp3")
        chestsound = pygame.mixer.Sound(r"Assets\Sounds\chestOpen.mp3")

        
        self.leaderboardTitleImage = pygame.image.load("Assets\Leaderboard\LeaderboardTitle.png").convert_alpha()
        self.leaderboardRowImage = pygame.image.load("Assets\Leaderboard\LeaderboardRow.png").convert_alpha()
        self.exitImage = pygame.image.load("Assets\Leaderboard\LeaderboardExitMessage.png").convert_alpha()
        self.rankHeaderImage = pygame.image.load("Assets\Leaderboard\RankHeader.png").convert_alpha()
        self.playerHeaderImage = pygame.image.load("Assets\Leaderboard\PlayerHeader.png").convert_alpha()
        self.scoreHeaderImage = pygame.image.load("Assets\Leaderboard\ScoreHeader.png").convert_alpha()
        self.timeHeaderImage = pygame.image.load("Assets\Leaderboard\TimeHeader.png").convert_alpha()

        #set the volume of all sfx to match stated volume
        shootsound.set_volume(self.volume / 100)
        enemydeathsound.set_volume(self.volume / 100)
        playerfootstep.set_volume(self.volume / 100)
        meleeattack.set_volume(self.volume / 100)
        winsound.set_volume(self.volume / 100)
        losesound.set_volume(self.volume / 100)
        chestsound.set_volume(self.volume / 100)

        tile_size = 64
        PLAYERWIDTH = 40
        PLAYERHEIGHT = 60

        clock = pygame.time.Clock()

        currentgamestate = "game"

        weaponTypes = {"basic" : {"name": "Pistol", "energycost" : 5, "damage" : 3, "bulletsize" : 20}, 
                       "sniper" : {"name": "Sniper","energycost" : 20, "damage": 30, "bulletsize" : 64}
                       , "machine" : {"name": "Machine Gun","energycost" : 2, "damage": 4, "bulletsize" : 10}}
        
        plrbullets = []
        enemybullets = []
        enemies = []
        walls = []

        dropped_weapons = []
        chests = []

        walkframeright = []

        #load damage indicator
        damageoverlay = pygame.image.load(r"Assets\Character\damageoverlay.png").convert_alpha()
        damageoverlay = pygame.transform.scale(damageoverlay, (self.width, self.height))
        
        for i in range(1, 5):  # Assuming files named walk1.png, walk2.png, etc.
            frame = pygame.image.load(rf"Assets\Character\walk{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (PLAYERWIDTH, PLAYERHEIGHT))
            walkframeright.append(frame)

        #flips all frames so i dont have to manually create new files for the different direction
        walkframesleft = [pygame.transform.flip(frame, True, False) for frame in walkframeright]

        #animation variables
        current_frame = 0 #refers to the index in the walkframe arrays to know what frame needs to show
        animation_speed = 0.2 #how fast the animations play  
        animation_timer = 0 #used to calculate when to change animations


        spawnx = 0 #initialses spawn positions
        spawny = 0

        walls = []
        closedBossDoor = None
        openedBossDoor = None

        

        for layer in tmx_data.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                if layer.name == "BossDoor":
                    closedBossDoor = layer
                    layer.visible = True  # Start closed
                elif layer.name == "BossDoorOpen":
                    openedBossDoor = layer
                    layer.visible = False  # Start hidden

        print(f"Boss door layers found: Closed={closedBossDoor is not None}, Open={openedBossDoor is not None}")

        #loops through all layers in the Tiled file
        for layer in tmx_data.layers:
            if isinstance(layer, pytmx.TiledTileLayer): #checks if its a layer
                if layer.name == "Chests": #and that layer is called Chests
                    for x, y, gid in layer:
                        if gid != 0:  #a chest tile is found
                            chestX = x * tile_size
                            chestY = y * tile_size
                            chests.append(Chest(chestX, chestY)) #adds it to the chest class

        def openBossDoor():
            nonlocal walls
            
            if closedBossDoor:
                closedBossDoor.visible = False
            if openedBossDoor:
                openedBossDoor.visible = True
            
            # Rebuild walls manually
            walls = []
    
            #this rebuilds all hitboxes of all walls in the game
            for layer in tmx_data.layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    #makes sure the layer is visible (closed boss door is disregarded since it becomes invisible)
                    #also makes sure its collidable
                    if layer.visible and layer.properties.get('collidable', False): #gets collidable property or returns false
                        for x, y, gid in layer:
                            if gid != 0:#makes sure it has a valid global id
                                worldx = x * tile_size #calculates hitbox position
                                worldy = y * tile_size
                                walls.append(pygame.Rect(worldx, worldy, tile_size, tile_size)) #adds to wall array
 
            print(f"Boss door opened! Total walls: {len(walls)}")
            print(f"Closed door layer visible: {closedBossDoor.visible if closedBossDoor else 'None'}")
            print(f"Open door layer visible: {openedBossDoor.visible if openedBossDoor else 'None'}")

            if not self.bossSpawned:
                #checks if the boss has not already spawned to prevent duplicate bosses
                for room in enemyspawnrooms: #loops through all rooms
                    if room['name'] == "boss_room": #checks if the name string is 'boss_room'
                        boss_x = room['x'] + room['width'] / 2 #finds the centre of the boss room
                        boss_y = room['y'] + room['height'] / 2
                        self.boss = Boss(boss_x, boss_y) #adds to boss file
                        self.bossSpawned = True #makes bossspawned true to prevent duplicates

                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(r"Assets\Sounds\BossMusic.mp3")
                        pygame.mixer.music.set_volume(self.volume / 100)
                        pygame.mixer.music.play(-1)
                        print("the boss has spawned")

                        break

        #spawns all the wall hitboxes before the game starts to initialise them
        for layer in tmx_data.layers:  #loops through every layer in my tile map
            if isinstance(layer, pytmx.TiledTileLayer):
                #checks for the attribute in tiled, 'collidable' this determins if its a wall or not
                # IMPORTANT: Also check if layer is visible AND if it's not the closed door when door is open
                if layer.visible and layer.properties.get('collidable', False):
                    for x, y, gid in layer:
                        if gid != 0:  #0 means empty tile
                            worldx = x * tile_size
                            worldy = y * tile_size
                            walls.append(pygame.Rect(worldx, worldy, tile_size, tile_size))
                
                #checks for the spawnpoint property, this determines where the player spawns
                if layer.properties.get('spawnpoint', False):
                    for x, y, gid in layer: 
                        if gid != 0:  #spawn tile found
                            spawnx = (x * tile_size) 
                            spawny = (y * tile_size) 
                            break


        screencenterx = self.width//2
        screencentery = self.height//2
        self.x = spawnx - screencenterx
        self.y = spawny - screencentery

        currentdirection = "right"
        player = Player(self.x,self.y)

        
        # Find all enemy spawn rooms
        enemyspawnrooms = []
        SCALEFACTOR = tile_size/16 #the room sized assume the tiles are 16x16, but they are not so we need to scale them
        for obj in tmx_data.objects: #loops through each object in Tileds object layer
            if 'Name' in obj.properties: #only rooms have this Name property, this prevents it getting other objects.
                roomname = obj.properties['Name'] #grabs the room name, e.g room_1, room_2, boss_room
                enemycount = obj.properties.get('enemy_count', 3) #this is a property given to each room in Tiled, this grabs the value of it
                
                enemyspawnrooms.append({ #stores all useful values of the room, this allows for the spawning of enemies in random parts of the room
                    'name': roomname,   
                    'x': obj.x *SCALEFACTOR,
                    'y': obj.y *SCALEFACTOR,
                    'width': obj.width *SCALEFACTOR,
                    'height': obj.height *SCALEFACTOR,
                    'enemy_count': enemycount,
                    'spawned': False    #useful since we can know if the enemies have spawned so they dont continiously spawn
                })

        enemiesToSpawn = sum(room['enemy_count'] for room in enemyspawnrooms) - 12
        enemieskilled = 0
        dooropened = False
        enemies = []
        #activerooms store the areas with enemies who spawned in them.
        activerooms = set() #allows the storing of multiple items in a single variable
        

        #when the tiles are loaded, put them into an array
        #so they dont have to be constantly grabbed from the file and back
        #saves on memory
        loadedtiles = {}

        for layer in tmx_data.layers: #loops through all layers
            if isinstance(layer, pytmx.TiledTileLayer): #checks if its a valid layer
                if "Door" in layer.name:
                    continue
                for x, y, gid in layer: #loops through the layer getting the global id
                    if gid != 0 and gid not in loadedtiles: #checks if its a valid tile and is not already in the list
                        image = tmx_data.get_tile_image_by_gid(gid) #since every tile has a gid its easy to get the image through this method
                        if image:
                            scaledimage = pygame.transform.scale(image, (tile_size, tile_size)) #scale it to the tile size
                            convertedimage = scaledimage.convert() #convert the image
                            convertedimage.set_colorkey((0, 0, 0)) #remove the black from the image

                            loadedtiles[gid] = convertedimage #add it to the dictionary

        self.starttime = pygame.time.get_ticks()
        weaponx = 0
        weapony = 0
        while self.running:
            clock.tick(60)

            if currentgamestate == "game":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F11:
                            toggleFullscreen() #when f11 is pressed full screen is toggled

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        
                        xmouse,ymouse = pygame.mouse.get_pos()
                        dx = xmouse - screencenterx
                        dy = ymouse - screencentery

                        length = math.hypot(dx,dy)
                        dx = (dx/length)*self.speed
                        dy = (dy/length)*self.speed

                        #initialises the bullet as an object in the bullet class
                        #dy and dy refer to the bullets velocity
                        #weaponx and weapony refer to the weapons position
                        currentWeapon = player.get_current_weapon()
                        if currentWeapon is None:
                            continue
                        
                        weaponworldx = weaponx + self.x
                        weaponworldy = weapony + self.y
                        
                        bulletinstance = Bullet(currentWeapon, weaponworldx, weaponworldy, dx, dy)

                        #checks if the player has enough energy to shoot 
                        if player.energy < bulletinstance.energyrequirement:
                            print("Insufficient energy!")
                        else:
                            player.energy -= bulletinstance.energyrequirement #takes away the energy requirement
                            player.drawHUD(screen, "Energy", currentWeapon, weaponTypes) #updates the HUD with the new energy
                            #adds the bullet to a bullet list which constantly updates the position of bullets
                            plrbullets.append(bulletinstance) 
                            shootsound.play() #plays shoot sound
                            
                        
                        print(str(player.energy) + " energy left/", "100 max energy") #prints how much energy is left out of 100
                        
                        print("Weapon: " + currentWeapon)
                        print("energy cost: " + str(bulletinstance.energyrequirement))
                        
                    

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            #players x and y position on the screen
                            playerworldx = self.x + screencenterx
                            playerworldy = self.y + screencentery

                            current_weapon = player.get_current_weapon() #get the currently equipped weapon from the player class
                            if current_weapon is not None: #If the player has a weapon equipped
                                #the weapon gets dropped and added to a table (player.width/height // 2 puts it in the centre)
                                dropped_weapons.append(Weapon(playerworldx - player.width // 4 ,playerworldy - player.height // 4 ,current_weapon))  
                            
                                player.weapon_slots[player.active_slot] = None #Changes the current weapon slot to be empty

                            else: #If no weapon is equipped, it will try to pick one up if its in range
                                #this creates a hitbox around the player to search for a dropped weapon
                                playerrect = pygame.Rect(playerworldx - player.width // 4, playerworldy - player.height // 4, player.width,  player.height)
                                for weapon in dropped_weapons:
                                    if playerrect.colliderect(weapon.rect):
                                        player.equip_weapon(weapon.weapon_type)
                                        # Update the weapon image after equipping
                                        if player.weapon_slots[player.active_slot] != None:
                                            player.weaponImage = pygame.image.load(f"Assets\\Weapons\\{player.weapon_slots[player.active_slot]}.png").convert_alpha()
                                            player.weaponSizeW = weaponSizes[player.weapon_slots[player.active_slot]]["width"] * player.weaponScale
                                            player.weaponSizeH = weaponSizes[player.weapon_slots[player.active_slot]]["height"] * player.weaponScale
                                        dropped_weapons.remove(weapon)
                                        print(f"picked {weapon.weapon_type}")
                                        break


                        elif event.key == pygame.K_TAB:
                            player.switch_weapon()



                screen.fill((0,0,0)) #resets screen by putting it all black 

                keys = pygame.key.get_pressed() #gets all keys so it can be passed into the player movement method
                oldx, oldy = self.x, self.y #gets the old position, so when a player hits a wall it puts them back.
                self.x, self.y = player.move(keys, self.up, self.down, self.left, self.right) #when the player moves it returns the new positions

                player.recoverenergy()

                for layer in tmx_data.layers: #loops through all layers in the tmx file
                    if isinstance(layer, pytmx.TiledTileLayer): #checks if its a tiled layer
                        for x, y, gid in layer:
                            if gid != 0 and gid in loadedtiles: #checks if that tile is in the cache array
                                drawx = x * tile_size - self.x #recalculates the new position (every frame)
                                drawy = y * tile_size - self.y
                                screen.blit(loadedtiles[gid], (drawx, drawy)) #adds them to screen

                for layer in tmx_data.layers: #loops through all layers in the tmx file
                    #checks if the layer has 'BossDoor' inside it and its currently visible
                    if isinstance(layer, pytmx.TiledTileLayer) and "BossDoor" in layer.name and layer.visible:
                        for x, y, gid in layer:
                            if gid != 0:
                                image = tmx_data.get_tile_image_by_gid(gid) #gets the image of the closed boss door (since this is the only one visible)
                                if image: #if theres a valid door it scales it and blits it to the screen
                                    scaled = pygame.transform.scale(image, (tile_size, tile_size))
                                    drawx = x * tile_size - self.x
                                    drawy = y * tile_size - self.y
                                    screen.blit(scaled, (drawx, drawy))
                                    
                
                ismoving = False
                if self.x == oldx: #checks if the old position (one frame ago) is the same as the new one
                    ismoving = False #in the current frame
                else:   #ismoving is true if the player has moved in the last frame and false if not
                    ismoving = True

                #changes direction depending on if left or right is pressed (works for both wasd and arrow keys)
                if keys[getattr(pygame, f'K_{self.left}')]:
                    currentdirection = "left"
                elif keys[getattr(pygame, f'K_{self.right}')]:
                    currentdirection = "right"

                #if its moving it cycles through each animation
                if ismoving:
                    animation_timer += animation_speed
                    if animation_timer >= 1:
                        animation_timer = 0
                        current_frame = (current_frame + 1) % 4  #cycles through each frame '%4' makes it strictly between 0 and 3 (frame numbers)
                        if current_frame == 1 or current_frame == 3:
                            playerfootstep.play()
                else: #if its not moving, it resets to the default animation (idle)
                    current_frame = 0  
                    animation_timer = 0

                #changes the sprite depending on the direction
                if currentdirection == "left":
                    currentsprite = walkframesleft[current_frame] #grabs the next frame in the cycle, this is what is shown to the screen
                else:
                    currentsprite = walkframeright[current_frame]

                #adds a hitbox on the player which will be used when finding if theres a collision
                playerscreenx = screencenterx - PLAYERWIDTH//2 #this gets the players position on the screen
                playerscreeny = screencentery - PLAYERHEIGHT//2 #to make it exact we need to factor in the player's proportions
                playerworldx = self.x + playerscreenx #gets the location of it in the actual map
                playerworldy = self.y + playerscreeny
                playerrect = pygame.Rect(playerworldx, playerworldy, PLAYERWIDTH, PLAYERHEIGHT) #adds the hitbox

                for wallrect in walls: #loops through all walls
                    if playerrect.colliderect(wallrect):
                        #checks if theres a collision between the wall and player
                        rectx = pygame.Rect(playerworldx, oldy + playerscreeny, PLAYERWIDTH, PLAYERHEIGHT)
                        #adds a rect on the x value to see if the wall is being hit on the x axis
                        if rectx.colliderect(wallrect): #if the wall is being hit on the x axis
                            self.x = oldx #the player is returned to its original position
                            player.x = oldx #changes both positions to be the old position 
                        
                        #does the same for the y axis to see if the collision is on the y axis
                        recty = pygame.Rect(oldx + playerscreenx, playerworldy, PLAYERWIDTH, PLAYERHEIGHT)
                        if recty.colliderect(wallrect):
                            self.y = oldy
                            player.y = oldy
                        #doing this allows the player to move along the wall instead of being stuck
                
                for chest in chests:
                    if not chest.opened and playerrect.colliderect(chest.rect):
                        chest.open(player, dropped_weapons)
                        chestsound.play()
                        print(f"Opened chest! Got {chest.rewardType}")

                #loops through each room which was identified before the game loop
                for room in enemyspawnrooms:
                    if room['name'] not in activerooms: #checks if the room is not currently active, (enemies havent spawned in it yet)
                        #finds the room center to calculate the distance between the player and the room
                        roomcenterx = room['x'] + room['width'] / 2 
                        roomcentery = room['y'] + room['height'] / 2
                        #distance is calculated using displacement from the centre using Pythagoras
                        distance = math.hypot(playerworldx - roomcenterx, playerworldy - roomcentery)
                        
                        SPAWNDISTANCE = 250
                        #if the distance is closer than 250 pixels the room becomes 'active'
                        if distance < SPAWNDISTANCE:
                            activerooms.add(room['name']) #adds to the list so enemies dont get added multiple times
                            
                            enemycount = room['enemy_count'] #gets the amount of enemies in the room
                            for i in range(enemycount): #loops through, each loop spawns an enemy
                                enemy_x = random.randint(int(room['x']), int(room['x'] + room['width']) - tile_size) #gets a random coordinate to spawn the enemy
                                enemy_y = random.randint(int(room['y']), int(room['y'] + room['height']) - tile_size)
                                
                                enemy = Enemy(enemy_x, enemy_y) 
                                enemies.append(enemy) #adds it to the enemy object class

                #draws bullets
                for bullet in plrbullets:
                    bullet.update()
                    bullet.draw(screen, self.x, self.y)

                #spawn enemies
                if keys[pygame.K_f] and len(enemies) == 0:
                    enemyinstance = Enemy(-self.x,-self.y)
                    enemies.append(enemyinstance.getrect())


                #handle enemy attacks
                for enemy in enemies:
                    bullet, melee = enemy.update(playerworldx, playerworldy, walls)
                    #enemy.update either returns None, False or True

                    if bullet: #if its a bullet its added to the enemybullet array
                        enemybullets.append(bullet)

                    if melee: #if its a melee enemy
                        player.health -= enemy.damage #the player takes damage
                        self.alphahit = 255
                        print(f"enemy hit player with melee, new health: {player.health}")
                        meleeattack.play()
                        if player.health <= 0: #if the players health reaches zero or below
                            currentgamestate = "end" #the game is then ended.

                # Update and draw enemy bullets
                for bullet in enemybullets:
                    bullet.update()
                    bullet.draw(screen, self.x, self.y)
                    
                    # Check if enemy bullet hits player
                    bullet_rect = bullet.getrect()
                    if bullet_rect.colliderect(playerrect):
                        player.health -= 1
                        enemybullets.remove(bullet)
                        self.alphahit = 255
                        print(f"Player hit! Health: {player.health}")
                        if player.health <= 0:
                            currentgamestate = "end"
                    
                    # Check if enemy bullet hits wall
                    else:
                        for wallrect in walls:
                            if bullet_rect.colliderect(wallrect):
                                if bullet in enemybullets:
                                    enemybullets.remove(bullet)
                                break

                for enemy in enemies:
                    enemy.draw(screen, self.x, self.y)

                if not dooropened and enemieskilled >= enemiesToSpawn:
                    dooropened = True
                    openBossDoor()
                    print("boss room unlocked")

                if self.boss and self.boss.alive:
                    bullets_list, melee = self.boss.update(playerworldx, playerworldy, walls)
                    
                    # Boss returns a LIST of bullets (for special attack)
                    for bullet in bullets_list:
                        enemybullets.append(bullet)
                    
                    if melee:
                        player.health -= self.boss.damage
                        self.alphahit = 255
                        print(f"BOSS MELEE HIT! Player health: {player.health}")
                        if player.health <= 0:
                            currentgamestate = "end"
                    
                    self.boss.draw(screen, self.x, self.y)

                for bullet in plrbullets[:]:
                    if self.boss and self.boss.alive and bullet.getrect().colliderect(self.boss.getrect()):
                        boss_died = self.boss.takedamage(bullet.weapon["damage"])
                        if boss_died:
                            print("BOSS DEFEATED!")
                            player.score += 1000
                            currentgamestate = "win"
                        if bullet in plrbullets:
                            plrbullets.remove(bullet)

                #bullet collisions
                for bullet in plrbullets:
                    rect = bullet.getrect()
                    hit = False
                    
                    # Check wall collision
                    for wallrect in walls:
                        if rect.colliderect(wallrect):
                            if bullet in plrbullets:
                                plrbullets.remove(bullet)
                            hit = True
                            break
                    
                    if not hit:
                        #loops through all enemies
                        for enemy in enemies:
                            if rect.colliderect(enemy.getrect()): #checks if the bullet has collided with the enemy rect
                                #using the bullet class dictionary, the damage of the currently held weapon is grabbed
                                bulletdamage = bullet.weapon["damage"]

                                #reduces the health of the enemy, the takedamage function returns a value
                                #returns false if the enemy is alive, true if it is dead
                                enemyDied = enemy.takedamage(bulletdamage)
                                
                                if enemyDied: #if the enemy has died (true is returned)
                                    enemies.remove(enemy) #its removed from the game and enemies array
                                    enemydeathsound.play()
                                    player.score += 10  #player gets score
                                    enemieskilled += 1
                                    print(f"{enemieskilled} / {enemiesToSpawn}")
                                
                                # Remove bullet
                                if bullet in plrbullets:
                                    plrbullets.remove(bullet)
                                hit = True
                                break

                #draw dropped weapons
                for weapon in dropped_weapons:
                    weapon.update_rect()
                    weapon.draw(screen, self.x, self.y)

                #draw weapon cursor
                xmouse, ymouse = pygame.mouse.get_pos()
                angle = math.atan2(ymouse - screencentery, xmouse - screencenterx)
                weaponx = screencenterx + math.cos(angle) * 40
                weapony = screencentery + math.sin(angle) * 40

                # Draw weapon cursor
                xmouse, ymouse = pygame.mouse.get_pos()
                angle = math.atan2(ymouse - screencentery, xmouse - screencenterx)
                weaponx = screencenterx + math.cos(angle) * 40
                weapony = screencentery + math.sin(angle) * 40

                

                #draw player on the screen
                playerscreenx = screencenterx - PLAYERWIDTH//2
                playerscreeny = screencentery - PLAYERHEIGHT//2
                screen.blit(currentsprite,(playerscreenx,playerscreeny))

                #Draw all chests
                for chest in chests:
                    chest.draw(screen, self.x, self.y)
                

                if player.weapon_slots[player.active_slot] != None: #checks if the player actually has a weapon
                    angleInDegrees = math.degrees(angle)
                    #converts the angle to degrees, the weapon is then scaled based on its specific aspect ratio
                    scaledWeapon = pygame.transform.scale(player.weaponImage, (player.weaponSizeW, player.weaponSizeH)) 
                    #weapon is rotated
                    rotatedWeapon = pygame.transform.rotate(scaledWeapon, -angleInDegrees)
                    weaponRect = rotatedWeapon.get_rect(center=(int(weaponx), int(weapony)))
                    screen.blit(rotatedWeapon, weaponRect) #adds to screen

                if self.alphahit > 0: #makes sure transparency cant go negative (errors out)
                    self.alphahit -= self.flashspeed #reduces it by flashspeed number every frame
                    if self.alphahit < 0: #makes sure it does not go negative
                        self.alphahit = 0

                #additionally, if its more than 255 (damage indicator is asked to be visible)
                if self.alphahit > 0:
                    damageoverlaycopy = damageoverlay.copy() #makes a copy so the original is not affected
                    damageoverlaycopy.set_alpha(self.alphahit) #uses set_alpha to change transparency
                    screen.blit(damageoverlaycopy, (0, 0)) #blits to whole screen
                    
                #draw the HUD
                player.drawHUD(screen, "Hearts", None, weaponTypes)
                player.drawHUD(screen, "Energy", player.get_current_weapon(), weaponTypes)
                player.drawHUD(screen, "Score", None, weaponTypes)
                if self.boss:
                    self.boss.drawHealthBar(screen, self.width, self.height)

                

            elif currentgamestate == "end":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False #stops program from running
                    elif (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and self.gameEnd == True:
                        #once the player clicks the screen, the leaderboard is then shown
                        self.leaderboardshown = True

                if not self.gameEnd: #if the game end hasnt already been fired
                    pygame.mixer.music.stop() #stops current music
                    losesound.play() #plays win sound
                    self.gameEnd = True #game end is now true, the above code will never execute again

                screen.fill((0,0,0))

                titleFont = pygame.font.Font(None, 72)
                subFont = pygame.font.Font(None, 30)
                text = titleFont.render("DEFEAT!", True, (255, 0, 0)) #adds the text to show the player they lost
                textsecond = subFont.render("Click any button to show the leaderboard", True, (255, 0, 0)) #visual indicator on what to do next

                #adds the text exactly in the middle of the screen
                screen.blit(text, (self.width/2 - text.get_width()/2, self.height/2 - text.get_height()/2)) 
                #adds the text 50 pixels below the middle of the screen
                screen.blit(textsecond, ((self.width/2 - textsecond.get_width()/2), (self.height/2 - textsecond.get_height()/2) + 50) )

                if self.leaderboardshown == True:
                    screen.fill((0,0,0)) #removes the DEFEAT! and click any button text 
                    gametime = (pygame.time.get_ticks() - self.starttime) / 1000 #converts game time to seconds
                    
                    if self.userData:#checks if the player is logged in (if they have userData)
                        leaderboard = Leaderboard() #leaderboard object
                        leaderboard.updatePlayerStats(self.userData[1], player.score, gametime) #updates player stats as shown

                    self.drawLeaderboard(screen, player.score, self.userData) #draws leaderboard

            elif currentgamestate == "win":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False #stops program from running
                    elif (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and self.gameEnd == True:
                        self.leaderboardshown = True

                if not self.gameEnd: #if the game end hasnt already been fired
                    pygame.mixer.music.stop() #stops current music
                    winsound.play() #plays win sound
                    self.gameEnd = True #game end is now true, the above code will never execute again

                screen.fill((0,0,0))

                titleFont = pygame.font.Font(None, 72)
                subFont = pygame.font.Font(None, 30)
                text = titleFont.render("VICTORY!", True, (0, 255, 0)) #adds the text to show the player they won
                textsecond = subFont.render("Click any button to show the leaderboard", True, (0, 255, 0)) #visual indicator on what to do next

                screen.blit(text, (self.width/2 - text.get_width()/2, self.height/2 - text.get_height()/2))
                screen.blit(textsecond, ((self.width/2 - textsecond.get_width()/2), (self.height/2 - textsecond.get_height()/2) + 50) )

                if self.leaderboardshown == True:
                    screen.fill((0,0,0)) #removes the VICTORY! and click any button text 
                    gametime = (pygame.time.get_ticks() - self.starttime) / 1000 #converts to seconds
                    
                    if self.userData: #checks if the player is logged in (if they have userData)
                        leaderboard = Leaderboard()
                        leaderboard.updatePlayerStats(self.userData[1], player.score, gametime) #updates player stats as shown
                        self.drawLeaderboard(screen, player.score, self.userData) #draws leaderboard

                    
                    
                
                


            pygame.display.update()

        pygame.quit()
        

