# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:54:03 2024

@author: John Quiambao
"""
import pgzrun
import pygame
import pgzero
from pgzero.builtins import Actor
from random import randint
from pygame.locals import *
import time
from sys import exit

# Screen dimensions and center coordinates
WIDTH = 1000  # Increased width for split-screen
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

# Game state and variables initialization
move_list = []
display_list = []
dance_length = 2

# --- Player 1 State Variables ---
p1_current_move = 0
p1_lives = 3
p1_round_failed = False
p1_active = True
p1_name = ""

# --- Player 2 State Variables ---
p2_current_move = 0
p2_lives = 3
p2_round_failed = False
p2_active = True
p2_name = ""

# --- Shared Game State ---
count = 4
say_dance = False
show_countdown = True
game_over = False
winner_name = ""
round_in_progress = False
first_round = True  # New variable to control the initial countdown timer

# --- Actors for Player 1 (Left Side) ---
p1_dancer = Actor("dancer-start")
p1_up = Actor("up")
p1_right = Actor("right")
p1_down = Actor("down")
p1_left = Actor("left")

# --- Actors for Player 2 (Right Side) ---
p2_dancer = Actor("dancer-start")
p2_up = Actor("up")
p2_right = Actor("right")
p2_down = Actor("down")
p2_left = Actor("left")

# Function to set the initial positions of all actors
def set_actor_positions():
    # Player 1 is permanently on the left side
    p1_dancer.pos = CENTER_X - 250, CENTER_Y - 40
    p1_up.pos = CENTER_X - 250, CENTER_Y + 110
    p1_right.pos = CENTER_X - 250 + 60, CENTER_Y + 170
    p1_down.pos = CENTER_X - 250, CENTER_Y + 230
    p1_left.pos = CENTER_X - 250 - 60, CENTER_Y + 170

    # Player 2 is permanently on the right side
    p2_dancer.pos = CENTER_X + 250, CENTER_Y - 40
    p2_up.pos = CENTER_X + 250, CENTER_Y + 110
    p2_right.pos = CENTER_X + 250 + 60, CENTER_Y + 170
    p2_down.pos = CENTER_X + 250, CENTER_Y + 230
    p2_left.pos = CENTER_X + 250 - 60, CENTER_Y + 170

# Call the function once at the beginning to set initial positions
set_actor_positions()

# Resets all game variables for a new game
def reset_game():
    global p1_current_move, p1_lives, p1_round_failed, p1_active
    global p2_current_move, p2_lives, p2_round_failed, p2_active
    global count, dance_length, say_dance, show_countdown, game_over, winner_name
    global round_in_progress, first_round
    
    p1_current_move = 0
    p1_lives = 3
    p1_round_failed = False
    p1_active = True
    
    p2_current_move = 0
    p2_lives = 3
    p2_round_failed = False
    p2_active = True
    
    count = 4
    dance_length = 2
    say_dance = False
    show_countdown = True
    game_over = False
    winner_name = ""
    round_in_progress = False
    first_round = True # Reset for new game
    
    generate_moves()
    music.play("vanishing-horizon")

# GUI to get player names before the game starts
def get_player_names_gui():
    global p1_name, p2_name
    
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
                        p1_name = p1_name[:-1]
                    else:
                        p1_name += event.unicode
                if active2:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        p2_name = p2_name[:-1]
                    else:
                        p2_name += event.unicode
        
        window.fill((30, 30, 30))
        font = pygame.font.Font(None, 36)
        text1 = font.render("Player 1, enter your name:", True, (255, 255, 255))
        text2 = font.render("Player 2, enter your name:", True, (255, 255, 255))
        window.blit(text1, (window_width // 2 - 150, window_height // 2 - 80))
        window.blit(text2, (window_width // 2 - 150, window_height // 2 + 20))
        pygame.draw.rect(window, color1, input_box1, 2)
        pygame.draw.rect(window, color2, input_box2, 2)
        text_surface1 = font.render(p1_name, True, (255, 255, 255))
        text_surface2 = font.render(p2_name, True, (255, 255, 255))
        window.blit(text_surface1, (input_box1.x + 5, input_box1.y + 5))
        window.blit(text_surface2, (input_box2.x + 5, input_box2.y + 5))
        pygame.display.flip()

def draw():
    global game_over, say_dance, count, show_countdown, winner_name
    global p1_lives, p2_lives, p1_active, p2_active
    
    if not game_over:
        screen.clear()
        screen.blit("stage", (0, 0))
        
        # Draw a divider line for the split-screen
        screen.draw.line((WIDTH / 2, 0), (WIDTH / 2, HEIGHT), (255, 255, 255))

        # Player 1 (Left Side) - Character on the left, score on the left
        p1_dancer.draw()
        p1_up.draw()
        p1_right.draw()
        p1_down.draw()
        p1_left.draw()
        if p1_active:
            screen.draw.text(f"{p1_name} Lives: {p1_lives}", color="yellow", topleft=(10, 40), fontname="digital", fontsize=30)
        else:
            screen.draw.text(f"{p1_name} OUT!", color="yellow", topleft=(10, 40), fontname="digital", fontsize=30)
            
        # Player 2 (Right Side) - Character on the right, score on the right
        p2_dancer.draw()
        p2_up.draw()
        p2_right.draw()
        p2_down.draw()
        p2_left.draw()
        if p2_active:
            screen.draw.text(f"{p2_name} Lives: {p2_lives}", color="white", topright=(WIDTH - 10, 40), fontname="digital", fontsize=30)
        else:
            screen.draw.text(f"{p2_name} OUT!", color="white", topright=(WIDTH - 10, 40), fontname="digital", fontsize=30)

        # --- Shared Elements ---
        if say_dance:
            screen.draw.text("Dance!", color="black", topleft=(CENTER_X - 55, 150), fontsize=50)
        if show_countdown:
            screen.draw.text(str(count), color="black", topleft=(CENTER_X - 8, 150), fontsize=50)
    else:
        screen.clear()
        screen.blit("stage", (0, 0))
        
        screen.draw.text(f"{p1_name} Lives: {p1_lives}", color="yellow",
                         topleft=(10, 40), fontname="digital", fontsize=30)
        screen.draw.text(f"{p2_name} Lives: {p2_lives}", color="white",
                         topright=(WIDTH - 10, 40), fontname="digital", fontsize=30)
        
        screen.draw.text(f"{winner_name}", color="white",
                         topleft=(CENTER_X - 130, 220), fontsize=60, fontname="digital",
                         ocolor="#FF0000", owidth=1.5)
        
        screen.draw.text("Press SPACE to play again", color="white",
                         topleft=(CENTER_X - 150, 300), fontsize=30, fontname="digital")
    
    return

def reset_dancer():
    p1_dancer.image = "dancer-start"
    p1_up.image = "up"
    p1_right.image = "right"
    p1_down.image = "down"
    p1_left.image = "left"
    p2_dancer.image = "dancer-start"
    p2_up.image = "up"
    p2_right.image = "right"
    p2_down.image = "down"
    p2_left.image = "left"

def update_dancer(player, move):
    if player == 1:
        if move == 0:
            p1_up.image = "up-lit"
            p1_dancer.image = "dancer-up"
        elif move == 1:
            p1_right.image = "right-lit"
            p1_dancer.image = "dancer-right"
        elif move == 2:
            p1_down.image = "down-lit"
            p1_dancer.image = "dancer-down"
        else:
            p1_left.image = "left-lit"
            p1_dancer.image = "dancer-left"
    else:
        if move == 0:
            p2_up.image = "up-lit"
            p2_dancer.image = "dancer-up"
        elif move == 1:
            p2_right.image = "right-lit"
            p2_dancer.image = "dancer-right"
        elif move == 2:
            p2_down.image = "down-lit"
            p2_dancer.image = "dancer-down"
        else:
            p2_left.image = "left-lit"
            p2_dancer.image = "dancer-left"
    
    clock.schedule(reset_dancer, 0.5)

def display_moves():
    global display_list, say_dance, show_countdown, round_in_progress
    
    if display_list:
        this_move = display_list[0]
        display_list = display_list[1:]
        
        update_dancer(1, this_move) # Update P1 dancer
        update_dancer(2, this_move) # Update P2 dancer
        
        clock.schedule(display_moves, 1)
    else:
        say_dance = True
        show_countdown = False
        round_in_progress = True

def countdown():
    global count, show_countdown
    if count > 1:
        count -= 1
        clock.schedule(countdown, 1)
    else:
        show_countdown = False
        display_moves()

def generate_moves():
    global move_list, display_list, dance_length
    global count, show_countdown, say_dance
    global p1_current_move, p2_current_move, p1_round_failed, p2_round_failed, first_round
    
    count = 4
    move_list = []
    display_list = []
    say_dance = False
    
    for _ in range(dance_length):
        rand_move = randint(0, 3)
        move_list.append(rand_move)
        display_list.append(rand_move)
        
    # Only show the countdown on the very first round
    if first_round:
        show_countdown = True
        countdown()
        first_round = False
    else:
        show_countdown = False
        display_moves()

    p1_current_move = 0
    p2_current_move = 0
    p1_round_failed = False
    p2_round_failed = False

def check_round_end():
    global game_over, p1_lives, p2_lives, p1_active, p2_active, winner_name
    global dance_length, p1_current_move, p2_current_move, round_in_progress, say_dance, p1_round_failed, p2_round_failed

    p1_complete = (p1_current_move >= dance_length)
    p2_complete = (p2_current_move >= dance_length)
    
    # Check if a player failed or completed the round, and if so, finalize their state.
    if (p1_complete and p1_active) or (p1_round_failed and p1_active):
        if not p1_complete:
            p1_lives -= 1
            if p1_lives > 0:
                sounds.wrong.play()
            p1_active = p1_lives > 0
        p1_current_move = dance_length # Mark player 1 as finished with the round.

    if (p2_complete and p2_active) or (p2_round_failed and p2_active):
        if not p2_complete:
            p2_lives -= 1
            if p2_lives > 0:
                sounds.wrong.play()
            p2_active = p2_lives > 0
        p2_current_move = dance_length # Mark player 2 as finished with the round.

    # Check if both players have finished the round (either by completing it or failing).
    if (p1_current_move >= dance_length or not p1_active) and (p2_current_move >= dance_length or not p2_active):
        if not p1_active and not p2_active:
            game_over = True
            music.stop()
            winner_name = "It's a Tie!"
            sounds.win.play()
        elif not p1_active:
            game_over = True
            music.stop()
            winner_name = f"Winner is {p2_name}!"
            sounds.win.play()
        elif not p2_active:
            game_over = True
            music.stop()
            winner_name = f"Winner is {p1_name}!"
            sounds.win.play()
        else:
            dance_length += 1
            generate_moves()
            say_dance = False
            round_in_progress = False

def on_key_down(key):
    global game_over, p1_current_move, p2_current_move, round_in_progress, p1_round_failed, p2_round_failed
    
    if game_over:
        if key == keys.SPACE:
            reset_game()
        return

    if not round_in_progress:
        return
        
    # Swapped Key maps for both players
    player1_keys = {keys.W: 0, keys.D: 1, keys.S: 2, keys.A: 3}
    player2_keys = {keys.UP: 0, keys.RIGHT: 1, keys.DOWN: 2, keys.LEFT: 3}

    # Player 1's input
    if p1_active and not p1_round_failed and key in player1_keys:
        if p1_current_move < len(move_list):
            expected_move = move_list[p1_current_move]
            if player1_keys[key] == expected_move:
                sounds.correct.play()
                update_dancer(1, expected_move)
                p1_current_move += 1
            else:
                sounds.wrong.play()
                p1_round_failed = True
            check_round_end()

    # Player 2's input
    if p2_active and not p2_round_failed and key in player2_keys:
        if p2_current_move < len(move_list):
            expected_move = move_list[p2_current_move]
            if player2_keys[key] == expected_move:
                sounds.correct.play()
                update_dancer(2, expected_move)
                p2_current_move += 1
            else:
                sounds.wrong.play()
                p2_round_failed = True
            check_round_end()

def update():
    pass

# Starts the game loop
get_player_names_gui()        
generate_moves()
music.play("vanishing-horizon")
pgzrun.go()