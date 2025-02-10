import streamlit as st

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
    if st.checkbox('Prévoir les repas de midi en semaine',value=True) == False :
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
