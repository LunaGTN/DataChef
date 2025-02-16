from fonctions.sql_manager import SQL_recipe_manager
import streamlit as st
from random import sample

st.write(st.session_state)

sql_manager = SQL_recipe_manager()

df = sql_manager.get_all_recipes()

# Header / Title
st.markdown("<h2 style='color: #DE684D;'>Le catalogue de recettes !</h2>", unsafe_allow_html=True)
st.write("---")

# Filter
    
st.markdown("<h4 style='text-align: center; color: black;'>Filtres</h4>", unsafe_allow_html=True)
st.write(" ")

col_flavor, col_country, col_ingredient = st.columns([1,2,2])

    # Flavor
with col_flavor:
    st.pills('Saveur',["Sucré", "Salé"], default=None, selection_mode='multi', key="taste")
    if 'taste' in st.session_state and len(st.session_state['taste']) !=0:
        tastes = [taste.lower() for taste in st.session_state['taste']]
        flavor_filter =  df['sweet_salt'].isin(tastes)
        df = df[flavor_filter]

    # Country
with col_country:
    if 'countries' in st.session_state:
        default_country = st.session_state['countries']
    else:
        default_country=None
    countries = list(df['country'].unique())

    st.multiselect('Nationalités', countries, key='countries', default=default_country, placeholder='Choisissez la nationalité des plats')
    if 'countries' in st.session_state and len(st.session_state['countries']) !=0:
        origines = st.session_state['countries']
        origines =  df['country'].isin(origines)
        df = df[origines]

    # Ingredients
with col_ingredient:
    if 'ingredients' in st.session_state:
        default_ingredient = st.session_state['ingredients']
    else:
        default_ingredient=None
    ingredient_list = list(df['ingredient_list'].values)
    ingredient_list = set((','.join(ingredient_list)).split(','))

    st.multiselect('Ingredients', ingredient_list, key='ingredients', default=default_ingredient, placeholder='Choisissez vos ingrédients')
    if 'ingredients' in st.session_state and len(st.session_state['ingredients']) !=0:
        ingredient_list = st.session_state['ingredients']
        for ingredient in ingredient_list:
            ingredient_filter =  df['ingredient_list'].str.contains(ingredient)
            df = df[ingredient_filter]

st.write('')

def create_short_list():
    receipe_list = list(zip(df['name'].values,df['image_link'].values))
    k = 12
    if len(df) > k:
        st.session_state.short_list = sample(receipe_list, k=k)
    else:
        st.session_state.short_list = sample(receipe_list, k=len(df))

     
if 'short_list' not in st.session_state :
    create_short_list()

if st.button("🔄 **Changer les propositions**",key='suggestion_button') :
    create_short_list()
st.write(' ')

# Recipe suggestion
    # Title
st.markdown("<h4 style='text-align: center; color: black;'>Nos idées recettes</h4>", unsafe_allow_html=True)
st.write(" ")

    # Containers

if len(df) == 0:
    st.subheader("Oups 😕\nIl n'y a pas de recette correspondant à vos critères dans le catalogue ")

n_cols = 3
n_rows = len(df) // n_cols
remains = len(df) % n_cols

if len(df) >= n_cols:
    for raw in range(3) :
        col_list = st.columns(4)
        for n_col,col in enumerate(col_list) :
            ind = raw*4 + n_col
            with col :  
                st.image(st.session_state.short_list[ind][1])
                if st.button(label=st.session_state.short_list[ind][0], key=f'but_{ind}',use_container_width =True) :
                    idx = df[df['name']==st.session_state.short_list[ind][0]]['id'].values[0]
                    st.session_state.current_receipe = sql_manager.get_recipe_detail(idx)
                    st.switch_page("app_page_show_recipe.py")
                    
if remains != 0:
    col_list = st.columns(n_cols)
    df_temp = df.tail(remains).reset_index(drop=True)
    for idx, col in enumerate(col_list[0:remains]):
        indice =  df_temp.iloc[idx]['id']
        with col : 
            st.image(df_temp.iloc[idx]['image_link'])
            if st.button(label=df_temp.iloc[idx]['name'], key=f'but_{indice}',use_container_width =True) :
                st.session_state.current_receipe = sql_manager.get_recipe_detail(indice)
                st.switch_page("app_page_show_recipe.py")

# Style 
st.markdown('''<style>
            .st-key-suggestion_button {text-align: center}
            .st-key-suggestion_button button {background : #f4846a;color:black}
            .st-key-suggestion_button :hover  {color : white}
            </style>''', unsafe_allow_html=True)
