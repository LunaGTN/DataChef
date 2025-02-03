import streamlit as st

def receipe_page():

# Header / Title
    st.markdown("<h2 style='color: #DE684D;'> Recettes </h2>", unsafe_allow_html=True)
    st.write('---')


# Receipe Selection
    # Receipe list creation for the selectbox
    receipe_list = ['Lasagnes à la bolognaise','Choucroute']  # 🟥🟥🟥🟥 Need to be update with SQL request 🟥🟥🟥🟥

    # Automatic selection if user already choose a receipe from another page
    if "current_receipe_name" not in st.session_state or st.session_state.current_receipe_name == None:
        receipe_index = None
    else :
        receipe_index = receipe_list.index(st.session_state.current_receipe_name)

    # Selectbox for receipe choice
    st.session_state.current_receipe_name = st.selectbox("", receipe_list, index = receipe_index, placeholder= 'Choisir une recette dans la liste')
    st.write('---')


    # 🟥🟥🟥🟥 Need to be update with SQL request 🟥🟥🟥🟥
    current_receipe = {'titre': 'Lasagnes à la bolognaise',
    'lien': 'https://www.marmiton.org/recettes/recette_lasagnes-a-la-bolognaise_18215.aspx',
    'id': '18215',
    'temps_preparation': '30 min',
    'tems_repos': '-',
    'temps_cuisson': '1h35',
    'image': 'https://assets.afcdn.com/recipe/20200408/109520_w300h200c1cx1866cy2800cxt0cyt0cxb3732cyb5600.webp',
    'nb_personne': '8',
    'temps_total': '2h05',
    'difficulte': 'moyenne',
    'cout': 'moyen',
    'etapes': ["Faire revenir gousses hachées d'ail et les oignons émincés dans un peu d'huile d'olive.",
    'Ajouter la carotte et la branche de céleri hachée puis la viande et faire revenir le tout.',
    "Au bout de quelques minutes, ajouter le vin rouge. Laisser cuire jusqu'à évaporation.",
    "Ajouter la purée de tomates, l'eau et les herbes.\nSaler, poivrer, puis laisser mijoter à feu doux 45 minutes.",
    'Préparer la béchamel : faire fondre 100 g de beurre.',
    "Hors du feu, ajouter la farine d'un coup.",
    "Remettre sur le feu et remuer avec un fouet jusqu'à l'obtention d'un mélange bien lisse. ",
    'Ajouter le lait peu à peu.',
    "Remuer sans cesse, jusqu'à ce que le mélange s'épaississe.",
    'Ensuite, parfumer avec la muscade, saler, poivrer. Laisser cuire environ 5 minutes, à feu très doux, en remuant. Réserver.',
    "Préchauffer le four à 200°C (thermostat 6-7).\nHuiler le plat à lasagnes. Poser une fine couche de béchamel puis des feuilles de lasagnes, de la bolognaise, de la béchamel et du parmesan.\nRépéter l'opération 3 fois de suite.",
    'Sur la dernière couche de lasagnes, ne mettre que de la béchamel et recouvrir de fromage râpé. Parsemer quelques noisettes de beurre.',
    'Enfourner pour environ 25 minutes de cuisson.',
    'Déguster'],
    'ingredients': [{'nom': 'beurre', 'quantite': '125', 'unite': 'g', 'id': '3'},
    {'nom': 'farine', 'quantite': '100', 'unite': 'g', 'id': '89'},
    {'nom': 'poivre', 'quantite': '0', 'unite': '', 'id': '35'},
    {'nom': 'sel', 'quantite': '0', 'unite': '', 'id': '90'},
    {'nom': 'fromage râpé', 'quantite': '70', 'unite': 'g', 'id': '225'},
    {'nom': 'muscade', 'quantite': '3', 'unite': 'pincée', 'id': '89'},
    {'nom': 'thym', 'quantite': '0', 'unite': '', 'id': '051'},
    {'nom': 'feuilles de laurier', 'quantite': '2', 'unite': '', 'id': '635'},
    {'nom': 'vin rouge', 'quantite': '20', 'unite': 'cl', 'id': '222'},
    {'nom': 'purée de tomate', 'quantite': '800', 'unite': 'g', 'id': '583'},
    {'nom': 'carottes', 'quantite': '1', 'unite': '', 'id': '72'},
    {'nom': 'oignons jaunes', 'quantite': '3', 'unite': '', 'id': '150'},
    {'nom': 'lasagnes', 'quantite': '1', 'unite': 'paquet', 'id': '91'},
    {'nom': 'ail', 'quantite': '2', 'unite': 'gousse', 'id': '0'},
    {'nom': 'céleri', 'quantite': '1', 'unite': 'branche', 'id': '83'},
    {'nom': 'boeuf haché', 'quantite': '600', 'unite': 'g', 'id': '758'},
    {'nom': 'eau', 'quantite': '15', 'unite': 'cl', 'id': '381'},
    {'nom': 'basilic', 'quantite': '0', 'unite': '', 'id': '6'},
    {'nom': 'Parmesan', 'quantite': '125', 'unite': 'g', 'id': '67'},
    {'nom': 'lait', 'quantite': '1', 'unite': 'l', 'id': '64'}]}


# Display receipe and details 
    # First line (picture and name)
    col1, _ , col2 = st.columns([2,0.4,5])
    with col1:
        st.image(current_receipe['image'],width=1000)

    with col2:
        st.markdown(f"<h2 style='text-align: center; color: black;'> {current_receipe['titre']} </h2>", unsafe_allow_html=True)

    st.write(' ')

    # Lists of ingredients and steps
    col1, _ , col2 = st.columns([2,0.4,5])

    with col1 :
        container = st.container(border=True)
        for ing in current_receipe['ingredients'] :
            if ing['quantite'] == '0' :
                result = f"**{ing['nom']}**"
            elif ing['unite'] == '' :
                result = f"{ing['quantite']} **{ing['nom']}**"
            else :
                result = f"{ing['quantite']} {ing['unite']} de **{ing['nom']}**"
        
            container.markdown(f'- {result}')
        container.write(' ')


    with col2 :
        for ind, step in enumerate(current_receipe['etapes']) :
                st.checkbox(f'**Etape {ind+1} :** {step}')
        



# Style 
    st.markdown('''<style>
                ul{line-height: 130%; margin-bottom : 0;}
                .stMarkdown{margin :auto}
                </style>''', unsafe_allow_html=True)
    