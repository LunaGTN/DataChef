def profile_page():

    import streamlit as st

# Header / Title
    st.markdown("<h2 style='color: #DE684D;'> Mon profil </h4>", unsafe_allow_html=True)
    st.write('---')


# Collect of user data 🟥🟥🟥🟥 Need to be update with SQL request 🟥🟥🟥🟥
    nb_person = 4
    diet = []


#  Choice of default nb of portion
    st.markdown("<h5 '> Nombre de part par défaut </h5>", unsafe_allow_html=True)

    nb_person = st.slider("Sélectionner le nombre de personne par défaut pour le calcul des quantités d'ingrédients", 1, 12,value = nb_person )
    if nb_person == 1 :
        st.text(f'Les quantités seront calculées par défaut pour {nb_person} personne')  
    elif nb_person > 1 : 
        st.markdown(f'Les quantités seront calculées par défaut pour **{nb_person}** personnes')  
    
    st.write("---")


#  Choice of diet
    st.markdown("<h5 '> Régime alimentaire </h5>", unsafe_allow_html=True)
    diet = st.multiselect('Choisir un ou plusieurs régime(s) alimentaire(s) spécifique(s)',
                          ['Végétarien','Vegan','Sans Gluten','Sans Lactose'],
                          placeholder = 'Choisir un régime',
                          default = diet)


    # Il reste à sauvegarder les variables np_person et diet dans la BDD