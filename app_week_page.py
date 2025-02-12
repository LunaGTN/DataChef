import streamlit as st
from fonctions.sql_manager import SQL_recipe_manager

sql_manager = SQL_recipe_manager()

# 🟥🟥🟥🟥 Il faut régler le pb des paramètres qui reviennent par défaut quand on change de page 🟥🟥🟥🟥

data = sql_manager.get_profile_info(st.session_state.user_info['id'])
if 'profil_parameters' not in st.session_state :
    st.session_state['profil_parameters'] = {'size' : data[1] if data[1] != None else 4 ,
                                            'diet' : data[2] if data[2] != None else None,
                                            'lunch' : data[3] if data[3] != None else True,
                                            'weekend' : data[4] if data[4] != None else False}

user_param = {
    "default_size": st.session_state.profil_parameters['size'],
    "default_lunch": st.session_state.profil_parameters['lunch'],
    "default_weekend": st.session_state.profil_parameters['weekend']
}

# Request recipes planned
user_id = st.session_state.user_info['id']
planned_recipes = sql_manager.request_planner(user_id=user_id)
planned_recipes.reset_index(drop=True, inplace=True)

# Header / Title
st.markdown("<h2 style='color: #DE684D;'> Mon menu de la semaine</h2>", unsafe_allow_html=True)
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
    if st.checkbox('Prévoir les repas de midi en semaine', value=user_param['default_lunch'] ,key='lunch_selector') != user_param['default_lunch'] :
        user_param['default_lunch'] = st.session_state['lunch_selector']


    if st.checkbox('Prévoir les repas du week-end',value=user_param['default_weekend'], key='weekend_selector') != user_param['default_weekend']:
        user_param['default_weekend'] = st.session_state['weekend_selector']
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
        if ind < 5 : # Week day 
            lunch_count_size+= st.number_input("", 0, 20, value = user_param['default_size'] * user_param['default_lunch'], key=f'lunch{days[ind]}', disabled= not user_param['default_lunch'])
        else : # Week end
            lunch_count_size+= st.number_input("", 0, 20, value = user_param['default_size'] * user_param['default_weekend'], key=f'lunch{days[ind]}', disabled= not user_param['default_weekend'])
st.write('')


    # dinner choices
dinner_count_size = 0
cols = st.columns(8)
with cols[0]:
    st.markdown(f'<span style="color: #DE684D">**Soir**</span>', unsafe_allow_html=True)
for ind,col in enumerate(cols[1:]) :
    with col :
        if ind < 5 :
            dinner_count_size+= st.number_input("", 0, 20, value = user_param['default_size'], key=f'dinner{days[ind]}')
        else :
            dinner_count_size+= st.number_input("", 0, 20, value = user_param['default_size'] * user_param['default_weekend'], key=f'dinner{days[ind]}',disabled= not user_param['default_weekend'])
st.write('')
st.write('---')

# Add Recipes

lunch_user_count = 0
dinner_user_count = 0

st.markdown("<h5 '> Choisir des recettes pour la semaine </h5>", unsafe_allow_html=True)
st.write(" ")

for idx, recipe in planned_recipes.iterrows():
    _, col,_ = st.columns([3,10,3])
    with col :
        st.write('---')
        st.markdown(f"**{recipe['name']}**")
        st.write('')
    _, col_1, col_2, col_3, _ = st.columns([2, 3, 2, 1, 5])
    with col_1:
        st.image(recipe['image_link'],width=250)
        st.write('')
    with col_3:
        st.write('')
        st.write("Midi")
        st.write('')
        st.write('')
        st.write("Soir")
    with col_2 :
        st.write('')
        lunch_user_count += st.number_input(label="Midi", min_value=0, max_value=20, value=0, key=f"recipe_{idx}_lunch_size")
        dinner_user_count += st.number_input(label="Soir", min_value=0, max_value=20, value=0, key=f"recipe_{idx}_dinner_size")

st.write('---')

# Display meals to plan
lunch_count_size -= lunch_user_count
dinner_count_size -= dinner_user_count
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
            p {text-align: center;margin: auto auto}
            .stNumberInput > div {margin : auto}
            </style>''', unsafe_allow_html=True)

#p {text-align: center;margin: auto auto}
#.stNumberInput > div {margin : auto}