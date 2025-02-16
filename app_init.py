import streamlit as st
from streamlit_google_auth import Authenticate
import streamlit_nested_layout
import os
from dotenv import load_dotenv
import requests
from fonctions.sql_manager import SQL_recipe_manager
import json

sql_manager = SQL_recipe_manager()

st.set_page_config(layout="wide")

# Charger les variables depuis .env
load_dotenv()

# Récupérer les valeurs des variables
cookie_key = os.getenv("COOKIE_KEY")
cookie_name = os.getenv("COOKIE_NAME")
google_credential = json.loads(st.secrets['GOOGLE_CREDENTIALS'])

with open("./credentials.json","w") as file:
    json.dump(google_credential, file)

flow = Flow.from_client_secrets_file(
    "./credentials.json",
    scopes=["https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://datachef.streamlit.app"
)

authenticator = Authenticate(
    secret_credentials_path= "./credentials.json",
    cookie_name=cookie_name,
    cookie_key= cookie_key,
    redirect_uri='https://datachef.streamlit.app'
)

authenticator.check_authentification()

# Title
if st.session_state['connected'] == False:
    st.markdown("<h2 style='color: #DE684D;text-align: center;'>Bienvenue sur Data Chef !</h2>", unsafe_allow_html=True)
    _,logo,_=st.columns([5,3,5])
    with logo :
        st.image('https://github.com/LunaGTN/DataChef/blob/main/logo.png?raw=true',use_container_width=True)
    st.markdown("<h5 style='text-align: center;'>Connectez vous avec votre compte google !</h5>", unsafe_allow_html=True)

if st.session_state['connected']:
    with st.sidebar :
        user_info = st.session_state['user_info']
        if not sql_manager.check_db_by_id(id=user_info['id'], table='users'):
            sql_manager.add_user(user_info=user_info)
        if st.button("**Se déconnecter**",key='button_logout'): 
            authenticator.logout()
            pages={}
else:
    authenticator.login()


if st.session_state['connected']:

    user_info = st.session_state['user_info']
    if not sql_manager.check_db_by_id(id=user_info['id'], table='users'):
        sql_manager.add_user(user_info=user_info)

    pages = {
        "Mon compte": [
            st.Page("app_page_dashboard.py", title = "Tableau de bord"),
            st.Page("app_page_week_meals.py", title="Menu de la semaine"),
            st.Page("app_page_profile.py", title="Mon profil"),
        ],
        "Livre de recettes": [
            st.Page("app_page_recipe_book.py", title="Mes recettes"),
            st.Page("app_page_show_recipe.py", title="Consulter une recette"),
            st.Page("app_page_modif_recipe.py", title="Modifier une recette"),
            st.Page("app_page_scrap_recipe.py", title="Importer une recette"),
            st.Page("app_page_suggestions.py", title="Suggestions")
        ]
    }
    _, mid, _ = st.columns([1,15,1])
    with mid :
        st.session_state.pg = st.navigation(pages)
        if st.session_state['connected']:
            st.session_state.pg.run()


# Style 
st.markdown('''<style>
            .st-key-logout {text-align: center}
            </style>''', unsafe_allow_html=True)

