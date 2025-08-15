# Dance Challenge Game
# Created by Jesse Toscano and Anahi Carrasco
# 2025
# This game is a fun dance challenge where two players compete by mimicking dance moves.
# -*- coding: utf-8 -*-
import os
# Get the absolute path to the sounds folder
sounds_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sounds')
import pgzrun
import pygame
import pgzero
from pgzero.builtins import Actor
from random import randint, choice
import time
from sys import exit
import os
import math

# Screen dimensions and center coordinates
WIDTH = 1000  # Increased width for split-screen
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

# Game state and variables initialization
move_list = []
display_list = []
dance_length = 2

# --- Background GIF variables ---
background_frames = []
current_frame = 0
frame_rate = 0.05 # Adjust this value to change the animation speed
last_frame_time = time.time()

# --- Player 1 State Variables ---
p1_current_move = 0
p1_lives = 3
p1_round_failed = False
p1_active = True
p1_name = ""
p1_score = 0
p1_combo = 0
p1_combo_text = ""

# --- Player 2 State Variables ---
p2_current_move = 0
p2_lives = 3
p2_round_failed = False
p2_active = True
p2_name = ""
p2_score = 0
p2_combo = 0
p2_combo_text = ""

# --- Shared Game State ---
count = 4
say_dance = False
show_countdown = True
game_over = False
winner_name = ""
round_in_progress = False
first_round = True  # New variable to control the initial countdown timer
song_ended = False

# NEW: Song selection variables
selected_song_file = ""
song_name = ""
song_artist = ""
song_playing = False
song_duration_ms = 0
song_start_time = 0

# NEW: Modern UI visual effects
bg_time = 0
particles = []
score_particles = []
combo_multiplier = 1
last_move_perfect = False
beat_pulse = 0
color_shift = 0

# NEW: Modern color palette - sleek and contemporary
modern_colors = [
    (255, 51, 153), # Electric Pink
    (0, 255, 127), # Spring Green
    (255, 140, 0), # Dark Orange
    (138, 43, 226), # Blue Violet
    (30, 144, 255), # Dodger Blue
    (255, 215, 0), # Gold
    (255, 69, 0), # Red Orange
    (147, 112, 219), # Medium Purple
    (0, 206, 209), # Dark Turquoise
    (255, 20, 147), # Deep Pink
]
current_theme_color = choice(modern_colors)

# NEW: Available songs list - updated with your requested songs
AVAILABLE_SONGS = [
    {
        'title': "Stayin’ Alive",
        'artist': "Bee Gees",
        'file': "stayin_alive",
        'difficulty': "⭐⭐",
        'bpm': 104
    },
    {
        'title': "Cruel Summer (Again)",
        'artist': "Bob Sinclair",
        'file': "cruel_summer",
        'difficulty': "⭐⭐⭐",
        'bpm': 120
    },
    {
        'title': "D.A.N.C.E.",
        'artist': "Peggy Gou",
        'file': "dance",
        'difficulty': "⭐⭐⭐",
        'bpm': 120
    },
    {
        'title': "Espresso",
        'artist': "Sabrina Carpenter",
        'file': "espresso",
        'difficulty': "⭐",
        'bpm': 105
    },
    {
        'title': "The Less I Know The Better",
        'artist': "Tame Impala",
        'file': "better",
        'difficulty': "⭐⭐",
        'bpm': 117
    }
]


# --- Actors for Player 1 (Left Side) ---
p1_dancer = Actor("p1_dancer")
p1_up = Actor("up")
p1_right = Actor("right")
p1_down = Actor("down")
p1_left = Actor("left")

# --- Actors for Player 2 (Right Side) ---
p2_dancer = Actor("p2_dancer")
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


# NEW: Helper function to clamp RGB values
def clamp_color(value):
    return max(0, min(255, int(value)))

# NEW: Enhanced Modern Particle classes
class ModernParticle:
    def __init__(self, x=None, y=None):
        self.x = x if x else randint(0, WIDTH)
        self.y = y if y else randint(0, HEIGHT)
        self.speed_x = randint(-3, 3)
        self.speed_y = randint(-4, -1)
        self.size = randint(2, 6)
        self.color = choice(modern_colors)
        self.alpha = randint(150, 255)
        self.life = randint(80, 150)
        self.max_life = self.life
        self.glow = randint(3, 8)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.alpha = int((self.life / self.max_life) * 255)
        self.glow = max(1, self.glow - 0.1)
        
        if self.life <= 0 or self.y < -10:
            self.reset()
    
    def reset(self):
        self.x = randint(0, WIDTH)
        self.y = HEIGHT + 10
        self.speed_x = randint(-3, 3)
        self.speed_y = randint(-4, -1)
        self.color = choice(modern_colors)
        self.life = randint(80, 150)
        self.max_life = self.life
        self.glow = randint(3, 8)

