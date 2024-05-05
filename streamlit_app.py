import streamlit as st
from streamlit_gsheets import GSheetsConnection
import hmac
from navigation import make_sidebar
from utils import create_client_to_update
from time import sleep

st.set_page_config(layout="wide")

make_sidebar()

tab1, tab2 = st.tabs(["Log in", "Create Account"])
with tab1:
    with st.form("Credentials"):
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        login_button = st.form_submit_button("Log in")
        if login_button:
            if st.session_state["username"] == '':
                st.error("Enter Username!")
            elif st.session_state["password"] == '':
                st.error("Enter Password!")
            else:
                # connection object to google sheets
                conn = st.connection("gsheets", type=GSheetsConnection)
                st.session_state.conn = conn
                # read the sheet with users and passwords
                df = conn.read(
                    worksheet="users",
                    ttl=0,
                    usecols=[0, 1],
                )
                if df['user_name'].isin([st.session_state["username"]]).any().any():
                    if hmac.compare_digest(st.session_state["password"],df[df['user_name'] == st.session_state["username"]]['password'].iloc[0],):
                        st.session_state["password_correct"] = True
                        del st.session_state["password"]  # Don't store the username or password.
                        df = st.session_state.conn.read(worksheet="macros_per_food", ttl = "5s")
                        meal_prep_df = st.session_state.conn.read(worksheet="meal_prep", ttl = "5s")
                        mpd_df = st.session_state.conn.read(worksheet="macros_per_day",ttl= "5s")
                        # Drop rows where all values are NaN
                        df = df.dropna(how='all')
                        meal_prep_df = meal_prep_df.dropna(how='all')
                        mpd_df = mpd_df.dropna(how='all')
                        # Drop columns where all values are NaN
                        st.session_state.macros_per_food_df = df.dropna(how='all', axis = 1)
                        st.session_state.meal_prep_df = meal_prep_df[meal_prep_df['user_name'] == st.session_state["username"]].dropna(how='all', axis = 1)
                        st.session_state.macros_per_day_df = mpd_df[mpd_df['user_name'] == st.session_state["username"]].dropna(how='all', axis = 1)
                        st.session_state.logged_in = True
                        st.session_state.food_added_p1 = 0
                        st.session_state.user = st.session_state["username"]
                        st.session_state.gsclient = create_client_to_update()
                        st.success("Logged in successfully!")
                        sleep(1)
                        st.switch_page("pages/page1.py")
                    else:
                        st.session_state["password_correct"] = False
                        st.error("Incorrect username or password")
                else:
                    st.error("User not found! Create an account.")

with tab2:
    with st.form("NewAccount"):
        st.text_input("Email id", key="email_id_cacc")
        st.form_submit_button("Send code")


