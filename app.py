import streamlit as st
import random

# The list of 5-letter words. In a real game, you might use a larger list.
WORDS = ["apple", "grape", "lemon", "melon", "peach"]

def check_guess(secret_word, guess):
    # Initialize a list of 'gray' for each letter in the guess.
    result = ['gray'] * len(guess)

    # Check each letter in the guess.
    for i in range(len(guess)):
        if guess[i] == secret_word[i]:
            # The letter is correct and in the correct position.
            result[i] = 'green'
        elif guess[i] in secret_word:
            # The letter is correct but in the wrong position.
            result[i] = 'yellow'

    return result


def main():
    st.title('My Wordle Clone')

    # Create two columns for the Wordle game and the chat.
    st.write("## Game")
    game_col, chat_col = st.columns(2)

    # Set up placeholders in each column where we'll display the game and the chat.
    game_placeholder = game_col.empty()
    chat_placeholder = chat_col.empty()

    # For now, just display a message in each placeholder.
    game_placeholder.write("Wordle game will go here.")
    chat_placeholder.write("Chat will go here.")

    # Initialize session state variables.
    if 'secret_word' not in st.session_state:
        st.session_state.secret_word = random.choice(WORDS)
    if 'guesses' not in st.session_state:
        st.session_state.guesses = []

    # Allow the user to enter a guess.
    guess = game_col.text_input("Enter your guess")

    # Check the guess.
    if guess in st.session_state.guesses:
        game_col.write("You already guessed that word.")
    elif len(guess) != 5:
        game_col.write("Please enter a 5-letter word.")
    else:
        st.session_state.guesses.append(guess)
        if guess == st.session_state.secret_word:
            game_col.write("You win!")
        else:
            game_col.write(check_guess(st.session_state.secret_word, guess))

if __name__ == "__main__":
    main()
