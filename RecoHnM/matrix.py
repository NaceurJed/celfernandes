from doctest import DocFileSuite
from baseline0 import *
from data import *
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

def encode_categories_articles(clusters_articles_df):  #df doit avoir les champs format ['article_id','catID']
    # création de dummies pour chaque catégorie de produits
    cluster_name=clusters_articles_df.columns[1]
    ohe = OneHotEncoder(sparse=False)# Instanciate encoder
    cat_encoded=pd.DataFrame(ohe.fit_transform(clusters_articles_df[[cluster_name]]))
    cat_names=ohe.categories_
    return pd.concat([articles_hetm[['article_id']],cat_encoded], axis=1)

def build_segment_base(segment):
    return segment[['customer_id']].merge(transact_history)


def build_matrix(segment_base,X_week,horizon):
    #filtrage sur l'horizon temporel pour connaitre les préférences des customers
    week_min= X_week-horizon+1
    week_max= X_week
    filtre=np.logical_and(segment_base['t_dat'] >= week_min,segment_base['t_dat'] <= week_max)

    Xh_week_achats=segment_base[filtre][['customer_id','article_id']]
    Xh_week_achats['counter']=1
    Xh_week_achats=Xh_week_achats.merge(articles_categories)

    #je fais un groupby par clients, sans le sort car j'ai ensuite besoin de refaire un tri par valeur de in104 derrière et j'ai
    # a nouveau besoin de refaire le tri par client pour cela donc gain de temps de calcul car on suppose que sort_values est plus rapide que le
    # sort de groupby
    achats_gb_cust_cat=Xh_week_achats.groupby(['customer_id'],as_index=False,sort=False)
    achats_gb_cust_cat_srt=achats_gb_cust_cat.sum().sort_values(by=['customer_id','counter'],ascending=False)

    # je refais ensuite un groupby par client pour calculer la somme de chaque dummy de categories
    segment_matrix=achats_gb_cust_cat_srt.drop(columns=['article_id']).groupby(['customer_id'],as_index=False).sum()
    return segment_matrix

def get_cat_max(segment_matrix, diversity, nb_cat):
    # diversity est compris entre 1 et 12 au maximum puisque nous devons restituer 12 articles_id comme prédiction
    # idéalement maximum 4 pour chercher ensuite le Top des articles vendus dans cheaque catégorie considérée
    # Si 1 on s'intéresse uniquement à la catégorie la plus férquemment acehtée sur l'horizon définit au préalable,
    # 2 ce sera les 2 les plus importantes, etc...

    if diversity==1:
        df=segment_matrix.iloc[:,0:-1]
        cat_max1=DocFileSuite.max(axis=1) # je cherche le max sur les lignes
    return df,cat_max1

    #définition du Top12 par catégorie: à la valeur de garment j'associe la valeur TOP12 associée
    #calcul du Top12 par catégorie stocké sous forme de dictionnaire
    achats_cat_art=X_achats.groupby(['garment_group_name','article_id'], as_index=False, sort=False).sum().sort_values(by=['garment_group_name', X_week_dummy], ascending=False)
    Top12_cat={}
    list=ohe.categories_[0]
    for cat in list:
        Top12=""
        mask=achats_cat_art['garment_group_name']==cat
        df=achats_cat_art[mask]
        Top12_arr=df['article_id'].head(12).values
        for article in Top12_arr:
            Top12=Top12+ " "+ str(article)
        Top12_cat[cat]= Top12.lstrip()

    achats_cat_max.loc[:,'Baseline1']=achats_cat_max['garment_group_name'].apply(lambda c: Top12_cat[c])





def predict():
# je retourne sur leurs achats et je vérifie si la baseline0 est un bon prédicteur
    # des achats réellement effectués par les clients en semaine y_week
    # je dois calculer combien de mes achats en y_week étaient dans ma Baseline
    # si ils sont dans ma Baseline0 alors 1 sinon 0

    y_achats['inBaseline0']=y_achats['article_id'].apply(lambda x: 1 if str(x) in Top12 else 0)
    Baseline0_precision=y_achats.groupby(['customer_id']).sum().drop(columns= ['article_id', y_week_dummy]).rename(columns={'inBaseline0':'Precision'})

    print("Statistiques concernant le segment:")
    print("Taille du segment : " + f'{len(segment)}')
    print("Nbre d'acheteurs en yweek : " + f'{len(Baseline0_precision)}')
    print("Précision moyenne:" + f'{Baseline0_precision.mean()}')

    return results Baseline0_precision.mean

def evaluate():
    pass

if __name__ == "__main__":

    articles_hetm = get_data('../raw_data/articles.csv')

    transactions_file='transaction_train_week_101_104.csv'
    transactions_file_path=f'../raw_data/{transactions_file}'
    transact_history=get_data(transactions_file_path)

    articles_categories=encode_categories_articles(clusters_articles_df,categories)
    segment_base=build_base_segment(segment)
    segment_matrix=build_matrix(segment,transact_history,X_week,y_week,horizon)
