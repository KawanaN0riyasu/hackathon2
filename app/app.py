from components.header import render_header
from components.input_menu import render_input_menu
from components.talk_menu import render_talk_menu
from components.summary_menu import render_summary_menu
from components.proposal_menu import render_proposal_menu
from utils.session import initialize_session

initialize_session()
render_header()
render_input_menu()
render_talk_menu()
render_summary_menu()
render_proposal_menu()