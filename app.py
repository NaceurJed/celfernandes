import streamlit as st
import numpy as np
import pandas as pd
import pickle
st.set_page_config(layout="wide")
#Modal
import streamlit_modal as modal
import streamlit.components.v1 as components

#Experimental
import hydralit_components as hc

# On recupére ce qu'on a rentré dans le modal (champ customer)
query_param = st.experimental_get_query_params()
# On verifie si le dictionnaire query_param est vide (si c'est vide alors dico = True)
dico = not bool(query_param)
# si dico est True alors en envoi 'baseline' comme paramétre dasn l'URL
if dico:
  st.experimental_set_query_params(
      id="baseline",
  )
else:
  id_customer = query_param['id'][0]
  if id_customer != 'caro' and id_customer != 'celine' and id_customer != 'baseline':
    st.warning(f'"{id_customer}" identifiant inconnu')
    st.experimental_set_query_params(
      id="baseline",
    )
    

#######################################################################################
#Haut de page
navbar = """
<nav class="navbar navbar-expand-lg navbar-light row">
    <div class="collapse navbar-collapse col-md-6" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Service Client</a>
        </li>
        <li class="nav-item">
          <a class="nav-link active" href="#">Newsletter</a>
        </li>
        <li class="nav-item">
          <a class="nav-link active" href="#">Trouver un magasin</a>
        </li>
      </ul>
    </div>
    <div class="collapse navbar-collapse col-md-6 d-flex justify-content-end" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <button type="button" class="btn btn-link text-dark" data-toggle="modal" data-target="#exampleModal">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-person" viewBox="0 0 16 16"><path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/></svg>
          Connexion
          </button>
        </li>
        <li class="nav-item">
          <a class="nav-link active" href="#"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
  <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
</svg> Favoris</a>
        </li>
        <li class="nav-item">
          <a class="nav-link active" href="#"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-handbag" viewBox="0 0 16 16">
  <path d="M8 1a2 2 0 0 1 2 2v2H6V3a2 2 0 0 1 2-2zm3 4V3a3 3 0 1 0-6 0v2H3.36a1.5 1.5 0 0 0-1.483 1.277L.85 13.13A2.5 2.5 0 0 0 3.322 16h9.355a2.5 2.5 0 0 0 2.473-2.87l-1.028-6.853A1.5 1.5 0 0 0 12.64 5H11zm-1 1v1.5a.5.5 0 0 0 1 0V6h1.639a.5.5 0 0 1 .494.426l1.028 6.851A1.5 1.5 0 0 1 12.678 15H3.322a1.5 1.5 0 0 1-1.483-1.723l1.028-6.851A.5.5 0 0 1 3.36 6H5v1.5a.5.5 0 1 0 1 0V6h4z"/>
</svg> Panier(0)</a>
        </li>
      </ul>
    </div>
</nav>

"""

####################################################################
# Modal
hc.hydralit_experimental(True)


modal_code = """
<div>
<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
<div class="modal-dialog" role="document">
<div class="modal-content">
<div class="modal-header">
  <h4 class="modal-title" id="exampleModalLabel">Connexion</h4>
  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>
</div>
<div class="modal-body">
  <div class="container">
<form class="form-horizontal" action="/">
<div class="form-group">
<label class="control-label col-sm-2" for="email">Identifiant</label>
<div class="col-sm-10">
  <input type="text" class="form-control" id="id" placeholder="Enter customer ID" name="id">
</div>
</div>

<div class="form-group">        
<div class="col-sm-offset-2 col-sm-10">
  <button type="submit" class="btn btn-default">Se connecter</button>
</div>
</div>
</form>
</div>
</div>

</div>
</div>
</div>
</div>
"""

#####################################################################

st.markdown(navbar,unsafe_allow_html=True)




#######################################################################################
# CSS
st.markdown(''' <style>
                    .stApp{background-color: #FAF9F8;}
                    div.etr89bj1>img {border-radius: 50px;}

                    .css-qrbaxs {font-size: 20px;}

                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}

                    .modal-dialog {
                    position: absolute;
                    top: 50px;
                    right: 100px;
                    bottom: 0;
                    left: 0;
                    z-index: 10040;
                    overflow: auto;
                    overflow-y: auto;
                    }
                    .btn:not(:disabled):not(.disabled){text-decoration: none;}

                    .css-18e3th9 {
                      padding-top: 2rem;
                      padding-bottom: 0}
                    .navbar-expand-lg {padding-bottom: 0}


                </style>''',unsafe_allow_html=True)
#######################################################################################


st.image('images/logo/header.png')
st.image('images/logo/collection.png')


# if(st.button('Login')):
st.markdown(modal_code,unsafe_allow_html=True)
query_param = st.experimental_get_query_params()

