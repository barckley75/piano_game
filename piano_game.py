import pygame
import pygame.midi
import sys
import random

# Initialize pygame and pygame.midi
pygame.init()
pygame.midi.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Learn Notes with Falling Squares")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
DEEP_PINK = (255, 20, 147)
INDIGO = (75, 0, 130)

# MIDI Notes to game notes mapping
MIDI_TO_GAME = {
    60: "C4", 61: "C#4", 62: "D4", 63: "D#4", 64: "E4",
    65: "F4", 66: "F#4", 67: "G4", 68: "G#4", 69: "A4",
    70: "A#4", 71: "B4"
}

# Note to color mapping
NOTE_TO_COLOR = {
    "C4": RED, "C#4": DARK_GRAY,
    "D4": GREEN, "D#4": GRAY,
    "E4": BLUE,
    "F4": YELLOW, "F#4": DEEP_PINK,
    "G4": MAGENTA, "G#4": INDIGO,
    "A4": CYAN, "A#4": ORANGE,
    "B4": BLACK
}

# Computer keyboard mapping
KEYBOARD_TO_GAME = {
    pygame.K_s: "C4", pygame.K_d: "D4", pygame.K_f: "E4",
    pygame.K_g: "F4", pygame.K_h: "G4", pygame.K_j: "A4",
    pygame.K_k: "B4", pygame.K_l: "C5",  # Tasti bianchi
    pygame.K_e: "C#4", pygame.K_r: "D#4", pygame.K_y: "F#4",
    pygame.K_u: "G#4", pygame.K_i: "A#4"  # Tasti neri
}

# Note to letter (for display)
NOTE_TO_LETTER = {note: note.replace('#', '♯') for note in NOTE_TO_COLOR.keys()}

# Square attributes
SQUARE_SIZE = 50
INITIAL_SPEED = 5
speed = INITIAL_SPEED

# Slider attributes
SLIDER_X = 100
SLIDER_Y = HEIGHT - 50
SLIDER_WIDTH = 300
SLIDER_HEIGHT = 10
SLIDER_HANDLE_WIDTH = 20
slider_handle_x = SLIDER_X + (speed - 1) * (SLIDER_WIDTH - SLIDER_HANDLE_WIDTH) // 14
dragging_slider = False

# Piano attributes
PIANO_WIDTH = WIDTH
PIANO_HEIGHT = 120
PIANO_Y = HEIGHT - PIANO_HEIGHT
NUM_WHITE_KEYS = 7
WHITE_KEY_WIDTH = PIANO_WIDTH // NUM_WHITE_KEYS
BLACK_KEY_WIDTH = WHITE_KEY_WIDTH // 2
KEY_HEIGHT = PIANO_HEIGHT

# Sound manager class
class SoundManager:
    def __init__(self):
        self.notes = {}
        for note in NOTE_TO_COLOR.keys():
            self.notes[note] = pygame.mixer.Sound(f"sounds/{note}.wav")
        self.current_channel = None

    def play(self, note):
        if self.current_channel is not None:
            self.current_channel.stop()
        self.current_channel = self.notes[note].play()

sound_manager = SoundManager()

# Game mode
is_easy_mode = False

def toggle_mode():
    global is_easy_mode, button_text
    is_easy_mode = not is_easy_mode
    button_text = "Mode: Easy" if is_easy_mode else "Mode: Difficult"

# Initialize button properties
button_width, button_height = 140, 40
button_position = (WIDTH - button_width - 20, 20)  # Top-right corner
button_color = GRAY
button_text = "Mode: Difficult"  # Default mode text

def draw_button():
    global button_color, button_text
    pygame.draw.rect(screen, button_color, (*button_position, button_width, button_height))
    text_surface = font.render(button_text, True, WHITE)
    screen.blit(text_surface, (button_position[0] + 5, button_position[1] + 5))