class ScoreParticle:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.life = 80
        self.color = choice(modern_colors)
        self.size = 52
        self.glow = 10
        
    def update(self):
        self.y -= 1.5
        self.life -= 1
        self.size = max(24, self.size - 0.4)
        self.glow = max(0, self.glow - 0.1)

# Initialize particles
for _ in range(60):
    particles.append(ModernParticle())

# NEW: Create modern score effect function
def create_score_effect(player_id, x, y, points):
    """Create modern score effects"""
    global score_particles
    
    if points >= 4:
        text = "PERFECT!"
    elif points >= 3:
        text = "GREAT!"
    elif points >= 2:
        text = "GOOD!"
    else:
        text = "OK"
    
    score_particles.append(ScoreParticle(x, y, text))
    
    # Add explosion particles
    for _ in range(12):
        particles.append(ModernParticle(x + randint(-40, 40), y + randint(-40, 40)))

def load_background_frames():
    global background_frames
    
    script_dir = os.getcwd()
    frame_dir = os.path.join(script_dir, "space_galaxy_frames")
    
    print(f"Checking for folder at: {frame_dir}")

    if os.path.exists(frame_dir):
        print(f"Folder found. Contents: {os.listdir(frame_dir)}")
        
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith(".png")])
        
        if not frame_files:
            print("Warning: 'space_galaxy_frames' folder is empty or does not contain .png files.")
        else:
            print(f"Found {len(frame_files)} frames. Loading...")
            for file in frame_files:
                try:
                    original_image = pygame.image.load(os.path.join(frame_dir, file))
                    scaled_image = pygame.transform.scale(original_image, (WIDTH, HEIGHT))
                    background_frames.append(scaled_image)
                except pygame.error as e:
                    print(f"Error loading frame '{file}': {e}")
                    
            if not background_frames:
                print("Warning: No frames were successfully loaded. Check file integrity.")
    else:
        print("Warning: 'space_galaxy_frames' folder not found.")

# Resets all game variables for a new game
def reset_game():
    global p1_current_move, p1_lives, p1_round_failed, p1_active, p1_score, p1_combo
    global p2_current_move, p2_lives, p2_round_failed, p2_active, p2_score, p2_combo
    global count, dance_length, say_dance, show_countdown, game_over, winner_name
    global round_in_progress, first_round, song_ended, selected_song_file, song_start_time

    p1_current_move = 0
    p1_lives = 3
    p1_round_failed = False
    p1_active = True
    p1_score = 0
    p1_combo = 0

    p2_current_move = 0
    p2_lives = 3
    p2_round_failed = False
    p2_active = True
    p2_score = 0
    p2_combo = 0

    count = 4
    dance_length = 2
    say_dance = False
    show_countdown = True
    game_over = False
    winner_name = ""
    round_in_progress = False
    first_round = True
    song_ended = False

    # Get the song selection and store it in the global variable
    selected_song_file = get_song_selection()
    
    # Play the selected song using the pgzero music module
    if selected_song_file:
        music.play(os.path.join(sounds_path, f"{selected_song_file}.ogg"))
        music.set_volume(0.8)
        song_start_time = time.time() * 1000  # Set the new song start time

    generate_moves()

