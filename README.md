# Learn Notes with Falling Squares

A fun and interactive game to help you learn musical notes using a MIDI keyboard or your computer keyboard. Watch the falling squares and match them to their corresponding notes on your piano keyboard or computer keyboard!

## Features

- **MIDI Keyboard Support:** Play with any MIDI keyboard.
- **Computer Keyboard Support:** Play using your computer keyboard.
  - White keys: `s, d, f, g, h, j, k`
  - Black keys: `e, r, y, u, i`
- **Easy/Difficult Mode:** Toggle between easy mode (without black keys) and difficult mode.
- **Adjustable Speed:** Control the speed of falling squares.
- **Score Tracking:** Keep track of your score as you play.

## How to Play

1. **Run the Game:**
   - Clone this repository.
   - Install dependencies with `pip install pygame`.
   - Execute `python learn_notes.py`.

2. **Controls:**
   - MIDI Keyboard: Play notes directly on your MIDI keyboard.
   - Computer Keyboard:
     - White keys: `a, s, d, f, g, h, j, k`
     - Black keys: `e, r, y, u, i`
   - Switch between Easy/Difficult mode by clicking the "Mode" button.
   - Adjust the speed using the slider.

## Installation

### Requirements

- **Python 3.6+**
- **pygame**
- **pygame.midi**

Install dependencies using:

```bash
pip install pygame
```

### Run the Game

1. Clone the repository:

```bash
git clone https://github.com/your-username/learn-notes-with-falling-squares.git
cd learn-notes-with-falling-squares
```

2. Run the game:

```bash
python learn_notes.py
```

### Creating an Executable

To create an executable `.exe` file using PyInstaller:

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. Create the executable:

```bash
pyinstaller --onefile --windowed learn_notes.py
```

The executable will be located in the `dist/` folder.

## Sounds

Make sure you have a folder named `sounds/` in the same directory as the Python script. The folder should contain `.wav` files for each note:

```
sounds/
    C4.wav
    Csharp4.wav
    D4.wav
    Dsharp4.wav
    E4.wav
    F4.wav
    Fsharp4.wav
    G4.wav
    Gsharp4.wav
    A4.wav
    Asharp4.wav
    B4.wav
```

You can find these sound files in various online resources or create your own.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.

## Acknowledgments

- The game is inspired by educational piano learning software.
- Thanks to the pygame and pygame.midi communities for their amazing libraries.
