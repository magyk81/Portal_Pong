# Professor Castellanos
# TA - Brett Hartel
# CS 105 - 009

#######CONTROLS#######
# W: Player A moves up
# X: Player A moves down
# D: Player A shoots straight
# E: Player A shoots upward
# C: Player A shoots downward
# L: Player A makes portal after bullet is shot
# O: Player B moves up
# PERIOD: Player B moves down
# K: Player B shoots straight
# I: Player B shoots upward
# COMMA: Player B shoots downward
# S: Player B makes portal after bullet is shot
# ESCAPE: Quits the game

# Xbox controller inputs also enabled for 2 players. If you're using a controller:
#The left thumbstick controls movement of the corresponding gun/paddle.
#B button:Shoots a straight bullet
#Y button: Shoots an upward diagonal bullet
#A button: Shoots a downward diagonal bullet
#X button: Press after you fire a bullet to create a portal

# Import everything
import sys
sys.path.insert(1,"C:/Users/Benjammin1701/Desktop/School Stuff/CS105/python_CS105/Python27/Lib/site-packages")
import math
import random
import pygame
from pygame.locals import *
from pygame import mixer

pygame.init()


screenWidth = 1024
screenHeight = 768
screen = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)
pygame.display.set_caption("Portal Pong")

# Define sounds and soundtrack
sound_Goodbye = pygame.mixer.Sound('Turret_Goodbye.wav')
sound_Hellooo = pygame.mixer.Sound('Turret_Hellooo.wav')
sound_Noooo = pygame.mixer.Sound('Turret_Noooo.wav')
sound_Wheee = pygame.mixer.Sound('Turret_Wheeee.wav')
sound_WellDone = pygame.mixer.Sound('Player_Scores.wav')
sound_ShootPowerup = pygame.mixer.Sound('Shoot_Bullet_Powerup.wav')
sound_ShootBullet = pygame.mixer.Sound('Shoot_Bullet.wav')
sound_PortalOpens = pygame.mixer.Sound('Portal_Opens.wav')
sound_PortalCloses = pygame.mixer.Sound('Portal_Closes.wav')
sound_PenaltyCollision = pygame.mixer.Sound('Penalty_Box_Collision.wav')
sound_BulletIntoPortal = pygame.mixer.Sound('Bullet_into_portal.wav')
sound_BulletHitBall = pygame.mixer.Sound('Bullet_Hit_Ball.wav')
sound_BulletBounceWall = pygame.mixer.Sound('Bullet_Bounce_Wall.wav')
sound_Powerup = pygame.mixer.Sound('Get_Powerup.wav')
sound_BallBounceWall = pygame.mixer.Sound('Ball_Bounce_Wall.wav')

music_menu = pygame.mixer.Sound('Menu music.ogg')
music_inGame = pygame.mixer.Sound('InGame Music.ogg')
music_end = pygame.mixer.Sound('End Game music.ogg')

# Define images
image_background = 'ApertureLabs.jpg'
image_blueBall = 'PortalGun_Blue.png'
image_greenBall = 'PortalGun_Green.png'
image_greenBall_powered = 'PortalGun_Green_Powered.png'
image_redBall = 'PortalGun_Red.png'
image_redBall_powered = 'PortalGun_Red_Powered.png'
sprite1_image_filename = 'BluePortal.png'
sprite2_image_filename = 'OrangePortal.png'
sprite3_image_filename = 'OrangePortal2.png'
sprite4_image_filename = 'BluePortal2.png'
sprite5_image_filename = 'Border_Top_Bottom.png'
sprite6_image_filename = 'Plasma Ball Small.png'
sprite6_image_faster = 'Plasma Ball Small_faster.png'
sprite6_image_stronger = 'Plasma Ball Small_stronger.png'
sprite7_image_filename = 'Plasma Ball Small_d1.png'
sprite7_image_faster = 'Plasma Ball Small_d1_faster.png'
sprite7_image_stronger = 'Plasma Ball Small_d1_stronger.png'
sprite8_image_filename = 'Plasma Ball Small_d2.png'
sprite8_image_faster = 'Plasma Ball Small_d2_faster.png'
sprite8_image_stronger = 'Plasma Ball Small_d2_stronger.png'
sprite9_image_filename = 'PortalGunSmall1.png'
sprite9_image_faster = 'PortalGunSmall1_faster.png'
sprite9_image_stronger = 'PortalGunSmall1_stronger.png'
sprite9_image_paddle = 'PortalGunSmall1_paddle.png'
sprite10_image_filename = 'PortalGunSmall2.png'
sprite10_image_faster = 'PortalGunSmall2_faster.png'
sprite10_image_stronger = 'PortalGunSmall2_stronger.png'
sprite10_image_paddle = 'PortalGunSmall2_paddle.png'
sprite11_image_filename = 'Power_Up.png'
sprite12_image_filename = 'penalty.png'

# Our clock object
clock = pygame.time.Clock()
BLACK = (0,0,0)
GREEN = (0,191,70)
RED = (191,70,70)
YELLOW = (220,220,0)
ORANGE = (255,140,0)
BLUE = (0,220,220)
ballcolor = YELLOW
temp = 0

# Powerups
def randpower(power):
    if power == 0: return 'Faster Bullets'
    if power == 1: return 'Faster Paddle'
    if power == 2: return 'Faster Ball'
    if power == 3: return 'Stronger Bullets'

def stronger_bullets(speed,playerA,playerB):
    if playerA == 'Stronger Bullets': new_speed = speed * 2
    elif playerB == 'Stronger Bullets': new_speed = speed * 2
    else: new_speed = speed
    return new_speed

def faster_bullets(speed,playerA,playerB):
    if playerA == 'Faster Bullets': new_speed = speed * 2
    elif playerB == 'Faster Bullets': new_speed = speed * 2
    else: new_speed = speed
    return new_speed

def faster_paddle(divider,playerA,playerB):
    if playerA == 'Faster Paddle': new_divider = divider - 0.7
    elif playerB == 'Faster Paddle': new_divider = divider - 0.7
    else: new_divider = divider
    return new_divider

def faster_ball(distance,playerA,playerB,ballBelongsTo):
    if playerA == 'Faster Ball' and ballBelongsTo == 0: new_distance = distance * 2
    elif playerB == 'Faster Ball' and ballBelongsTo == 1: new_distance = distance * 2
    else: new_distance = distance
    return new_distance

# For the score and powerups display on the top and bottom bars
font = pygame.font.SysFont("arial", 20)
font4 = pygame.font.Font(None, 65)
font5 = pygame.font.Font(None, 20)
font6 = pygame.font.Font(None, 50)

playerA = 'No Power'
playerB = 'No Power'

ballSize = 40
poweruptimer = 0
ballBelongsTo = 2

