import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from fonctions.dashboard_func import get_weekly_recipe, get_weekly_ingredient, metric_system, conversion, card, nb_conso_per_recipe,get_nb_repas
from streamlit_extras.let_it_rain import rain
from time import sleep

st.markdown("""
<style>
    .st-bb {margin:auto auto;
            text-align:center}
    .st-br div {text-align:center}
<style>
""", unsafe_allow_html=True)

user_id = st.session_state['user_info']['id']

color_palet = px.colors.sequential.RdBu
recettes_hebdo = pd.DataFrame(get_weekly_recipe(str(user_id)))

@st.dialog(" ", width='small', )
def vote():
    st.markdown("# Merci de votre attention")
    st.markdown("## Merci Léo")

# Header / Title / Bonus 
col_1, col_2 = st.columns([8,2], vertical_alignment='center')
with col_1:
    st.markdown("<h2 style='color: #DE684D;'> Votre Dashboard hebdomadaire 🧐</h2>", unsafe_allow_html=True)
with col_2:
    if st.button('Fin de présentation', icon='🎁'):
        vote()
        rain(emoji='♥️', font_size=50, falling_speed=5, animation_length='infinite')
        sleep(0.5)
        rain(emoji='♠️', font_size=50, falling_speed=3, animation_length='infinite')
        sleep(0.5)
        rain(emoji='♦️', font_size=50, falling_speed=4, animation_length='infinite')
        sleep(0.5)
        rain(emoji='♣️', font_size=50, falling_speed=4, animation_length='infinite')
st.write('---')