def draw():
    global game_over, say_dance, count, show_countdown, winner_name
    global p1_lives, p2_lives, p1_active, p2_active, p1_score, p2_score, p1_combo, p2_combo, p1_combo_text, p2_combo_text
    
    if not game_over:
        screen.clear()
        # Draw the current GIF frame as the background
        if background_frames:
            screen.blit(background_frames[current_frame], (0, 0))
        else:
            screen.blit("stage", (0, 0))
        
        # Draw floating particles from friend's code
        for p in particles:
            screen.draw.filled_circle((p.x, p.y), p.size, p.color)

        # Player 1 (Left Side) - Character on the left, score on the left
        p1_dancer.draw()
        p1_up.draw()
        p1_right.draw()
        p1_down.draw()
        p1_left.draw()
        
        # New code to draw hearts for Player 1
        x_start_p1 = 100
        for i in range(p1_lives):
            heart = Actor("heart")
            heart.pos = x_start_p1 + (i * 40), 40
            heart.draw()
        if not p1_active:
            screen.draw.text(f"{p1_name} OUT!", color="yellow", topleft=(10, 40), fontname="digital", fontsize=30)
            
        # Player 2 (Right Side) - Character on the right, score on the right
        p2_dancer.draw()
        p2_up.draw()
        p2_right.draw()
        p2_down.draw()
        p2_left.draw()
        
        # New code to draw hearts for Player 2
        x_start_p2 = WIDTH - 100
        for i in range(p2_lives):
            heart = Actor("heart")
            heart.pos = x_start_p2 - (i * 40), 40
            heart.draw()
        if not p2_active:
            screen.draw.text(f"{p2_name} OUT!", color="white", topright=(WIDTH - 10, 40), fontname="digital", fontsize=30)

        # --- Shared Elements ---
        if say_dance:
            screen.draw.text("Dance!", color="black", topleft=(CENTER_X - 55, 150), fontsize=50)
        if show_countdown:
            screen.draw.text(str(count), color="black", topleft=(CENTER_X - 8, 150), fontsize=50)
            
        # NEW: Draw scores and combos
        screen.draw.text(f"{p1_name}: {p1_score}", color="white", topleft=(10, 80), fontsize=30, fontname="digital")
        screen.draw.text(f"Combo: {p1_combo}x", color="yellow", topleft=(10, 110), fontsize=25, fontname="digital")
        
        screen.draw.text(f"{p2_name}: {p2_score}", color="white", topright=(WIDTH - 10, 80), fontsize=30, fontname="digital")
        screen.draw.text(f"Combo: {p2_combo}x", color="yellow", topright=(WIDTH - 10, 110), fontsize=25, fontname="digital")

        # Draw score particles
        for p in score_particles:
            text_surface = pygame.font.Font(None, int(p.size)).render(p.text, True, p.color)
            text_rect = text_surface.get_rect(center=(p.x, p.y))
            screen.blit(text_surface, text_rect)
    else:
        # NEW: Call the new draw_game_over_screen() function here
        draw_game_over_screen()
    
    return

def reset_dancer():
    p1_dancer.image = "p1_dancer"
    p1_up.image = "up"
    p1_right.image = "right"
    p1_down.image = "down"
    p1_left.image = "left"
    p2_dancer.image = "p2_dancer"
    p2_up.image = "up"
    p2_right.image = "right"
    p2_down.image = "down"
    p2_left.image = "left"

def update_dancer(player, move):
    if player == 1:
        if move == 0:
            p1_up.image = "up-lit"
            p1_dancer.image = "p1_dancer_up"
        elif move == 1:
            p1_right.image = "right-lit"
            p1_dancer.image = "p1_dancer_right"
        elif move == 2:
            p1_down.image = "down-lit"
            p1_dancer.image = "p1_dancer_down"
        else:
            p1_left.image = "left-lit"
            p1_dancer.image = "p1_dancer_left"
    else:
        if move == 0:
            p2_up.image = "up-lit"
            p2_dancer.image = "p2_dancer_up"
        elif move == 1:
            p2_right.image = "right-lit"
            p2_dancer.image = "p2_dancer_right"
        elif move == 2:
            p2_down.image = "down-lit"
            p2_dancer.image = "p2_dancer_down"
        else:
            p2_left.image = "left-lit"
            p2_dancer.image = "p2_dancer_left"
    
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
    global p1_combo, p2_combo

    p1_complete = (p1_current_move >= dance_length)
    p2_complete = (p2_current_move >= dance_length)
    
    # Check if a player failed or completed the round, and if so, finalize their state.
    if (p1_complete and p1_active) or (p1_round_failed and p1_active):
        if not p1_complete:
            p1_lives -= 1
            p1_combo = 0 # Reset combo on failure
            if p1_lives > 0:
                sounds.wrong.play()
            p1_active = p1_lives > 0
        p1_current_move = dance_length # Mark player 1 as finished with the round.

    if (p2_complete and p2_active) or (p2_round_failed and p2_active):
        if not p2_complete:
            p2_lives -= 1
            p2_combo = 0 # Reset combo on failure
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