# Initial location of ball
ballX = screenWidth/2.0
ballY = screenHeight/2.0

# Ball Speed in pixels per second
ballSpeed = 250.0

# It's okay for the ball to start in an awkward direction since bullets can push
# it into any direction.
angle = random.randint(0,600)/100.
speedX = ballSpeed * math.cos(angle)
speedY = ballSpeed * math.sin(angle)

# Initial conditions
# FYI, PosX = -100 and PosY = -100 are the default coordinates to "hide" things
colorSpeed = 75
paddleWidth = 30
paddleHeight = 15
bulletWidth = 22
bulletHeight = 7
portalLong = 118
portalShort = 37
paddleAx = 10
paddleBx = (screenWidth - 10) - paddleWidth
paddleAy = (screenHeight-paddleHeight)/2.0
paddleBy = paddleAy
bulletAx = paddleAx + paddleWidth
sideshotAx = bulletAx
bulletBx = paddleBx - paddleWidth - bulletWidth
sideshotBx = bulletBx
bulletAy = paddleAy + (paddleHeight / 2) - (bulletHeight / 2)
sideshotAy = bulletAy
bulletBy = paddleBy + (paddleHeight / 2) - (bulletHeight / 2)
sideshotBy = bulletBy
portalAx = -100
portalAy = -100
portalBx = -100
portalBy = -100
powerPosX = -100
powerPosY = -100
penaltyPosX = -100
penaltyPosY = -100
paddleASpeed = 0.0
paddleBSpeed = 0.0
bulletA = False
bulletB = False
sideUPshotA = False
sideDOWNshotA = False
sideUPshotB = False
sideDOWNshotB = False
portalAhorizontal = False
portalAvertical = False
portalBhorizontal = False
portalBvertical = False
random_direction = 0
penaltywidth = 150
penaltyheight = 150
penaltytimer = 0
blitpenalty = False

blitpowerup = False

playerAscore = 0
playerBscore = 0

wallTop = 25;
wallBottom = (screenHeight - 30)

# Set up list of Joysticks detected
joysticks = []
for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
    print "Detected joystick '",joysticks[-1].get_name(),"'"
print joysticks


if joysticks != []:
    joyA = joysticks[0]
    joyA.init()
if len(joysticks) > 1:
    joyB = joysticks[1]
    joyB.init()

# Assign images
background = pygame.image.load(image_background).convert()
sprite1 = pygame.image.load(sprite1_image_filename).convert_alpha()
sprite2 = pygame.image.load(sprite2_image_filename).convert_alpha()
sprite3 = pygame.image.load(sprite3_image_filename).convert_alpha()
sprite4 = pygame.image.load(sprite4_image_filename).convert_alpha()
sprite5 = pygame.image.load(sprite5_image_filename).convert_alpha()
sprite11 = pygame.image.load(sprite11_image_filename).convert_alpha()
sprite12 = pygame.image.load(sprite12_image_filename).convert_alpha()

pygame.display.update()
sound_Hellooo.play(0)
music_inGame.play(0)

gamePhase = 1

