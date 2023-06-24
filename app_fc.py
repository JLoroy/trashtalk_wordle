# LANGCHAIN with FUNCTION CALLING

## Langchain part
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain_decorators import llm_prompt, llm_function
from langchain_decorators.common import GlobalSettings
from langchain_decorators import llm_prompt

GlobalSettings.define_settings(verbose=True)

print("rerun")

@llm_function
def roast(reaction:str)->str:
    """ 
    Write a very short and unpleasant comment about the player's strategy. Keep the secret word secret.

    Args:
        reaction (str): the sacarstic annoying comment. 
    """
    st.session_state.chat_history.append(reaction.replace( st.session_state.secret_word, '*****'))

class RoastAgent:

    def __init__(self) -> None:
        self.todo_list=[]

    @llm_prompt
    def judge(self, secret_word:str, history:str, guess:str, functions=[roast]):
        """ 
        ``` <prompt:system>
        You are a very cynique and sarcastic commenter. You're watching someone playing WORDLE and you are making a comment over each guess the player tries to roast him in just a few passive aggressive words. The player feels motivated by a bit of trashtalk. they have a lot of humor so you don't have to fear offending them.
        ```
        ``` <prompt:user>
        Here is the state of the game:
        The secret word is {secret_word}. 
        {history}
        the guess the player just submitted is {guess}. 
        What is your comment? (keep it very short and unpleasant. Keep the secret word secret) 
        ```
        """

    def react(self, secret_word, guesses, guess):
        history = "this is the opening guess"
        if len(guesses) > 0:
            history = "here's what the player tried before: "+", ".join(guesses)
        result = self.judge(secret_word=secret_word, history=history, guess=guess)
        result.execute()


# STREAMLIT Part
import streamlit as st
import random, re, time

# The list of 5-letter words. In a real game, you might use a larger list.
WORDS = ["apple","beach","brain","bread","brush","chair","chest","chord","click","clock","cloud","dance","diary","drink","earth","flute","fruit","ghost","grape","green","happy","heart","house","juice","light","money","music","party","pizza","plant","radio","river","salad","sheep","shoes","smile","snack","snake","spice","spoon","storm","table","toast","tiger","train","water","whale","wheel","woman","world","write","youth","abuse","adult","agent","anger","apple","award","basis","beach","birth","block","blood","board","brain","bread","break","brown","buyer","cause","chain","chair","chest","chief","child","china","claim","class","clock","coach","coast","court","cover","cream","crime","cross","crowd","crown","cycle","dance","death","depth","doubt","draft","drama","dream","dress","drink","drive","earth","enemy","entry","error","event","faith","fault","field","fight","final","floor","focus","force","frame","frank","front","fruit","glass","grant","grass","green","group","guide","heart","henry","horse","hotel","house","image","index","input","issue","japan","jones","judge","knife","laura","layer","level","lewis","light","limit","lunch","major","march","match","metal","model","money","month","motor","mouth","music","night","noise","north","novel","nurse","offer","order","other","owner","panel","paper","party","peace","peter","phase","phone","piece","pilot","pitch","place","plane","plant","plate","point","pound","power","press","price","pride","prize","proof","queen","radio","range","ratio","reply","right","river","round","route","rugby","scale","scene","scope","score","sense","shape","share","sheep","sheet","shift","shirt","shock","sight","simon","skill","sleep","smile","smith","smoke","sound","south","space","speed","spite","sport","squad","staff","stage","start","state","steam","steel","stock","stone","store","study","stuff","style","sugar","table","taste","terry","theme","thing","title","total","touch","tower","track","trade","train","trend","trial","trust","truth","uncle","union","unity","value","video","visit","voice","waste","watch","water","while","white","whole","woman","world","youth"]

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

def message_html(msg, color='gray'):
    return f"""
    <div style="
        display: inline-block;
        padding: 10px;
        border-radius: 10px;
        margin: 2px;
        background-color: {color};
        ">
        {msg}
    </div>
    """

def main():
    st.title('Trashtalk Wordle')

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
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Handle play again logic.
    if st.session_state.game_over:
        if game_col.button("Play again? click twice" ):
            st.session_state.game_over = False
            st.session_state.secret_word = random.choice(WORDS)
            st.session_state.guesses = []
            st.session_state.feedbacks = []
            st.session_state.chat_history = []
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
            RoastAgent().react(st.session_state.secret_word, st.session_state.guesses, guess)
            
            st.session_state.guesses.append(guess)
            st.session_state.feedbacks.append(feedback)
            st.session_state.input_key = "input" + str(random.randint(0, 1000000))

        if guess == st.session_state.secret_word:
            game_col.write("You win!")
            st.session_state.game_over = True
            if game_col.button("Next"):
                pass
        elif len(st.session_state.guesses) >= 6:
            game_col.write("You lost! the word was "+st.session_state.secret_word)
            st.session_state.game_over = True
            if game_col.button("Next"):
                pass

        # Display previous feedbacks
        for past_feedback, past_guess in zip(st.session_state.feedbacks, st.session_state.guesses):
            past_feedback_html = generate_feedback_html(past_feedback, past_guess)
            game_col.markdown(past_feedback_html, unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            chat_col.markdown(message_html(message, 'purple'), unsafe_allow_html=True)
        


if __name__ == "__main__":
    main()
