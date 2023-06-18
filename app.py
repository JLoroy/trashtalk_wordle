import streamlit as st
import random, re

# The list of 5-letter words. In a real game, you might use a larger list.
WORDS = ["apple", "grape", "lemon", "melon", "peach"]

def check_guess(secret_word, guess):
    # Initialize a list of 'gray' for each letter in the guess.
    result = []
    for n in range(len(guess)):
        result.append({'letter':guess[n], 'color':'gray'})

    # Initialize a list to keep track of which letters in the secret word have been used.
    used = [False] * len(secret_word)

    # First, check for letters in the correct position.
    for m in range(len(guess)):
        if guess[m] == secret_word[m]:
            # The letter is correct and in the correct position.
            result[m]['color'] = 'green'
            used[m] = True

    # Then, check for letters in the wrong position.
    for l in range(len(guess)):
        if result[l]['color'] == 'gray'and guess[l] in secret_word and not used[secret_word.index(guess[l])]:
            # The letter is correct but in the wrong position.
            result[l]['color'] = 'yellow'
            used[secret_word.index(guess[l])] = True

    return result

def generate_feedback_html(feedback, guess):
    # Encapsulate the feedback display in a function for reuse
    feedback_html = "<div style='display: flex;'>"
    for i, color in enumerate(feedback):
        block_color = 'lime' if color['color'] == 'green' else 'yellow' if color['color'] == 'yellow' else 'lightgray'
        feedback_html += f'<div style="display: flex; justify-content: center; align-items: center; background-color: {block_color}; width: 50px; height: 50px; margin: 5px; font-weight: bold; color: black;">{guess[i]}</div>'
    feedback_html += "</div>"
    return feedback_html


def sanitize_input(input_string):
    # Remove leading/trailing whitespace and convert to lowercase
    sanitized_input = input_string.strip().lower()
    # Ensure input only contains alphabetic characters
    if re.match("^[a-z]*$", sanitized_input):
        return sanitized_input
    else:
        return ""

def main():
    st.title('My Wordle Clone')

    # Create two columns for the Wordle game and the chat.
    st.write("## Game")
    game_col, chat_col = st.columns(2)

    # Initialize session state variables.
    if 'secret_word' not in st.session_state:
        st.session_state.secret_word = random.choice(WORDS)
    if 'guesses' not in st.session_state:
        st.session_state.guesses = []
    if 'feedbacks' not in st.session_state:
        st.session_state.feedbacks = []
    if 'input_key' not in st.session_state:
        st.session_state.input_key = "input"
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

    # Handle play again logic.
    if st.session_state.game_over:
        if game_col.button("Play again?"):
            st.session_state.game_over = False
            st.session_state.secret_word = random.choice(WORDS)
            st.session_state.guesses = []
            st.session_state.feedbacks = []
            st.session_state.input_key = "input" + str(random.randint(0, 1000000))

    # Check if game is still ongoing.
    if not st.session_state.game_over:
        # Allow the user to enter a guess.
        guess = game_col.text_input("Enter your guess", key=st.session_state.input_key)
        guess = sanitize_input(guess)  # Sanitize the user input

        # Check the guess.
        if guess in st.session_state.guesses:
            game_col.write("You already guessed that word.")
        elif len(guess) != 5:
            game_col.write("Please enter a 5-letter word.")
        else:
            feedback = check_guess(st.session_state.secret_word, guess)
            st.session_state.guesses.append(guess)
            st.session_state.feedbacks.append(feedback)

        if guess == st.session_state.secret_word:
            game_col.write("You win!")
            st.session_state.game_over = True
            if game_col.button("Next"):
                pass
        elif len(st.session_state.guesses) >= 6:
            game_col.write("You lost!")
            st.session_state.game_over = True

        # Display previous feedbacks
        for past_feedback, past_guess in zip(st.session_state.feedbacks, st.session_state.guesses):
            past_feedback_html = generate_feedback_html(past_feedback, past_guess)
            game_col.markdown(past_feedback_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