if len(recettes_hebdo) != 0:

    data_ingredient = get_weekly_ingredient(str(user_id))
    dico_qtity = []  # Liste pour stocker les nouvelles quantités d'ingrédients
    conso_recette_hebdo = nb_conso_per_recipe(user_id,recettes_hebdo)  # Nombre de fois que la personne consomme chaque recette

    for ingredient in data_ingredient:
        quantity_g = metric_system(ingredient)
        # Normalisation à 1 personne et ajustement pour la consommation hebdomadaire
        normalized_quantity = round((quantity_g /ingredient['nb_person']) * conso_recette_hebdo)
        if ingredient["category"] != 'Autre':  # Exclusion des catégories "Autre"
            dico_qtity.append({
                "Nom":ingredient["name"],
                "Catégorie": ingredient["category"],
                "Quantité": normalized_quantity})

    df = pd.DataFrame(dico_qtity)

    if len(recettes_hebdo) == 1:
        st.subheader(f"Il y a {recettes_hebdo.shape[0]} recette dans votre semainier !")
    else:
        st.subheader(f"Il y a {recettes_hebdo.shape[0]} recettes dans votre semainier !")
    st.write('')

    col1, col2 , col3, col4 = st.columns([2,2,2,3])
    with col1 :
        prep_mean = card(recettes_hebdo['prepa'].mean(), 'Temps de préparation moyen')
        st.plotly_chart(prep_mean)
    with col2:
        prep_sum = card(recettes_hebdo['prepa'].sum(), 'Temps de préparation Total')
        st.plotly_chart(prep_sum)
    with col3:
        sum_cook = card(recettes_hebdo['cuisson'].sum(), 'Temps de cuisson Total')
        st.plotly_chart(sum_cook)

    with col4:
        st.write("""**Top 3 des ingrédients** """)
        df = df.rename(columns = {'Quantité': 'Quantité (g)'})
        top_3 = df.sort_values(by = 'Quantité (g)', ascending = False).head(3).reset_index(drop = True)
        top_3.index = top_3.index + 1
        st.write(top_3)
        with st.expander("Explications"):
            st.write("""Voici les 3 ingrédients les plus consommés cette semaine en termes de quantité.
                    Il s'agit des quantités **en grammes, pour une personne**.
                    Cette visualisation vous montre les ingrédients qui apparaissent le plus souvent dans
                    vos repas, vous permettant ainsi de mieux comprendre les tendances de votre alimentation hebdomadaire. """)


    col1, col2, col3 = st.columns([1,1.5,1.5])
    with col1:
        # Pie chart Nationalité
        data_origin = recettes_hebdo['pays'].value_counts()
        origin_chart = px.pie(data_origin, data_origin.index, values=data_origin.values, title='Répartition de la nationalité des recettes',
                    color_discrete_sequence=color_palet,
                    width = 400, height = 400 )

        st.plotly_chart(origin_chart)

        with st.expander("Explications"):
            st.write("""
                    Cette visualisation permet de mieux comprendre la diversité culinaire du menu
                    hebdomadaire et d’évaluer l’équilibre entre différentes influences gastronomiques.
                    """)
    with col2:
        # Durée de préparation
        bar_duration = px.bar(
            recettes_hebdo, 
            x=recettes_hebdo.index, 
            y=["prepa", "cuisson"],  # Empilage des deux colonnes
            title="Temps de préparation et de cuisson des recettes",
            labels={"value": "Temps (min)", "variable": "Type de temps", "x": "Recettes"},
            color_discrete_map={"prepa": color_palet[0], "cuisson": color_palet[2]},
            text_auto = True,
            width = 580, height = 400 # Couleurs personnalisées
        )
        bar_duration.update_layout(
            xaxis_title="Recette",
            yaxis_title="Temps Total (min)",
        )
        st.plotly_chart(bar_duration)
        with st.expander("Recettes"):
            st.write(recettes_hebdo['name'])
            
        with st.expander("Explications"):
            st.write("""
                    Ce graphique vous aide à organiser vos recettes en fonction du temps que vous avez devant vous.
                    Chaque barre représente une recette. La couleur la plus foncée montre le temps de préparation,
                    en plus clair, le temps de cuisson. Sur l'axe vertical, vous voyez le temps total.
                    Cette visualisation vous permet de mieux planifier votre semaine en un coup d’œil.""")
            st.write('')

    with col3:
        data = df.drop(columns = 'Nom').groupby('Catégorie').sum()
        data = data.sort_values(by = 'Quantité (g)', ascending = False)
        bar_qtity = px.bar(data, x='Quantité (g)', y=data.index, orientation='h',
                        title='Quantité consommée par catégorie',
                        color_discrete_sequence=color_palet,
                        color=data.index,
                        text_auto = True,
                        width = 570, height = 400 )
        bar_qtity.update_layout(
            xaxis_title="Quantité (g)",
            yaxis_title="",
        )
        st.plotly_chart(bar_qtity)
        with st.expander("Explications"):
            st.write("""
                    Ce graphique montre la quantité totale en grammes de chaque catégorie d'ingrédients utilisée dans
                    vos recettes.
                    Il s'agit de la **quantité pour une personne sur toute la semaine**. 
                    Il vous permet de visualiser rapidement quelles catégories sont les plus présentes
                    dans vos repas, en termes de poids.
                    Cela peut vous aider à mieux équilibrer vos repas ou encore à identifier des catégories qui sont très représentées.""")

else:
    st.subheader(f"Il n'y a pas de recette dans votre semainier !")
    st.write('')

    st.write('Préparez votre semainier pour profiter de votre dashboard complet')

    col1, col2 = st.columns(2)
    with col1:
        if st.button("**Voir mon livre de recettes**", icon='📕',key='recipe_book'):
            st.switch_page('app_page_recipe_book.py')
    with col2:
        if st.button("**Découvrir des plats**", icon='🥙',key='suggestions'):
            st.switch_page('app_page_suggestions.py')

# Style 
st.markdown('''<style>
            .st-key-recipe_book {text-align: center;}
            .st-key-recipe_book button {background : #d2a679 ;color:black}
            .st-key-recipe_book :hover {color : white; border: white;}
            .st-key-recipe_book :focus {border: #996600}
            .st-key-recipe_book :focus p {color : #990000}
            .st-key-suggestions {text-align: center;}
            .st-key-suggestions button {background : #d2a679 ;color:black}
            .st-key-suggestions :hover {color : white; border: white;}
            .st-key-suggestions :focus {border: #996600}
            .st-key-suggestions :focus p {color : #990000}
            </style>''', unsafe_allow_html=True)