while True:
  for event in pygame.event.get():
    if (event.type == QUIT):
      pygame.quit()
      sys.exit()
    if (event.type == KEYDOWN):
      if (event.key == K_ESCAPE):
            pygame.quit()
            exit()

  # GamePhase 1 :  Start Menu
  while (gamePhase == 1):
    for event in pygame.event.get():
      if (event.type == QUIT):
        pygame.quit()
        sys.exit()
      if (event.type == KEYDOWN):
        if (event.key == K_ESCAPE):
          pygame.quit()
          exit()
        if (event.key == K_RETURN):
            gamePhase = 2
      if (event.type == JOYBUTTONDOWN) and (joysticks[event.joy].get_id() == 0) and (event.button == 0):
        gamePhase = 2
      if (event.type == JOYBUTTONDOWN) and (joysticks[event.joy].get_id() == 1) and (event.button == 0):
        gamePhase = 2

    welcomeTextA = font6.render("Welcome to", False, BLACK)
    welcomeTextB = font4.render("Portal Pong!", False, BLACK)
    controlText = font5.render("To start game, press 'Enter' on keyboard or 'A' button on either controller.", False, BLACK)
    pygame.draw.rect (screen, ORANGE, ((0, (screenHeight - 50)), (screenWidth, 50)))
    pygame.draw.rect (screen, BLUE, ((screenWidth/2 - (screenWidth/4)),(screenHeight/2 - (screenHeight/4)), (screenWidth/2),(screenHeight/2)))
    screen.blit(welcomeTextA, (screenWidth/3, screenHeight/3))
    screen.blit(welcomeTextB, (screenWidth/3, screenHeight/3 + 60))
    screen.blit(controlText, (50, screenHeight - 40))
    pygame.display.update()

  # GamePhase 2 : This is the actual game loop
  while (gamePhase == 2):
    for event in pygame.event.get():
        if (event.type == QUIT):
            pygame.quit()
            sys.exit()

        if (event.type == JOYAXISMOTION):
            if (joysticks[event.joy].get_id() == 0) and (event.axis == 1) and (joyA.get_axis(1) <= -0.3): paddleASpeed = -ballSpeed/faster_paddle(1.5,playerA,'No Power')
            if (joysticks[event.joy].get_id() == 0) and (event.axis == 1) and (joyA.get_axis(1) >= 0.3): paddleASpeed = ballSpeed/faster_paddle(1.5,playerA,'No Power')
            if (joysticks[event.joy].get_id() == 1) and (event.axis == 1) and (joyB.get_axis(1) <= -0.3): paddleBSpeed = -ballSpeed/faster_paddle(1.5,'No Power',playerB)
            if (joysticks[event.joy].get_id() == 1) and (event.axis == 1) and (joyB.get_axis(1) >= 0.3): paddleBSpeed = ballSpeed/faster_paddle(1.5,'No Power',playerB)

        if (event.type == JOYBUTTONDOWN):
            if(joysticks[event.joy].get_id() == 0):
                if(event.button == 0) and bulletA == False and sideUPshotA == False and sideDOWNshotA == False:
                    sideDOWNshotA = True
                    sideshotAy = paddleAy + (paddleHeight / 2) - (bulletHeight / 2)
                    sound_ShootBullet.play(0)
                if(event.button == 1) and bulletA == False and sideUPshotA == False and sideDOWNshotA == False:
                    bulletA = True
                    bulletAy = paddleAy + (paddleHeight / 2) - (bulletHeight / 2)
                    sound_ShootBullet.play(0)
                if(event.button == 3) and bulletA == False and sideUPshotA == False and sideDOWNshotA == False:
                    sideUPshotA = True
                    sideshotAy = paddleAy + (paddleHeight / 2) - (bulletHeight / 2)
                    sound_ShootBullet.play(0)
                if(event.button == 2):
                    if bulletA == True:
                        bulletA = False
                        portalAhorizontal = False
                        portalAvertical = True
                        portalAx = bulletAx - 18 + bulletWidth / 2
                        portalAy = bulletAy - 49 + bulletHeight / 2
                        sound_PortalOpens.play(0)
                    elif sideUPshotA == True or sideDOWNshotA == True:
                        sideUPshotA = False
                        sideDOWNshotA = False
                        portalAhorizontal = True
                        portalAvertical = False
                        portalAx = sideshotAx - 49 + bulletWidth * 0.3
                        portalAy = sideshotAy - 18 + bulletHeight * 0.3
                        sound_PortalOpens.play(0)
            if(joysticks[event.joy].get_id() == 1):
                if(event.button == 0) and bulletB == False and sideUPshotB == False and sideDOWNshotB == False:
                    sideDOWNshotB = True
                    sideshotBy = paddleBy + (paddleHeight / 2) - (bulletHeight / 2)
                    sound_ShootBullet.play(0)
                if(event.button == 1) and bulletB == False and sideUPshotB == False and sideDOWNshotB == False:
                    bulletB = True
                    bulletBy = paddleBy + (paddleHeight / 2) - (bulletHeight / 2)
                    sound_ShootBullet.play(0)
                if(event.button == 3) and bulletB == False and sideUPshotB == False and sideDOWNshotB == False:
                    sideUPshotB = True
                    sideshotBy = paddleBy + (paddleHeight / 2) - (bulletHeight / 2)
                    sound_ShootBullet.play(0)
                if(event.button == 2):
                    if bulletB == True:
                        bulletB = False
                        portalBhorizontal = False
                        portalBvertical = True
                        portalBx = bulletBx - 18 + bulletWidth / 2
                        portalBy = bulletBy - 49 + bulletHeight / 2
                        sound_PortalOpens.play(0)
                    elif sideUPshotB == True or sideDOWNshotB == True:
                        sideUPshotB = False
                        sideDOWNshotB = False
                        portalBhorizontal = True
                        portalBvertical = False
                        portalBx = sideshotBx - 49 + bulletWidth * 0.3
                        portalBy = sideshotBy - 18 + bulletHeight * 0.3
                        sound_PortalOpens.play(0)

        if (event.type == KEYDOWN):
            if (event.key == K_ESCAPE):
                pygame.quit()
                exit()

            if (event.key == K_w): paddleASpeed = -ballSpeed/faster_paddle(1.5,playerA,'No Power')
            if (event.key == K_x): paddleASpeed = ballSpeed/faster_paddle(1.5,playerA,'No Power')
            if (event.key == K_o): paddleBSpeed = -ballSpeed/faster_paddle(1.5,'No Power',playerB)
            if (event.key == K_PERIOD): paddleBSpeed = ballSpeed/faster_paddle(1.5,'No Power',playerB)
            if (event.key == K_e) and bulletA == False and sideUPshotA == False and sideDOWNshotA == False:
                sideUPshotA = True
                sideshotAy = paddleAy + (paddleHeight / 2) - (bulletHeight / 2)
                sound_ShootBullet.play(0)
            if (event.key == K_c) and bulletA == False and sideUPshotA == False and sideDOWNshotA == False:
                sideDOWNshotA = True
                sideshotAy = paddleAy + (paddleHeight / 2) - (bulletHeight / 2)
                sound_ShootBullet.play(0)
            if (event.key == K_d) and bulletA == False and sideUPshotA == False and sideDOWNshotA == False:
                bulletA = True
                bulletAy = paddleAy + (paddleHeight / 2) - (bulletHeight / 2)
                sound_ShootBullet.play(0)
            if (event.key == K_i) and bulletB == False and sideUPshotB == False and sideDOWNshotB == False:
                sideUPshotB = True
                sideshotBy = paddleBy + (paddleHeight / 2) - (bulletHeight / 2)
                sound_ShootBullet.play(0)
            if (event.key == K_COMMA) and bulletB == False and sideUPshotB == False and sideDOWNshotB == False:
                sideDOWNshotB = True
                sideshotBy = paddleBy + (paddleHeight / 2) - (bulletHeight / 2)
                sound_ShootBullet.play(0)
            if (event.key == K_k) and bulletB == False and sideUPshotB == False and sideDOWNshotB == False:
                bulletB = True
                bulletBy = paddleBy + (paddleHeight / 2) - (bulletHeight / 2)
                sound_ShootBullet.play(0)
            if(event.key == K_l):
                if bulletB == True:
                    bulletB = False
                    portalBhorizontal = False
                    portalBvertical = True
                    portalBx = bulletBx - 18 + bulletWidth / 2
                    portalBy = bulletBy - 49 + bulletHeight / 2
                    sound_PortalOpens.play(0)
                elif sideUPshotB == True or sideDOWNshotB == True:
                    sideUPshotB = False
                    sideDOWNshotB = False
                    portalBhorizontal = True
                    portalBvertical = False
                    portalBx = sideshotBx - 49 + bulletWidth * 0.3
                    portalBy = sideshotBy - 18 + bulletHeight * 0.3
                    sound_PortalOpens.play(0)
            if(event.key == K_s):
                if bulletA == True:
                    bulletA = False
                    portalAhorizontal = False
                    portalAvertical = True
                    portalAx = bulletAx - 18 + bulletWidth / 2
                    portalAy = bulletAy - 49 + bulletHeight / 2
                    sound_PortalOpens.play(0)
                elif sideUPshotA == True or sideDOWNshotA == True:
                    sideUPshotA = False
                    sideDOWNshotA = False
                    portalAhorizontal = True
                    portalAvertical = False
                    portalAx = sideshotAx - 49 + bulletWidth * 0.3
                    portalAy = sideshotAy - 18 + bulletHeight * 0.3
                    sound_PortalOpens.play(0)

    # To make paddles stop moving when person lets go
        if (event.type == KEYUP):
            if (event.key == K_w) or (event.key == K_x): paddleASpeed = 0.0
            if (event.key == K_o) or (event.key == K_PERIOD): paddleBSpeed = 0.0
        if (event.type == JOYAXISMOTION) and (joysticks[event.joy].get_id() == 0) and (event.axis == 1) and ((joyA.get_axis(1) >= -0.3) and (joyA.get_axis(1) <= 0.3)): paddleASpeed = 0.0
        if (event.type == JOYAXISMOTION) and (joysticks[event.joy].get_id() == 1) and (event.axis == 1) and ((joyB.get_axis(1) >= -0.3) and (joyB.get_axis(1) <= 0.3)): paddleBSpeed = 0.0

    screen.blit(background, (0,0))

    # Assign more images
    if ballBelongsTo == 2: ballImage = pygame.image.load(image_blueBall).convert_alpha()
    if ballBelongsTo == 0:
        if playerA == 'Faster Ball': ballImage = pygame.image.load(image_greenBall_powered).convert_alpha()
        else: ballImage = pygame.image.load(image_greenBall).convert_alpha()
    if ballBelongsTo == 1:
        if playerB == 'Faster Ball': ballImage = pygame.image.load(image_redBall_powered).convert_alpha()
        else: ballImage = pygame.image.load(image_redBall).convert_alpha()

    if playerA == 'Faster Bullets':
        sprite6a = pygame.image.load(sprite6_image_faster).convert_alpha()
        sprite7a = pygame.image.load(sprite7_image_faster).convert_alpha()
        sprite8a = pygame.image.load(sprite8_image_faster).convert_alpha()
    elif playerA == 'Stronger Bullets':
        sprite6a = pygame.image.load(sprite6_image_stronger).convert_alpha()
        sprite7a = pygame.image.load(sprite7_image_stronger).convert_alpha()
        sprite8a = pygame.image.load(sprite8_image_stronger).convert_alpha()
    else:
        sprite6a = pygame.image.load(sprite6_image_filename).convert_alpha()
        sprite7a = pygame.image.load(sprite7_image_filename).convert_alpha()
        sprite8a = pygame.image.load(sprite8_image_filename).convert_alpha()
    if playerB == 'Faster Bullets':
        sprite6b = pygame.image.load(sprite6_image_faster).convert_alpha()
        sprite7b = pygame.image.load(sprite7_image_faster).convert_alpha()
        sprite8b = pygame.image.load(sprite8_image_faster).convert_alpha()
    elif playerB == 'Stronger Bullets':
        sprite6b = pygame.image.load(sprite6_image_stronger).convert_alpha()
        sprite7b = pygame.image.load(sprite7_image_stronger).convert_alpha()
        sprite8b = pygame.image.load(sprite8_image_stronger).convert_alpha()
    else:
        sprite6b = pygame.image.load(sprite6_image_filename).convert_alpha()
        sprite7b = pygame.image.load(sprite7_image_filename).convert_alpha()
        sprite8b = pygame.image.load(sprite8_image_filename).convert_alpha()

    if playerA == 'Faster Bullets': sprite9 = pygame.image.load(sprite9_image_faster).convert_alpha()
    elif playerA == 'Stronger Bullets': sprite9 = pygame.image.load(sprite9_image_stronger).convert_alpha()
    elif playerA == 'Faster Paddle':  sprite9 = pygame.image.load(sprite9_image_paddle).convert_alpha()
    else: sprite9 = pygame.image.load(sprite9_image_filename).convert_alpha()
    if playerB == 'Faster Bullets': sprite10 = pygame.image.load(sprite10_image_faster).convert_alpha()
    elif playerB == 'Stronger Bullets': sprite10 = pygame.image.load(sprite10_image_stronger).convert_alpha()
    elif playerB == 'Faster Paddle':  sprite10 = pygame.image.load(sprite10_image_paddle).convert_alpha()
    else: sprite10 = pygame.image.load(sprite10_image_filename).convert_alpha()

    # Display score
    text_surface_A = font.render(playerA, True, ORANGE)
    text_surface_B = font.render(playerB, True, ORANGE)
    text_surface_scoreA = font.render('Score: ' + str(playerBscore), True, ORANGE)
    text_surface_scoreB = font.render('Score: ' + str(playerAscore), True, ORANGE)

    # To control when a penalty box appears
    if penaltytimer > 10:
        penaltyPosX = random.randint(150,screenWidth-150) - penaltywidth / 2
        penaltyPosY = random.randint(150,screenHeight-150) - penaltyheight / 2
        blitpenalty = True
        penaltytimer = 0

    # To decide when a powerup will appear on the screen
    if poweruptimer > 3:
        powerPosX = random.randint(60,screenWidth-60)
        powerPosY = random.randint(60,screenHeight-60)
        blitpowerup = True
        poweruptimer = 0

    # Draws the penalty
    if blitpenalty == True: screen.blit(sprite12, (penaltyPosX, penaltyPosY))

    # Draws the portals depending on what kind of bullet was shot
    if portalAhorizontal == True:
        screen.blit(sprite4, (portalAx - 20, portalAy - 30))
    if portalAvertical == True:
        screen.blit(sprite1, (portalAx - 30, portalAy - 20))
    if portalBhorizontal == True:
        screen.blit(sprite3, (portalBx - 20, portalBy - 30))
    if portalBvertical == True:
        screen.blit(sprite2, (portalBx - 30, portalBy - 20))

    # Draws the bullets
    if bulletA == True: screen.blit(sprite6a, (bulletAx - 4, bulletAy - 1))
    if sideUPshotA == True: screen.blit(sprite7a, (sideshotAx - 2, sideshotAy - 2))
    if sideDOWNshotA == True: screen.blit(sprite8a, (sideshotAx - 2, sideshotAy - 2))
    if bulletB == True: screen.blit(sprite6b, (bulletBx - 4, bulletBy - 1))
    if sideUPshotB == True: screen.blit(sprite8b, (sideshotBx - 2, sideshotBy - 2))
    if sideDOWNshotB == True: screen.blit(sprite7b, (sideshotBx - 2, sideshotBy - 2))

    # Draws the powerup
    if blitpowerup == True: screen.blit(sprite11, (powerPosX, powerPosY))

    # Draws the ball and paddles
    screen.blit(ballImage, (ballX, ballY))
    screen.blit(sprite9, (paddleAx, paddleAy))
    screen.blit(sprite10, (paddleBx, paddleBy))

    #draw top and bottom walls. Even though these never move, they must be redrawn
    #each frame since at the start of each frame, the screen is filled with BLACK.
    screen.blit(sprite5, (0,               5, screenWidth, 20))
    screen.blit(sprite5, (0, screenHeight-30, screenWidth, 20))

    screen.blit(text_surface_A, (20,screenHeight-32))
    screen.blit(text_surface_B, (screenWidth-text_surface_B.get_width()-20,screenHeight-32))
    screen.blit(text_surface_scoreA, (20,4))
    screen.blit(text_surface_scoreB, (screenWidth-text_surface_scoreB.get_width()-20,4))

    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000.0

    distanceX = time_passed_seconds * speedX
    distanceY = time_passed_seconds * speedY

    # Ball goes faster for other player with "faster ball" powerup
    ballX += faster_ball(distanceX,playerA,playerB,ballBelongsTo)
    ballY += faster_ball(distanceY,playerA,playerB,ballBelongsTo)

    # Changes the color of the ball depending on who the ball belongs to
    if speedX < colorSpeed and speedX > -colorSpeed: ballBelongsTo = 2
    if speedX < -colorSpeed: ballBelongsTo = 1
    elif speedX > colorSpeed: ballBelongsTo = 0
    else: ballBelongsTo = 2

    # Bullets go faster with "faster bullets" powerup
    if bulletA == True: bulletAx += faster_bullets(3,playerA,'No Power')
    if sideUPshotA == True or sideDOWNshotA == True: sideshotAx += faster_bullets(2.1,playerA,'No Power')
    if sideUPshotA == True: sideshotAy -= faster_bullets(2.1,playerA,'No Power')
    if sideDOWNshotA == True: sideshotAy += faster_bullets(2.1,playerA,'No Power')
    if bulletB == True: bulletBx -= faster_bullets(3,'No Power',playerB)
    if sideUPshotB == True or sideDOWNshotB == True: sideshotBx -= faster_bullets(2.1,'No Power',playerB)
    if sideUPshotB == True: sideshotBy -= faster_bullets(2.1,'No Power',playerB)
    if sideDOWNshotB == True: sideshotBy += faster_bullets(2.1,'No Power',playerB)
    if bulletA == False: bulletAx = 0 - bulletWidth
    if sideUPshotA == False and sideDOWNshotA == False: sideshotAx = paddleAx + paddleWidth
    if bulletB == False: bulletBx = screenWidth
    if sideUPshotB == False and sideDOWNshotB == False: sideshotBx = paddleBx - bulletWidth

    # When the ball collides with portals from the right or bottom
    if (portalAvertical == True) and (ballX < portalAx + portalShort) and (ballX > portalAx) and (ballY + ballSize < portalAy + portalLong) and (ballY > portalAy) or (portalAhorizontal == True) and (ballX > portalAx) and (ballX + ballSize < portalAx + portalLong) and (ballY > portalAy) and (ballY < portalAy + portalShort):
        if portalBhorizontal == True and portalAvertical == True or portalBvertical == True and portalAhorizontal == True:
            speedX = speedY
            speedY = speedX
            if portalBhorizontal == True:
                ballX = portalBx + 49
                ballY = portalBy + 18
            if portalBvertical == True:
                ballX = portalBx + 18
                ballY = portalBy + 49
        elif portalBhorizontal == True:
            ballX = portalBx + 49
            ballY = portalBy + 18
        elif portalBvertical == True:
            ballX = portalBx + 18
            ballY = portalBy + 49
        else:
            ballX = random.randint(600,900)
            ballY = random.randint(40,700)
        portalAx = -100
        portalAy = -100
        portalBx = -100
        portalBy = -100

    if (portalBvertical == True) and (ballX < portalBx + portalShort) and (ballX > portalBx) and (ballY + ballSize < portalBy + portalLong) and (ballY > portalBy) or (portalBhorizontal == True) and (ballX > portalBx) and (ballX + ballSize < portalBx + portalLong) and (ballY > portalBy) and (ballY < portalBy + portalShort):
        if portalAhorizontal == True and portalBvertical == True or portalAvertical == True and portalBhorizontal == True:
            sound_PortalCloses.play(0)
            temp = speedX
            speedY = speedX
            speedY = temp
            temp = 0
            if portalAhorizontal == True:
                ballX = portalAx + 49
                ballY = portalAy + 18
            if portalAvertical == True:
                ballX = portalAx + 18
                ballY = portalAy + 49
        elif portalAhorizontal == True:
            sound_PortalCloses.play(0)
            ballX = portalAx + 49
            ballY = portalAy + 18
        elif portalAvertical == True:
            sound_PortalCloses.play(0)
            ballX = portalAx + 18
            ballY = portalAy + 49
        else:
            sound_BulletIntoPortal.play(0)
            ballX = random.randint(600,900)
            ballY = random.randint(40,700)
        portalAx = -100
        portalAy = -100
        portalBx = -100
        portalBy = -100


    # When the ball collides with portals from the left or top
    if (portalAvertical == True) and (ballX + ballSize > portalAx) and (ballX + ballSize < portalAx + portalShort) and (ballY < portalAy) and (ballY + ballSize > portalAy + portalLong) or (portalAhorizontal == True) and (ballX > portalAx) and (ballX + ballSize < portalAx + portalLong) and (ballY + ballSize > portalAy) and (ballY + ballSize < portalAy + portalShort):
        if portalBhorizontal == True and portalAvertical == True or portalBvertical == True and portalAhorizontal == True:
            sound_PortalCloses.play(0)
            temp = speedX
            speedX = speedY
            speedY = temp
            temp = 0
            if portalBhorizontal == True:
                ballX = portalBx + 49
                ballY = portalBy + 18
            if portalBvertical == True:
                ballX = portalBx + 18
                ballY = portalBy + 49
        elif portalBhorizontal == True:
            sound_PortalCloses.play(0)
            ballX = portalBx + 49
            ballY = portalBy + 18
        elif portalBvertical == True:
            sound_PortalCloses.play(0)
            ballX = portalBx + 18
            ballY = portalBy + 49
        else:
            sound_BulletIntoPortal.play(0)
            ballX = random.randint(600,900)
            ballY = random.randint(40,700)
        portalAx = -100
        portalAy = -100
        portalBx = -100
        portalBy = -100

    if (portalBvertical == True) and (ballX + ballSize > portalBx) and (ballX + ballSize < portalBx + portalShort) and (ballY < portalBy) and (ballY + ballSize > portalBy + portalLong) or (portalBhorizontal == True) and (ballX > portalBx) and (ballX + ballSize < portalBx + portalLong) and (ballY + ballSize > portalBy) and (ballY + ballSize < portalBy + portalShort):
        if portalAhorizontal == True and portalBvertical == True or portalAvertical == True and portalBhorizontal == True:
            sound_BulletIntoPortal.play(0)
            temp = speedX
            speedX = speedY
            speedY = temp
            temp = 0
            if portalAhorizontal == True:
                ballX = portalAx + 49
                ballY = portalAy + 18
            if portalAvertical == True:
                ballX = portalAx + 18
                ballY = portalAy + 49
        elif portalAhorizontal == True:
            sound_BulletIntoPortal.play(0)
            ballX = portalAx + 49
            ballY = portalAy + 18
        elif portalAvertical == True:
            sound_BulletIntoPortal.play(0)
            ballX = portalAx + 18
            ballY = portalAy + 49
        else:
            sound_BulletIntoPortal.play(0)
            ballX = random.randint(600,900)
            ballY = random.randint(40,700)
        portalAx = -100
        portalAy = -100
        portalBx = -100
        portalBy = -100

    # When the ball collides with the penalty
    if (ballBelongsTo == 1) and (ballX + ballSize > penaltyPosX) and (ballX + ballSize < penaltyPosX + penaltywidth)and(playerAscore>0):
        if (ballY + ballSize > penaltyPosY) and (ballY + ballSize < penaltyPosY + penaltyheight) or (ballY < penaltyPosY + penaltyheight) and (ballY > penaltyPosY):
            blitpenalty = False
            penaltyPosX = -100
            penaltyPosY = -100
            playerAscore = playerAscore - 1
            sound_PenaltyCollision.play(0)

    if (ballBelongsTo == 0) and (ballX < penaltyPosX + penaltywidth) and (ballX > penaltyPosX)and(playerBscore>0):
        if (ballY + ballSize > penaltyPosY) and (ballY + ballSize < penaltyPosY + penaltyheight) or (ballY < penaltyPosY + penaltyheight) and (ballY > penaltyPosY):
            blitpenalty = False
            penaltyPosX = -100
            penaltyPosY = -100
            playerBscore = playerBscore - 1
            sound_PenaltyCollision.play(0)

    # When bullets collide with the ball
    if (ballX < bulletAx + bulletWidth) and (ballX + ballSize > bulletAx) and (ballY + ballSize > bulletAy) and (ballY < bulletAy + bulletHeight) and (bulletA == True):
        speedX = speedX + stronger_bullets(100,playerA,'No Power')
        bulletA = False
        poweruptimer = poweruptimer + random.randint(0,1)
        penaltytimer = penaltytimer + random.randint(0,1)
        sound_BulletHitBall.play(0)

    if (ballX < sideshotAx) and (ballX + ballSize > sideshotAx - bulletWidth * 0.7) and (ballY + ballSize > sideshotAy) and (ballY < sideshotAy + bulletHeight):
        if (sideUPshotA == True) or (sideDOWNshotA == True):
            speedX = speedX + stronger_bullets(71,playerA,'No Power')
            if sideUPshotA == True:
                speedY = speedY - stronger_bullets(71,playerA,'No Power')
                sideUPshotA = False
            if sideDOWNshotA == True:
                speedY = speedY + stronger_bullets(71,playerA,'No Power')
                sideDOWNshotA = False
            poweruptimer = poweruptimer + random.randint(0,1)
            penaltytimer = penaltytimer + random.randint(0,5)
            sound_BulletHitBall.play(0)

    if (ballX + ballSize > bulletBx) and (ballX + ballSize < bulletBx + bulletWidth) and (ballY + ballSize > bulletBy) and (ballY < bulletBy + bulletHeight) and (bulletB == True):
        speedX = speedX - stronger_bullets(100,'No Power',playerB)
        bulletB = False
        poweruptimer = poweruptimer + random.randint(0,1)
        penaltytimer = penaltytimer + random.randint(0,5)
        sound_BulletHitBall.play(0)

    if (ballX + ballSize > sideshotBx) and (ballX + ballSize < sideshotBx + bulletWidth * 0.7) and (ballY + ballSize > sideshotBy) and (ballY < sideshotBy + bulletHeight):
        if (sideUPshotB == True) or (sideDOWNshotB == True):
            speedX = speedX - stronger_bullets(71,'No Power',playerB)
            if sideUPshotB == True:
                speedY = speedY - stronger_bullets(71,'No Power',playerB)
                sideUPshotB = False
            if sideDOWNshotB == True:
                speedY = speedY + stronger_bullets(71,'No Power',playerB)
                sideDOWNshotB = False
            poweruptimer = poweruptimer + random.randint(0,1)
            penaltytimer = penaltytimer + random.randint(0,5)
            sound_BulletHitBall.play(0)

    # When bullets collide with powerups
    if (powerPosX < bulletAx + bulletWidth) and (powerPosX + ballSize > bulletAx + bulletWidth) and (powerPosY + ballSize > bulletAy + bulletHeight) and (powerPosY < bulletAy):
        bulletA = False
        blitpowerup = False
        powerPosX = -100
        powerPosY = -100
        playerA = randpower(random.randint(0,3))
        sound_ShootPowerup.play(0)
        sound_Powerup.play(0)

    if (powerPosX + ballSize > bulletBx) and (powerPosX + ballSize < bulletBx + bulletWidth) and (powerPosY + ballSize > bulletBy + bulletHeight) and (powerPosY < bulletBy):
        bulletB = False
        blitpowerup = False
        powerPosX = -100
        powerPosY = -100
        playerB = randpower(random.randint(0,3))
        sound_ShootPowerup.play(0)
        sound_Powerup.play(0)

    if (powerPosX < sideshotAx) and (powerPosX + ballSize > sideshotAx - bulletWidth * 0.7) and (powerPosY + ballSize > sideshotAy) and (powerPosY < sideshotAy + bulletHeight):
        sideUPshotA = False
        sideDOWNshotA = False
        powerPosX = -100
        powerPosY = -100
        playerA = randpower(random.randint(0,3))
        sound_ShootPowerup.play(0)
        sound_Powerup.play(0)

    if (powerPosX + ballSize > sideshotBx) and (powerPosX + ballSize < sideshotBx + bulletWidth * 0.7) and (powerPosY + ballSize > sideshotBy) and (powerPosY < sideshotBy + bulletHeight):
        sideUPshotB = False
        sideDOWNshotB = False
        powerPosX = -100
        powerPosY = -100
        playerB = randpower(random.randint(0,3))
        sound_ShootPowerup.play(0)
        sound_Powerup.play(0)

    # When straight bullets collide with portals
    if (bulletAx + bulletWidth > portalAx) and (bulletAx + bulletWidth < portalAx + portalShort) and (bulletAy > portalAy) and (bulletAy + bulletHeight < portalAy + portalLong) and (portalAvertical == True):
        if portalBvertical == True:
            bulletAx = portalBx + 18
            bulletAy = portalBy + 49 - bulletHeight / 2
        if portalBhorizontal == True:
            bulletA = False
            random_direction = random.randint(0,1)
            if random_direction == 0:
                sideUPshotA = True
                sideshotAy = portalBy + 18 - bulletWidth
            else:
                sideDOWNshotA = True
                sideshotAy = portalBy + 18 + bulletWidth
            sideshotAx = portalBx + 49 + bulletWidth

    if (bulletAx + bulletWidth > portalBx) and (bulletAx + bulletWidth < portalBx + portalShort) and (bulletAy > portalBy) and (bulletAy + bulletHeight < portalBy + portalLong) and (portalBvertical == True):
        if portalAvertical == True:
            bulletAx = portalAx + 18
            bulletAy = portalAy + 49 - bulletHeight / 2
        if portalAhorizontal == True:
            bulletA = False
            random_direction = random.randint(0,1)
            if random_direction == 0:
                sideUPshotA = True
                sideshotAy = portalAy + 18 - bulletWidth
            else:
                sideDOWNshotA = True
                sideshotAy = portalAy + 18 + bulletWidth
            sideshotAx = portalAx + 49 + bulletWidth

    if (bulletBx > portalBx) and (bulletBx < portalBx + portalShort) and (bulletBy > portalBy) and (bulletBy + bulletHeight < portalBy + portalLong) and (portalBvertical == True):
        if portalAvertical == True:
            bulletBx = portalAx + 18 - bulletWidth
            bulletBy = portalAy + 49 - bulletHeight / 2
        if portalAhorizontal == True:
            bulletB = False
            random_direction = random.randint(0,1)
            if random_direction == 0:
                sideUPshotB = True
                sideshotBy = portalAy + 18 - bulletWidth
            else:
                sideDOWNshotB = True
                sideshotBy = portalAy + 18 + bulletWidth
            sideshotBx = portalAx + 49 - bulletWidth

    if (bulletBx > portalAx) and (bulletBx < portalAx + portalShort) and (bulletBy > portalAy) and (bulletBy + bulletHeight < portalAy + portalLong) and (portalAvertical == True):
        if portalBvertical == True:
            bulletBx = portalBx + 18 - bulletWidth
            bulletBy = portalBy + 49 - bulletHeight / 2
        if portalBhorizontal == True:
            bulletB = False
            random_direction = random.randint(0,1)
            if random_direction == 0:
                sideUPshotB = True
                sideshotBy = portalAy + 18 - bulletWidth
            else:
                sideDOWNshotB = True
                sideshotBy = portalAy + 18 + bulletWidth
            sideshotBx = portalAx + 49 - bulletWidth

    # When sideshot bullets collide with portals
    if (sideshotAx + bulletWidth * 0.7 > portalAx) and (sideshotAx + bulletWidth * 0.7 < portalAx + portalShort) and (sideshotAy > portalAy) and (sideshotAy + bulletHeight * 0.7 < portalAy + portalLong) and (portalAvertical == True) or (sideshotAx > portalAx) and (sideshotAx + bulletWidth * 0.7 < portalAx + portalLong) and (sideUPshotA == True) and (sideshotAy > portalAy) and (sideshotAy < portalAy + portalShort) and (portalAhorizontal == True) or (sideshotAx > portalAx) and (sideshotAx + bulletHeight * 0.7 < portalAx + portalLong) and (sideDOWNshotA == True) and (sideshotAy + bulletHeight * 0.7 > portalAy) and (sideshotAy + bulletHeight * 0.7 < portalAy + portalShort) and (portalAhorizontal == True):
        if portalBhorizontal == True:
            sideshotAx = portalBx + 49 + bulletWidth
            if sideUPshotA == True:
                sideshotAy = portalBy + 18 - bulletWidth
            else:
                sideshotAy = portalBy + 18 + bulletWidth
        if portalBvertical == True:
            sideUPshotA = False
            sideDOWNshotA = False
            bulletA = True
            bulletAx = portalBx + 18
            bulletAy = portalBy + 49 - bulletHeight / 2
    #                                                                                                                                                                                                                 Vertical          ########        Horizontal with sideUPshot                                                                                                                                                                                ######    Horizontal with sideDOWNshot
    if (sideshotAx + bulletWidth * 0.7 > portalBx) and (sideshotAx + bulletWidth * 0.7 < portalBx + portalShort) and (sideshotAy > portalBy) and (sideshotAy + bulletHeight * 0.7 < portalBy + portalLong) and (portalBvertical == True) or (sideshotAx > portalBx) and (sideshotAx + bulletWidth * 0.7 < portalBx + portalLong) and (sideUPshotA == True) and (sideshotAy > portalBy) and (sideshotAy < portalBy + portalShort) and (portalBhorizontal == True) or (sideshotAx > portalBx) and (sideshotAx + bulletHeight * 0.7 < portalBx + portalLong) and (sideDOWNshotA == True) and (sideshotAy + bulletHeight * 0.7 > portalBy) and (sideshotAy + bulletHeight * 0.7 < portalBy + portalShort) and (portalBhorizontal == True):
        if portalAhorizontal == True:
            sideshotAx = portalAx + 49 + bulletWidth
            if sideUPshotA == True:
                sideshotAy = portalAy + 18 - bulletWidth
            else:
                sideshotAy = portalAy + 18 + bulletWidth
        if portalAvertical == True:
            sideUPshotA = False
            sideDOWNshotA = False
            bulletA = True
            bulletAx = portalAx + 18
            bulletAy = portalAy + 49 - bulletHeight / 2
    #                                                                                                                                                                         Vertical          ########         Horizontal with sideUPshot                                                                                                                                                                              ######    Horizontal with sideDOWNshot
    if (sideshotBx < portalAx + portalShort) and (sideshotBx > portalAx) and (sideshotBy > portalAy) and (sideshotBy + bulletHeight * 0.7 < portalAy + portalLong) and (portalAvertical == True) or (sideshotBx > portalAx) and (sideshotBx + bulletWidth * 0.7 < portalAx + portalLong) and (sideUPshotB == True) and (sideshotBy > portalAy) and (sideshotBy < portalAy + portalShort) and (portalAhorizontal == True) or (sideshotBx > portalAx) and (sideshotBx + bulletHeight * 0.7 < portalAx + portalLong) and (sideDOWNshotB == True) and (sideshotBy + bulletHeight * 0.7 > portalAy) and (sideshotBy + bulletHeight * 0.7 < portalAy + portalShort) and (portalAhorizontal == True):
        if portalBhorizontal == True:
            sideshotBx = portalBx + 49 - bulletWidth
            if sideUPshotB == True:
                sideshotBy = portalBy + 18 - bulletWidth
            else:
                sideshotBy = portalBy + 18 + bulletWidth
        if portalBvertical == True:
            sideUPshotB = False
            sideDOWNshotB = False
            bulletB = True
            bulletBx = portalBx + 18 - bulletWidth
            bulletBy = portalBy + 49 - bulletHeight / 2

    if (sideshotBx < portalBx + portalShort) and (sideshotBx > portalBx) and (sideshotBy > portalBy) and (sideshotBy + bulletHeight * 0.7 < portalBy + portalLong) and (portalBvertical == True) or (sideshotBx > portalBx) and (sideshotBx + bulletWidth * 0.7 < portalBx + portalLong) and (sideUPshotB == True) and (sideshotBy > portalBy) and (sideshotBy < portalBy + portalShort) and (portalBhorizontal == True) or (sideshotBx > portalBx) and (sideshotBx + bulletHeight * 0.7 < portalBx + portalLong) and (sideDOWNshotB == True) and (sideshotBy + bulletHeight * 0.7 > portalBy) and (sideshotBy + bulletHeight * 0.7 < portalBy + portalShort) and (portalBhorizontal == True):
        if portalAhorizontal == True:
            sideshotBx = portalAx + 49 - bulletWidth
            if sideUPshotB == True:
                sideshotBy = portalAy + 18 - bulletWidth
            else:
                sideshotBy = portalAy + 18 + bulletWidth
        if portalAvertical == True:
            sideUPshotB = False
            sideDOWNshotB = False
            bulletB = True
            bulletBx = portalAx + 18 - bulletWidth
            bulletBy = portalAy + 49 - bulletHeight / 2


    # If bullets go off the end of the screen, bullets disappear
    if (bulletAx > screenWidth): bulletA = False
    if (bulletBx + bulletWidth < 0): bulletB = False
    if (sideshotAx - bulletWidth * 0.7 > screenWidth):
        sideUPshotA = False
        sideDOWNshotA = False
    if (sideshotBx + bulletWidth * 0.7 < 0):
        sideUPshotB = False
        sideDOWNshotB = False

    # If ball goes off the end of the screen, ball respawns, ball's speed resets,
    # increase the score
    if (ballX+ballSize > screenWidth) :
        ballX = screenWidth / 2
        ballY = screenHeight / 2
        angle = random.randint(0,600)/100.
        speedX = ballSpeed * math.cos(angle)
        speedY = ballSpeed * math.sin(angle)
        playerBscore = playerBscore + 1
        randint = random.randint(0,2)
        sound_WellDone.play(0)

    if (ballX < 0) :
        ballX = screenWidth / 2
        ballY = screenHeight / 2
        angle = random.randint(0,600)/100.
        speedX = ballSpeed * math.cos(angle)
        speedY = ballSpeed * math.sin(angle)
        playerAscore = playerAscore + 1
        randint = random.randint(0,2)
        sound_Noooo.play(0)

    # Changes the color of the ball depending on who the ball belongs to
    if speedX < colorSpeed and speedX > -colorSpeed: ballBelongsTo = 2
    if speedX < -colorSpeed: ballBelongsTo = 1
    elif speedX > colorSpeed: ballBelongsTo = 0
    else: ballBelongsTo = 2



    # If ball hits the top or bottom wall, bounce it back.
    if (ballY + ballSize > wallBottom) or (ballY < wallTop) :
        speedY = -speedY
        sound_BallBounceWall.play(0)
        if (speedX < 35) and (speedX > -35):
            speedX = speedX * 5
            s = random.randint(0,1)
            if (s == 1):
                sound_Wheee.play(0)
        elif (speedX < 65) and (speedX > -65):
            speedX = speedX * 4
            s = random.randint(0,1)
            if (s == 1):
                sound_Wheee.play(0)
        elif (speedX < 175) and (speedX > -175):
            speedX = speedX * 2
            s = random.randint(0,1)
            if (s == 1):
                sound_Wheee.play(0)
        if (ballY + ballSize > wallBottom): ballY = wallBottom - ballSize -1
        elif (ballY < wallTop): ballY = wallTop + 1

    # If bullets hit the top or bottom wall, bounce it back.
    if (sideshotAy > wallBottom):
        sideDOWNshotA = False
        sideUPshotA = True
        sound_BulletBounceWall.play(0)

    if (sideshotAy < wallTop):
        sideUPshotA = False
        sideDOWNshotA = True
        sound_BulletBounceWall.play(0)

    if (sideshotBy > wallBottom):
        sideDOWNshotB = False
        sideUPshotB = True
        sound_BulletBounceWall.play(0)

    if (sideshotBy < wallTop):
        sideUPshotB = False
        sideDOWNshotB = True
        sound_BulletBounceWall.play(0)

    distanceA = time_passed_seconds * paddleASpeed
    distanceB = time_passed_seconds * paddleBSpeed
    paddleAy += distanceA
    paddleBy += distanceB

    if (paddleAy < wallTop): paddleAy = wallTop
    if (paddleBy < wallTop): paddleBy = wallTop

    if (paddleAy+paddleHeight > wallBottom): paddleAy = wallBottom - paddleHeight
    if (paddleBy+paddleHeight > wallBottom): paddleBy = wallBottom - paddleHeight

    # Maximum score
    if (playerAscore > 20) or (playerBscore > 20):
          gamePhase = 3
