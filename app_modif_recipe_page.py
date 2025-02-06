import streamlit as st
from data_exporters.sql_manager import SQL_recipe_manager
from random import choice

sql_manager = SQL_recipe_manager()


# Header / Title
st.markdown("<h2 style='color: #DE684D;'> Modifier un recette </h2>", unsafe_allow_html=True)
st.write('---')

# Receipe Selection
    # Receipe list creation for the selectbox
df = sql_manager.get_all_recipes()
receipe_list = list(df['name'].values)

    # Automatic selection if user already choose a receipe from another page
if 'current_receipe_name' not in st.session_state :
    st.session_state.receipe_index = None

    # Selectbox for receipe choice
def change_index() :
    if 'selectbox' in st.session_state :
        st.session_state.current_receipe_name = st.session_state["selectbox"]
st.selectbox("", receipe_list,index=None,key="selectbox", placeholder= 'Choisir une recette dans la liste', on_change= change_index)
st.write('---')

if 'current_receipe_name' in st.session_state and st.session_state.current_receipe_name is not None :

    idx = df[df['name']==st.session_state.current_receipe_name]['id'].values[0]
    current_receipe = sql_manager.get_recipe_detail(idx)

    # Modification title and details
    st.markdown("<h5 '> Informations</h5>", unsafe_allow_html=True)
    current_receipe['name'] = st.text_input('Modifier le titre',value = current_receipe['name'])
    st.write(' ')
    _ , col1, _ , col2, _ = st.columns([1,5,1,5,1])
    with col1 :
        st.text_input("Temps de préparation :", value = current_receipe['time_preparation'])
        st.text_input("Temps de repos :", value = current_receipe['time_rest'])
        st.text_input("Temps de cuisson :", value = current_receipe['time_cooking'])

    with col2 :
        st.text_input("Coût :", value = current_receipe['cost'])
        st.text_input("Difficulté :", value = current_receipe['difficulty'])
        st.number_input("Nombre de part :", 1,20, value = int(current_receipe['nb_person']))

    st.write('---')


    # Modification ingredients
    st.markdown("<h5 '>Ingrédients</h5>", unsafe_allow_html=True)
    st.write(' ')
    container = st.container(key='ing_container')
    with container :
        for ind,ing in enumerate(current_receipe['ingredients']):
            col0 ,col1, _ , col2, _ , col3 , _ = st.columns([1,2,0.5,2,0.5,5,1])
            with col0 :
                if st.button('❌',key = f'ing_b_{ind}') :
                    ing['quantity'] = ing['unit'] = ing['name'] = ''
            with col1 :
                st.text_input(label = '',value = ing['quantity'],key = f'qty_{ind}')
            with col2 :
                st.text_input(label = '',value = ing['unit'],key = f'unit_{ind}')
            with col3 :
                st.text_input(label = '',value = ing['name'],key = f'name_{ind}')
        with col1 :
            st.text_input(label = '',value = '',key = f'qty_{ind+1}')
        with col2 :
            st.text_input(label = '',value = '',key = f'unit_{ind+1}')
        with col3 :
            st.text_input(label = '',value = '',key = f'name_{ind+1}')
    
    st.write('---')

    # Modification steps
    st.markdown("<h5 '>Etapes</h5>", unsafe_allow_html=True)
    container = st.container(key='step_container')
    with container :
        for ind, step in enumerate(current_receipe['steps']) :
            _, col1, col2 = st.columns([0.2,1,10])
            with col1 :
                st.markdown(f'**Etape {ind+1}**')
                st.button('❌',key = f'step_b_{ind}')
            with col2 :
                st.text_area(label = '',value = step ,key = f'step_{ind}')
        with col1 :
            st.markdown(f'**Etape {ind+2}**')
        with col2 :
            st.text_area(label = '',value = '' ,key = f'step_{ind+1}')





    st.markdown('''<style>
                .st-key-ing_container label {display: none;}
                .st-key-step_container label {display: none;}
                </style>''', unsafe_allow_html=True)

# .st-key-step_container input {background-color: #DE684D;}