class Square:
    def __init__(self, note):
        self.note = note
        self.color = NOTE_TO_COLOR[note]
        self.letter = NOTE_TO_LETTER[note]
        self.font = pygame.font.Font(None, 36)
        self.reset_position()

    def reset_position(self):
        if is_easy_mode and '#' in self.note:
            self.rect = pygame.Rect(-SQUARE_SIZE, -SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            return

        if self.note in white_positions:
            key_x = white_positions[self.note]
            self.x = key_x + (WHITE_KEY_WIDTH - SQUARE_SIZE) // 2
        elif self.note in black_positions:
            key_x = black_positions[self.note]
            self.x = key_x + (BLACK_KEY_WIDTH - SQUARE_SIZE) // 2
        else:
            self.x = random.randint(0, WIDTH - SQUARE_SIZE)

        self.rect = pygame.Rect(self.x, -SQUARE_SIZE - random.randint(0, 600), SQUARE_SIZE, SQUARE_SIZE)
        
    def update(self):
        self.rect.y += speed

    def draw(self):
        if not (is_easy_mode and '#' in self.note):
            pygame.draw.rect(screen, self.color, self.rect)
            letter_text = self.font.render(self.letter, True, WHITE)
            text_rect = letter_text.get_rect(center=self.rect.center)
            screen.blit(letter_text, text_rect)

    def play_note(self):
        sound_manager.play(self.note)

# Note positions for squares
white_positions = {note: i * WHITE_KEY_WIDTH for i, note in enumerate(["C4", "D4", "E4", "F4", "G4", "A4", "B4"])}
black_positions = {
    "C#4": white_positions["C4"] + WHITE_KEY_WIDTH - BLACK_KEY_WIDTH // 2,
    "D#4": white_positions["D4"] + WHITE_KEY_WIDTH - BLACK_KEY_WIDTH // 2,
    "F#4": white_positions["F4"] + WHITE_KEY_WIDTH - BLACK_KEY_WIDTH // 2,
    "G#4": white_positions["G4"] + WHITE_KEY_WIDTH - BLACK_KEY_WIDTH // 2,
    "A#4": white_positions["A4"] + WHITE_KEY_WIDTH - BLACK_KEY_WIDTH // 2
}

# Create squares for each note with random positions
squares = [Square(note) for note in NOTE_TO_COLOR.keys()]

# Score system
score = 0
font = pygame.font.Font(None, 36)

# Functions to draw UI elements
def draw_slider():
    global slider_handle_x
    pygame.draw.rect(screen, GRAY, (SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT))
    pygame.draw.rect(screen, BLACK, (slider_handle_x, SLIDER_Y - 5, SLIDER_HANDLE_WIDTH, SLIDER_HEIGHT + 10))

def process_slider():
    global slider_handle_x, speed
    slider_value = (slider_handle_x - SLIDER_X) * 14 // (SLIDER_WIDTH - SLIDER_HANDLE_WIDTH) + 1
    speed = slider_value

def draw_piano():
    # Draw white keys
    for i in range(NUM_WHITE_KEYS):
        key_x = i * WHITE_KEY_WIDTH
        pygame.draw.rect(screen, WHITE, (key_x, PIANO_Y, WHITE_KEY_WIDTH, KEY_HEIGHT))
        pygame.draw.rect(screen, BLACK, (key_x, PIANO_Y, WHITE_KEY_WIDTH, KEY_HEIGHT), 1)

    # Draw black keys
    for key in ["C#4", "D#4", "F#4", "G#4", "A#4"]:
        if key in black_positions:
            key_x = black_positions[key]
            pygame.draw.rect(screen, BLACK, (key_x, PIANO_Y, BLACK_KEY_WIDTH, KEY_HEIGHT * 2 // 3))

# Get the MIDI input device
def get_midi_input():
    for i in range(pygame.midi.get_count()):
        interface, name, is_input, is_output, opened = pygame.midi.get_device_info(i)
        if is_input and 'MIDI' in name.decode():
            return i
    return None

# Open the MIDI input
midi_input_id = get_midi_input()
if midi_input_id is None:
    print("No MIDI input device found.")
    pygame.quit()
    sys.exit()
else:
    midi_input = pygame.midi.Input(midi_input_id)

# Main game loop
clock = pygame.time.Clock()
running = True
dragging_slider = False

while running:
    screen.fill(WHITE)
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if SLIDER_X <= x <= SLIDER_X + SLIDER_WIDTH and SLIDER_Y - 5 <= y <= SLIDER_Y + SLIDER_HEIGHT + 5:
                dragging_slider = True
            elif button_position[0] <= x <= button_position[0] + button_width and button_position[1] <= y <= button_position[1] + button_height:
                toggle_mode()
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_slider = False
        elif event.type == pygame.MOUSEMOTION and dragging_slider:
            x, _ = event.pos
            slider_handle_x = max(SLIDER_X, min(x, SLIDER_X + SLIDER_WIDTH - SLIDER_HANDLE_WIDTH))
            process_slider()
        elif event.type == pygame.KEYDOWN:
            if event.key in KEYBOARD_TO_GAME:
                note = KEYBOARD_TO_GAME[event.key]
                for square in squares:
                    if square.note == note and square.rect.y >= 0:
                        square.play_note()
                        score += 1
                        square.reset_position()
                        break

    # Update and draw squares
    for square in squares:
        square.update()
        if square.rect.y >= PIANO_Y:
            square.reset_position()
        square.draw()

    # Check for MIDI input
    if midi_input.poll():
        midi_events = midi_input.read(10)
        for event in midi_events:
            data = event[0]
            midi_status = data[0]
            midi_note = data[1]
            velocity = data[2]

            if midi_status == 144 and velocity > 0:  # Note on
                if midi_note in MIDI_TO_GAME:
                    note = MIDI_TO_GAME[midi_note]
                    for square in squares:
                        if square.note == note and square.rect.y >= 0:
                            square.play_note()
                            score += 1
                            square.reset_position()
                            break
            elif midi_status == 128 or (midi_status == 144 and velocity == 0):  # Note off
                pass

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Draw the piano
    draw_piano()

    # Draw the mode toggle button
    draw_button()

    # Draw slider
    draw_slider()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

print("Exiting the game.")
pygame.quit()
