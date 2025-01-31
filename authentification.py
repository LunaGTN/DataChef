import streamlit as st
from streamlit_google_auth import Authenticate
import os
from dotenv import load_dotenv

# Charger les variables depuis .env
load_dotenv()

# Récupérer les valeurs des variables
cookie_key = os.getenv("COOKIE_KEY")
cookie_name = os.getenv("COOKIE_NAME")

authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',
    cookie_name=cookie_key,
    cookie_key= cookie_name,
    redirect_uri='http://localhost:8501',
)

# Vérification de l'authentification
authenticator.login()


# Affichage basé sur l'état d'authentification
if st.session_state['connected']:
    user_info = st.session_state['user_info']
    st.image(user_info.get('picture'))
    st.write(f"Hello, {user_info.get('name')}")
    st.write(f"Your email is {user_info.get('email')}")
    if st.button('Log out'):
        authenticator.logout()
        st.session_state['connected'] = False
else:
    print(st.session_state)
    st.title("Log In with Google")
    st.write("Connect to Data Chef with google to access delicious recipes!")
