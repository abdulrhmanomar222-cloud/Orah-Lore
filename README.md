# Orah Lore

Realistic life simulation and roleplay game prototype built in Python.

A text-based game focused on character creation, city life, tactical movement, agency systems, weapons, equipment, and future expansion toward a larger world simulation.

## Overview

Orah-Lore is a prototype realistic life simulator designed around a hybrid 3D/2D world concept:

- fully 3D world simulation for characters, buildings, vehicles, and environment
- 2D HUD, UI, map, and UI overlays for readability and interaction
- RPG-style character progression
- tactical movement mechanics
- agency, law enforcement, and intelligence simulation
- persistence through JSON-based save files

This project acts as a strong foundation for a larger life-simulation game and is structured for easy extension.

## Key Features

### Character system
- identity creation
- age, appearance, style, and clothing selection
- financial starting balance
- health, hunger, thirst, and energy system
- session and persistence support

### World and gameplay systems
- travel between locations
- menu-driven gameplay loop
- movement controls and tactical options
- weapons and agency equipment catalog
- police, FBI, CIA, and military-inspired systems
- future-ready structure for missions, jobs, vehicles, and economy

### Technical features
- Python 3.7+
- no external game engine required
- JSON save system
- modular architecture
- built-in test suite

## Project Structure

```text
/Orah-Lore 
├── main.py                 # entry point
├── ui.py                   # main menu and gameplay loop
├── models.py               # character and game data models
├── character_creator.py    # character creation flow
├── database.py             # save/load/session management
├── movement.py             # movement and language mechanics
├── weapons.py              # weapons, cuffs, facilities, sector data
├── test_suite.py           # automated regression tests
├── data/
│   └── characters.json     # saved character data
├── requirements.txt        # project dependencies
├── setup.py                # packaging metadata
├── README.md               # project overview
├── ARCHITECTURE.md         # architecture notes
├── PROJECT_SUMMARY.md      # project summary
├── QUICKSTART.py           # quick start utility
├── LICENSE                 # MIT license
├── .gitignore              # git ignore rules
├── .github/
│   └── workflows/
│       └── python-tests.yml
└── __pycache__/            # generated Python cache
```

## Installation

### Requirements
- Python 3.7 or newer
- macOS, Linux, or Windows

### Install dependencies

```bash
git clone https://github.com/<YOUR_USERNAME>/3D-Land-Bot.git
cd 3D-Land-Bot
pip install -r requirements.txt
```

## Run the game

```bash
python3 main.py
```

Or from the project directory:

```bash
python main.py
```

## Gameplay Flow

1. Launch the main menu
2. Create a new character
3. Choose identity, look, and outfit
4. Review and save the character
5. Select the character in-game
6. Travel, manage inventory, check stats, and explore the world
7. Learn and use tactical movement commands

## Controls and Movement

The game includes a basic tactical movement system with:

- walking and sprinting
- crouching and sneaking
- jumping
- free look
- lean and slide actions
- tactical roll
- language rendering and speech logic

## Testing

Run the verification suite:

```bash
python3 test_suite.py
```

The current project test suite verifies:
- data models
- database logic
- session management
- movement system
- advanced movement + language behaviors
- weapons and facility catalog

## Roadmap

### Completed
- character model
- creation system
- save and load database
- session manager
- UI loop
- tactical movement
- language mechanic
- weapons and facility module
- regression tests

### Planned
- economic systems
- jobs and careers
- vehicles
- houses and property ownership
- combat and weapon usage
- missions and factions
- larger city map with districts
- advanced AI and NPC behaviors

## GitHub Publishing

To push this project to GitHub:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/3D-Land-Bot.git
git push -u origin main
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome. Please open a pull request with a clear description and keep changes focused.

## Project Status

Current build status: active prototype / foundation phase

This repository is structured as a playable foundation for a larger realistic life simulation game and remains open for continuous expansion.

---

Developed as a Python-based roleplay and life simulation prototype for future expansion into a richer city simulation experience.
