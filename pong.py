import pygame as pg
import sys
import random

pg.init()

screen_h = 800
screen_w = 1280
screen = pg.display.set_mode((screen_w, screen_h)) # width, height
pg.display.set_caption("Coding Challenges Pong")
clock = pg.time.Clock()

difficulty = 5
trap_status = True        

# Ball

ball = pg.Rect(0, 0, 20, 20)
ball.center = (screen_w // 2, screen_h // 2)
ball_speed = [6,6] # ball_speed = [x, y]

def ball_move():
    global ball_speed
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.left <= 0:
        goal("player")
    
    if ball.right >= screen_w:
        goal("ai")

    if ball.bottom >= screen_h or ball.top <= 0:
        ball_speed[1] *= -1
    
    if ball.colliderect(player) or ball.colliderect(ai):
        ball_speed[0] *= -1
    
    if trap_status:
        if ball.colliderect(trap):
            ball_speed[0] *= -1

# Players


player = pg.Rect(0, 0, 20, 100)
player.midright = (screen_w, screen_h // 2)
player_speed = 0

def player_move():
    global player_speed
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_h:
        player.bottom = screen_h

ai = pg.Rect(0, 0, 20, 100)
ai.centery = screen_h // 2
ai_speed = 0
difficulty = 4

def ai_move():
    global ai_speed
    ai.y += ai_speed

    if ai.top <= 0:
        ai.top = 0
    if ai.bottom >= screen_h:
        ai.bottom = screen_h
    if ball.centerx <= screen_w // 2:
        if ball.centery <= ai.centery:
            ai_speed = -difficulty
        if ball.centery >= ai.centery:
            ai_speed = difficulty

if trap_status:
    trap = pg.Rect(0, 0, 20, 100)
    trap.center = (screen_w // 2, 50)
    trap_speed = 6

def trap_move():
    global trap_speed
    trap.y += trap_speed

    if trap.top <= 0 or trap.bottom >= screen_h:
        trap_speed *= -1

# Score Table

player_score = 0
ai_score = 0
score_font = pg.font.Font(None, 50)

def goal(winner):
    global ball_speed, player_score, ai_score
    ball.center = (screen_w // 2, screen_h // 2)
    ball_speed = [random.choice([-6, 6]), random.choice([-6, 6])]

    trap.center = (screen_w // 2, 50)
    if winner == "player":
        player_score += 1
        print("Player scored!")
    if winner == "ai":
        ai_score += 1
        print("AI scored!")
    
    print(f"Player: {player_score} | AI: {ai_score}")


def start_screen():
    global difficulty, trap_status
    screen.fill((66, 249, 255))
    title_font = pg.font.Font(None, 80)
    title_text = title_font.render("Coding Challenges Pong", True, (0, 0, 0))
    screen.blit(title_text, (screen_w // 2 - title_text.get_width() // 2, 100))

    easy_button = pg.Rect(screen_w // 2 - 100, 300, 200, 50)
    hard_button = pg.Rect(screen_w // 2 - 100, 400, 200, 50)

    pg.draw.rect(screen, (0, 52, 240), easy_button)
    pg.draw.rect(screen, (106, 0, 163), hard_button)

    button_font = pg.font.Font(None, 30)
    easy_text = button_font.render("Easy", True, (255, 255, 255))
    hard_text = button_font.render("Hard", True, (255, 255, 255))

    screen.blit(easy_text, (easy_button.centerx - easy_text.get_width() // 2, easy_button.centery - easy_text.get_height() // 2))
    screen.blit(hard_text, (hard_button.centerx - hard_text.get_width() // 2, hard_button.centery - hard_text.get_height() // 2))

    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if easy_button.collidepoint(mouse_pos):
                    difficulty = 5
                    trap_status = False
                    return
                elif hard_button.collidepoint(mouse_pos):
                    difficulty = 6
                    trap_status = True
                    return

def main():
    global player_speed, ai_speed, trap_speed, difficulty, player_score, ai_score, trap_status
    start_screen()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    player_speed = 6
                if event.key == pg.K_UP:
                    player_speed = -6
            
            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN:
                    player_speed = 0
                if event.key == pg.K_UP:
                    player_speed = 0

        # Changing positions
        ball_move()
        player_move()
        ai_move()

        if trap_status:
            trap_move()
        

        # Draw objects
        screen.fill((0,0,0)) # fill the screen with a color

        ai_score_text = score_font.render("AI " + str(ai_score), True, "white")
        player_score_text = score_font.render("P1 " + str(player_score), True, "white")
        screen.blit(ai_score_text, (screen_w // 2 - 200, 50))
        screen.blit(player_score_text, (screen_w // 2 + 50, 50))

        pg.draw.aaline(screen, "white", (screen_w // 2, 0), (screen_w // 2, screen_h))
        pg.draw.ellipse(screen, "white", ball) # diff between rect and ellipse? rect is a rectangle, ellipse is an ellipse
        pg.draw.rect(screen, "blue", ai)
        pg.draw.rect(screen, "blue", player)

        if trap_status:
            pg.draw.rect(screen, "white", trap)

        # pg.display.flip() # diff between flip and update? flip updates the entire screen, update updates only the changes
        pg.display.update() # update the screen with the new changes
        clock.tick(60) # 60 frames per second

if __name__ == "__main__":
    main()