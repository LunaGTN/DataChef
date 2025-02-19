import streamlit as st
from fonctions.sql_manager import SQL_recipe_manager

sql_manager = SQL_recipe_manager()

# Header / Title
st.markdown("<h2 style='color: #DE684D;'> Mon profil </h4>", unsafe_allow_html=True)
st.write('---')


# Collect of user data
data = sql_manager.get_profile_info(st.session_state.user_info['id'])
if 'profil_parameters' not in st.session_state :
    st.session_state['profil_parameters'] = {'size' : data[1] if data[1] != None else 4 ,
                                            #'diet' : data[2] if data[2] != None and data[2] != [''] else None,
                                            'lunch' : data[3] if data[3] != None else True,
                                            'weekend' : data[4] if data[4] != None else False}


# Choice of default nb of portion
st.markdown("<h5 '> Paramètres par défaut pour le semainier</h5>", unsafe_allow_html=True)
st.number_input("Nombre de personnes par repas par défaut", 1, 12,value = st.session_state.profil_parameters['size'],key='size_test')
st.checkbox('Prévoir les repas de midi en semaine',value=st.session_state.profil_parameters['lunch'],key='lunch_selec')
st.checkbox('Prévoir les repas du week-end',value=st.session_state.profil_parameters['weekend'], key ='weekend_selec')
st.write("---")


#  Choice of diet
# st.markdown("<h5 '> Régime alimentaire </h5>", unsafe_allow_html=True)
# st.multiselect('Choisir un ou plusieurs régime(s) alimentaire(s) spécifique(s)',
#                         ['Végétarien','Vegan','Sans Gluten','Sans Lactose'],
#                         placeholder = 'Choisir un régime',
#                         default = st.session_state.profil_parameters['diet'],
#                         key ='diet')
# st.write("---")

# Save button
if st.button('💾 **Enregistrer**',key='save') :
    st.session_state.profil_parameters['size'] = st.session_state['size_test']
    st.session_state.profil_parameters['lunch'] = st.session_state['lunch_selec']
    st.session_state.profil_parameters['weekend'] = st.session_state['weekend_selec']
    #st.session_state.profil_parameters['diet'] = st.session_state['diet']
    sql_manager.add_user_info(st.session_state.user_info, st.session_state.profil_parameters)
    st.toast('Profil mis à jour', icon='🧑‍🍳')


# Style 
st.markdown('''<style>
            [data-baseweb='input'] {width:50px; text-align: center}
            [data-baseweb='select'] {width:300px;}
            input {text-align: center}
            .st-key-save {text-align: center;}
            .st-key-save button {background : #d2a679 ;color:black}
            .st-key-save :hover {color : white; border: white;}
            .st-key-save :focus {border: #996600}
            .st-key-save :focus p {color : #990000}
            </style>''', unsafe_allow_html=True)



