from fonctions.sql_manager import SQL_recipe_manager
import re
import streamlit as st

sql_manager = SQL_recipe_manager()

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
st.markdown("<h4 '> Etape n°1 - Sélectionnez parmi vos recettes, celles que vous voulez plannifier pour la semaine </h4>", unsafe_allow_html=True)
st.write('---')
# Size choice for each meal
st.markdown("<h4 '> Etape n°2 - Choisir le nombre de repas dans la semaine </h4>", unsafe_allow_html=True)
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
st.write('---')
st.markdown("<h4 '> Etape n°3 - Si vous avez des invités, modifiez le nombre de couverts </h4>", unsafe_allow_html=True)
st.write(" ")
cont_ing = st.container(border=True,key = 'container_ing')
    # Day names
days = ['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']
cols = cont_ing.columns([1,2,2,2,2,2,2,2])
for ind,col in enumerate(cols[1:]) :
    with col :
        st.markdown(f'<span style="color: #DE684D">**{days[ind].title()}**</span>', unsafe_allow_html=True)
cont_ing.write('')

    # Lunch choices
lunch_count_size = 0
cols = cont_ing.columns([1,2,2,2,2,2,2,2])
with cols[0]:
    st.markdown(f'<span style="color: #DE684D">**Midi**</span>', unsafe_allow_html=True)
for ind,col in enumerate(cols[1:]) :
    with col :
        if ind < 5 : # Week day 
            lunch_count_size+= st.number_input("", 0, 20, value = user_param['default_size'] * user_param['default_lunch'], key=f'lunch{days[ind]}', disabled= not user_param['default_lunch'])
        else : # Week end
            lunch_count_size+= st.number_input("", 0, 20, value = user_param['default_size'] * user_param['default_weekend'], key=f'lunch{days[ind]}', disabled= not user_param['default_weekend'])
cont_ing.write('')


    # dinner choices
dinner_count_size = 0
cols = cont_ing.columns([1,2,2,2,2,2,2,2])
with cols[0]:
    st.markdown(f'<span style="color: #DE684D">**Soir**</span>', unsafe_allow_html=True)
for ind,col in enumerate(cols[1:]) :
    with col :
        if ind < 5 :
            dinner_count_size+= st.number_input("", 0, 20, value = user_param['default_size'], key=f'dinner{days[ind]}')
        else :
            dinner_count_size+= st.number_input("", 0, 20, value = user_param['default_size'] * user_param['default_weekend'], key=f'dinner{days[ind]}',disabled= not user_param['default_weekend'])
cont_ing.write('')
st.write('---')

# Add Recipes

lunch_user_count = 0
dinner_user_count = 0

st.markdown("<h4 '> Etape n°4 - Assigner un nombre de part et un repas pour chaque recette </h4>", unsafe_allow_html=True)
st.write('')

for idx, recipe in planned_recipes.iterrows():
    _, col,_ = st.columns([3,10,3])
    with col :
        st.write('---')
        st.markdown(f"**{recipe['name']}**")
        st.write('')
    _, col_1, col_2= st.columns([2, 3, 3])
    with col_1:
        st.image(recipe['image_link'],width=250)
        st.write('')
    with col_2 :
        lunch_user_count += st.number_input(label="**Midi**", min_value=0, max_value=20, value=recipe['lunch_size'], key=f"recipe_{recipe['id']}_lunch_size")
        dinner_user_count += st.number_input(label="**Soir**", min_value=0, max_value=20, value=recipe['dinner_size'], key=f"recipe_{recipe['id']}_dinner_size")

st.write('---')

st.markdown("<h4 '> Etape n°5 - Une fois le planning terminé, sauvegardez ! </h4>", unsafe_allow_html=True)
st.write('')
# Display meals to plan and save button

col_1, col_2 = st.columns(2)

lunch_count_size -= lunch_user_count
dinner_count_size -= dinner_user_count

with col_1:
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

with col_2:
    if st.button("**Enregistrer**", icon='💾',key='button_save'):
        # Filter les portions dans le session state
        filtre = {k: v for k, v in st.session_state.items() if 'dinner_size' in k or 'lunch_size' in k}
        print(planned_recipes)
        for key, value in filtre.items():
            indice = int(re.findall(r'\d+', key)[0])
            meal = 'dinner' if 'dinner' in key else 'lunch'
            sql_manager.update_recipe_size(user_id=user_id, recipe_id=indice, meal=meal, size=value)
        st.toast("Planning mis à jour", icon='😁')    

# Style
st.markdown('''<style>
            [data-baseweb='input'] {width:40px; text-align: center}
            [data-baseweb='select'] {width:300px;}
            .st-key-container_ing [data-testid='stNumberInputContainer'] {justify-content: center;}
            .st-key-container_ing input {text-align: center}
            .st-key-container_ing .stNumberInput label {display: none;}
            .st-key-container_ing p {text-align: center;margin: auto auto}
            .st-key-container_ing  .stNumberInput > div {margin : auto}
            .st-key-button_save button {background : #f4846a;color:black}
            .st-key-button_save :hover  {color : white}
            </style>''', unsafe_allow_html=True)
