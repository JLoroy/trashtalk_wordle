# LANGCHAIN
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

system_prompt_template = """
    Tu es un commentateur très cynique et sarcastique. Tu regardes quelqu'un jouer à WORDLE et tu fais un commentaire pour juger chaque proposition du joueur pour le taquiner en quelques mots passif-agressifs. Le joueur se sent motivé par un peu de trashtalk. Ils ont beaucoup d'humour donc tu n'as pas à craindre de les offenser.
"""

human_prompt_template = """Voici où en est la partie:
le mot secret est {secret_word}. 
{history}
et le joueur vient d'essayer {guess}. 

Donne maintenant ton commentaire. Garde cela court et piquant. Surtout ne révèle pas le mot secret."""

system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt_template)
human_message_prompt = HumanMessagePromptTemplate.from_template(human_prompt_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

def load_Chat():
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    chat = ChatOpenAI(temperature=0.8)
    return chat

chat = load_Chat()

def react(secret_word, guesses, guess):
    history = "C'est son premier essai"
    if len(guesses) > 0:
        history = "voici les mots que le joueur a déjà essayé: " + ", ".join(guesses)
    chat_prompt_with_values = chat_prompt.format_prompt(secret_word=secret_word, history=history, guess=guess)
    response = chat(chat_prompt_with_values.to_messages()).content
    return response



# STREAMLIT Part
import streamlit as st
import random, re, time

# The list of 5-letter words. In a real game, you might use a larger list.
WORDS = ["aider","aigle","aimer","album","aller","amour","angle","annee","arbre","arete","arret","assez","assis","avion","bague","balai","balle","bande","barbe","barre","baver","bebes","belle","betes","bijou","bille","bisou","blanc","blond","boire","bosse","botte","bouee","boule","bruit","cache","cadre","calme","canne","casse","champ","chaud","chene","chien","chose","chute","clair","clown","cÅ“ur","colle","conte","corde","corps","coude","court","crabe","craie","creux","crier","croix","cruel","cuire","cygne","danse","debut","doigt","droit","ecole","ecran","eleve","engin","envie","epais","etang","etude","evier","faire","farce","faute","femme","ferme","fesse","filet","fille","finir","fleur","foire","fonce","foret","frein","frere","frite","froid","front","fruit","fumee","fumer","fusee","fusil","garer","geant","geler","gener","genou","glace","gomme","gorge","grain","grand","guepe","gueri","habit","herbe","heure","hibou","hiver","homme","huile","image","jambe","jaune","jeter","jeudi","jeune","jouer","jouet","lacer","lacet","laine","lampe","lapin","large","larme","laver","leger","lever","ligne","linge","lisse","liste","litre","livre","loupe","lourd","lundi","lutin","magie","mains","maman","mardi","marin","matin","melon","metal","metre","micro","mieux","mince","mixer","moins","monde","moule","moyen","nager","nappe","navet","neige","noyau","nuage","obeir","objet","odeur","ombre","ongle","orage","ordre","outil","paire","panda","panne","patte","payer","peche","pelle","pente","perle","peser","petit","photo","pieds","place","plage","plein","plier","pluie","plume","poche","poele","poing","point","poire","pomme","pompe","poney","porte","poser","poste","pouce","poule","preau","prune","punir","puree","queue","radio","radis","ramer","rampe","rater","rayon","reine","repas","rever","riche","rouge","route","ruban","sable","salle","sante","sapin","savon","serre","siege","signe","singe","soupe","sourd","sport","stylo","sucer","sucre","table","tache","talon","taper","tapis","tarte","tasse","taupe","temps","tenir","tente","terre","teter","tigre","tirer","tissu","titre","tordu","train","trait","trier","trois","trous","tuyau","usine","utile","vache","vague","venir","verre","veste","vider","vieux","ville","vitre","vivre","voile","voler","volet","wagon","zebre"]

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
    st.write("## Jeu")
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
        if game_col.button("Rejouer? (clique 2 fois)" ):
            st.session_state.game_over = False
            st.session_state.secret_word = random.choice(WORDS)
            st.session_state.guesses = []
            st.session_state.feedbacks = []
            st.session_state.chat_history = []
            st.session_state.input_key = "input" + str(random.randint(0, 1000000))

    # Check if game is still ongoing.
    if not st.session_state.game_over:
        # Allow the user to enter a guess.
        guess = game_col.text_input("Trouve le mot", key=st.session_state.input_key)
        guess = sanitize_input(guess)  # Sanitize the user input

        # Check the guess.
        if guess in st.session_state.guesses:
            game_col.write("Tu as déjà essayé ce mot.")
        elif len(guess) != 5:
            game_col.write("Trouve le mot de 5 lettres")
        else:
            feedback = check_guess(st.session_state.secret_word, guess)
            reaction= react(st.session_state.secret_word, st.session_state.guesses, guess)
            st.session_state.chat_history.append(reaction)
            st.session_state.guesses.append(guess)
            st.session_state.feedbacks.append(feedback)
            st.session_state.input_key = "input" + str(random.randint(0, 1000000))

        if guess == st.session_state.secret_word:
            game_col.write("C'est gagné!")
            st.session_state.game_over = True
            if game_col.button("Suivant"):
                pass
        elif len(st.session_state.guesses) >= 6:
            game_col.write("Perdu! tu devais trouver "+st.session_state.secret_word)
            st.session_state.game_over = True
            if game_col.button("Suivant"):
                pass

        # Display previous feedbacks
        for past_feedback, past_guess in zip(st.session_state.feedbacks, st.session_state.guesses):
            past_feedback_html = generate_feedback_html(past_feedback, past_guess)
            game_col.markdown(past_feedback_html, unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            chat_col.markdown(message_html(message, 'purple'), unsafe_allow_html=True)
        
        

if __name__ == "__main__":
    main()
