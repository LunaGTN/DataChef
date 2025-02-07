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
                    st.switch_page("app_receipe_page.py")



# Style 
st.markdown('''<style>
            .st-key-suggestion_button {text-align: center}
            </style>''', unsafe_allow_html=True)