##        pygame.quit()
##        exit()

    pygame.display.update()

  #GamePhase 3 : End Game screen, option to continue
  while (gamePhase == 3):
      playerAscore = 0
      playerBscore = 0
      for event in pygame.event.get():
        if (event.type == QUIT):
            pygame.quit()
            sys.exit()
        if (event.type == KEYDOWN):
            if (event.key == K_ESCAPE):
                    sound_Goodbye.play(0)
                    pygame.time.wait(1500)
                    pygame.quit()
                    exit()
            if (event.key == K_RETURN):
                gamePhase = 2
        if (event.type == JOYBUTTONDOWN) and (joysticks[event.joy].get_id() == 0) and (event.button == 0):
                    gamePhase = 2
        if (event.type == JOYBUTTONDOWN) and (joysticks[event.joy].get_id() == 1) and (event.button == 0):
                    gamePhase = 2
        if (event.type == JOYBUTTONDOWN) and (joysticks[event.joy].get_id() == 0) and (event.button == 1):
                    sound_Goodbye.play(0)
                    pygame.time.wait(1500)
                    pygame.quit()
                    exit()
        if (event.type == JOYBUTTONDOWN) and (joysticks[event.joy].get_id() == 1) and (event.button == 1):
                    sound_Goodbye.play(0)
                    pygame.time.wait(1500)
                    pygame.quit()
                    exit()

      goodbyeTextA = font6.render("We hope you enjoyed", False, BLACK)
      goodbyeTextB = font4.render("Portal Pong!", False, BLACK)
      controlTextA = font5.render("To start a new game, press 'Enter' on keyboard or 'A' button on either controller.", False, BLACK)
      controlTextB = font5.render("To exit game, press 'Escape' on keyboard or 'B' button on either controller.", False, BLACK)
      pygame.draw.rect (screen, ORANGE, ((0, (screenHeight - 50)), (screenWidth, 50)))
      pygame.draw.rect (screen, BLUE, ((screenWidth/2 - (screenWidth/4)),(screenHeight/2 - (screenHeight/4)), (screenWidth/2),(screenHeight/2)))
      screen.blit(goodbyeTextA, (screenWidth/3 - 35, screenHeight/3))
      screen.blit(goodbyeTextB, (screenWidth/3 + 10, screenHeight/3 + 90))
      screen.blit(controlTextA, (50, screenHeight - 40))
      screen.blit(controlTextB, (50, screenHeight - 25))
      pygame.display.update()
