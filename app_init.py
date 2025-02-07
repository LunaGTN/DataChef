import streamlit as st

st.set_page_config(layout="wide")

pages = {
    ' ':[st.Page("app_home_page.py", title="Accueil")],
    "Mon compte": [
        st.Page("app_profile_page.py", title="Mon profil"),
    ],
    "Livre de recettes": [
        st.Page("app_receipe_page.py", title="Consulter une recette"),
        st.Page("app_modif_recipe_page.py", title="Modifier une recette"),
    ],
}

with st.sidebar:
    # if
    st.button('Se déconnecter')
        # authenticator.logout()

_, mid, _ = st.columns([1,15,1])
with mid :
    st.session_state.pg = st.navigation(pages)
    st.session_state.pg.run()
