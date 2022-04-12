import streamlit as st
import numpy as np
import pandas as pd
import pickle



st.image('images/h&m.webp', width=100)

# Champ de saisi du customer id
customer_id = st.text_input('Customer ID',)

if(st.button('Login')):
    result = customer_id.title().lower()
    # st.success(result)
    with open('data_test.json', 'rb') as fp:
        data = pickle.load(fp)

    customerX = data[result]  
    np.loadtxt('baseline_test.txt', dtype=int)

    st.markdown("""## Catégories tendance""")
    col1, col2, col3, col4, col5, col6= st.columns(6)

    with col1:
        st.image(f'images/0{customerX[0]}.jpg', width=100)

    with col2:
        st.image(f'images/0{customerX[1]}.jpg', width=100)

    with col3:
        st.image(f'images/0{customerX[2]}.jpg', width=100)

    with col4:
        st.image(f'images/0{customerX[3]}.jpg', width=100)

    with col5:
        st.image(f'images/0{customerX[4]}.jpg', width=100)

    with col6:
        st.image(f'images/0{customerX[5]}.jpg', width=100)

    #Deuxiéme ligne des ligne
    col11, col12, col13, col14, col15, col16= st.columns(6)

    with col11:
        st.image(f'images/0{customerX[6]}.jpg', width=100)

    with col12:
        st.image(f'images/0{customerX[7]}.jpg', width=100)

    with col13:
        st.image(f'images/0{customerX[8]}.jpg', width=100)

    with col14:
        st.image(f'images/0{customerX[9]}.jpg', width=100)

    with col15:
        st.image(f'images/0{customerX[10]}.jpg', width=100)

    with col16:
        st.image(f'images/0{customerX[11]}.jpg', width=100)

else:

# st.image('images/image.jpg', width=200)

#Premiére ligne des articles
# On récupére les données (id images) du fichier baseline_test.txt
    liste_id_image = np.loadtxt('baseline_test.txt', dtype=int)
    st.markdown("""## Catégories tendance""")
    col1, col2, col3, col4, col5, col6= st.columns(6)

    with col1:
        st.image(f'images/0{liste_id_image[0]}.jpg', width=100)

    with col2:
        st.image(f'images/0{liste_id_image[1]}.jpg', width=100)

    with col3:
        st.image(f'images/0{liste_id_image[2]}.jpg', width=100)

    with col4:
        st.image(f'images/0{liste_id_image[3]}.jpg', width=100)

    with col5:
        st.image(f'images/0{liste_id_image[4]}.jpg', width=100)

    with col6:
        st.image(f'images/0{liste_id_image[5]}.jpg', width=100)

    #Deuxiéme ligne des ligne
    col11, col12, col13, col14, col15, col16= st.columns(6)

    with col11:
        st.image(f'images/0{liste_id_image[6]}.jpg', width=100)

    with col12:
        st.image(f'images/0{liste_id_image[7]}.jpg', width=100)

    with col13:
        st.image(f'images/0{liste_id_image[8]}.jpg', width=100)

    with col14:
        st.image(f'images/0{liste_id_image[9]}.jpg', width=100)

    with col15:
        st.image(f'images/0{liste_id_image[10]}.jpg', width=100)

    with col16:
        st.image(f'images/0{liste_id_image[11]}.jpg', width=100)




# Récupérer les id customers avec leur id images dans le fichier data.jason
# with open('data.json', 'rb') as fp:
#    data = pickle.load(fp)

# data
# print(data)
# print(type(data))

# Récupérer les photos baseline
# a2 = np.loadtxt('baseline.txt', dtype=int)
# a2
# a2[0]