# NEW: Song Selection GUI with scrolling support
def get_song_selection():
    global current_theme_color, song_name, song_artist, song_duration_ms

    # Initialize pygame for the GUI
    pygame.init()
    window_width = 800
    window_height = 600
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("🎵 SELECT YOUR SONG 🎵")
    
    selected_index = 0
    done = False
    anim_time = 0
    mouse_hover_index = -1
    
    # Scrolling variables
    scroll_offset = 0
    max_visible_items = 5
    item_height = 70
    
    # Initialize pygame mixer for song previews
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.music.set_volume(0.4)
    
    preview_start_time = 30.0
    preview_duration = 10000
    hover_delay = 500
    hover_timer = 0
    pending_preview_index = -1
    
    clock = pygame.time.Clock()
    
    while not done:
        dt = clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        
        # Calculate scroll boundaries
        total_songs = len(AVAILABLE_SONGS)
        max_scroll = max(0, total_songs - max_visible_items)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(AVAILABLE_SONGS)
                    current_theme_color = choice(modern_colors)
                    if selected_index < scroll_offset:
                        scroll_offset = selected_index
                    elif selected_index >= scroll_offset + max_visible_items:
                        scroll_offset = selected_index - max_visible_items + 1
                    pygame.mixer.music.stop()
                    
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(AVAILABLE_SONGS)
                    current_theme_color = choice(modern_colors)
                    if selected_index >= scroll_offset + max_visible_items:
                        scroll_offset = min(max_scroll, selected_index - max_visible_items + 1)
                    elif selected_index < scroll_offset:
                        scroll_offset = selected_index
                    pygame.mixer.music.stop()
                    
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    selected_song_info = AVAILABLE_SONGS[selected_index]
                    selected_song_file = selected_song_info["file"]
                    song_name = selected_song_info["title"]
                    song_artist = selected_song_info["artist"]
                    
                    try:
                        music_file_path = f"sounds/{selected_song_file}.ogg"
                        music_sound = pygame.mixer.Sound(music_file_path)
                        song_duration_ms = music_sound.get_length() * 1000
                    except (pygame.error, FileNotFoundError) as e:
                        print(f"❌ Could not load song '{selected_song_file}': {e}")
                        print(f"Make sure the file exists at: {music_file_path}")
                        song_duration_ms = 60000 # Default to 1 minute if not found
                    
                    pygame.mixer.music.stop()
                    done = True
                    
                elif event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    list_start_y = 140
                    for i in range(scroll_offset, min(scroll_offset + max_visible_items, len(AVAILABLE_SONGS))):
                        display_index = i - scroll_offset
                        y_pos = list_start_y + display_index * item_height
                        song_rect = pygame.Rect(60, y_pos - 5, window_width - 120, item_height - 10)
                        if song_rect.collidepoint(mouse_pos):
                            selected_song_info = AVAILABLE_SONGS[i]
                            selected_song_file = selected_song_info["file"]
                            song_name = selected_song_info["name"]
                            song_artist = selected_song_info["artist"]
                            
                            try:
                                music_file_path = f"sounds/{selected_song_file}.ogg"
                                music_sound = pygame.mixer.Sound(music_file_path)
                                song_duration_ms = music_sound.get_length() * 1000
                            except (pygame.error, FileNotFoundError) as e:
                                print(f"❌ Could not load song '{selected_song_file}': {e}")
                                print(f"Make sure the file exists at: {music_file_path}")
                                song_duration_ms = 60000
                                
                            pygame.mixer.music.stop()
                            done = True
                            break
                
                elif event.button == 4:
                    scroll_offset = max(0, scroll_offset - 1)
                elif event.button == 5:
                    scroll_offset = min(max_scroll, scroll_offset + 1)
        
        # Drawing code (from friend's code)
        window.fill((0, 0, 0)) # Clear the window before drawing

        # Modern gradient background
        for y in range(window_height):
            progress = y / window_height
            r = clamp_color(20 + 60 * math.sin(anim_time * 0.008 + progress * 2))
            g = clamp_color(15 + 45 * math.cos(anim_time * 0.01 + progress * 1.5))
            b = clamp_color(40 + 80 * math.sin(anim_time * 0.012 + progress * 3))
            pygame.draw.line(window, (r, g, b), (0, y), (window_width, y))
        
        # Modern floating elements
        for i in range(25):
            x = (anim_time * 1.2 + i * 32) % (window_width + 80)
            y = 60 + i * 20 + int(15 * math.sin(anim_time * 0.015 + i * 0.3))
            
            if i % 4 == 0:
                size = 4 + int(3 * math.sin(anim_time * 0.02 + i))
                color = modern_colors[i % len(modern_colors)]
                for glow in range(3):
                    glow_size = size + glow * 2
                    pygame.draw.circle(window, color, (int(x), y), glow_size)
            else:
                color = modern_colors[i % len(modern_colors)]
                pygame.draw.circle(window, color, (int(x), y), 3)

        # Modern title
        title_font = pygame.font.Font(None, 72)
        title_text = "SELECT YOUR SONG"
        title_bg = pygame.Rect(50, 20, window_width - 100, 80)
        title_surface = pygame.Surface((title_bg.width, title_bg.height))
        title_surface.set_alpha(120)
        title_surface.fill((30, 30, 50))
        window.blit(title_surface, title_bg)
        pygame.draw.rect(window, current_theme_color, title_bg, 3, border_radius=20)
        
        for i, char in enumerate(title_text):
            if char != " ":
                offset = int(8 * math.sin(anim_time * 0.1 + i * 0.3))
                color = modern_colors[i % len(modern_colors)]
                char_surface = title_font.render(char, True, color)
                char_x = 90 + i * 28
                window.blit(char_surface, (char_x, 45 + offset))

        # Song list with scrolling support
        list_start_y = 140
        for i in range(scroll_offset, min(scroll_offset + max_visible_items, len(AVAILABLE_SONGS))):
            song = AVAILABLE_SONGS[i]
            display_index = i - scroll_offset
            y_pos = list_start_y + display_index * item_height
            
            song_rect = pygame.Rect(60, y_pos - 5, window_width - 120, item_height - 10)
            is_selected = (i == selected_index)
            
            if is_selected:
                glow_intensity = int(100 + 50 * math.sin(anim_time * 0.15))
                glow_color = current_theme_color
                for glow in range(5):
                    glow_rect = pygame.Rect(song_rect.x - glow * 3, song_rect.y - glow * 2,
                                             song_rect.width + glow * 6, song_rect.height + glow * 4)
                    glow_surface = pygame.Surface((glow_rect.width, glow_rect.height))
                    glow_surface.set_alpha(max(20, glow_intensity - glow * 20))
                    glow_surface.fill(glow_color)
                    window.blit(glow_surface, glow_rect)

                selection_surface = pygame.Surface((song_rect.width, song_rect.height))
                selection_surface.set_alpha(150)
                selection_surface.fill((40, 40, 70))
                window.blit(selection_surface, song_rect)
                pygame.draw.rect(window, glow_color, song_rect, 3, border_radius=20)
                
            name_font = pygame.font.Font(None, 38)
            artist_font = pygame.font.Font(None, 26)
            difficulty_font = pygame.font.Font(None, 30)
            
            name_color = (255, 255, 255) if is_selected else (200, 200, 220)
            artist_color = (180, 180, 255) if is_selected else (140, 140, 160)
            difficulty_color = current_theme_color if is_selected else (180, 180, 100)
            
            name_surface = name_font.render(f"♪ {song['title']}", True, name_color)
            window.blit(name_surface, (80, y_pos))
            
            artist_surface = artist_font.render(f"by {song['artist']}", True, artist_color)
            window.blit(artist_surface, (80, y_pos + 30))
            
            difficulty_surface = difficulty_font.render(song['difficulty'], True, difficulty_color)
            window.blit(difficulty_surface, (window_width - 180, y_pos + 15))
        
        # Instructions
        instruction_panel = pygame.Rect(50, window_height - 80, window_width - 100, 60)
        panel_surface = pygame.Surface((instruction_panel.width, instruction_panel.height))
        panel_surface.set_alpha(100)
        panel_surface.fill((20, 20, 40))
        window.blit(panel_surface, instruction_panel)
        pygame.draw.rect(window, current_theme_color, instruction_panel, 2, border_radius=15)
        
        instruction_font = pygame.font.Font(None, 24)
        instructions = [
            "Use ↑ and ↓ to navigate and ENTER to select.",
            "Press ESC to exit."
        ]
        
        for i, instruction in enumerate(instructions):
            text = instruction_font.render(instruction, True, (220, 220, 255))
            window.blit(text, (70, window_height - 70 + i * 25))
            
        anim_time += 1
        pygame.display.flip()
    
    return selected_song_file

