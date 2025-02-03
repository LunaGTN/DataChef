import streamlit as st
from app_profile_page import profile_page  
from app_receipe_page import receipe_page

st.set_page_config(
    page_title="Data Chef",  
    page_icon="👨🏾‍🍳",               
    layout="wide",       
)

st.markdown('''<style>
            .ef3psqc19 {width: 70%;}
            </style>''', unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

def set_page(page_name):
    st.session_state.page = page_name

with st.sidebar:
    st.markdown('<h2> Navigation </h2>', unsafe_allow_html=True)
    if st.button("Accueil"):
        set_page("home")
    if st.button("Mon Profil"):  # Bouton Accueil, use_container_width=True
        set_page("my_profile")
    if st.button("Recettes"):  # Bouton Accueil, use_container_width=True
        set_page("receipe")

if st.session_state.page == "home":
    st.markdown("<h2 style='color: #DE684D;'>Bienvenue sur Data Chef !</h2>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<h4 style='text-align: center; color: black;'>Nos recettes</h4>", unsafe_allow_html=True)
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

elif st.session_state.page == "receipe":
    receipe_page()