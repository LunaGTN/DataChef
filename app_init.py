import streamlit as st
from streamlit_google_auth import Authenticate
import streamlit_nested_layout
import os
from dotenv import load_dotenv
import requests
from fonctions.sql_manager import SQL_recipe_manager

sql_manager = SQL_recipe_manager()

st.set_page_config(layout="wide")

pages = {
    ' ':[st.Page("app_home_page.py", title="Accueil")],
    "Mon compte": [
        st.Page("app_profile_page.py", title="Mon profil"),
    ],
    "Livre de recettes": [
        st.Page("app_receipe_page.py", title="Consulter une recette"),
        st.Page("app_modif_recipe_page.py", title="Modifier une recette"),
        st.Page("app_suggestions_page.py", title="Suggestions")
    ],
    "Ma semaine" :[
        st.Page("app_week_page.py", title="Planning de la semaine")
    ]
}


# Charger les variables depuis .env
load_dotenv()

# Récupérer les valeurs des variables
cookie_key = os.getenv("COOKIE_KEY")
cookie_name = os.getenv("COOKIE_NAME")

authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',
    cookie_name=cookie_name,
    cookie_key= cookie_key,
    redirect_uri='http://localhost:8501'
)

authenticator.check_authentification()



with st.sidebar:
    if st.session_state['connected']:
        user_info = st.session_state['user_info']
        if not sql_manager.check_db_by_id(id=user_info['id'], table='users'):
            sql_manager.add_user(user_info=user_info)
        if st.button('Se déconnecter'): 
            authenticator.logout()
    else:
        authenticator.login()

_, mid, _ = st.columns([1,15,1])
with mid :
    st.session_state.pg = st.navigation(pages)
    st.session_state.pg.run()