# NEW: Game Over Menu
import pygame

def draw_game_over_screen():
    global current_theme_color, winner_name, anim_time, selected_option
    
    # Game Over Title
    title_font = pygame.font.Font(None, 88)
    title_text = "GAME OVER"
    title_bg = pygame.Rect(100, 50, WIDTH - 200, 100)
    title_surface = pygame.Surface((title_bg.width, title_bg.height))
    title_surface.set_alpha(120)
    title_surface.fill((30, 30, 50))
    screen.blit(title_surface, title_bg)
    pygame.draw.rect(screen, current_theme_color, title_bg, 4, border_radius=25)
    
    # Final Scores Display
    scores_bg = pygame.Rect(150, 180, WIDTH - 300, 140)
    scores_surface = pygame.Surface((scores_bg.width, scores_bg.height))
    scores_surface.set_alpha(130)
    scores_surface.fill((25, 25, 45))
    screen.blit(scores_surface, scores_bg)
    pygame.draw.rect(screen, current_theme_color, scores_bg, 3, border_radius=20)
    
    # Display final scores
    score_font = pygame.font.Font(None, 36)
    winner_font = pygame.font.Font(None, 42)
    
    player1_text = score_font.render(f"🕺 {p1_name}: {p1_score}", True, (255, 100, 150))
    player2_text = score_font.render(f"💃 {p2_name}: {p2_score}", True, (100, 150, 255))
    
    screen.blit(player1_text, (170, 200))
    screen.blit(player2_text, (170, 240))
    
    # Winner announcement
    if p1_score > p2_score:
        winner_text = f"🏆 {p1_name} WINS!"
        winner_color = (255, 215, 0)
    elif p2_score > p1_score:
        winner_text = f"🏆 {p2_name} WINS!"
        winner_color = (255, 215, 0)
    else:
        winner_text = "🤝 IT'S A TIE!"
        winner_color = (100, 255, 100)
    
    winner_pulse = int(42 + 8 * math.sin(anim_time * 0.2))
    winner_surface = pygame.font.Font(None, winner_pulse).render(winner_text, True, winner_color)
    winner_rect = winner_surface.get_rect(center=(WIDTH // 2, 280))
    screen.blit(winner_surface, winner_rect)
    
    # Option buttons
    button_font = pygame.font.Font(None, 36)
    
    # Play Again button
    play_again_bg = pygame.Rect(150, 350, 200, 60)
    if selected_option == 0:
        glow_intensity = int(120 + 40 * math.sin(anim_time * 0.2))
        for glow in range(4):
            glow_rect = pygame.Rect(play_again_bg.x - glow * 3, play_again_bg.y - glow * 2,
                                     play_again_bg.width + glow * 6, play_again_bg.height + glow * 4)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height))
            glow_surface.set_alpha(max(30, glow_intensity - glow * 25))
            glow_surface.fill((100, 255, 100))
            screen.blit(glow_surface, glow_rect)
        
        button_surface = pygame.Surface((play_again_bg.width, play_again_bg.height))
        button_surface.set_alpha(150)
        button_surface.fill((40, 70, 40))
        screen.blit(button_surface, play_again_bg)
        pygame.draw.rect(screen, (100, 255, 100), play_again_bg, 3, border_radius=20)
        button_color = (255, 255, 255)
    else:
        button_surface = pygame.Surface((play_again_bg.width, play_again_bg.height))
        button_surface.set_alpha(100)
        button_surface.fill((40, 40, 60))
        screen.blit(button_surface, play_again_bg)
        pygame.draw.rect(screen, (120, 120, 140), play_again_bg, 2, border_radius=20)
        button_color = (200, 200, 220)
    
    play_text = button_font.render("🔄 PLAY AGAIN", True, button_color)
    play_rect = play_text.get_rect(center=(play_again_bg.centerx, play_again_bg.centery))
    screen.blit(play_text, play_rect)
    
    # Quit button
    quit_bg = pygame.Rect(450, 350, 200, 60)
    if selected_option == 1:
        glow_intensity = int(120 + 40 * math.sin(anim_time * 0.2))
        for glow in range(4):
            glow_rect = pygame.Rect(quit_bg.x - glow * 3, quit_bg.y - glow * 2,
                                     quit_bg.width + glow * 6, quit_bg.height + glow * 4)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height))
            glow_surface.set_alpha(max(30, glow_intensity - glow * 25))
            glow_surface.fill((255, 100, 100))
            screen.blit(glow_surface, glow_rect)
        
        button_surface = pygame.Surface((quit_bg.width, quit_bg.height))
        button_surface.set_alpha(150)
        button_surface.fill((70, 40, 40))
        screen.blit(button_surface, quit_bg)
        pygame.draw.rect(screen, (255, 100, 100), quit_bg, 3, border_radius=20)
        button_color = (255, 255, 255)
    else:
        button_surface = pygame.Surface((quit_bg.width, quit_bg.height))
        button_surface.set_alpha(100)
        button_surface.fill((40, 40, 60))
        screen.blit(button_surface, quit_bg)
        pygame.draw.rect(screen, (120, 120, 140), quit_bg, 2, border_radius=20)
        button_color = (200, 200, 220)
        
    quit_text = button_font.render("❌ QUIT", True, button_color)
    quit_rect = quit_text.get_rect(center=(quit_bg.centerx, quit_bg.centery))
    screen.blit(quit_text, quit_rect)
    
