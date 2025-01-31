def profile_page():
    import streamlit as st
    st.markdown("<h4 style='color: #DE684D;'> Data Chef </h4>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'> Mon profil </h2>", unsafe_allow_html=True)
    st.write("")

    with st.sidebar:
        st.button("Accueil")

    if st.button("Accueil", use_container_width=True):
        st.write('test')

    st.markdown("<h5 '> Nombre de part </h5>", unsafe_allow_html=True)
    nb_person = st.slider("Sélectionner le nombre de personne par défaut pour le calcul des quantités d'ingrédients", 1, 12)
    st.text('{} personne.s'.format(nb_person))  