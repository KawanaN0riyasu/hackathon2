import streamlit as st

def initialize_session():
    default_states = {
        "user_input": "",
        "questions": [],
        "answers": [],
        "free_texts": [],
        "current_question": "",
        "current_choices": [],
    }
    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value
