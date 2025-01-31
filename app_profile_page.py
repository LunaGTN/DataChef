def profile_page():
    import streamlit as st
    st.markdown("<h2 style='color: #DE684D;'> Data Chef </h4>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: black;'> Mon profil </h2>", unsafe_allow_html=True)

    # Il faut initialiser les variables suivantes avec des valeurs issues de la BDD
    nb_person = 4
    diet = []


    st.write("---")

    nb_person = 10
    st.markdown("<h5 '> Nombre de part </h5>", unsafe_allow_html=True)

    nb_person = st.slider("Sélectionner le nombre de personne par défaut pour le calcul des quantités d'ingrédients", 1, 12,value = nb_person )
    if nb_person == 1 :
        st.text(f'Vos recettes sont par défaut pour {nb_person} personne')  
    elif nb_person > 1 : 
        st.text(f'Vos recettes sont par défaut pour {nb_person} personnes')  
    
    st.write("---")

    st.markdown("<h5 '> Régime alimentaire </h5>", unsafe_allow_html=True)
    diet = st.multiselect('Choisir un ou plusieurs régime(s) alimentaire(s) spécifique(s)',['Végétarien','Vegan','Sans Gluten','Sans Lactose'],default=diet)


    # Il reste à sauvegarder les variables np_person et diet dans la BDD