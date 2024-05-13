import pygame, sys, random, time, math



def reset_ball():
    global ball_speed_x, ball_speed_y, last_touch
    ball.x = screen_width/2 - 10
    ball.y = screen_height/2
    ball_speed_x = 4 * random.choice([-1, 1])
    ball_speed_y = 4 * random.choice([-1, 1])
    last_touch = None



def point_won(winner):
    global player1_points, player2_points

    if winner == "player1":
        player1.points += 1
    if winner == "player2":
        player2.points += 1

    reset_ball()



def animate_ball():
    global ball_speed_x, ball_speed_y, last_touch
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    if ball.colliderect(player1):
        ball_speed_x *= -1.05
        ball_speed_y += (ball.centery - player1.rect.centery) * 0.05 
        ball.left = player1.rect.right
        last_touch = player1

    if ball.colliderect(player2):
        ball_speed_x *= -1.05
        ball_speed_y += (ball.centery - player2.rect.centery) * 0.05
        ball.right = player2.rect.left 
        last_touch = player2

    if ball.right >= screen_width:
        point_won("player1")
    if ball.left <= 0:
        point_won("player2")

    if powerups and ball.colliderect(powerups[0]) and last_touch != None:
        callevent(powerups[0].type, last_touch)
        del powerups[0]



def animate_player1():
    player1.rect.y += player1.y_speed * player1.speed_multiplier
    player1.rect.x += player1.x_speed * player1.speed_multiplier
    player1.x_speed = 0
    player1.y_speed = 0

    if player1.rect.top <= 0:
        player1.rect.top = 0

    if player1.rect.bottom >= screen_height:
        player1.rect.bottom = screen_height

    if player1.rect.right >= screen_width:
        player1.rect.right = screen_width

    if player1.rect.left <= 0:
        player1.rect.left = 0
    if player1.rect.right >= screen_width/4:
        player1.rect.right = screen_width/4



def animate_player2():
    player2.rect.y += player2.y_speed * player2.speed_multiplier
    player2.rect.x += player2.x_speed * player2.speed_multiplier
    player2.x_speed = 0
    player2.y_speed = 0

    if player2.rect.top <= 0:
        player2.rect.top = 0

    if player2.rect.bottom >= screen_height:
        player2.rect.bottom = screen_height

    if player2.rect.right >= screen_width:
        player2.rect.right = screen_width

    if player2.rect.left <= (screen_width - (screen_width/4)):
        player2.rect.left = (screen_width - (screen_width/4))
    
    
    
def callevent(selected_event, player):
    if selected_event == "Large Paddle":
        player.rect.inflate_ip(10, 100)
        


def randomevent(eo):
    if random.random() <= 0.004 and eo == False:
        global event_ongoing
        powerup_list = ["Large Paddle", "Increase Speed", "Confusion", "Darkness", "Time Warp"]
        selected_event = powerup_list[random.randint(0, len(powerup_list) - 1)]
        event_ongoing = "Large Paddle"

        x = random.randrange(int(screen_width/4), int((screen_width - (screen_width/4))))
        y = random.randrange(0, screen_height)

        pw_up = Powerup(x, y, 32, event_ongoing)
        powerups.append(pw_up)
        


def draw(players, background):
    screen.fill(background)

    plr1_score_surface = score_font.render(str(players[0].points), True, "pink")
    plr2_score_surface = score_font.render(str(players[1].points), True, "pink")


    screen.blit(plr1_score_surface,(screen_width/4,20))
    screen.blit(plr2_score_surface,(3*screen_width/4,20))

    pygame.draw.aaline(screen,'pink',(screen_width/2, 0), (screen_width/2, screen_height))
    pygame.draw.aaline(screen,'blue',(screen_width/4, 0), (screen_width/4, screen_height))
    pygame.draw.aaline(screen,'blue',(screen_width - (screen_width/4), 0), (screen_width - (screen_width/4), screen_height))
    pygame.draw.ellipse(screen,'pink',ball)

    if players[0].dashing:
        pygame.draw.rect(screen,'green',players[0])
    else:
        pygame.draw.rect(screen,'pink',players[0])
    if players[1].dashing:
        pygame.draw.rect(screen,'green',players[1])
    else:
        pygame.draw.rect(screen,'pink',players[1])

    for i in powerups:
        if i:
            pygame.draw.rect(screen, "red", i)



def dash(player):
    if not player.dashing and time.time() - player.last_dash_time >= 1:
        player.dash_speed_x = player.x_speed
        player.dash_speed_y = player.y_speed
        player.speed_multiplier = 2
        player.dashing = True
        player.dash_start_time = time.time()
        player.last_dash_time = time.time()
        player.dash_start_pos = player.rect.center



def handle_movement(plr):
    keys = pygame.key.get_pressed()

    if plr == player1:
        if keys[pygame.K_w] and not keys[pygame.K_s]:
            plr.y_speed = -plr.vel
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            plr.y_speed = plr.vel

        if keys[pygame.K_a] and not keys[pygame.K_d]:
            plr.x_speed = -plr.vel
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            plr.x_speed = plr.vel

        if abs(plr.x_speed) + abs(plr.y_speed) >= plr.vel*2:
            plr.x_speed = plr.x_speed/math.sqrt(2)
            plr.y_speed = plr.y_speed/math.sqrt(2)

        if keys[pygame.K_SPACE] and plr.dashing != True:
            dash(plr)

        if plr.dashing and time.time() - plr.dash_start_time >= 0.25:
            plr.speed_multiplier = 1
            plr.dashing = False  



    if plr == player2:
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            plr.y_speed = -plr.vel
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            plr.y_speed = plr.vel

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            plr.x_speed = -plr.vel
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            plr.x_speed = plr.vel

        if abs(plr.x_speed) + abs(plr.y_speed) >= plr.vel*2:
            plr.x_speed = plr.x_speed/math.sqrt(2)
            plr.y_speed = plr.y_speed/math.sqrt(2)

        if keys[pygame.K_m] and plr.dashing != True:
            dash(plr)

        if plr.dashing and time.time() - plr.dash_start_time >= 0.25:
            plr.speed_multiplier = 1
            plr.dashing = False  



class Player():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.y_speed = 0
        self.x_speed = 0
        self.vel = 5
        self.speed_multiplier = 1
        self.points = 0
        self.dashing = False
        self.last_direction = 0
        self.dash_start_time = 0  
        self.last_dash_time = 0
        self.dash_start_pos = 0



class Powerup():
    def __init__(self, x, y, size, type):
        self.rect = pygame.Rect(x, y, size, size)
        self.type = type



pygame.init()

screen_width = 900
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ping pong")

clock = pygame.time.Clock()

ball = pygame.Rect(0,0,30,30)
ball.center = (screen_width/2, screen_height/2)

player1 = Player(0, screen_height/2, 10, 75)
player2 = Player(screen_width - 10, screen_height/2, 10, 75)

ball_speed_x = 4
ball_speed_y = 4
last_touch = None

global event_ongoing
event_ongoing = False
powerups = []

score_font = pygame.font.Font(None, 100)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    handle_movement(player1)
    handle_movement(player2)
    animate_player1()
    animate_player2()

    animate_ball()
    draw([player1, player2], "black")

    randomevent(event_ongoing)

    pygame.display.update()
    clock.tick(60)