import streamlit as st

# Header / Title
st.markdown("<h2 style='color: #DE684D;'>Bienvenue sur Data Chef !</h2>", unsafe_allow_html=True)
st.write("---")

# Recipe suggestion
st.markdown("<h4 style='text-align: center; color: black;'>Nos idées recettes</h4>", unsafe_allow_html=True)
st.write(" ")

for row in range(3) :
    col_list = st.columns(4)
    for col in col_list :
        with col :
            cont = st.container(border= True, height= 150)
            cont.write("🚩")
    st.write(" ")
