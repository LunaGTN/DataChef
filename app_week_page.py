import streamlit as st
from fonctions.sql_manager import SQL_recipe_manager

# Request recipes planned
user_id = st.session_state.user_info['id']
sql_manager = SQL_recipe_manager()
planned_recipes = sql_manager.request_planner(user_id=user_id)
planned_recipes.reset_index(drop=True, inplace=True)

# Header / Title
st.markdown("<h2 style='color: #DE684D;'> Mes menus de la semaine</h2>", unsafe_allow_html=True)
st.write('---')

# Size choice for each meal
st.markdown("<h5 '> Choisir le nombre de part pour chaque repas </h5>", unsafe_allow_html=True)
st.write(" ")
st.write('')

    # Filters
_, col = st.columns([1,10])
disa_we = True
disa_lunch = False
with col :
    if st.checkbox('Prévoir les repas de midi en semaine', key='lunch_selector') == False :
        disa_lunch = True
        testvalue = 0
    if st.checkbox('Prévoir les repas du week-end',value=False) :
        disa_we = False
st.write('')
st.write('')

    # Day names
days = ['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']
cols = st.columns(8)
for ind,col in enumerate(cols[1:]) :
    with col :
        st.markdown(f'<span style="color: #DE684D">**{days[ind].title()}**</span>', unsafe_allow_html=True)
st.write('')

    # Lunch choices
lunch_count_size = 0
cols = st.columns(8)
with cols[0]:
    st.markdown(f'<span style="color: #DE684D">**Midi**</span>', unsafe_allow_html=True)
for ind,col in enumerate(cols[1:]) :
    with col :
        if ind < 5 :
            lunch_count_size+= st.number_input("", 0, 20,value = 0 ,key=f'lunch{days[ind]}',disabled=disa_lunch)
        else :
            lunch_count_size+= st.number_input("", 0, 20,value = 0 ,key=f'lunch{days[ind]}',disabled=disa_we)
st.write('')


    # dinner choices
dinner_count_size = 0
cols = st.columns(8)
with cols[0]:
    st.markdown(f'<span style="color: #DE684D">**Soir**</span>', unsafe_allow_html=True)
for ind,col in enumerate(cols[1:]) :
    with col :
        if ind < 5 :
            dinner_count_size+= st.number_input("", 0, 20,value = 0 ,key=f'dinner{days[ind]}')
        else :
            dinner_count_size+= st.number_input("", 0, 20,value = 0 ,key=f'dinner{days[ind]}',disabled=disa_we)
st.write('')
st.write('---')

# Add Recipes
st.markdown("<h5 '> Choisir des recettes pour la semaine </h5>", unsafe_allow_html=True)
st.write(" ")

n_cols = 4
n_rows = len(planned_recipes) // n_cols
remains = len(planned_recipes) % n_cols

for row in range(n_rows) :
    col_list = st.columns(n_cols)
    for idx, col in enumerate(col_list) :
        index = row * n_cols + idx
        with col :  
            st.image(planned_recipes.iloc[index]['image_link'], width=1000)
            if st.button(label=planned_recipes.iloc[index]['name'], key=f'but_{index}',use_container_width =True) :
                idx = planned_recipes.iloc[index]['id']


if remains != 0:
    col_list = st.columns(n_cols)
    df_temp = planned_recipes.tail(remains).reset_index(drop=True)
    for idx, col in enumerate(col_list[0:remains]):
        with col:
            st.image(df_temp.iloc[idx]['image_link'], width=1000)
            if st.button(label=df_temp.iloc[idx]['name'], key=f'but_{n_rows*4+idx}', use_container_width=True):
                idx = df_temp.iloc[idx]['id']


st.write('---')

# Display meals to plan
if lunch_count_size == 0 :
    st.markdown(f'##### ✅ Tous vos repas de midi sont prévus', unsafe_allow_html=True)
elif lunch_count_size < 0 :
    st.markdown(f'##### ❌ <span style="color: red">Trop de parts pour les repas du midi</span>', unsafe_allow_html=True)
else :
    st.markdown(f'##### Il reste <span style="color: #DE684D">**{lunch_count_size} parts**</span> à prévoir pour les repas de midi', unsafe_allow_html=True)
if dinner_count_size == 0 :
    st.markdown(f'##### ✅ Tous vos repas du soir sont prévus', unsafe_allow_html=True)
elif dinner_count_size <0 :
    st.markdown(f'##### ❌ <span style="color: red">Trop de parts pour les repas du soir</span>', unsafe_allow_html=True)
else :
    st.write(f'##### Il reste <span style="color: #DE684D">**{dinner_count_size} parts**</span> à prévoir pour les repas du soir', unsafe_allow_html=True)


# Style
st.markdown('''<style>
            [data-baseweb='input'] {width:40px; text-align: center}
            [data-baseweb='select'] {width:300px;}
            [data-testid='stNumberInputContainer'] {justify-content: center;}
            input {text-align: center}
            .stNumberInput label {display: none;}
            .stNumberInput > div {margin : auto}
            p {text-align: center;margin: auto auto}
            </style>''', unsafe_allow_html=True)