def on_key_down(key):
    global game_over, p1_current_move, p2_current_move, round_in_progress, p1_round_failed, p2_round_failed
    global p1_score, p2_score, p1_combo, p2_combo, selected_option

    if game_over and song_ended:
        if key == keys.UP or key == keys.LEFT:
            selected_option = 0
        elif key == keys.DOWN or key == keys.RIGHT:
            selected_option = 1
        elif key == keys.RETURN or key == keys.SPACE:
            if selected_option == 0:
                reset_game()
            elif selected_option == 1:
                exit()
        return

    if not round_in_progress:
        return
        
    player1_keys = {keys.W: 0, keys.D: 1, keys.S: 2, keys.A: 3}
    player2_keys = {keys.UP: 0, keys.RIGHT: 1, keys.DOWN: 2, keys.LEFT: 3}

    # Player 1's input
    if p1_active and not p1_round_failed and key in player1_keys:
        if p1_current_move < len(move_list):
            expected_move = move_list[p1_current_move]
            if player1_keys[key] == expected_move:
                sounds.correct.play()
                p1_combo += 1
                p1_score += p1_combo * 5 # Scoring system
                create_score_effect(1, CENTER_X - 250, CENTER_Y - 100, 4) # Add score effect
                update_dancer(1, expected_move)
                p1_current_move += 1
            else:
                sounds.wrong.play()
                p1_round_failed = True
                p1_combo = 0 # Reset combo
            check_round_end()

    # Player 2's input
    if p2_active and not p2_round_failed and key in player2_keys:
        if p2_current_move < len(move_list):
            expected_move = move_list[p2_current_move]
            if player2_keys[key] == expected_move:
                sounds.correct.play()
                p2_combo += 1
                p2_score += p2_combo * 5
                create_score_effect(2, CENTER_X + 250, CENTER_Y - 100, 4)
                update_dancer(2, expected_move)
                p2_current_move += 1
            else:
                sounds.wrong.play()
                p2_round_failed = True
                p2_combo = 0 # Reset combo
            check_round_end()

def update():
    global current_frame, last_frame_time, game_over, song_ended, winner_name
    global song_duration_ms, song_start_time

    # Update the GIF background frame
    if background_frames:
        if time.time() - last_frame_time > frame_rate:
            current_frame = (current_frame + 1) % len(background_frames)
            last_frame_time = time.time()
            
    # Update particles
    for p in particles:
        p.update()
    
    # Update score particles
    for p in score_particles:
        p.update()
    score_particles[:] = [p for p in score_particles if p.life > 0] # Remove dead particles

    # Check if the song has ended
    if not game_over and time.time() * 1000 - song_start_time > song_duration_ms:
        game_over = True
        song_ended = True
        music.stop()
        sounds.win.play()
        if p1_score > p2_score:
            winner_name = f"Winner is {p1_name}!"
        elif p2_score > p1_score:
            winner_name = f"Winner is {p2_name}!"
        else:
            winner_name = "It's a Tie!"
        
    # If the game is over, show the game over menu and handle its result
    if game_over and song_ended:
        result = show_game_over_menu()
        if result == "play_again":
            reset_game()
        elif result == "quit":
            exit()
                
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

# --- Initial Setup ---
load_background_frames()
get_player_names_gui()
reset_game()
pgzrun.go()