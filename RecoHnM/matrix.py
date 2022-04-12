from RecoHnM.data import *
import pandas as pd
import numpy as np


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
    ######################################################################################################
    #  catégories de produits achetés par customer, de la plus achetée (rank=1) à la moins achetée       #
    ######################################################################################################
    # contrairement à la construction de la matrice, ici je veut les infos de transactions en lignes
    tmp=Xh_week_achats.drop(columns='t_dat').merge(clusters_articles_df)
    cluster_name=clusters_articles_df.columns[1]
    cust_max_cats=tmp.groupby(['customer_id',cluster_name],as_index=False).sum()
    cust_max_cats.sort_values(by=['customer_id','counter'],ascending=False,inplace=True)
    cust_max_cats['rank']=cust_max_cats.groupby('customer_id')['counter'].rank(method='first',ascending=False)
    cust_max_cats['cat_perc']=cust_max_cats.groupby('customer_id', as_index=True, group_keys=False)['counter'].apply(lambda x: x / x.sum())
    return cust_max_cats

def calc_diversity_per_cust(cust_max_cats,threshold): #threshold est un pourcentage , exemple 30 pour 30%
    max_nb_cats=int(100/threshold)
    cust_max_cats['keep_cat']=cust_max_cats['cat_perc'].map(lambda x : 1 if x>=(threshold/100) else 0)
    # dans la ligne ci-dessous je suis obligée de lui mettre x/x (=1) dans la lambda fonction sinon il retourne NaN si dans le 
    # calcul on utilise pas la valeur x elle-même
    cust_max_cats['cust_diversity']=cust_max_cats.groupby('customer_id', as_index=True, group_keys=False)['keep_cat'].apply(lambda x: x/x * x.sum())
    return cust_max_cats

def top12_per_cat(segment_base,X_week,p,clusters_articles_df):
    # p est le nombre de périodes utilisées pour déterminer le top12 (différent de horizon)
    week_min= X_week-p+1
    week_max= X_week
    filtre=np.logical_and(segment_base['t_dat'] >= week_min,segment_base['t_dat'] <= week_max)
    tmp=segment_base[filtre].drop(columns=['customer_id','t_dat']).merge(clusters_articles_df)
    cluster_name=clusters_articles_df.columns[1]
    tmp['counter']=1
    tmp=tmp.groupby([cluster_name,'article_id'],as_index=False).sum()
    tmp.sort_values(by=[cluster_name,'counter'],ascending=False,inplace=True)
    tmp['rank']=tmp.groupby(cluster_name)['counter'].rank(method='first',ascending=False)
    keep_first_12=tmp['rank']<=12
    top12_cat=tmp[keep_first_12] 
    return top12_cat
    
def top_df_to_dict(top_df): # transforme le Top format dataframe à format dictionnaire
    #########j'ai un warning pour cette ligne de code ci après:
    #A value is trying to be set on a copy of a slice from a DataFrame.
    #Try using .loc[row_indexer,col_indexer] = value instead
    #############################################################################
    #top_df['article_id']=top_df['article_id'].astype(str) #nécessaire pour utiliser la méthode .join qui travaille sur des str
    cat_list=top_df.iloc[:,0].values
    dict_top_cats={}
    for cat in cat_list:
        mask=top_df.iloc[:,0]==cat
        tmp=top_df[mask]
        #je passe à ma clef de dictionnaire (= cat) une string contenant les articles_id associés à la cat
        articles_arr=tmp['article_id'].values
        #articles_str=" ".join(tmp['article_id'].values) 
        dict_top_cats[cat]= articles_arr #articles_str
    return dict_top_cats

############ je généralise la méthode ci-dessus à tout df qu'on veut transformer en dictionnaire##############
## group_name = nom de la série quon veut considérer comme un group_by 
## value_to_list = nom de la variable dont les valeurs prises par le groupe sont à passer dans une liste

def df_to_dict(df,group_name,value_to_list): # transforme le format dataframe à format dictionnaire
    df[value_to_list]=df[value_to_list].astype(str) #nécessaire pour utiliser la méthode .join qui travaille sur des str
    group_list=df.loc[:,group_name].values
    dict_group_values={}
    for group in group_list:
        mask=df.loc[:,group_name]==group
        tmp=df[mask]
        #je passe à ma clef de dictionnaire (=group) une string contenant les values associées au sein du groupe
        values_list=tmp[value_to_list].values
        #values_str=" ".join(tmp[value_to_list].values) 
        dict_group_values[group]=values_list
    return dict_group_values 

def top12_filtre(top12_cat): # dans cette version l'algo gère nb_cat_to_predict in [1,2,3,4,6,12]
        nb_cat_to_predict=[1,2,3,4,6,12]
        for nb in nb_cat_to_predict:
            top_nb=12/nb
            if nb==1:
                top12x1cat=top12_cat
                dict_top12x1cat=top_df_to_dict(top12x1cat)
                top12x1cat.to_csv('top12x1cat.csv')
            elif nb==2:
                top6x2cat=top12_cat[top12_cat['rank']<=top_nb]
                dict_top6x2cat=top_df_to_dict(top6x2cat)
                top6x2cat.to_csv('top6x2cat.csv')
            elif nb==3:
                top4x3cat=top12_cat[top12_cat['rank']<=top_nb]
                dict_top4x3cat=top_df_to_dict(top4x3cat)
                top4x3cat.to_csv('top4x3cat.csv')
            elif nb==4:
                top3x4cat=top12_cat[top12_cat['rank']<=top_nb]
                dict_top3x4cat=top_df_to_dict(top3x4cat)
                top3x4cat.to_csv('top3x4cat.csv')
            elif nb==6:
                top2x6cat=top12_cat[top12_cat['rank']<=top_nb]
                dict_top2x6cat=top_df_to_dict(top2x6cat)
                top2x6cat.to_csv('top2x6cat.csv')
            elif nb==12:    
                top1x12cat=top12_cat[top12_cat['rank']<=top_nb]
                dict_top1x12cat=top_df_to_dict(top1x12cat)
                top1x12cat.to_csv('top1x12cat.csv')
        return dict_top12x1cat#,dict_top6x2cat,dict_top4x3cat,dict_top3x4cat,dict_top2x6cat,dict_top1x12cat
 



