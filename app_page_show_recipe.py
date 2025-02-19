from fonctions.sql_manager import SQL_recipe_manager
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from time import sleep

sql_manager = SQL_recipe_manager()
user_id = st.session_state.user_info['id']

# Header / Title
st.markdown("<h2 style='color: #DE684D;'> Consulter une recette </h2>", unsafe_allow_html=True)
st.write('---')


# Receipe Selection
    # Receipe list creation for the selectbox
df = sql_manager.get_all_recipes_and_user(user_id=user_id)
receipe_list = list(df['name'].values)

    # Selectbox for receipe choice
def load_recipe() :
    if 'selectbox' in st.session_state and st.session_state.selectbox in receipe_list :
        idx = df[df['name']==st.session_state["selectbox"]]['id'].values[0]
        st.session_state.current_receipe = sql_manager.get_recipe_detail(idx)
st.selectbox("", receipe_list,index=None,key="selectbox", placeholder= 'Choisir une recette dans la liste', on_change= load_recipe)
st.write('---')

# Display receipe and details 
if 'current_receipe' in st.session_state and st.session_state.current_receipe is not None:
    idx = df[df['name']==st.session_state.current_receipe['name']]['id'].values[0]
    current_receipe = sql_manager.get_recipe_detail(idx)

    # First line (picture and name)
    st.markdown(f"<h2 style='text-align: center; color: black;'> {st.session_state.current_receipe['name']} </h2>", unsafe_allow_html=True)
    st.write(' ')
    col1, _ , col2 , _ , col3 = st.columns([5,1.5,5,1.5,5])
    with col1:
        st.image(st.session_state.current_receipe['image_link'],width=1000)

    with col2:
        st.write(' ')
        st.markdown(f"**Temps de préparation :** {st.session_state.current_receipe['time_preparation']}", unsafe_allow_html=True)
        st.markdown(f"**Temps de repos :** {st.session_state.current_receipe['time_rest']}", unsafe_allow_html=True)
        st.markdown(f"**Temps de cuisson :** {st.session_state.current_receipe['time_cooking']}", unsafe_allow_html=True)


    with col3 :
        st.write(' ')
        st.markdown(f"**Coût :** {st.session_state.current_receipe['cost']}")
        st.markdown(f"**Difficulté :** {st.session_state.current_receipe['difficulty']}")
        size = st.number_input("**Nombre de part :**", 1, 20,value = int(st.session_state.current_receipe['nb_person'] ), key='size_selector')
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
            for ing in st.session_state.current_receipe['ingredients'] :
                if ing['quantity'] == 0 or str(ing['quantity']) == '' :
                    result = f"**{ing['name']}**"
                elif ing['unit'] == '' :
                    result = f"{round(int(ing['quantity'])/int(current_receipe['nb_person'])*size)} **{ing['name']}**"
                elif ing['name'][0].lower() in ['a','e','i','o','u','h'] or  ing['name'][:5].lower()in ['huile','huitr','huîtr','herbe'] : 
                    result = f"{round(int(ing['quantity'])/int(current_receipe['nb_person'])*size)} {ing['unit']} d'**{ing['name']}**"
                else :
                    result = f"{round(int(ing['quantity'])/int(current_receipe['nb_person'])*size)} {ing['unit']} de **{ing['name']}**"
                
                container.markdown(f'- {result}')

    with col2 :
        st.markdown("<h4 style= color: black;'> Etapes de la recette :</h4>", unsafe_allow_html=True)
        for ind, step in enumerate(st.session_state.current_receipe['steps']) :
                st.checkbox(f'**Etape {ind+1} :** {step['detail']}')


    st.write(' ')
    st.write('---')
    cols = st.columns (2)
    with cols[0] :
        if st.button("**Personnaliser la recette**",key='button-add', icon='✏️') :
            st.switch_page("app_page_modif_recipe.py")
    with cols[1] :
        recipe_id=st.session_state.current_receipe['id']
        if sql_manager.check_recipe_in_user_book(user_id=user_id, recipe_id=recipe_id):
            if st.button('**Ajouter à mon menu de la semaine**',key='button_add_week', icon='📆') :
                msg = st.toast('Préparation...', icon='🧑‍🍳')
                sleep(1)
                if sql_manager.add_recipe_to_planner(user_id=user_id, recipe_id=recipe_id):
                    msg.toast('Recette ajoutée à mon planning', icon = '✅')
        else:
            if st.button('**Ajouter à mon livre**',key='button_add_book', icon='📕') :
                msg = st.toast('Préparation...', icon='🧑‍🍳')
                if sql_manager.add_user_recipe(recipe_data=sql_manager.get_recipe_detail(recipe_id), user_id=user_id):
                    st.toast('Recette ajoutée à mon livre', icon = '✅')
            #st.switch_page("app_modif_recipe_page.py")


# Style 
st.markdown('''<style>
            ul{line-height: 130%; margin-bottom : 0;}
            .stMarkdown{margin :auto}
            .test {background-color: #f4846a;}
            .st-key-size_selector input {text-align: center}
            .st-key-size_selector p {font-size: 1rem;}
            .st-key-button-add {text-align: center;}
            .st-key-button-add button {background : #d2a679 ;color:black}
            .st-key-button-add :hover {color : white; border: white;}
            .st-key-button-add :focus {border: #996600}
            .st-key-button-add :focus p {color : #990000}
            .st-key-button_add_week {text-align: center;}
            .st-key-button_add_week button {background : #d2a679 ;color:black}
            .st-key-button_add_week :hover {color : white; border: white;}
            .st-key-button_add_week :focus {border: #996600}
            .st-key-button_add_week :focus p {color : #990000}
            .st-key-button_add_book {text-align: center;}
            .st-key-button_add_book button {background : #d2a679 ;color:black}
            .st-key-button_add_book :hover {color : white; border: white;}
            .st-key-button_add_book :focus {border: #996600}
            .st-key-button_add_book :focus p {color : #990000}
            [data-baseweb='input'] {width:50px;}
            </style>''', unsafe_allow_html=True)


