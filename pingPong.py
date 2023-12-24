from tkinter import messagebox
from tkinter import *

import pygame
import random
import sys


def disable_close_window():
    pass


def ball_animation():
    global ball_speed_y, ball_speed_x, player_points, opponent_points
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <= 0:
        ball_restart()
        player_points += 1
    elif ball.right >= screen_width:
        ball_restart()
        opponent_points += 1

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
    # Is not equal than, but instead equal or more than/less than, because the
    # Multiplying within the ball animation, it either can exceed or be less than the screen height
    # Which is why when that happens, the ball simply reverts back to the screen dividing by -1
    # The ball will restart if it goes too much left (The opponent's wall) or too much right (Main player's wall)


def player_border():
    player.y += player_move
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height
    # If it is less than 0 or exceeds the screen height, the player block will simply teleport to intended
    # location.


def opponent_border():
    opponent.y += opponent_move
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def opponent_ai():
    global opponent_move_difficulty

    if opponent.top < ball.y:
        opponent.top += (opponent_move + opponent_move_difficulty)
    if opponent.bottom > ball.y:
        opponent.bottom -= (opponent_move + opponent_move_difficulty)
    player.y += player_move

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    global ball_speed_y, ball_speed_x

    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))


def difficulty_check(difficulty):
    global opponent_move_difficulty

    if difficulty == "easy":
        opponent_move_difficulty = -2
    elif difficulty == "normal":
        opponent_move_difficulty = 2
    elif difficulty == "hard":
        opponent_move_difficulty = 5

    difficulty_menu.destroy()


def update_text():
    global player_score_text, opponent_score_text

    player_score_text = font.render(f"{player_points}", True, light_grey, bg_colour)
    opponent_score_text = font.render(f"{opponent_points}", True, light_grey, bg_colour)


# Single Player or Multiplayer option
msg = Tk()
msg.withdraw()
choice = messagebox.askyesno("Pong!", "Do you have a friend to play with? ")
msg.destroy()

# Difficulty menu
difficulty_menu = Tk()
difficulty_menu.title("Pong! | Difficulty")
difficulty_menu.geometry("318x50")
difficulty_menu.resizable(False, False)
difficulty_menu.protocol("WM_DELETE_WINDOW", disable_close_window)

easy_btn = Button(difficulty_menu,
                  text="Easy",
                  padx=10,
                  font=("consolas", 22, "bold"),
                  command=lambda: difficulty_check("easy"))
easy_btn.grid(row=0, column=0)

normal_btn = Button(difficulty_menu,
                    text="Normal",
                    font=("Consolas", 22, "bold"),
                    command=lambda: difficulty_check("normal"))
normal_btn.grid(row=0, column=1)

hard_btn = Button(difficulty_menu,
                  text="Hard",
                  padx=10,
                  font=("Consolas", 22, "bold"),
                  command=lambda: difficulty_check("hard"))
hard_btn.grid(row=0, column=2)

if choice is False:  # For if they said they did not have any friends to play with
    difficulty_menu.focus()
    difficulty_menu.attributes("-topmost", True)
    difficulty_menu.mainloop()

# Points logic
player_points = 0
opponent_points = 0

# Main Window set up
screen_width = 1280
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong!")

pygame.init()
clock = pygame.time.Clock()

# Colours
bg_colour = (51, 49, 53)
light_grey = (95, 96, 98)
ball_colour = (255, 50, 0)

# Assets (Font)
font = pygame.font.SysFont("consolas", 128, bold=True)
player_score_text = font.render(f"{player_points}", True, light_grey, bg_colour)
opponent_score_text = font.render(f"{opponent_points}", True, light_grey, bg_colour)

player_score_rect = player_score_text.get_rect()
opponent_score_rect = opponent_score_text.get_rect()

player_score_rect.center = ((screen_width // 4) * 3, screen_height / 2)
opponent_score_rect.center = (screen_width // 4, screen_height / 2)

# Assets (Rectangles)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Movement
ball_speed_x = 7
ball_speed_y = 7
player_move = 0
opponent_move = 7
# Movement Difficulty (Added on in order to change the experience. Set variable is changed within a function)
opponent_move_difficulty = 0

if choice is False:  # Player does not have friend
    # A choice was added to give a decision towards the user and to make me look like a cooler programmer
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_move += 7
                if event.key == pygame.K_UP:
                    player_move -= 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_move -= 7
                if event.key == pygame.K_UP:
                    player_move += 7

        ball_animation()
        player_border()
        opponent_ai()
        update_text()

        # Drawing of the Visuals
        screen.fill(bg_colour)
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)

        # Writing out the text
        screen.blit(player_score_text, player_score_rect)
        screen.blit(opponent_score_text, opponent_score_rect)

        # Continued visuals (to be above text)
        pygame.draw.ellipse(screen, ball_colour, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

        # Updating the frames
        pygame.display.flip()
        clock.tick(60)
else:  # Player has friend
    opponent_move = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_move += 7
                if event.key == pygame.K_UP:
                    player_move -= 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_move -= 7
                if event.key == pygame.K_UP:
                    player_move += 7

            # Opponent movement

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    opponent_move -= 7
                if event.key == pygame.K_s:
                    opponent_move += 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    opponent_move += 7
                if event.key == pygame.K_s:
                    opponent_move -= 7

        ball_animation()
        player_border()
        opponent_border()
        update_text()

        # Writing out the text
        screen.blit(player_score_text, player_score_rect)
        screen.blit(opponent_score_text, opponent_score_rect)

        # Drawing of the Visuals
        screen.fill(bg_colour)
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)

        # Writing out the text
        screen.blit(player_score_text, player_score_rect)
        screen.blit(opponent_score_text, opponent_score_rect)

        # Continued visuals (to be above text)
        pygame.draw.ellipse(screen, ball_colour, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

        # Updating the frames
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
