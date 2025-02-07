from data_exporters.sql_manager import SQL_recipe_manager
import streamlit as st
from random import choices

sql_manager = SQL_recipe_manager()

df = sql_manager.get_all_recipes()
receipe_list = list(zip(df['name'].values,df['image_link'].values))

# Header / Title
st.markdown("<h2 style='color: #DE684D;'>Bienvenue sur Data Chef !</h2>", unsafe_allow_html=True)
st.write("---")

# Recipe suggestion
    # Title
st.markdown("<h4 style='text-align: center; color: black;'>Nos idées recettes</h4>", unsafe_allow_html=True)
st.write(" ")
if "page" not in st.session_state:
    st.session_state.page = "home"

def set_page(page_name):
    st.session_state.page = page_name

with st.sidebar:
    _ , col , _ = st.columns([1,5,1])
    with col :
        st.markdown("<h1 style='text-align: center;'> Navigation </h1>", unsafe_allow_html=True)
        st.write(' ')
        if st.button("Accueil"):
            set_page("home")
        if st.button("Mon profil"):  # Bouton Accueil, use_container_width=True
            set_page("my_profile")
        if st.button("Recettes"):  # Bouton Accueil, use_container_width=True
            set_page("receipe")
        if st.button('Modifier la recette') :
            set_page("receipe_modif")

_, mid, _ = st.columns([1,10,1])

with mid :
    if st.session_state.page == "home":
        st.markdown("<h2 style='color: #DE684D;'>Bienvenue sur Data Chef !</h2>", unsafe_allow_html=True)
        st.write("---")
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

<<<<<<< HEAD
def create_short_list():
    st.session_state.short_list = choices(receipe_list, k=12)
     
if 'short_list' not in st.session_state :
    create_short_list()

if st.button("Changer les propositions",key='suggestion_button') :
    create_short_list()
st.write(' ')
     
    # Containers
for raw in range(3) :
    col_list = st.columns(4)
    for n_col,col in enumerate(col_list) :
        ind = raw*4 + n_col
        with col :
                st.image(st.session_state.short_list[ind][1])
                if st.button(label=st.session_state.short_list[ind][0], key=f'but_{ind}',use_container_width =True) :
                    idx = df[df['name']==st.session_state.short_list[ind][0]]['id'].values[0]
                    st.session_state.current_receipe = sql_manager.get_recipe_detail(idx)
                    # st.page_link("app_receipe_page.py")


# Style 
st.markdown('''<style>
            .st-key-suggestion_button {text-align: center}
            </style>''', unsafe_allow_html=True)
=======
>>>>>>> 492e13594f5a1f548a576fd75575238163a536cd
