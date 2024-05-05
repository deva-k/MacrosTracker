import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]

def logout():
    st.session_state.logged_in = False
    st.sidebar.info("Logged out successfully!")
    sleep(1)
    st.switch_page("streamlit_app.py")

def make_sidebar():
    with st.sidebar:
        st.title("🥦🥚🥔🥑 Macros Tracker")

        if st.session_state.get("logged_in", False):
            col1, col2 = st.columns(2)
            col1.header(f'Hey {st.session_state.user.title()} !')
            col2.write("")
            col2.button("Log out", on_click = logout, type = 'primary')
            st.page_link("pages/page1.py", label="My Macros", icon="🔒")
            st.page_link("pages/page2.py", label="Add Macros", icon="🕵️")
            st.page_link("pages/page3.py", label="Add a Meal", icon="🕵️")

        elif get_current_page_name() != "streamlit_app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("streamlit_app.py")

