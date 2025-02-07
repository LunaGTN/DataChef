from data_exporters.sql_manager import SQL_recipe_manager
import streamlit as st
from random import choices

sql_manager = SQL_recipe_manager()

df_user = sql_manager.get_user_recipes(user_id=st.session_state.user_info['id'])
df_user.reset_index(drop=True, inplace=True)


# Header / Title
st.markdown("<h2 style='color: #DE684D;'>Bienvenue sur Data Chef !</h2>", unsafe_allow_html=True)
st.write("---")

# User Recipe
    # Title
st.markdown("<h4 style='text-align: center; color: black;'>Mes recettes</h4>", unsafe_allow_html=True)
st.write(" ")
  

    # Containers

n_cols = 3
n_rows = len(df_user) // n_cols
remains = len(df_user) % n_cols

for row in range(n_rows) :
    col_list = st.columns(n_cols)
    for idx, col in enumerate(col_list) :
        index = row * n_cols + idx
        with col :  
            st.image(df_user.iloc[index]['image_link'], width=1000)
            if st.button(label=df_user.iloc[index]['name'], key=f'but_{index}',use_container_width =True) :
                idx = df_user.iloc[index]['id']
                st.session_state.current_receipe = sql_manager.get_recipe_detail(idx)
                st.switch_page("app_receipe_page.py")

if remains != 0:
    col_list = st.columns(n_cols)
    df_temp = df_user.tail(remains).reset_index(drop=True)
    for idx, col in enumerate(col_list[0:remains]):
        with col:
            st.image(df_temp.iloc[idx]['image_link'], width=1000)
            if st.button(label=df_temp.iloc[idx]['name'], key=f'but_{n_rows*4+idx}', use_container_width=True):
                idx = df_temp.iloc[idx]['id']
                st.session_state.current_recipe = sql_manager.get_recipe_detail(id_recipe=idx)
                st.switch_page("app_receipe_page.py")


# Style 
st.markdown('''<style>
            .st-key-suggestion_button {text-align: center}
            </style>''', unsafe_allow_html=True)
