import streamlit as st
from streamlit_google_auth import Authenticate
import os
from dotenv import load_dotenv
import requests

# Charger les variables depuis .env
load_dotenv()

# Récupérer les valeurs des variables
cookie_key = os.getenv("COOKIE_KEY")
cookie_name = os.getenv("COOKIE_NAME")

authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',
    cookie_name=cookie_name,
    cookie_key= cookie_key,
    redirect_uri='http://localhost:8501',)

st.title("DataChef !")
st.subheader("Votre carnet de recette en ligne ")
authenticator.check_authentification()

# Vérification de l'authentification
authenticator.login()
st.write("")
st.write("Connectez vous avec votre compte Google ⬆️")


# Affichage basé sur l'état d'authentification
if st.session_state['connected']:
    user_info = st.session_state['user_info']
    st.write(f"Bonjour, {user_info.get('name')}! ")
    st.write("")
    if st.button('Log out'):
        authenticator.logout()
