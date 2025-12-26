# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Type**: Python game (Asteroids clone)
**Tech Stack**: Python 3.10+, Pygame 2.6.1
**Purpose**: Classic Asteroids arcade game with telemetry logging

## Development Commands

```bash
# Install dependencies
uv sync

# Run the game
python main.py

# Activate virtual environment (if needed)
source .venv/bin/activate
```

## Architecture & Structure

### Game Loop Architecture
The game follows a standard Pygame game loop pattern in `main.py`:
1. Event handling (quit, keyboard input)
2. Update all sprites (`updatable` group)
3. Collision detection (player-asteroid, shot-asteroid)
4. Rendering (`drawable` group)
5. Frame rate limiting (60 FPS)

### Sprite Container System
Pygame sprite groups are used as class-level containers. Game entities automatically register themselves with groups when instantiated:
- `Player.containers = (updatable, drawable)` - Player updates and draws
- `Asteroid.containers = (asteroids, updatable, drawable)` - Asteroids in all three groups
- `Shot.containers = (shots, updatable, drawable)` - Shots in all three groups
- `AsteroidField.containers = updatable` - Field only needs updates (spawns asteroids)

### Class Hierarchy
- `CircleShape` (base class) - Provides position, velocity, radius, collision detection
  - `Player` - Triangle-shaped ship with rotation, movement, shooting
  - `Asteroid` - Circular obstacles that split when hit
  - `Shot` - Projectiles fired by player
- `AsteroidField` - Spawns asteroids from screen edges at intervals

### Telemetry System
The game includes comprehensive logging via `logger.py`:
- `log_state()` - Called every frame, writes game state snapshots to `game_state.jsonl` (once per second, max 16 seconds)
- `log_event(type, **details)` - Logs discrete events to `game_events.jsonl` (player_hit, asteroid_shot, asteroid_split)
- Captures sprite positions, velocities, rotation, and counts for all groups
- Both log files are overwritten on each game run

## Code Conventions

### Game Constants
All magic numbers are defined in `constants.py`:
- Screen dimensions (1280x720)
- Player properties (radius, speed, turn speed, shoot cooldown)
- Asteroid properties (min/max radius, spawn rate, kinds)
- Shot properties (radius, speed)

### Coordinate System
- Origin (0,0) is top-left corner
- Positive Y is downward
- Rotation is in degrees, with 0° pointing upward
- All game objects use `pygame.Vector2` for position and velocity

### Movement & Physics
- Delta time (`dt`) is passed to all `update()` methods for frame-rate independent movement
- Position updates use: `position += velocity * dt`
- No screen wrapping - objects can move off screen

### Collision Detection
Circle-to-circle collision using radius-based distance check in `CircleShape.collides_with()`

## Game Mechanics

### Asteroid Spawning
`AsteroidField` spawns asteroids from 4 screen edges:
- Random edge selection
- Random speed (40-100)
- Random angle variation (±30°)
- Size based on `ASTEROID_KINDS` multiplier (1-3x min radius)

### Asteroid Splitting
When shot, asteroids split into two smaller asteroids:
- Each child is one `ASTEROID_MIN_RADIUS` smaller
- Children rotate ±20-50° from parent trajectory
- Children move 1.2x faster than parent
- Asteroids below min radius are destroyed without splitting

### Player Controls
- `A` / `D` - Rotate left/right
- `W` / `S` - Move forward/backward
- `Space` - Shoot (0.3s cooldown)

### Game Over
Game ends immediately when player collides with asteroid (no lives system)

## Future Improvements & Architectural Considerations

### Target State: Game State Management
**Current**: Game runs in a single continuous state until player dies
**Limitation**: No separation between game states, no persistence of score/lives across frames
**To implement**:
- Create a `GameState` class to track current mode (menu, playing, paused, game_over)
- Add state transition logic in main loop
- Refactor collision handling to check game state before applying death
- Store score, lives, level as state variables
- Consider state pattern for clean transitions

### Target State: Scoring System
**Current**: No scoring mechanism exists
**To implement**:
- Add score tracking variable in game state
- Award points in asteroid collision handler (vary by asteroid size)
- Create HUD rendering system (see UI/HUD below)
- Consider score multipliers for consecutive hits

### Target State: Multiple Lives & Respawning
**Current**: Single death ends game immediately via `sys.exit()`
**Limitation**: No respawn logic, player object is never recreated
**To implement**:
- Replace `sys.exit()` with lives decrement and state transition
- Create player respawn method (reset position, temporary invulnerability)
- Add invulnerability timer and visual indicator (blinking sprite)
- Clear nearby asteroids or create safe spawn zone

