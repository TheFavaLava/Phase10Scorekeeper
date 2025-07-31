Phase 10 Scorekeeper
A simple Python desktop application to keep score for the popular card game Phase 10.
Built with Tkinter for an easy-to-use graphical interface.

Features
Manage multiple players and their phases

Enter and track scores per round

Mark phases completed for each player

Automatic dealer rotation every round

"All Finish Phase" button to mark all players as completed for a round

Built-in score calculator for leftover cards

Display Phase 10 rules in-app

Edit player names at any time

End game automatically and show winner

Requirements
Python 3.6+

Tkinter (usually included with standard Python installations)

Installation
Make sure Python 3 is installed on your system.

Clone or download this repository.

Run the main script:

bash
Copy
Edit
python phase10_scorekeeper.py
(Replace phase10_scorekeeper.py with the filename if different)

Usage
Launch the app.

Enter player names separated by commas (e.g., Alice, Bob, Charlie).

Click Start Game.

For each round:

Enter each player's score.

Check the box if the player completed their phase this round.

Click Next Round to proceed.

Use the All Finish Phase button to mark all players as having completed their phase for the round.

Use Calculate Scores to open the score calculator where you can input cards left and auto-calculate scores.

Access the Rules button to review the Phase 10 game rules.

Once a player finishes all phases, the game ends and the winner is displayed.

Option to start a new game with the same or different players.

Scoring Rules (Phase 10)
Number cards (1-9): 5 points each

Number cards (10-12): 10 points each

Skip cards: 15 points each

Wild cards: 25 points each

How the Game Works in This App
Each player progresses through phases 1 to 10.

Scores accumulate each round based on leftover cards.

The dealer rotates after each round.

The first player to complete all 10 phases wins, or if multiple players finish simultaneously, the player with the lowest total score wins.

Customization
Edit player names anytime from the Options menu.

The UI colors and fonts are defined in the script and can be customized by editing the source code.

Troubleshooting
Ensure your Python installation includes Tkinter (python -m tkinter can test).

Run from a terminal to see any error output.

Errors during launch are logged to ~/phase10_launch.log.

License
This project is open-source and free to use.
