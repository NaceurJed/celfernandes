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

def build_segment_base(segment): # ce df contient toutes les transactions des individus du segment
    return segment[['customer_id']].merge(transact_history)

def build_segment_horizon_transactions(segment_base,X_week,horizon):
    #filtrage sur l'horizon temporel pour connaitre les préférences des customers
    week_min= X_week-horizon+1
    week_max= X_week
    filtre=np.logical_and(segment_base['t_dat'] >= week_min,segment_base['t_dat'] <= week_max)
    Xh_week_achats=segment_base[filtre][['customer_id','t_dat','article_id']]
    Xh_week_achats['counter']=1
    return Xh_week_achats

def build_matrix(Xh_week_achats):
    achats_for_matrix=Xh_week_achats.drop(columns='t_dat')
    #achats_for_matrix['counter']=1 je pense pouvoir supprimer
    achats_for_matrix=achats_for_matrix.merge(articles_categories)

    # je fais un groupby par clients, sans le sort car j'ai ensuite besoin de refaire un tri
    # donc gain de temps de calcul car on suppose que sort_values est plus rapide que le sort de groupby
    achats_gb_cust_cat=achats_for_matrix.groupby(['customer_id'],as_index=False,sort=False)
    achats_gb_cust_cat_srt=achats_gb_cust_cat.sum().sort_values(by=['customer_id','counter'],ascending=False)

    # je refais ensuite un groupby par client pour calculer la somme de chaque dummy de categories
    segment_matrix=achats_gb_cust_cat_srt.drop(columns=['article_id']).groupby(['customer_id'],as_index=False).sum()
    return segment_matrix

def get_max_cats(Xh_week_achats,clusters_articles_df):
    # contrairement à la construction de la matrice, ici je veut les infos de transactions en lignes
    # diversity sera le nbre de catégories utilisées pour proposer 12 références
    tmp=Xh_week_achats.drop(columns='t_dat').merge(clusters_articles_df)
    cluster_name=clusters_articles_df.columns[1]
    achats_for_max_cats=tmp.groupby(['customer_id',cluster_name],as_index=False).sum()
    achats_for_max_cats.sort_values(by=['customer_id','counter'],ascending=False,inplace=True)
    achats_for_max_cats['rank']=achats_for_max_cats.groupby('customer_id')['counter'].rank(method='first',ascending=False)
    return achats_for_max_cats

def top12_per_cat(segment_base,X_week,p,clusters_articles_df):
    # p est le nombre de périodes utilisées pour déterminer le top12 (différent de horizon)
    week_min= X_week-p+1
    week_max= X_week
    filtre=np.logical_and(segment_base['t_dat'] >= week_min,segment_base['t_dat'] <= week_max)
    top12_cat=segment_base[filtre].drop(columns=['customer_id','t_dat']).merge(clusters_articles_df)
    cluster_name=clusters_articles_df.columns[1]
    top12_cat['counter']=1
    top12_cat=top12_cat.groupby([cluster_name,'article_id'],as_index=False).sum()
    top12_cat.sort_values(by=[cluster_name,'counter'],ascending=False,inplace=True)
    top12_cat['rank']=top12_cat.groupby(cluster_name)['counter'].rank(method='first',ascending=False)
    keep_first_12=top12_cat['rank']<=12
    top12_cat_12=top12_cat[keep_first_12]
    return top12_cat_12

def top12_split(top12_cat_12,diversity): # dans cette version l'algo gère diversity in [1,2,3,4,6,12]
        if diversity==1:
            return top12_cat_12
        else:
            top_nb=12/diversity
            return top12_cat_12[top12_cat_12['rank']<=top_nb]


def predict()

    # je donne baseline0 à tout le segment, puis j'affine ?
    #ou pour optimiser if vide -> je donne baseline0




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