if query_param:
    result = query_param['id'][0]
    with open('demod.json', 'rb') as fp:
        data = pickle.load(fp)

    customerX = data[result]  
    # np.loadtxt('baseline_test.txt', dtype=int)

    if result == 'baseline':
      st.markdown("""<div class="text-center"><h4>Catégories tendance</h4> </div>""",unsafe_allow_html=True)
    else:
      st.markdown("""<div class="text-center"><h4>Vos recommandations personnalisées</h4> </div>""",unsafe_allow_html=True)
    # st.markdown("""<div class="text-center"><h4>Vos recommandations personnalisées</h4> </div>""",unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10= st.columns(10)

    with col1:
        st.image('images/produits/blanc.jpg', width=120)
    with col2:
        st.image('images/produits/blanc.jpg', width=120)

    with col3:
        st.image(f'images/produits/0{customerX[0]}.jpg', width=120)

    with col4:
        st.image(f'images/produits/0{customerX[1]}.jpg', width=120)

    with col5:
        st.image(f'images/produits/0{customerX[2]}.jpg', width=120)

    with col6:
        st.image(f'images/produits/0{customerX[3]}.jpg', width=120)

    with col7:
        st.image(f'images/produits/0{customerX[4]}.jpg', width=120)

    with col8:
        st.image(f'images/produits/0{customerX[5]}.jpg', width=120)
    
    with col9:
        st.image('images/produits/blanc.jpg', width=120)
    with col10:
        st.image('images/produits/blanc.jpg', width=120)

    #Deuxiéme ligne des ligne
    col11, col12, col13, col14, col15, col16, col17, col18, col19, col110= st.columns(10)

    with col11:
        st.image('images/produits/blanc.jpg', width=120)
    with col12:
        st.image('images/produits/blanc.jpg', width=120)

    with col13:
        st.image(f'images/produits/0{customerX[6]}.jpg', width=120)

    with col14:
        st.image(f'images/produits/0{customerX[7]}.jpg', width=120)

    with col15:
        st.image(f'images/produits/0{customerX[8]}.jpg', width=120)

    with col16:
        st.image(f'images/produits/0{customerX[9]}.jpg', width=120)

    with col17:
        st.image(f'images/produits/0{customerX[10]}.jpg', width=120)

    with col18:
        st.image(f'images/produits/0{customerX[11]}.jpg', width=120)

    with col19:
        st.image('images/produits/blanc.jpg', width=120)
    with col110:
        st.image('images/produits/blanc.jpg', width=120)

    
    # st.markdown("""<div class="text-center"><h2>Mes derniers achats</h2> </div>""",unsafe_allow_html=True)
    # col111, col112, col113, col114, col115, col116, col117, col118, col119, col120= st.columns(10)

    # with col111:
    #     st.image('images/produits/blanc.jpg', width=120)
    # with col112:
    #     st.image('images/produits/blanc.jpg', width=120)

    # with col113:
    #     st.image(f'images/produits/0{customerX[6]}.jpg', width=120)

    # with col114:
    #     st.image(f'images/produits/0{customerX[7]}.jpg', width=120)

    # with col115:
    #     st.image(f'images/produits/0{customerX[8]}.jpg', width=120)

    # with col116:
    #     st.image(f'images/produits/0{customerX[9]}.jpg', width=120)

    # with col117:
    #     st.image(f'images/produits/0{customerX[10]}.jpg', width=120)

    # with col118:
    #     st.image(f'images/produits/0{customerX[1]}.jpg', width=120)

    # with col119:
    #     st.image('images/produits/blanc.jpg', width=120)
    # with col120:
    #     st.image('images/produits/blanc.jpg', width=120)

# else:


#     # On récupére les données (id images) du fichier baseline_test.txt
#     liste_id_image = np.loadtxt('baseline_test.txt', dtype=int)
#     st.markdown("""<div class="text-center"><h4>Catégories tendance</h4> </div>""",unsafe_allow_html=True)
#     col1, col2, col3, col4, col5, col6, col7, col8, col9, col10= st.columns(10)

#     #Premiére ligne des articles
#     with col1:
#         st.image('images/produits/blanc.jpg', width=120)
#     with col2:
#         st.image('images/produits/blanc.jpg', width=120)

#     with col3:
#         st.image(f'images/produits/0{liste_id_image[0]}.jpg', width=120)

#     with col4:
#         st.image(f'images/produits/0{liste_id_image[1]}.jpg', width=120)

#     with col5:
#         st.image(f'images/produits/0{liste_id_image[2]}.jpg', width=120)

#     with col6:
#         st.image(f'images/produits/0{liste_id_image[3]}.jpg', width=120)

#     with col7:
#         st.image(f'images/produits/0{liste_id_image[4]}.jpg', width=120)

#     with col8:
#         st.image(f'images/produits/0{liste_id_image[5]}.jpg', width=120)

#     with col9:
#         st.image('images/produits/blanc.jpg', width=120)
#     with col10:
#         st.image('images/produits/blanc.jpg', width=120)

#     #Deuxiéme ligne des ligne
#     col11, col12, col13, col14, col15, col16, col17, col18, col19, col20= st.columns(10)

#     with col11:
#         st.image('images/produits/blanc.jpg', width=120)
#     with col12:
#         st.image('images/produits/blanc.jpg', width=120)

#     with col13:
#         st.image(f'images/produits/0{liste_id_image[6]}.jpg', width=120)

#     with col14:
#         st.image(f'images/produits/0{liste_id_image[7]}.jpg', width=120)

#     with col15:
#         st.image(f'images/produits/0{liste_id_image[8]}.jpg', width=120)

#     with col16:
#         st.image(f'images/produits/0{liste_id_image[9]}.jpg', width=120)

#     with col17:
#         st.image(f'images/produits/0{liste_id_image[10]}.jpg', width=120)

#     with col18:
#         st.image(f'images/produits/0{liste_id_image[11]}.jpg', width=120)

#     with col19:
#         st.image('images/produits/blanc.jpg', width=120)
#     with col20:
#         st.image('images/produits/blanc.jpg', width=120)

st.image('images/logo/nouveautes.png')

st.image('images/logo/footer.png')

