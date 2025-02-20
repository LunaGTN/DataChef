from fonctions.sql_manager import SQL_recipe_manager
import streamlit as st
from time import sleep

#st.write(st.session_state)

sql_manager = SQL_recipe_manager()
user_id = st.session_state.user_info['id']

# Pop up recette enregistrée
def pop_up_start():
    msg = st.toast('Préparation des ingrédients', icon='🔪')
    sleep(2)
    msg.toast('Cuisson', icon='🍳')
    return msg

def pop_up_end():
    st.toast('Recette ajoutée à votre livre !', icon = "📕")


# Header / Title
if 'current_receipe' in st.session_state and st.session_state.current_receipe is not None :
    personnal_recipe =  st.session_state.current_receipe['name'][0] == '👤'
    if not personnal_recipe:
        st.markdown("<h2 style='color: #DE684D;'> Modifier une recette </h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='color: #DE684D;'> Modifier ma recette </h2>", unsafe_allow_html=True)

st.write('---')
st.write("Vous pouvez choisir une recette, la modifier et l'ajouter à votre propre livre de recette")

# Receipe Selection
    # Receipe list creation for the selectbox
df = sql_manager.get_all_recipes_and_user(user_id=user_id)
receipe_list = list(df['name'].values)

    # Selectbox for receipe choice
def load_recipe() :
    if 'selectbox' in st.session_state and st.session_state.selectbox in receipe_list:
        idx = df[df['name']==st.session_state["selectbox"]]['id'].values[0]
        st.session_state.current_receipe = sql_manager.get_recipe_detail(idx)
st.selectbox("", receipe_list,index=None,key="selectbox", placeholder= 'Choisir une recette dans la liste', on_change= load_recipe)
st.write('---')

if 'current_receipe' in st.session_state and st.session_state.current_receipe is not None :

    # Modification title and details
    st.markdown("<h5 '> Informations</h5>", unsafe_allow_html=True)
    if personnal_recipe:
        st.session_state.current_receipe['temp_name'] = st.session_state.current_receipe['name'][2:]
    else:
        st.session_state.current_receipe['temp_name'] = st.session_state.current_receipe['name']
    st.session_state.current_receipe['temp_name'] = st.text_input('Modifier le titre',value = st.session_state.current_receipe['temp_name'])
    st.write(' ')
    _ , col1, _ , col2, _ = st.columns([1,5,1,5,1])
    with col1 :
        st.text_input("Temps de préparation (min) :", value = st.session_state.current_receipe['time_preparation'])
        st.text_input("Temps de repos (min) :", value = st.session_state.current_receipe['time_rest'])
        st.text_input("Temps de cuisson (min) :", value = st.session_state.current_receipe['time_cooking'])

    with col2 :
        st.text_input("Coût :", value = st.session_state.current_receipe['cost'])
        st.text_input("Difficulté :", value = st.session_state.current_receipe['difficulty'])
        st.number_input("Nombre de part :", 1,20, value = int(st.session_state.current_receipe['nb_person']))

    st.write('---')


    # Modification ingredients
    def change_ing(ind):
        st.session_state.current_receipe['ingredients'][ind]['quantity'] = float(st.session_state[f'qty_{ind}'])
        st.session_state.current_receipe['ingredients'][ind]['unit'] = st.session_state[f'unit_{ind}']
        st.session_state.current_receipe['ingredients'][ind]['name'] = st.session_state[f'name_{ind}']

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
                st.text_input(label = '',value = ing['quantity'],key = f'qty_{ind}',on_change=change_ing,args=(ind,))
            with col2 :
                st.text_input(label = '',value = ing['unit'],key = f'unit_{ind}',on_change=change_ing,args=(ind,))
            with col3 :
                st.text_input(label = '',value = ing['name'],key = f'name_{ind}',on_change=change_ing,args=(ind,))
        with col0 :
                if st.button('➕',key = f'ing_b_{ind+1}') :
                    st.session_state.current_receipe['ingredients'].append({'name':'','unit': '', 'quantity':0, 'id': 0})
                    st.rerun()
    st.write('---')

    # Modification steps

    def change_step(ind):
        st.session_state.current_receipe['steps'][ind]['detail'] = st.session_state[f'step_{ind}']

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
                st.text_area(label = '',value = step['detail'] ,key = f'step_{ind}', on_change=change_step,args=(ind,))

        with col1 :
            st.write(' ')
            st.write(' ')
            if st.button('➕',key = f'step_b_{ind+1}') :
                st.session_state.current_receipe['steps'].append({"step_number" : ind+2 , 'detail' : '' })
                st.rerun()


    st.write('---')

    if personnal_recipe:
        col_1, col_2 = st.columns(2)
        with col_1:
            if st.button('**Modifier ma recette**', icon='✏️', key='button_save_1'):
                msg = pop_up_start()
                st.session_state.current_receipe['name'] = f"👤 {st.session_state.current_receipe['temp_name']}"
                sql_manager.update_user_recipe(
                    recipe_data=st.session_state['current_receipe'],
                    user_id=user_id
                )
                st.toast('Recette modifiée', icon='👍')
                
        with col_2:
            if st.button('**Créer une nouvelle version**', icon='💾', key='button_save_2'):
                msg = pop_up_start()
                st.session_state.current_receipe['name'] = st.session_state.current_receipe['temp_name']
                sql_manager.add_user_recipe(recipe_data=st.session_state['current_receipe'], user_id=user_id)
                pop_up_end()

    else:
        if st.button('📘 **Ajouter à mon livre de recette**',key='button_save'):
            msg = pop_up_start()
            sql_manager.add_user_recipe(
                recipe_data=st.session_state['current_receipe'],
                user_id=user_id
            )
            pop_up_end()


    st.markdown('''<style>
                .st-key-ing_container label {display: none;}
                .st-key-step_container label {display: none;}
                .st-key-button_save {text-align: center;}
                .st-key-button_save button {background : #d2a679 ;color:black}
                .st-key-button_save :hover {color : white; border: white;}
                .st-key-button_save :focus {border: #996600}
                .st-key-button_save :focus p {color : #990000}
                .st-key-button_save_1 {text-align: center;}
                .st-key-button_save_1 button {background : #d2a679 ;color:black}
                .st-key-button_save_1 :hover {color : white; border: white;}
                .st-key-button_save_1 :focus {border: #996600}
                .st-key-button_save_1 :focus p {color : #990000}
                .st-key-button_save_2 {text-align: center;}
                .st-key-button_save_2 button {background : #d2a679 ;color:black}
                .st-key-button_save_2 :hover {color : white; border: white;}
                .st-key-button_save_2 :focus {border: #996600}
                .st-key-button_save_2 :focus p {color : #990000}
                </style>''', unsafe_allow_html=True)

# .st-key-step_container input {background-color: #DE684D;}

