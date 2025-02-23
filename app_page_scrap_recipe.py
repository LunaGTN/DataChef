import streamlit as st
from fonctions.sql_manager import SQL_recipe_manager
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from transformers.utils import *

sql_manager = SQL_recipe_manager()

# Header / Title
st.markdown("<h2 style='color: #DE684D;'> Ajouter une recette Marmiton</h2>", unsafe_allow_html=True)
st.write('---')

st.write('Grâce à cette page, vous pouvez importer une recette qui vous plait depuis le site Marmiton')

def run_scraping():
    msg = st.toast('Recherche de la recette...', icon='🔍')
    new_recipe = load_recipe(st.session_state.url)[0]
    if sql_manager.check_db_by_id(int(new_recipe['id']),'recipe') :
        msg.toast('La recette est déja dans la base de données')
        st.session_state['message'] = '👍 Cette recette est déja dans la base de données'
    else :
        msg.toast('Import de la recette...', icon='🔪')
        new_recipe['name'] = new_recipe['titre']
        new_recipe['time_rest'] = new_recipe["time_repos"]
        new_recipe['time_cooking'] = new_recipe["time_cuisson"]
        new_recipe['image_link'] = new_recipe["image"]
        sql_manager.manage_recipe(recipe_data = new_recipe)
        st.toast('Recette importée avec succès', icon='✅')
        st.session_state['message'] = f'✅ La recette {new_recipe['titre']} a été ajouté à la base de donnée'

def reset_message():
    st.session_state['message']=''

    
# Url 
st.markdown("<h5 '> Saisir l'URL de la recette Marmiton :</h5>", unsafe_allow_html=True)
st.text_input("", key='url',value=None,placeholder='https://www.marmiton.org/recettes/...',on_change = reset_message)
if 'url' in st.session_state and st.session_state.url !=None :
    if 'https://www.marmiton.org/recettes/' in st.session_state.url :
        # st.write('')
        # st.markdown("✅ Le lien est conforme pour la récupération de la recette", unsafe_allow_html=True)
        st.write('')
        st.button('🔽 **Lancer la récupération**',key='scrap',on_click=run_scraping)
    else :
        st.write('')
        st.markdown("❌ Le lien n'est pas valide", unsafe_allow_html=True)
    if 'message' in st.session_state :
        st.write(st.session_state['message'])
st.write('---')

# if 'message' in st.session_state :
#     st.write(st.session_state['message'])


# Style 
st.markdown('''<style>
            .st-key-scrap button {background : #f4846a;color:black}
            .st-key-scrap :hover  {color : white}
            </style>''', unsafe_allow_html=True)