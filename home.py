import streamlit as st
from my_profile import profile_page  

st.set_page_config(
    page_title="Data Chef",  
    page_icon="👨🏾‍🍳",               
    layout="wide",       
)

if "page" not in st.session_state:
    st.session_state.page = "home"

def set_page(page_name):
    st.session_state.page = page_name

with st.sidebar:
    if st.button("Accueil"):
        set_page("home")
    if st.button("Mon Profile"):  # Bouton Accueil, use_container_width=True
        set_page("my_profile")

if st.session_state.page == "home":
    st.markdown("<h2 style='color: #DE684D;'>Bienvenue sur Data Chef !</h3>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<h4 style='text-align: center; color: black;'>Nos recettes</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("Recettes col 1")

    with col2:
        st.write("Recettes col 2")

    with col3:
        st.write("Recettes col 3")

    with col4:
        st.write("Recettes col 4")

elif st.session_state.page == "my_profile":
# Page de visualisation : Appel de la fonction pour afficher les visualisations
    profile_page()
