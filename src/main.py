import pygame
import sys
from pygame.locals import *
WIDTH = 1240
HEIGHT = 720
getTicksLastFrame = 0
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minigolf Masters")

class gamestate:
    def __init__(self, level, ui):
        self.players = 4
        self.level = level
        self.ui = ui
        self.amountWon = 0
        #                         1           2           3           4           5            6           7           8           9           10          11          12          13          14          15          16          17          18          19          20      
        self.levelStartpos = [(200, 360), (170, 170), (300, 150), (160, 170), (150, 360), (170, 360), (1100, 170), (170, 170), (170, 550), (100, 100), (170, 360), (100, 100), (170, 360), (620, 600), (150, 360), (130, 130), (170, 330), (100, 100), (200, 200), (660, 330)]
    
    def changeLevel(self, players, level):
        self.level = level
        for ball in players:
            ball.reset(self.levelStartpos[self.level])

#                    Game Objects Classes
# ============================================================

def wall(WINDOW, COLOR, players, startX, startY, length, width):
    # Draw wall to screen
    pygame.draw.rect(WINDOW, GRAY, (startX, startY, length, width))
    pygame.draw.rect(WINDOW, COLOR, (startX + 25, startY + 25, length - 50, width - 50))
    
    # Check for a collision with each player
    for ball in players:
        # Check if ball is within Y range
        if ball.y > startY and ball.y < startY + width:
            # Check if in top hit box
            if ball.x > startX - ball.r and ball.x < startX + length/2:
                # Move ball out of hit box 
                ball.x = startX - ball.r - 1
                # Reverse ball X Direction
                ball.speed[0] = -abs(ball.speed[0])
                # If ball hit hard play hit sound
                if ball.speed[0] > 100:
                    hit_sound.play()
            # Check if in bottom hit box
            elif ball.x > startX + length/2 and ball.x < startX + length + ball.r:
                # Move ball out of hit box 
                ball.x = startX + length + ball.r + 1
                # Reverse ball X Direction
                ball.speed[0] = abs(ball.speed[0])
                # If ball hit hard play hit sound
                if ball.speed[0] < -100:
                    hit_sound.play()
        # Check if ball is within X range
        elif ball.x > startX and ball.x < startX + length:
            # Check if in left hit box
            if ball.y > startY - ball.r and ball.y < startY + width/2:
                # Move ball out of hit box 
                ball.y = startY - ball.r - 1
                # Reverse ball Y Direction
                ball.speed[1] = -abs(ball.speed[1]) 
                # If ball hit hard play hit sound
                if (ball.speed[1] > 100):
                    hit_sound.play()
            # Check if in right hit box
            elif ball.y > startY + width/2 and ball.y < startY + width + ball.r:
                # Move ball out of hit box 
                ball.y = startY + width + ball.r + 1
                # Reverse ball Y Direction
                ball.speed[1] = abs(ball.speed[1])
                # If ball hit hard play hit sound
                if ball.speed[1] < -100:
                    hit_sound.play()

def BRcorner(WINDOW, players, x, y, size):
    # Draw wall to screen
    pygame.draw.polygon(WINDOW, GRAY, ((x, y), (x + size, y), (x, y + size)))
    # Get needed wall stuff
    slope = -1
    b = -(slope*x - (y + size)) + 12
    # Check for a collision with each player
    for ball in players:
            # Check if inside rectangle around wall
            if ball.x > x and ball.x < x + size and ball.y > y and ball.y < y + size:
                # Check if inside wall
                if ball.y < slope * ball.x + b:
                    hit_sound.play()
                    # Move ball out of hit box 
                    ball.x += 1
                    ball.y += 1
                    # Flip X and Y speed
                    temp = ball.speed[0]
                    ball.speed[0] = -ball.speed[1]
                    ball.speed[1] = -temp

def BLcorner(WINDOW, players, x, y, size):
    # Draw wall to screen
    pygame.draw.polygon(WINDOW, GRAY, ((x, y), (x - size, y), (x, y + size)))
    # Get needed wall stuff
    slope = 1
    b = y - (x - size) + 12
    
    # Check for a collision with each player
    for ball in players:
            # check if inside rectangle around wall
            if ball.x < x and ball.x > x - size and ball.y > y and ball.y < y + size:
                # check if inside wall
                if ball.y < slope * ball.x + b:
                    hit_sound.play()
                    # Move ball out of hit box 
                    ball.x -= 1
                    ball.y += 1
                    # Flip X and Y speed
                    temp = ball.speed[0]
                    ball.speed[0] = ball.speed[1]
                    ball.speed[1] = temp

