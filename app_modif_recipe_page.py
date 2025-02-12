from fonctions.sql_manager import SQL_recipe_manager
import streamlit as st
from time import sleep


sql_manager = SQL_recipe_manager()

# Pop up recette enregistrée
def pop_up_start():
    msg = st.toast('Préparation des ingrédients', icon='🔪')
    sleep(2)
    msg.toast('Cuisson', icon='🍳')
    return msg

def pop_up_end(msg):
    msg.toast('Recette ajoutée à votre livre !', icon = "📕")


# Header / Title
st.markdown("<h2 style='color: #DE684D;'> Modifier un recette </h2>", unsafe_allow_html=True)
st.write('---')

# Receipe Selection
    # Receipe list creation for the selectbox
df = sql_manager.get_all_recipes()
receipe_list = list(df['name'].values)

    # Selectbox for receipe choice
def load_recipe() :
    if 'selectbox' in st.session_state and st.session_state.selectbox in receipe_list:
        idx = df[df['name']==st.session_state["selectbox"]]['id'].values[0]
        st.session_state.current_receipe = sql_manager.get_recipe_detail(idx)
st.selectbox("", receipe_list,index=None,key="selectbox", placeholder= 'Choisir une recette dans la liste', on_change= load_recipe)
st.write('---')

if 'current_receipe' in st.session_state and st.session_state.current_receipe is not None :

    # idx = df[df['name']==st.session_state.current_receipe_name]['id'].values[0]
    # current_receipe = sql_manager.get_recipe_detail(idx)

    # Modification title and details
    st.markdown("<h5 '> Informations</h5>", unsafe_allow_html=True)
    st.session_state.current_receipe['name'] = st.text_input('Modifier le titre',value = st.session_state.current_receipe['name'])
    st.write(' ')
    _ , col1, _ , col2, _ = st.columns([1,5,1,5,1])
    with col1 :
        st.text_input("Temps de préparation :", value = st.session_state.current_receipe['time_preparation'])
        st.text_input("Temps de repos :", value = st.session_state.current_receipe['time_rest'])
        st.text_input("Temps de cuisson :", value = st.session_state.current_receipe['time_cooking'])

    with col2 :
        st.text_input("Coût :", value = st.session_state.current_receipe['cost'])
        st.text_input("Difficulté :", value = st.session_state.current_receipe['difficulty'])
        st.number_input("Nombre de part :", 1,20, value = int(st.session_state.current_receipe['nb_person']))

    st.write('---')


    # Modification ingredients
    st.markdown("<h5 '>Ingrédients</h5>", unsafe_allow_html=True)
    st.write(' ')

    container = st.container(key='ing_container')
    
    with container :
        for ind,ing in enumerate(st.session_state.current_receipe['ingredients']):
            col0 ,col1, _ , col2, _ , col3 , _ = st.columns([1,2,0.5,2,0.5,5,1])
            with col0 :
                if st.button('❌',key = f'ing_b_{ind}') :
                    st.session_state.current_receipe['ingredients'].pop(ind)
                    st.rerun()
            with col1 :
                st.text_input(label = '',value = ing['quantity'],key = f'qty_{ind}')
            with col2 :
                st.text_input(label = '',value = ing['unit'],key = f'unit_{ind}')
            with col3 :
                st.text_input(label = '',value = ing['name'],key = f'name_{ind}')
        with col0 :
                if st.button('➕',key = f'ing_b_{ind+1}') :
                    st.session_state.current_receipe['ingredients'].append({'name':st.session_state.name_add,'unit':st.session_state.unit_add, 'quantity':st.session_state.qty_add, 'id': 0})
                    st.session_state.name_add = st.session_state.unit_add = st.session_state.qty_add = ''
                    st.rerun()
        with col1 :
            st.text_input(label = '',value = '',key = 'qty_add')
        with col2 :
            st.text_input(label = '',value = '',key = 'unit_add')
        with col3 :
            st.text_input(label = '',value = '',key = 'name_add')
    st.write('---')

    # Modification steps
    st.markdown("<h5 '>Etapes</h5>", unsafe_allow_html=True)
    container = st.container(key='step_container')
    with container :
        for ind, step in enumerate(st.session_state.current_receipe['steps']) :
            _, col1, col2 = st.columns([0.2,1,10])
            with col1 :
                st.markdown(f'**Etape {ind+1}**')
                if st.button('❌',key = f'step_b_{ind}') :
                    st.session_state.current_receipe['steps'].pop(ind)
                    st.rerun()
            with col2 :
                st.text_area(label = '',value = step['detail'] ,key = f'step_{ind}')
        with col1 :
            st.markdown(f'**Etape sup.**')
            if st.button('➕',key = f'step_b_{ind+1}') :
                st.session_state.current_receipe['steps'].append({"step_number" : ind+1 , 'detail' : st.session_state.step_add })
                st.session_state.step_add  = ''
                st.rerun()
        with col2 :
            st.text_area(label = '',value = '' ,key = 'step_add')

    st.write('---')

    if st.button('📘 **Ajouter à mon livre de recette**',key='button_save'):
        msg = pop_up_start()
        sql_manager.add_user_recipe(
            recipe_data=st.session_state['current_receipe'],
            user_id=st.session_state.user_info['id']
        )
        pop_up_end(msg)


    st.markdown('''<style>
                .st-key-ing_container label {display: none;}
                .st-key-step_container label {display: none;}
                .st-key-button_save {text-align: center}
                .st-key-button_save button {background : #f4846a;color:black}
                .st-key-button_save :hover  {color : white}
                </style>''', unsafe_allow_html=True)

# .st-key-step_container input {background-color: #DE684D;}
