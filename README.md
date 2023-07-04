# Hangman-game

This Hangman game is a simple interactive game implemented in Python using the Tkinter library. It allows users to play the classic game of Hangman by guessing letters to complete a hidden word.

Features:
  -Interactive GUI interface using Tkinter.
  -Randomly selects a word from a pre-defined list of words.
  -Tracks the number of incorrect guesses and displays the corresponding parts of the hangman.
  -Provides an option to start a new game.
  -Keeps track of player scores and displays a leaderboard with the top three players.
  -Allows players to enter their name and saves their scores in a SQLite database.

  How to play?
  -Run the hangman.py script using Python.
  -The game window will open, and you will see the hangman figure on the left side of the screen.
  -Enter your name in the provided text box and click "Enter".
  -The hidden word will be displayed as a sequence of asterisks, representing the letters to be guessed.
  -Click on the letter buttons on the on-screen keyboard to make your guesses.
  -If the guessed letter is correct, it will be revealed in the hidden word. Otherwise, a part of the hangman figure will be drawn.
  -Keep guessing letters until you either complete the word or make too many incorrect guesses.
  -If you win, a victory message will be displayed along with the actual word. Your score will be recorded in the leaderboard.
  -If you lose, a defeat message will be displayed, showing the correct word. Your score will also be recorded.
  -To start a new game, click the "New Game" button.
  -To exit the game, click the "Quit" button or close the game window.