def TRcorner(WINDOW, players, x, y, size):
    # Draw wall to screen
    pygame.draw.polygon(WINDOW, GRAY, ((x, y), (x + size, y), (x, y - size)))
    # Get needed wall stuff
    slope = 1
    b = y - (x + size) - 12

    # Check for a collision with each player
    for ball in players:
            #check if inside rectangle around wall
            if ball.x > x and ball.x < x + size and ball.y < y and ball.y > y - size:
                #check if inside wall
                if ball.y > slope * ball.x + b:
                    hit_sound.play()
                    # Move ball out of hit box 
                    ball.x += 1
                    ball.y -= 1
                    # Flip X and Y speed
                    temp = ball.speed[0]
                    ball.speed[0] = ball.speed[1]
                    ball.speed[1] = temp

def TLcorner(WINDOW, players, x, y, size):
    # Draw wall to screen
    pygame.draw.polygon(WINDOW, GRAY, ((x, y), (x - size, y), (x, y - size)))
    # Get needed wall stuff
    slope = -1
    b = y + (x - size) - 12

    # Check for a collision with each player
    for ball in players:
            #check if inside rectangle around wall
            if ball.x < x and ball.x > x - size and ball.y < y and ball.y > y - size:
                #check if inside wall
                if ball.y > slope * ball.x + b:
                    hit_sound.play()
                    # Move ball out of hit box 
                    ball.x -= 1
                    ball.y -= 1
                    # Flip X and Y speed
                    temp = ball.speed[0]
                    ball.speed[0] = -ball.speed[1]
                    ball.speed[1] = -temp

def slope(WINDOW, color, players, startX, startY, length, width, strengthX, strengthY):
    # Draw slope to screen
    pygame.draw.rect(WINDOW, color, [startX, startY, length, width])
    # Repeat collision check for each player
    for ball in players:
        # Check if inside slope
        if ball.x > startX and ball.x < startX + length and ball.y > startY and ball.y < startY + width:
            # Push ball in direction of slope
            ball.speed[0] += strengthX * deltaTime
            ball.speed[1] += strengthY * deltaTime
            
def sand(WINDOW, players, startX, startY, length, width):
    # Draw sand to screen
    pygame.draw.rect(WINDOW, YELLOW, [startX, startY, length, width])
    # Repeat collision check for each player
    for ball in players:
        # Check if inside sand
        if ball.x > startX and ball.x < startX + length and ball.y > startY and ball.y < startY + width:
            # Slow down ball
            ball.speed[0] -= ball.speed[0] * 5 * deltaTime
            ball.speed[1] -= ball.speed[1] * 5 * deltaTime     

def bouncepad(WINDOW, players, startX, startY, length, width, strength):
    # Same as wall but multiply with speed and different sound
    # Draw bounce pad to screen
    pygame.draw.rect(WINDOW, BLACK, (startX, startY, length, width))
    # Repeat collision check for each player
    for ball in players:
        # Check if ball is within Y range
        if ball.y > startY and ball.y < startY + width:
            # Check if in top hit box
            if ball.x > startX - ball.r and ball.x < startX + length/2:
                # Move ball out of hit box 
                ball.x = startX - ball.r - 1
                # Reverse ball Y Direction and increase speed
                ball.speed[0] = -abs(ball.speed[0]) * strength
                # Play bounce sound
                bounce_sound.play()
            # Check if in bottom hit box
            elif ball.x > startX + length/2 and ball.x < startX + length + ball.r:
                # Move ball out of hit box 
                ball.x = startX + length + ball.r + 1
                # Reverse ball Y Direction and increase speed
                ball.speed[0] = abs(ball.speed[0]) * strength
                # Play bounce sound
                bounce_sound.play()
        # Check if ball is within X range
        elif ball.x > startX and ball.x < startX + length:
            # Check if in left hit box
            if ball.y > startY - ball.r and ball.y < startY + width/2:
                # Move ball out of hit box 
                ball.y = startY - ball.r - 1
                # Reverse ball X Direction and increase speed
                ball.speed[1] = -abs(ball.speed[1]) * strength
                # Play bounce sound
                bounce_sound.play()
            # Check if in right hit box
            elif ball.y > startY + width/2 and ball.y < startY + width + ball.r:
                # Move ball out of hit box 
                ball.y = startY + width + ball.r + 1
                # Reverse ball X Direction and increase speed
                ball.speed[1] = abs(ball.speed[1]) * strength
                # Play bounce sound
                bounce_sound.play()
        
        # Set max speed
        if ball.speed[0] > 2200:
            ball.speed[0] = 2200
        if ball.speed[1] > 2200: 
            ball.speed[1] = 2200
        if ball.speed[0] < -2200:
            ball.speed[0] = -2200
        if ball.speed[1] < -2200:
            ball.speed[1] = -2200

