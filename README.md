# Phase 10 Scorekeeper

A simple Python desktop application to keep score for the popular card game Phase 10.
Built with Tkinter for an easy-to-use graphical interface.

## Features
- Manage multiple players and their phases
- Enter and track scores per round
- Mark phases completed for each player
- Automatic dealer rotation every round
- "All Finish Phase" button to mark all players as completed for a round
- Built-in score calculator for leftover cards
- Display Phase 10 rules in-app
- Edit player names at any time
- End game automatically and show winner

## Requirements
- Python 3.6+
- Tkinter (usually included with standard Python installations)

## Installation
1. Make sure [Python3](https://www.python.org/downloads/) is installed on your system.
2. Clone or download this repository.
3. Setup a virutal environment - `python3 -m venv .venv`
4. Activate and install `source .venv/bin/activate; pip install -r requirements.txt`
5. Run the main script:

```bash
python phase10_scorekeeper.py
```

## Building the app locally

### CLI App
Execute the following command:
```bash
pyinstaller --onefile phase10.py
```

### macOS App
Execute the following command:
```bash
pyinstaller --windowed phase10.py
```

## Usage
1. Launch the app.
2. Enter player names separated by commas (e.g., Alice, Bob, Charlie).
3. Click Start Game.
4. For each round:
    1. Enter each player's score.
    2. Check the box if the player completed their phase this round.
    3. Click Next Round to proceed.
5. Use the All Finish Phase button to mark all players as having completed their phase for the round.
6. Use Calculate Scores to open the score calculator where you can input cards left and auto-calculate scores.
7. Access the Rules button to review the Phase 10 game rules.
8. Once a player finishes all phases, the game ends and the winner is displayed.
9. Option to start a new game with the same or different players.

## Scoring Rules (Phase 10)
| Card Type           | Points       |
|---------------------|--------------|
| Number cards (1–9)  | 5 points each|
| Number cards (10–12)| 10 points each|
| Skip cards          | 15 points each|
| Wild cards          | 25 points each|


## How the Game Works in This App
- Each player progresses through phases 1 to 10.
- Scores accumulate each round based on leftover cards.
- The dealer rotates after each round.
- The first player to complete all 10 phases wins, or if multiple players finish simultaneously, the player with the lowest total score wins.

## Customization
- Edit player names anytime from the Options menu.
- The UI colors and fonts are defined in the script and can be customized by editing the source code.

## Troubleshooting
- Ensure your Python installation includes Tkinter (python -m tkinter can test).
- Run from a terminal to see any error output.
- Errors during launch are logged to ~/phase10_launch.log.

## License
This project is open-source and free to use.