### Target State: Collision System Improvements
**Current**: All entities use circle-based collision (`CircleShape.collides_with()`)
**Limitation**: Player renders as triangle but has circular hitbox (less precise)
**To implement**:
- Create `PolygonShape` base class or collision mixin
- Implement point-in-polygon or SAT collision detection
- Separate visual representation from collision geometry
- Allow entities to define custom collision shapes
- Consider performance impact of polygon collision (may need spatial partitioning)

### Target State: Power-up System
**Current**: No power-up entities or temporary effect system
**Architecture needed**:
- Create `PowerUp` class (inherits from `CircleShape` or new base)
- Add `powerups` sprite group and collision detection in main loop
- Design effect system:
  - Option 1: Timer-based dictionary on player (`self.active_effects = {effect_type: remaining_time}`)
  - Option 2: Effect objects that update and expire themselves
- Apply effects in player's `update()` or `move()` methods
- Add visual indicators (HUD icons, player color changes)
- Power-up types: shield (extra hit), speed boost, rapid fire, weapon upgrades

### Target State: Screen Wrapping
**Current**: Objects move off-screen and disappear
**To implement**:
- Add position wrapping in `CircleShape.update()` or entity-specific updates
- Modulo position by screen dimensions: `pos.x %= SCREEN_WIDTH`
- Special handling for large asteroids (wrap when center crosses edge vs when fully off-screen)
- May need to adjust `AsteroidField` spawn logic to prevent overlap with wrapping objects
- Consider rendering wrapped objects twice if spanning screen edge (visual polish)

### Target State: Visual Effects & Particles
**Current**: No explosion effects or visual feedback beyond object removal
**Architecture needed**:
- Create `Particle` or `Effect` class for temporary visual elements
- Add `effects` sprite group (updatable, drawable)
- Effects should self-destruct after duration
- Implement particle patterns:
  - Explosion: Radial particles with random velocities
  - Thrust trail: Particles behind player when moving
  - Hit effect: Flash or particles on shot impact
- Consider using pygame's `Surface.set_alpha()` for fade effects

### Target State: Weapon System
**Current**: Player.shoot() creates single `Shot` type, hard-coded
**To implement**:
- Decouple weapon from player (weapon as property or separate system)
- Create weapon types: single shot, triple shot, laser beam, bombs
- Add weapon switching mechanism (pickup or key binding)
- For bombs: new `Bomb` class with area-of-effect damage and different collision logic
- Consider ammo system for special weapons

### Target State: UI/HUD System
**Current**: No on-screen UI elements (score, lives, etc.)
**To implement**:
- Create `HUD` class or UI rendering functions
- Use `pygame.font.Font()` or `pygame.freetype.Font()` for text
- Render HUD elements after game sprites but before `pygame.display.flip()`
- Display: score (top-left), lives (icons or number), active power-ups (icons), wave/level number
- Consider separate render layer to avoid sprite group complexity

### Target State: Audio System
**Current**: No sound effects or music
**To implement**:
- Use `pygame.mixer` for sound effects and background music
- Load sounds at initialization (not in game loop)
- Trigger sounds on events: shoot, asteroid_hit, asteroid_split, player_death, power-up
- Add background music with looping
- Consider volume controls and mute option

### Target State: Pause Functionality
**Current**: No pause mechanism
**To implement**:
- Add pause state to game state management
- Check for pause key (ESC or P) in event loop
- Skip update logic when paused, continue rendering
- Display "PAUSED" text overlay
- Prevent pause during game over state

### Target State: Enhanced Telemetry
**Current**: Logging stops after 16 seconds, overwrites files on each run
**Improvements**:
- Add command-line flag to enable/disable logging
- Use unique filenames with timestamps instead of overwriting
- Remove or increase the 16-second limit for longer play sessions
- Add session summary (total score, survival time, asteroids destroyed)
- Consider CSV format option for easier analysis

### Known Issues to Address
- **Asteroid spawning fairness**: Asteroids can spawn directly toward player position (unfair deaths)
- **Shot persistence**: Shots never despawn, accumulate off-screen (memory leak)
- **Framerate dependency**: If system lags, `dt` becomes large, objects can tunnel through each other
- **No boundary checking**: Player can fly completely off-screen and get lost