def stickyWallX(WINDOW, players, startX, startY, length, width):
    # Draw wall to screen
    pygame.draw.rect(WINDOW, YELLOW, (startX, startY, length, width))
    # Repeat collision check for each player
    for ball in players:
        # Check if inside wall
        if ball.x > startX - ball.r + 3 and ball.x < startX + length + ball.r - 3 and ball.y > startY and ball.y < startY + width:
            # Move out of wall
            ball.x -= 1
            # Stop ball
            ball.speed[0] = 0
            ball.speed[1] = 0
            # Play stick sound
            stick_sound.play()

def stickyWallY(WINDOW, players, startX, startY, length, width):
    # Draw wall to screen
    pygame.draw.rect(WINDOW, YELLOW, (startX, startY, length, width))
    # Repeat collision check for each player
    for ball in players:
        # Check if inside wall
        if ball.x > startX - ball.r + 3 and ball.x < startX + length + ball.r - 3 and ball.y > startY and ball.y < startY + width:
            # Move out of wall
            ball.y -= 1
            # Stop ball
            ball.speed[0] = 0
            ball.speed[1] = 0
            # Play stick sound
            stick_sound.play()

def water(WINDOW, players, startX, startY, length, width):
    # Draw water to screen
    pygame.draw.rect(WINDOW, BLUE, (startX, startY, length, width))
    for ball in players:
        # Check if inside water
        if ball.x > startX - ball.r + 3 and ball.x < startX + length + ball.r - 3 and ball.y > startY and ball.y < startY + width:
            # Reset ball
            ball.reset(game.levelStartpos[game.level])
            # Play Splash sound 
            splash_sound.play()
            
def hole(WINDOW, COLOR, players, x, y, r):
    # Draw hole to screen
    pygame.draw.circle(WINDOW, COLOR, (x, y), r)
    # Repeat collision check for each player
    for ball in players:
        # Check if inside hole
        if ball.x > x - r and ball.x < x + r and ball.y > y - r and ball.y < y + r and not(ball.won):
            hole_sound.play()
            game.amountWon += 1
            # Move ball out side play area and turn of ball
            ball.x = 1500
            ball.y = 1000
            ball.speed = [0, 0]
            ball.won = True
        # Check if amount of every one won
        if game.amountWon == game.players:
            # Reset each ball
            for ball in players:
                ball.reset(game.levelStartpos[game.level-1])
            game.amountWon = 0
            # Change level
            game.changeLevel(players, game.level + 1)

class movableWall:
    def __init__(self, startX, startY, endX, endY, length, width, speedX, speedY):
        self.x = startX
        self.y = startY
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        self.length = length
        self.width = width
        self.speedX = speedX
        self.speedY = speedY

    def update(self):
        # Check if wall is out side of X range
        if self.x < self.startX:
            self.speedX = -self.speedX
            self.x = self.startX + 1
        elif self.x > self.endX:
            self.speedX = -self.speedX
            self.x = self.endX - 1
        # Check if wall is out side of Y range
        if self.y < self.startY:
            self.speedY = -self.speedY
            self.y = self.startY + 1
        elif self.y > self.endY:
            self.speedY = -self.speedY
            self.y = self.endY - 1
        # Move wall
        self.x += self.speedX * deltaTime
        self.y += self.speedY * deltaTime
        
        # draw wall and collision
        wall(WINDOW, GRAY, players, self.x, self.y, self.length, self.width)

