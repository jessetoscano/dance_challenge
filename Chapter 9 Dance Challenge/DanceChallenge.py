# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:54:03 2024

@author: John Quiambao
"""
# Imports essential modules for game logic, graphics, and user input handling
import pgzrun
import pygame
import pgzero
from pgzero.builtins import Actor
from random import randint
from pygame.locals import *
import time
from sys import exit

# Screen dimensions and center coordinates
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

# Game state and variables initialization
move_list = []  # Stores sequence of dance moves
display_list = []  # Moves to display for the player

score = 0  # Player 1's score
score1 = 0  # Player 2's score
current_move = 0  # Index for current move in the sequence
count = 4  # Countdown before the dance begins
dance_length = 2  # Number of moves in the sequence
rounds = 0  # Tracks game rounds

say_dance = False  # Flag to display "Dance!" text
show_countdown = True  # Flag to display the countdown
moves_complete = False  # Tracks completion of moves
game_over = False  # Flag to end the game
winner_name = "" # Stores the name of the winner

player1_name = ""  # Name for Player 1
player2_name = ""  # Name for Player 2

# Initialize dancer and arrow Actors with positions
dancer = Actor("dancer-start")  #create the dancer character
dancer.pos = CENTER_X + 5, CENTER_Y - 40

up = Actor("up")
up.pos = CENTER_X, CENTER_Y + 110
right = Actor("right")
right.pos = CENTER_X + 60, CENTER_Y + 170
down = Actor("down")
down.pos = CENTER_X, CENTER_Y + 230
left = Actor("left")
left.pos = CENTER_X - 60, CENTER_Y + 170

# GUI to get player names before the game starts
def get_player_names_gui():
    global player1_name, player2_name
    
    # Opens a window to collect names from two players
    window_width = 800
    window_height = 600
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Enter Player Names:")
    
    input_box1 = pygame.Rect(window_width // 2 - 100, window_height // 2 - 50, 200, 32)
    input_box2 = pygame.Rect(window_width // 2 - 100, window_height // 2 + 50, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color1 = color_inactive
    color2 = color_inactive
    active1 = False
    active2 = False
    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active1 = not active1
                else:
                    active1 = False
                if input_box2.collidepoint(event.pos):
                    active2 = not active2
                else:
                    active2 = False
                color1 = color_active if active1 else color_inactive
                color2 = color_active if active2 else color_inactive
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN:
                        active1 = False
                    elif event.key == pygame.K_BACKSPACE:
                        player1_name = player1_name[:-1]
                    else:
                        player1_name += event.unicode
                if active2:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    else:
                        player2_name += event.unicode
        
        window.fill((30, 30, 30))
        font = pygame.font.Font(None, 36)
        text1 = font.render("Player 1, enter your name:", True, (255, 255, 255))
        text2 = font.render("Player 2, enter your name:", True, (255, 255, 255))
        window.blit(text1, (window_width // 2 - 150, window_height // 2 - 80))
        window.blit(text2, (window_width // 2 - 150, window_height // 2 + 20))
        pygame.draw.rect(window, color1, input_box1, 2)
        pygame.draw.rect(window, color2, input_box2, 2)
        text_surface1 = font.render(player1_name, True, (255, 255, 255))
        text_surface2 = font.render(player2_name, True, (255, 255, 255))
        window.blit(text_surface1, (input_box1.x + 5, input_box1.y + 5))
        window.blit(text_surface2, (input_box2.x + 5, input_box2.y + 5))
        pygame.display.flip()

# Main draw function to render game graphics
def draw():
    global game_over, score, say_dance
    global count, show_countdown, score1
    global rounds, winner_name
    if not game_over:
        # Render background, dancer, arrows, scores, and prompts
        screen.clear()
        screen.blit("stage", (0, 0))    #displays the background stage of the game
        dancer.draw()
        up.draw()
        down.draw()
        right.draw()
        left.draw()
        screen.draw.text(f"Score for {player1_name}: " +
                         str(score), color="black",
                         topleft=(10, 10))
        screen.draw.text(f"Score for {player2_name}: " +
                         str(score1), color="black",
                         topleft=(625, 10))
        if say_dance:
            screen.draw.text("Dance!", color="black",
                             topleft=(CENTER_X - 55, 150), fontsize=50)
        if show_countdown:
            screen.draw.text(str(count), color="black",
                             topleft=(CENTER_X - 8, 150), fontsize=50)
            if (rounds % 2 == 0):
                screen.draw.text(f"{player1_name}'s turn", color="red",
                                 topleft=(CENTER_X - 100, 100), fontsize=50)
            else:
                screen.draw.text(f"{player2_name}'s turn", color="blue",
                                 topleft=(CENTER_X - 100, 100), fontsize=50)
                
    else:
        # Display game over screen with final scores
        screen.clear()
        screen.blit("stage", (0, 0))
        screen.draw.text(f"Score for {player1_name}: " +
                         str(score), color="black",
                         topleft=(10, 10))
        screen.draw.text(f"Score for {player2_name}: " +
                         str(score1), color="black",
                         topleft=(600, 10))
        
        # Determine and display the winner
        if winner_name:
            winner_text = f"Winner is {winner_name}!"
        else:
            # Handle a tie
            winner_text = "It's a Tie!"
        
        screen.draw.text(winner_text, color="black",
                         topleft=(CENTER_X - 130, 220), fontsize=60)
        
    return

# Resets the dancer and arrows to default state
def reset_dancer():
    global game_over
    if not game_over:  #for when the game is not over
        dancer.image = "dancer-start"
        up.image = "up"
        right.image = "right"
        down.image = "down"
        left.image = "left"
    return

# Updates dancer and arrows based on the current move
def update_dancer(move):
    global game_over
    if not game_over:
        # Changes images and schedules a reset after 0.5 seconds
        if move == 0:  #if move is up, it changes to lit image of arrow, then changes dancer's position
            up.image = "up-lit"
            dancer.image = "dancer-up"
            clock.schedule(reset_dancer, 0.5)
        elif move == 1:
            right.image = "right-lit"
            dancer.image = "dancer-right"
            clock.schedule(reset_dancer, 0.5)
        elif move == 2:
            down.image = "down-lit"
            dancer.image = "dancer-down"
            clock.schedule(reset_dancer, 0.5)
        else:
            left.image = "left-lit"
            dancer.image = "dancer-left"
            clock.schedule(reset_dancer, 0.5)
    return

# Displays the sequence of moves to the players
def display_moves():
    global move_list, display_list, dance_length
    global say_dance, show_countdown, current_move
    if display_list:
        # Iterates through and shows each move in the sequence
        this_move = display_list[0]
        display_list = display_list[1:]
        if this_move == 0:
            update_dancer(0)
            clock.schedule(display_moves, 1)
        elif this_move == 1:
            update_dancer(1)
            clock.schedule(display_moves, 1)
        elif this_move == 2:
            update_dancer(2)
            clock.schedule(display_moves, 1)
        else:
            update_dancer(3)
            clock.schedule(display_moves, 1)
    else:
        say_dance = True
        show_countdown = False
    return

# Countdown before the sequence is displayed
def countdown():
    global count, game_over, show_countdown
    if count > 1:
        count = count - 1
        clock.schedule(countdown, 1)
    else:
        show_countdown = False
        display_moves()
    return

# Generates a new random sequence of dance moves
def generate_moves():
    global move_list, dance_length, count
    global show_countdown, say_dance
    count = 4
    move_list = []
    say_dance = False
    for move in range(0, dance_length):
        rand_move = randint(0, 3)
        move_list.append(rand_move)
        display_list.append(rand_move)
    show_countdown = True
    countdown()
    return

# Moves to the next dance move in the sequence
def next_move():
    global dance_length, current_move, moves_complete
    if current_move < dance_length - 1:
        current_move = current_move + 1
    else:
        moves_complete = True
    return

def check_player_input(key_map, move_key, player_score):
    """
    Checks if a keypress matches the current dance move.
    
    :param key_map: A dictionary mapping keypresses to move indices.
    :param move_key: The key that was pressed.
    :param player_score: The score to increment if the move is correct.
    """
    global score, score1, game_over, move_list, current_move, rounds, winner_name
    
    if move_key in key_map:
        move_index = key_map[move_key]
        update_dancer(move_index)
        
        if move_list[current_move] == move_index:
            if player_score == 'score':
                score += 1
            else:
                score1 += 1
            next_move()
        else:
            game_over = True
            # Determine the winner when the game ends
            if score > score1:
                winner_name = player1_name
            elif score1 > score:
                winner_name = player2_name
            else:
                winner_name = ""  # For a tie
            
def on_key_up(key):
    global rounds
    
    print(f"Current round: {rounds}. Player turn: {'Player 1' if rounds % 2 == 0 else 'Player 2'}")
    
    # Define key maps for each player
    player1_keys = {
        keys.UP: 0,
        keys.RIGHT: 1,
        keys.DOWN: 2,
        keys.LEFT: 3
    }
    
    player2_keys = {
        keys.W: 0,
        keys.D: 1,
        keys.S: 2,
        keys.A: 3
    }

    # Check input based on whose turn it is
    if (rounds % 2 == 0):
        # It's Player 1's turn
        check_player_input(player1_keys, key, 'score')
    else:
        # It's Player 2's turn
        check_player_input(player2_keys, key, 'score1')

# Initialize game setup and play background music
get_player_names_gui()        
generate_moves()
music.play("vanishing-horizon")

# Game update loop
def update():
    global game_over, current_move, moves_complete
    global rounds, dance_length
    if not game_over:
        if moves_complete:
            rounds = rounds + 1
            if (rounds % 2 == 0):
                dance_length = dance_length + 1
            generate_moves()
            moves_complete = False
            current_move = 0
    else:
        music.stop()

# Starts the game loop
pgzrun.go()