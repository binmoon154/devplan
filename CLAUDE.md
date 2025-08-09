# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python game development project using Pygame to create a detective/escape game. The project appears to be in active development with multiple game prototypes and experiments.

## Development Environment

### Python Virtual Environment
- Uses `myvenv/` virtual environment with Python
- Pygame 2.6.1 is installed as the main game engine
- Activate virtual environment before running any code:
  - Windows: `myvenv\Scripts\activate`
  - macOS/Linux: `source myvenv/bin/activate`

### Running Games
- Main game files are Python scripts that can be run directly:
  - `python N-game/0-game.py` - Main walking detective game
  - `python game/prac.py` - Camera following practice
  - `python pa/game.py` - Player/background system test

## Project Structure

### Core Game Components
- **N-game/**: Contains the main game implementations
  - `0-game.py` - Primary walking detective game with scrolling background
  - Character movement with walking/running animations
  - Collision detection with obstacles (desk, drawer, door)
  - A/D movement with Shift for running speed

- **animation.py**: Animation class for sprite animations
  - Frame-based animation system
  - Support for looping and one-shot animations
  - Used for walking/running character states

- **image.py**: Image loading utilities
  - Centralized image path management
  - Loads character sprites (idle, walk, run in both directions)

- **game/**: Practice and experimental game code
  - `prac.py` - Camera system that follows player
  - Player class with inventory system
  - Door interaction mechanics with 'E' key

- **pa/**: Modular game architecture experiment
  - `game.py` - Uses separate Player and Background classes
  - More object-oriented approach to game structure

### Game Assets
- **game-image/**: Sprite assets for characters
  - Character animations: stop.png, walk.png, run.png
  - Directional sprites: back_walk.png, back_run.png, back_stop.png
  - Background: home.png

- **NanumGothic.ttf**: Korean font file for text rendering

### Documentation
- **gamedev.md**: Game design document in Korean
  - Detective/escape game concept
  - Character controls and mechanics
  - Development timeline and testing checklist

- **story.txt**: Game story and development resources
  - Plot outline for escape game scenario
  - Links to design tools and asset resources

## Game Architecture Patterns

### Character Movement System
- Fixed character position on screen with scrolling background
- Direction-based sprite selection (left/right facing)
- Speed modifiers with Shift key for running
- Collision detection prevents movement through obstacles

### Animation System
- Frame-based sprite animation with configurable speed
- State-based animation switching (idle, walk, run)
- Direction-aware animations for left/right movement

### Camera/Viewport System
- Background scrolling relative to character position
- World coordinates vs screen coordinates separation
- Camera following player with collision boundary checking

## Development Workflow

### Game Testing
Run individual game files to test specific mechanics:
```bash
# Activate virtual environment first
python N-game/0-game.py    # Main game
python game/prac.py        # Camera system
python pa/game.py          # Modular architecture
```

### Asset Management
- Place new sprites in `game-image/` directory
- Follow naming convention: `[action]_[direction].png`
- Update `image.py` when adding new sprite assets

## Game Controls
- **A/Left Arrow**: Move left
- **D/Right Arrow**: Move right  
- **Shift + Movement**: Run (faster movement)
- **E**: Interact with objects (doors, items)
- **M**: Open/close memo/notebook (planned feature)

## Technical Notes

### Pygame Specifics
- Screen resolution: 1440x1080 for main game
- 60 FPS target frame rate
- Uses `convert()` and `convert_alpha()` for optimized image loading
- Collision detection using `pygame.Rect.colliderect()`

### Character Physics
- Fixed screen position with world coordinate tracking
- Scroll speed: 5 pixels per frame (7 pixels when running)
- Character positioned at screen center horizontally

This is a learning/educational game development project focused on 2D side-scrolling mechanics and interactive storytelling.