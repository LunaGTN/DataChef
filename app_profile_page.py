import streamlit as st

# Header / Title
st.markdown("<h2 style='color: #DE684D;'> Mon profil </h4>", unsafe_allow_html=True)
st.write('---')


# Collect of user data 🟥🟥🟥🟥 Need to be update with SQL request 🟥🟥🟥🟥
if 'week_parameters' not in st.session_state :
    st.session_state['profil_parameters'] = {'size' : 4,
                                       'diet' : [],
                                       'lunch' : False,
                                       'weekend' : False}


# Choice of default nb of portion
st.markdown("<h5 '> Paramètres par défaut pour le semainier</h5>", unsafe_allow_html=True)
st.number_input("Nombre de parts par défaut", 1, 12,value = st.session_state.week_parameters['size'],key='size_test')
st.checkbox('Prévoir les repas de midi en semaine',value=st.session_state.week_parameters['lunch'],key='lunch_selec')
st.checkbox('Prévoir les repas du week-end',value=st.session_state.week_parameters['weekend'], key ='weekend_selec')
st.write("---")

# st.session_state.week_parameters['size'] = st.session_state['size_test'

#  Choice of diet
st.markdown("<h5 '> Régime alimentaire </h5>", unsafe_allow_html=True)
diet = st.multiselect('Choisir un ou plusieurs régime(s) alimentaire(s) spécifique(s)',
                        ['Végétarien','Vegan','Sans Gluten','Sans Lactose'],
                        placeholder = 'Choisir un régime',
                        default = st.session_state.week_parameters['diet'])
st.write("---")


if st.button('Enregistrer') :
    st.session_state.profil_parameters['size'] = st.session_state['size_test']
    st.session_state.profil_parameters['lunch'] = st.session_state['lunch_selec']
    st.session_state.profil_parameters['weekend'] = st.session_state['weekend_selec']


# Il reste à sauvegarder les variables np_person et diet dans la BDD
st.markdown('''<style>
            [data-baseweb='input'] {width:50px; text-align: center}
            [data-baseweb='select'] {width:300px;}
            input {text-align: center}
            </style>''', unsafe_allow_html=True)

