from fonctions.sql_manager import SQL_recipe_manager
import streamlit as st
import re

sql_manager = SQL_recipe_manager()
user_id = st.session_state.user_info['id']

df_user = sql_manager.get_user_recipes(user_id=user_id)
df_user.reset_index(drop=True, inplace=True)

# Header / Title
st.markdown("<h2 style='color: #DE684D;'>Bienvenue sur Data Chef !</h2>", unsafe_allow_html=True) 
st.write("---")

# User Recipe
    # Title
st.markdown("<h4 style='text-align: center; color: black;'>Mes recettes</h4>", unsafe_allow_html=True)
st.write(" ")
  

    # Containers

n_cols = 4
n_rows = len(df_user) // n_cols
remains = len(df_user) % n_cols

for row in range(n_rows) :
    col_list = st.columns(n_cols)
    for idx, col in enumerate(col_list) :
        index = row * n_cols + idx
        indice = df_user.iloc[index]['id']
        in_planner = sql_manager.check_recipe_in_user_planning(user_id=user_id, recipe_id=indice)
        with col :
            st.image(df_user.iloc[index]['image_link'], width=1000)
            if st.button(label=df_user.iloc[index]['name'][2:].capitalize(), key=f'but_{index}',use_container_width =True) :
                st.session_state.current_receipe = sql_manager.get_recipe_detail(indice)
                st.switch_page("app_receipe_page.py")
            st.checkbox(label='dans le planning', value=in_planner, key=f'check_{indice}')
            if st.button('Supprimer', icon='❌', key=f'del_{indice}'):
                if sql_manager.delete_user_recipe(user_id=user_id, recipe_id=indice):
                    st.toast('Recette supprimée de mon livre', icon=':material/ink_eraser:')
                    st.rerun()
                else:
                    st.toast("Une erreur s'est produite", icon='❌')
            
if remains != 0:
    col_list = st.columns(n_cols)
    df_temp = df_user.tail(remains).reset_index(drop=True)
    for idx, col in enumerate(col_list[0:remains]):
        indice =  df_temp.iloc[idx]['id']
        in_planner = sql_manager.check_recipe_in_user_planning(user_id=user_id, recipe_id=indice)
        with col:
            st.image(df_temp.iloc[idx]['image_link'], width=1000)
            if st.button(label=df_temp.iloc[idx]['name'][2:].capitalize(), key=f'but_{n_rows*4+idx}', use_container_width=True):
                st.session_state.current_recipe = sql_manager.get_recipe_detail(id_recipe=indice)
                st.switch_page("app_receipe_page.py")
            st.checkbox(label='dans le planning', value=in_planner, key=f'check_{indice}')
            if st.button('Supprimer', icon='❌', key=f'del_{indice}'):
                if sql_manager.delete_user_recipe(user_id=user_id, recipe_id=indice):
                    st.toast('Recette supprimée de mon livre', icon=':material/ink_eraser:')
                    st.rerun()
                else:
                    st.toast("Une erreur s'est produite", icon='❌')


filtre = {k: v for k, v in st.session_state.items() if 'check' in k}
for key, value in filtre.items():
    idx = int(re.findall(r'\d+', key)[0])
    if value != sql_manager.check_recipe_in_user_planning(user_id=user_id, recipe_id=idx):
        sql_manager.update_recipe_in_planner(
            user_id=user_id,
            recipe_id=idx
        )

# Style 
st.markdown('''<style>
            .st-key-suggestion_button {text-align: center}
            </style>''', unsafe_allow_html=True)
