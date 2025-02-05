from data_exporters.sql_manager import SQL_recipe_manager
from random import choice
import streamlit as st
from streamlit_extras.stylable_container import stylable_container

sql_manager = SQL_recipe_manager()


# Header / Title
st.markdown("<h2 style='color: #DE684D;'> Recettes </h2>", unsafe_allow_html=True)
st.write('---')


# Receipe Selection
    # Receipe list creation for the selectbox
df = sql_manager.get_all_recipes()
receipe_list = list(df['name'].values)

    # Automatic selection if user already choose a receipe from another page
if 'current_receipe_name' not in st.session_state:
    st.session_state.receipe_index = None

    # Selectbox for receipe choice
def change_index() :
    if 'selectbox' in st.session_state :
        st.session_state.current_receipe_name = st.session_state["selectbox"]
st.selectbox("", receipe_list,index=None,key="selectbox", placeholder= 'Choisir une recette dans la liste', on_change= change_index())
st.write('---')


# Display receipe and details 
if 'current_receipe_name' in st.session_state and st.session_state.current_receipe_name is not None:

    idx = df[df['name']==st.session_state.current_receipe_name]['id'].values[0]
    current_receipe = sql_manager.get_recipe_detail(idx)

    # First line (picture and name)
    st.markdown(f"<h2 style='text-align: center; color: black;'> {current_receipe['name']} </h2>", unsafe_allow_html=True)
    st.write(' ')
    col1, _ , col2 , _ , col3 = st.columns([5,1.5,5,1.5,5])
    with col1:
        st.image(current_receipe['image_link'],width=1000)

    with col2:
        st.write(' ')
        st.markdown(f"**Temps de préparation :** {current_receipe['time_preparation']}", unsafe_allow_html=True)
        st.markdown(f"**Temps de repos :** {current_receipe['time_rest']}", unsafe_allow_html=True)
        st.markdown(f"**Temps de cuisson :** {current_receipe['time_cooking']}", unsafe_allow_html=True)


    with col3 :
        st.write(' ')
        st.markdown(f"**Coût :** {current_receipe['cost']}")
        st.markdown(f"**Difficulté :** {current_receipe['difficulty']}")
        size = st.number_input("**Nombre de part :**", 1, 20,value = int(current_receipe['nb_person'] ), key='size_selector')
    st.write(' ')

    # Lists of ingredients and steps
    col1, _ , col2 = st.columns([4,1,10])

    with col1 :
        st.write(' ')
        b_container = stylable_container(css_styles= """{
                                        border-radius: 20px;
                                        background-color: #f4846a;
                                        padding: 0em 2em 2em 2em ;
                                        """, key='ingredients')
        with b_container :
            container=st.container()

            container.markdown("<h4 style= color: black;'> Ingrédients :</h4>", unsafe_allow_html=True)
            for ing in current_receipe['ingredients'] :
                if ing['quantity'] == '0' :
                    result = f"**{ing['name']}**"
                elif ing['unit'] == '' :
                    result = f"{round(int(ing['quantity'])/int(current_receipe['nb_person'])*size)} **{ing['name']}**"
                else :
                    result = f"{round(int(ing['quantity'])/int(current_receipe['nb_person'])*size)} {ing['unit']} de **{ing['name']}**"
                
                container.markdown(f'- {result}')

    with col2 :
        st.markdown("<h4 style= color: black;'> Etapes de la recette :</h4>", unsafe_allow_html=True)
        for ind, step in enumerate(current_receipe['steps']) :
                st.checkbox(f'**Etape {ind+1} :** {step['detail']}')
        

# Style 
st.markdown('''<style>
            ul{line-height: 130%; margin-bottom : 0;}
            .stMarkdown{margin :auto}
            .test {background-color: #f4846a;}
            .st-key-size_selector input {text-align: center}
            .st-key-size_selector p {font-size: 1rem;}
            [data-baseweb='input'] {background-color: #f4846a; width:50px;}
            </style>''', unsafe_allow_html=True)

