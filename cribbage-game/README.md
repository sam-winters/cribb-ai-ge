# Cribbage Game

This project is a Python implementation of the classic card game Cribbage. It includes the core game logic, player management, scoring, and utilities to facilitate gameplay.

## Project Structure

```
cribbage-game
├── src
│   ├── main.py          # Entry point of the application
│   ├── game
│   │   ├── __init__.py  # Initializes the game module
│   │   ├── deck.py      # Manages the deck of cards
│   │   ├── player.py     # Represents a player in the game
│   │   └── scoring.py    # Contains scoring functions
│   └── utils
│       ├── __init__.py  # Initializes the utils module
│       └── helpers.py    # Utility functions for the game
├── tests
│   ├── __init__.py      # Initializes the tests module
│   ├── test_deck.py     # Unit tests for the Deck class
│   ├── test_player.py    # Unit tests for the Player class
│   └── test_scoring.py   # Unit tests for scoring functions
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd cribbage-game
pip install -r requirements.txt
```

## Usage

To start the game, run the following command:

```bash
python src/main.py
```

## Game Rules

Cribbage is played with a standard 52-card deck and can be played by 2 to 4 players. The objective is to be the first player to score 121 points. Points are scored for combinations of cards in the player's hand and during the pegging phase.

For detailed rules, refer to the official Cribbage rulebook or other resources online.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.