class button:
    def __init__(self, img, target, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        self.target = target
        self.length = self.img.get_width()
        self.width = self.img.get_height()

    def isPressed(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        # Check if mouse is inside button
        if mouseY > self.y and mouseY < self.y + self.width and mouseX > self.x and mouseX < self.x + self.length:
            # Change ui to target
            game.ui = self.target
        # Returns true or false for custom actions
            return True
        return False

    def draw(self):
        # displays button
        WINDOW.blit(self.img, (self.x, self.y))


class balls:
    def __init__(self, COLOR):
        self.color = COLOR
        self.r = 10
        self.x = 100
        self.y = 100
        self.speed = [0.0, 0.0]
        self.charge = 600
        self.angle = 1
        self.angleChange = 0
        self.won = False
        self.shotsTaken = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]

    def update(self):
        # Update balls angle
        if self.speed[0] > -5  and self.speed[0] < 5 and self.speed[1] > -5 and self.speed[1] < 5 and not(self.won):
            pygame.draw.arc(WINDOW, self.color, (self.x - 50, self.y - 50, 100, 100), (self.angle - 0.05) * 3.1415/2, (self.angle + 0.05) * 3.1415/2, 50)
            self.angle += self.angleChange*deltaTime

        # Move ball
        self.x += self.speed[0] * deltaTime
        self.y += self.speed[1] * deltaTime

        # Slow down ball
        self.speed[0] -= self.speed[0] * ((0.95) * deltaTime)
        self.speed[1] -= self.speed[1] * ((0.95) * deltaTime)

        # Draw ball
        pygame.draw.circle(WINDOW, (255, 255, 255), (round(self.x), round(self.y)), self.r)

    def reset(self, pos):
        # Change to defaults
        self.x = pos[0]
        self.y = pos[1]
        self.speed = [0.0, 0.0]
        self.charge = 600
        self.angle = 1
        self.angleChange = 0
        self.won = False
        

    def shoot(self):
        # check if not moving
        if self.speed[0] > -5 and self.speed[0] < 5 and self.speed[1] > -5 and self.speed[1] < 5:
            # Play sound
            ball_shoot_sound.play()
            # Add one to score
            self.shotsTaken[game.level] += 1
            
            # TODO: replace with modulus
            # Correct angle so its between 1 - 4
            while self.angle > 4:
                self.angle -= 4
            while self.angle < 0:
                self.angle += 4
                
            # TODO: replace with sin and cos
            # Find the quadrant the angle is in and split the angle and charge in to x and y speed
            if self.angle >= 0 and self.angle <= 1:
                self.speed[0] = (self.charge * (1 - self.angle))
                self.speed[1] = (-(self.charge * self.angle))
            elif self.angle >= 1 and self.angle <= 2:
                self.speed[0] = (-(self.charge * (self.angle - 1)))
                self.speed[1] = -(self.charge * (1 - (self.angle - 1)))
            elif self.angle >= 2 and self.angle <= 3:
                self.speed[0] = -(self.charge * (1 - (self.angle - 2)))
                self.speed[1] = (self.charge * (self.angle - 2))
            elif self.angle >= 3 and self.angle <= 4:
                self.speed[0] = self.charge * (self.angle - 3)
                self.speed[1] = self.charge * (1 - (self.angle - 3))
      
#                         Constants
# ============================================================          

# Colors
GRAY = (165, 165, 165)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (26, 148, 34)
LIGHTGREEN = (95, 173, 86)
DARKGREEN = (19, 130, 17)
BLUE = (16, 178, 202)
RED = (228, 87, 46)
YELLOW = (208, 190, 162)
playerColors = [BLUE, RED, YELLOW, LIGHTGREEN]

# Level buttons
levels = []
buttonX = 90
buttonY = 50
# Repeat for each button
for i in range(1, 21):
    # Move down row 
    if buttonX > 1000:
        buttonX = 90
        buttonY += 155
    lev = button("assets/level-thumbnails/"+str(i)+".png", 0, buttonX, buttonY)
    buttonX += 210
    levels.append(lev)

# Ui buttons
menu = button("assets/menu.png", 1, 55, 3)
play = button("assets/play.png", 0, 550, 200)
Exit = button("assets/back.png", 1, 12, 12)
back = button("assets/exit.png", 0, 1195, 12)
levelbutton = button("assets/levels.png", 4, 490, 290)
scorebutton = button("assets/score.png", 2, 525, 375)
controls = button("assets/controls.png", 5, 480, 480)
playersDown = button("assets/playerdown.png", 1, 700, 570)
playersUp = button("assets/playerup.png", 1, 800, 572)

# Text
title = pygame.image.load("assets/title.png")
playercontrols = pygame.image.load("assets/playercontrols.png")
playersbutton = pygame.image.load("assets/players.png")
hooge = pygame.font.SysFont("hooge 05_55", 28)
hooge52 = pygame.font.SysFont("hooge 05_55", 52)
levelsText = hooge.render("Hole ", False, WHITE)

# Sound effects
hit_sound = pygame.mixer.Sound("assets/sound-effects/ballhitsound.wav")
ball_shoot_sound = pygame.mixer.Sound("assets/sound-effects/ballshootsound.wav")
splash_sound = pygame.mixer.Sound("assets/sound-effects/watersplashsound.wav")
bounce_sound = pygame.mixer.Sound("assets/sound-effects/rubberbounce.wav")
stick_sound = pygame.mixer.Sound("assets/sound-effects/sticksound.wav")
hole_sound = pygame.mixer.Sound("assets/sound-effects/holesound.wav")
background_music = pygame.mixer.music.load("assets/soundtrack.mp3")
pygame.mixer.music.play(-1)

# Players
game = gamestate(0, 1)
players = []
for i in range(game.players):
    players.append(balls(playerColors[i]))
    players[i].reset(game.levelStartpos[0])

# Level 13 moveable walls
wall1 = movableWall(300, 235, 400, 395, 50, 100, 0, 100)
wall2 = movableWall(600, 235, 700, 395, 50, 100, 0, 100)
wall3 = movableWall(900, 235, 1000, 395, 50, 100, 0, 100)

# Level 14 moveable walls
wall4 = movableWall(400, 170, 800, 180, 50, 330, 70, 0)

# Level 15 moveable walls
wall5 = movableWall(300, 200, 310, 500, 650, 50, 0, 325)

# Level 16 moveable walls
wall6 = movableWall(340, 230, 1000, 400, 50, 300, 150, 0)
wall7 = movableWall(340, 230, 1000, 400, 150, 50, 150, 0)
wall8 = movableWall(340, 530, 1000, 600, 150, 50, 150, 0)

# TODO: clean up god awful main loop
def main():
    #                         Main Loop
    # ============================================================       

    while True:
        # Get delta time
        t = pygame.time.get_ticks()
        deltaTime = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t
        WINDOW.fill(GREEN)
        
    #                             Controls
    # ==================================================================
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # In game controls
            elif game.ui == 0:
                if event.type == pygame.KEYDOWN:
                    if game.players >= 4:
                        # Controls for player 4
                        if not players[3].won:
                            if event.key == pygame.K_KP5:
                                if players[3].charge > 600:
                                    players[3].charge -= 400
                            elif event.key == pygame.K_KP8:
                                if players[3].charge < 1800:
                                    players[3].charge += 400
                            elif event.key == pygame.K_KP6:
                                players[3].angleChange = -2
                            elif event.key == pygame.K_KP4:
                                players[3].angleChange = 2
                            elif event.key == pygame.K_KP0:
                                players[3].shoot()
                    if game.players >= 3:
                        # Controls for player 3
                        if not players[2].won:
                            if event.key == pygame.K_k:
                                if players[2].charge > 600:
                                    players[2].charge -= 400
                            elif event.key == pygame.K_i:
                                if players[2].charge < 1800:
                                    players[2].charge += 400
                            elif event.key == pygame.K_l:
                                players[2].angleChange = -2
                            elif event.key == pygame.K_j:
                                players[2].angleChange = 2
                            elif event.key == pygame.K_SPACE:
                                players[2].shoot()
                    if game.players >= 2:
                        # Controls for player 2
                        if not players[1].won:
                            if event.key == pygame.K_s:
                                if players[1].charge > 600:
                                    players[1].charge -= 400
                            elif event.key == pygame.K_w:
                                if players[1].charge < 1800:
                                    players[1].charge += 400
                            elif event.key == pygame.K_d:
                                players[1].angleChange = -2
                            elif event.key == pygame.K_a:
                                players[1].angleChange = 2
                            elif event.key == pygame.K_LCTRL:
                                players[1].shoot()
                        # Controls for player 1
                    if not players[0].won:
                        if event.key == pygame.K_DOWN:
                            if players[0].charge > 600:
                                players[0].charge -= 400
                        elif event.key == pygame.K_UP:
                            if players[0].charge < 1800:
                                players[0].charge += 400
                        elif event.key == pygame.K_RIGHT:
                            players[0].angleChange = -2
                        elif event.key == pygame.K_LEFT:
                            players[0].angleChange = 2
                        elif event.key == event.key == K_RETURN:
                            players[0].shoot()
                # Reset move values
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        players[0].angleChange = 0
                    elif game.players >= 2 and (event.key == pygame.K_a or event.key == pygame.K_d):
                        players[1].angleChange = 0
                    elif game.players >= 3 and (event.key == pygame.K_j or event.key == pygame.K_l):
                        players[2].angleChange = 0
                    elif game.players >= 4 and (event.key == pygame.K_KP4 or event.key == pygame.K_KP6):
                        players[3].angleChange = 0

                # Buttons
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Check buttons
                        back.isPressed()
                        menu.isPressed()

            # Title screen controls
            elif game.ui == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        scorebutton.isPressed()
                        play.isPressed()
                        controls.isPressed()
                        levelbutton.isPressed()
                        #custom button changes player amount
                        if playersDown.isPressed():
                            if game.players > 1:
                                game.players -= 1
                                players.pop()
                        #custom button changes player amount
                        if playersUp.isPressed():
                            if game.players < 4:
                                players.append(balls(playerColors[game.players]))
                                game.players += 1

            # Score controls
            elif game.ui == 2:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        Exit.isPressed()
                        back.isPressed()

            # Level selector controls
            elif game.ui == 4:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        Exit.isPressed()
                        back.isPressed()
                        index = 0
                        # Check each level button
                        for button in levels:
                            if button.isPressed():
                                game.changeLevel(players, index)
                            index += 1
            
            # Controls Screen
            elif game.ui == 5:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        Exit.isPressed()
                        back.isPressed()


    #                            levels
    # ==================================================================

        if game.level == 0:
            BLcorner(WINDOW, players, 1215, 35, 200)
            TLcorner(WINDOW, players, 1215, 695, 200)
            wall(WINDOW, GRAY, players, 800, 200, 50, 325)
            hole(WINDOW, WHITE, players, 1070, 360, 15)
            
        elif game.level == 1:
            BLcorner(WINDOW, players, 1215, 35, 200)
            TLcorner(WINDOW, players, 1215, 695, 200)
            wall(WINDOW, GRAY, players, 30, 330, 850, 50)
            hole(WINDOW, WHITE, players, 200, 530, 15)

        elif game.level == 2:
            wall(WINDOW, GRAY, players, 800, 30, 50, 250)
            wall(WINDOW, GRAY, players, 800, 400, 50, 300)
            TRcorner(WINDOW, players, 50, 700, 200)
            hole(WINDOW, WHITE, players, 1050, 145, 15)

        elif game.level == 3:
            TRcorner(WINDOW, players, 50, 700, 150)
            TLcorner(WINDOW, players, 600, 700, 150)
            BRcorner(WINDOW, players, 350, 35, 200)
            BLcorner(WINDOW, players, 900, 35, 150)
            TRcorner(WINDOW, players, 650, 700, 200)
            wall(WINDOW, GRAY, players, 300, 30, 50, 400)
            wall(WINDOW, GRAY, players, 900, 30, 315, 400)
            wall(WINDOW, GRAY, players, 600, 340, 50, 400)
            hole(WINDOW, WHITE, players, 1050, 570, 15)
        
        elif game.level == 4:
            slope(WINDOW, LIGHTGREEN, players, 300, 35, 100, 700, -2000, 0)
            slope(WINDOW, DARKGREEN, players, 400, 35, 100, 700, 2000, 0)
            slope(WINDOW, LIGHTGREEN, players, 750, 35, 100, 700, -2000, 0)
            slope(WINDOW, DARKGREEN, players, 850, 35, 100, 700, 2000, 0)
            hole(WINDOW, WHITE, players, 1075, 360, 15)
        
        elif game.level == 5:
            slope(WINDOW, LIGHTGREEN, players, 550, 33, 450, 300, -350,  0)
            slope(WINDOW, LIGHTGREEN, players, 550, 495, 450, 300, -350,  0)
            wall(WINDOW, GRAY, players, 550, 225, 450, 270)
            hole(WINDOW, WHITE, players, 1100, 360, 15)
            
        elif game.level == 6:
            BRcorner(WINDOW, players, 54, 35, 200)
            slope(WINDOW, DARKGREEN, players, 320, 35, 650, 400, 350,  0)
            slope(WINDOW, LIGHTGREEN, players, 55, 300, 270, 250, 0, -1000)
            wall(WINDOW, DARKGREEN, players, 320, 300, 1000, 600)
            hole(WINDOW, WHITE, players, 180, 620, 15)

        elif game.level == 7:
            slope(WINDOW, LIGHTGREEN, players, 320, 35, 560, 345, -430,  0)
            slope(WINDOW, LIGHTGREEN, players, 320, 370, 560, 370, -430,  0)
            BLcorner(WINDOW, players, 1215, 35, 200)
            TLcorner(WINDOW, players, 1215, 695, 200)
            wall(WINDOW, GRAY, players, 30, 330, 850, 50)
            hole(WINDOW, WHITE, players, 950, 360, 15)    
        
        elif game.level == 8:
            BRcorner(WINDOW, players, 54, 35, 200)
            BLcorner(WINDOW, players, 1215, 35, 200)
            sand(WINDOW, players, 300, 300, 625, 400)
            hole(WINDOW, WHITE, players, 1050, 550, 15)
        
        elif game.level == 9:
            sand(WINDOW, players, 940, 33, 300, 675)
            wall(WINDOW, GRAY, players, 30, 330, 650, 50)
            hole(WINDOW, WHITE, players, 200, 530, 15)

        elif game.level == 10:
            slope(WINDOW, LIGHTGREEN, players, 500, 33, 250, 675, -300, 0)
            BLcorner(WINDOW, players, 1215, 35, 200)
            TRcorner(WINDOW, players, 50, 700, 150)
            sand(WINDOW, players, 300, 33, 200, 400)
            sand(WINDOW, players, 750, 350, 200, 400)
            wall(WINDOW, GRAY, players, 375, 33, 50, 340)
            wall(WINDOW, GRAY, players, 825, 410, 50, 340)
            hole(WINDOW, WHITE, players, 1100, 550, 15)
        
        elif game.level == 11:
            slope(WINDOW, DARKGREEN, players, 55, 170, 245, 163, 0, 700)
            slope(WINDOW, LIGHTGREEN, players, 55, 375, 245, 400, 0, -700)
            sand(WINDOW, players, 300, 33, 700, 300)
            sand(WINDOW, players, 300, 375, 700, 320)
            wall(WINDOW, GRAY, players, 1000, 33, 40, 300)
            wall(WINDOW, GRAY, players, 1000, 375, 40, 320)
            hole(WINDOW, WHITE, players, 1125, 350, 15)
            
        elif game.level == 12:
            wall1.update()
            wall2.update()
            wall3.update()
            wall(WINDOW, GRAY, players, 300, 33, 50, 200)
            wall(WINDOW, GRAY, players, 600, 33, 50, 200)
            wall(WINDOW, GRAY, players, 900, 33, 50, 200)
            wall(WINDOW, GRAY, players, 300, 495, 50, 200)
            wall(WINDOW, GRAY, players, 600, 495, 50, 200)
            wall(WINDOW, GRAY, players, 900, 495, 50, 200)
            hole(WINDOW, WHITE, players, 1050, 360, 15)

        elif game.level == 13:
            slope(WINDOW, DARKGREEN, players, 55, 33, 345, 680, 1000, 0)
            slope(WINDOW, LIGHTGREEN, players, 850, 33, 370, 680, -1000, 0)
            hole(WINDOW, WHITE, players, 620, 330, 15)
            wall(WINDOW, GRAY, players, 400, 170, 450, 50)
            wall(WINDOW, GRAY, players, 400, 450, 450, 50)
            wall4.update()

        elif game.level == 14:
            sand(WINDOW, players, 300, 33, 650, 165)
            sand(WINDOW, players, 300, 550, 650, 165)
            wall(WINDOW, GRAY, players, 275, 33, 50, 165)
            wall(WINDOW, GRAY, players, 925, 33, 50, 165)
            wall(WINDOW, GRAY, players, 275, 550, 50, 165)
            wall(WINDOW, GRAY, players, 925, 550, 50, 165)
            wall5.update()
            hole(WINDOW, WHITE, players, 1100, 370, 15)

        elif game.level == 15:
            slope(WINDOW, LIGHTGREEN, players, 250, 33, 730, 690, -1500, 0)
            wall6.update()
            wall7.update()
            wall8.update()
            hole(WINDOW, WHITE, players, 1100, 550, 15)

        elif game.level == 16:
            stickyWallX(WINDOW, players, 1165, 33, 50, 690)
            bouncepad(WINDOW, players, 55, 200, 50, 300, 3)
            wall(WINDOW, GRAY, players, 55, 33, 50, 167)
            wall(WINDOW, GRAY, players, 55, 500, 50, 200)
            slope(WINDOW, LIGHTGREEN, players, 300, 33, 670, 690, -1500, 0)
            hole(WINDOW, WHITE, players, 1050, 360, 15)

        elif game.level == 17:
            slope(WINDOW, DARKGREEN, players, 0, 0, 300, 650, 0, 1800)
            slope(WINDOW, DARKGREEN, players, 300, 0, 300, 600, 0, 1800)
            slope(WINDOW, DARKGREEN, players, 600, 0, 620, 550, 0, 1800)
            stickyWallY(WINDOW, players, 0, 670, 300, 50)
            stickyWallY(WINDOW, players, 300, 620, 1240, 100)
            stickyWallY(WINDOW, players, 600, 580, 1240, 100)
            wall(WINDOW, GRAY, players, 250, 340, 50, 500)
            wall(WINDOW, GRAY, players, 850, 270, 50, 500)
            wall(WINDOW, GRAY, players, 550, 290, 50, 500)
            TRcorner(WINDOW, players, 275, 340, 24)
            TLcorner(WINDOW, players, 274, 340, 24)
            TRcorner(WINDOW, players, 575, 290, 24)
            TLcorner(WINDOW, players, 574, 290, 24)
            TRcorner(WINDOW, players, 875, 270, 24)
            TLcorner(WINDOW, players, 874, 270, 24)
            hole(WINDOW, WHITE, players, 1050, 400, 15)

        elif game.level == 18:
            water(WINDOW, players, 430, 200, 50, 300)
            water(WINDOW, players, 430, 200, 350, 50)
            water(WINDOW, players, 430, 500, 350, 50)
            BRcorner(WINDOW, players, 54, 35, 150)
            TRcorner(WINDOW, players, 55, 700, 150)
            BLcorner(WINDOW, players, 1215, 35, 200)
            TLcorner(WINDOW, players, 1215, 695, 200)
            hole(WINDOW, WHITE, players, 620, 370, 15)

        # Test level 
        elif game.level == 19:
            BRcorner(WINDOW, players, 54, 35, 150)
            TRcorner(WINDOW, players, 55, 700, 150)
            BLcorner(WINDOW, players, 1215, 35, 150)
            TLcorner(WINDOW, players, 1215, 695, 150)
            wall(WINDOW, GRAY, players, 300, 200, 50, 200)
            wall(WINDOW, GRAY, players, 300, 200, 200, 50)
            wall(WINDOW, GRAY, players, 300, 300, 200, 50)
            wall(WINDOW, GRAY, players, 300, 400, 200, 50)
            wall(WINDOW, GRAY, players, 550, 200, 50, 250)
            wall(WINDOW, GRAY, players, 700, 200, 50, 250)
            wall(WINDOW, GRAY, players, 550, 200, 150, 50)
            wall(WINDOW, GRAY, players, 800, 200, 50, 250)
            wall(WINDOW, GRAY, players, 940, 210, 50, 230)
            wall(WINDOW, GRAY, players, 800, 200, 150, 50)
            wall(WINDOW, GRAY, players, 800, 400, 150, 50)

        # default level objects
        wall(WINDOW, GRAY, players, -20, 0, 75, 720)
        wall(WINDOW, GRAY, players, 0, -40, 1240, 75)
        wall(WINDOW, GRAY, players, 1215, 0, 75, 720)
        wall(WINDOW, GRAY, players, 0, 695, 1240, 75)
        for ball in players:
            ball.update()


    #                         User Interface
    # ==================================================================

        # Ingame display
        if game.ui == 0:
            # Buttons
            menu.draw()

            # Reset positions
            meterX = 5
            meterY = 5
            shotsX = 70
            i = 1

            # Draw power meter for each player
            for ball in players:
                pygame.draw.rect(WINDOW, (200, 200, 200), (meterX, meterY, 21, -350))
                pygame.draw.rect(WINDOW, ball.color, (meterX, meterY, 21, (ball.charge/4 - 100)))
                pygame.draw.rect(WINDOW, WHITE, (meterX, meterY, 21, 50), 3)
                pygame.draw.rect(WINDOW, WHITE, (meterX, meterY, 21, 150), 3)
                pygame.draw.rect(WINDOW, WHITE, (meterX, meterY, 21, 250), 3)
                pygame.draw.rect(WINDOW, WHITE, (meterX, meterY, 21, 350), 3)

                # Score on top of screen
                WINDOW.blit(hooge.render("P" + str(i) + ": " + str(ball.shotsTaken[game.level]), False, WHITE), (shotsX + 33, 10))

                # Change positions
                i += 1
                meterX += 21
                shotsX += 120
                # moves down power meter two second row 
                if meterX > 30:
                    meterX = 5
                    meterY += 359

            # Level indicator
            WINDOW.blit(levelsText, (580, 10))
            WINDOW.blit(hooge.render('#' + str(game.level + 1), False, WHITE), (660, 10))

        # Main menu
        elif game.ui == 1:
            WINDOW.fill(GREEN)
            WINDOW.blit(title, (365, 30))
            play.draw()
            levelbutton.draw()
            scorebutton.draw()
            WINDOW.blit(playersbutton, (400, 550))
            controls.draw()
            playersUp.draw()
            playersDown.draw()
            WINDOW.blit(hooge52.render(str(game.players), False, WHITE), (757, 590))

        # Score screen
        elif game.ui == 2:
            WINDOW.fill(GREEN)
            # page and out line
            pygame.draw.rect(WINDOW, WHITE, (40, 100, 1160, 350))
            pygame.draw.rect(WINDOW, BLACK, (40, 100, 1160, 350), 5)
            WINDOW.blit(hooge.render("T" , False, BLACK), (1160, 125))
            
            # Buttons
            Exit.draw()
            back.draw()
            w = 0
            # row for each player
            for ball in players:
                w += 1
                WINDOW.blit(hooge.render("P" + str(w), False, BLACK), (50, w * 50 + 150))
                WINDOW.blit(hooge.render(str(sum(ball.shotsTaken)), False, BLACK), (1160, w * 50 + 150))
                pygame.draw.rect(WINDOW, BLACK, (40, w * 50 + 130, 1160, 5))
                # Show player score for each player
                for i in range(20):
                    WINDOW.blit(hooge.render(str(ball.shotsTaken[i]), False, BLACK), (i * 50 + 150, w * 50 + 150))
            # Show player score for each player
            for z in range(20):
                WINDOW.blit(hooge.render(str(z + 1), False, BLACK), (z * 50 + 145, 125))
                pygame.draw.rect(WINDOW, BLACK, (z * 50 + 130, 100, 5, 350))

        # Level selector screen
        elif game.ui == 4:
            WINDOW.fill(GREEN)

            #Draw each level button
            for button in levels:
                button.draw()
            Exit.draw()
            back.draw()

        # Controls screen
        elif game.ui == 5:
            WINDOW.fill(GREEN)
            WINDOW.blit(playercontrols, (0, 0))
            Exit.draw()
            back.draw()

        # Check if player escaped play area
        for ball in players:
            if ball.x < 0:
                ball.x += 50
            elif ball.x > 1240 and not(ball.x == 1500):
                ball.x -= 50
            if ball.y < 0:
                ball.y += 50
            elif ball.y > 720 and not(ball.y == 1000):
                ball.y -= 50

        pygame.display.update()

if __name__ == "__main__":
    main()