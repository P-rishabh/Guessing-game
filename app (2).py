import random

import streamlit as st

MIN_NUM = 1
MAX_NUM = 100

st.set_page_config(page_title="Number Guessing Game", page_icon="🎯")


def new_game():
    """Reset everything for a fresh round."""
    st.session_state.secret = random.randint(MIN_NUM, MAX_NUM)
    st.session_state.tries = 0
    st.session_state.won = False
    st.session_state.history = []
    st.session_state.feedback = None


# Streamlit reruns the whole script on every click, so the game state
# has to live in st.session_state or it would reset each time.
if "secret" not in st.session_state:
    new_game()

st.title("🎯 Number Guessing Game")
st.write(f"I'm thinking of a number between **{MIN_NUM}** and **{MAX_NUM}**. Can you guess it?")

# A form lets the user press Enter to submit, just like input() in the terminal.
with st.form("guess_form"):
    guess = st.number_input(
        f"Your guess ({MIN_NUM} - {MAX_NUM})",
        min_value=MIN_NUM,
        max_value=MAX_NUM,
        value=50,
        step=1,
        disabled=st.session_state.won,
    )
    submitted = st.form_submit_button("Guess", disabled=st.session_state.won)

if submitted:
    st.session_state.tries += 1
    tries = st.session_state.tries
    secret = st.session_state.secret

    if guess == secret:
        st.session_state.won = True
        st.session_state.feedback = ("success", f"🎉 Congratulations! You won in {tries} tries!")
        hint = "Correct!"
    elif guess > secret:
        st.session_state.feedback = ("warning", "Sorry, wrong guess. Go lower! 👇")
        hint = "Too high"
    else:
        st.session_state.feedback = ("warning", "Sorry, wrong guess. Go higher! 👆")
        hint = "Too low"

    st.session_state.history.append({"Try": tries, "Guess": int(guess), "Result": hint})

# Show the latest message
if st.session_state.feedback:
    kind, message = st.session_state.feedback
    if kind == "success":
        st.success(message)
        st.balloons()
    else:
        st.warning(message)

# Stats and history
col1, col2 = st.columns(2)
col1.metric("Tries", st.session_state.tries)
if st.session_state.history:
    col2.metric("Last guess", st.session_state.history[-1]["Guess"])

if st.session_state.history:
    with st.expander("Guess history", expanded=False):
        st.dataframe(st.session_state.history, hide_index=True, use_container_width=True)

st.button("🔄 New game", on_click=new_game)
