import pygame, sys, random, time, math

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = screen_width/2 - 10
    ball.y = screen_height/2
    ball_speed_x = 0
    ball_speed_y = 0


def point_won(winner):
    global player1_points, player2_points

    if winner == "player1":
        player1.points += 1
    if winner == "player2":
        player2.points += 1

    reset_ball()


def animate_ball():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Check collision with walls
    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1

    # Check collision with player1's dash racket
    if player1.dashing:
        if ball.colliderect(player1):
            ball_speed_x *= -1.05
            ball_speed_y += (ball.centery - player1.rect.centery) * 0.05  # Transfer momentum based on collision position
            reset_ball()
            return 

    if player2.dashing:
        if ball.colliderect(player2):
            ball_speed_x *= -1.05
            ball_speed_y += (ball.centery - player2.rect.centery) * 0.05  # Transfer momentum based on collision position
            reset_ball()
            return

    if ball.colliderect(player1):
        ball_speed_x *= -1.05
        ball_speed_y += (ball.centery - player1.rect.centery) * 0.05  # Transfer momentum based on collision position
    if ball.colliderect(player2):
        ball_speed_x *= -1.05
        ball_speed_y += (ball.centery - player2.rect.centery) * 0.05  # Transfer momentum based on collision position

    if ball.right >= screen_width:
        point_won("player1")
    if ball.left <= 0:
        point_won("player2")


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
    

def animate_player2():
    player2.rect.y += player2.y_speed * player2.speed_multiplier
    player2.rect.x += player2.x_speed * player2.speed_multiplier
    player2.x_speed = 0
    player2.y_speed = 0

    if player2.rect.top <= 0:
        player2.rect.top = 0

    if player2.rect.bottom >= screen_height:
        player2.rect.bottom = screen_height

    if player1.rect.right >= screen_width:
        player1.rect.right = screen_width

    if player1.rect.left <= 0:
        player1.rect.left = 0


def dash(player):
    if not player.dashing and time.time() - player.last_dash_time >= 1:
        player.dash_speed_x = player.x_speed
        player.dash_speed_y = player.y_speed
        player.speed_multiplier = 2
        player.dashing = True
        player.dash_start_time = time.time()
        player.last_dash_time = time.time()
        player.dash_start_pos = player.rect.center


def handle_movement(plr, rackets):
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


pygame.init()

screen_width = 900
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ping pong")

clock = pygame.time.Clock()

ball = pygame.Rect(0,0,30,30)
ball.center = (screen_width/2, screen_height/2)

player1 = Player(0, screen_height/2, 10, 150)
player2 = Player(screen_width - 10, screen_height/2, 10, 150)

ball_speed_x = 0
ball_speed_y = 0
rackets = []

score_font = pygame.font.Font(None, 100)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    
    handle_movement(player1, rackets)
    handle_movement(player2, rackets)

    animate_ball()
    animate_player1()
    animate_player2()
        
    draw([player1, player2], "black", rackets)
    pygame.display.update()
    clock.tick(60)