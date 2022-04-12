import pandas as pd
import numpy as np
import pickle
from matrix import *

#**********************************************************************************************************************
# Paramètres:
#**********************************************************************************************************************
# 
# X_week= semaine T0
#
# horizon= nbre de semaines utilisées pour observer les achats effectués dans chaque catégorie d'articles (Xweek inclus)
#
# p=nbre de semaines utilisées pour définir les articles_id (Xweek inclus)
#
# cat_threshold = seuil en % (ex 30 pour 30%) pour définir quelles sont les categories d'articles considérées pour 
# chaque individu pour effectuer la recommandation personnalisée
#
#*********************************************************************************************************************

def fit_recommender(segment_base,clusters_articles_df,X_week,horizon,p,cat_threshold):
        
    # 1.construction des infos clients
    cluster_name=clusters_articles_df.columns[1]
    #segment_base=build_segment_base(segment_df)
    Xh_week_achats=build_segment_horizon_transactions(segment_base,X_week,horizon)
    cust_max_cats=get_max_cats(Xh_week_achats,clusters_articles_df)
    cust_max_cats=calc_diversity_per_cust(cust_max_cats,cat_threshold)
    filtre=cust_max_cats['keep_cat']==1
    cust_max_cats_filtered=cust_max_cats[filtre]
    dict_cust_cat=df_to_dict(cust_max_cats_filtered,'customer_id',cluster_name)
    
    # 2.construction des infos articles à faire correspondre ensuite aux clients
    top12_cat=top12_per_cat(segment_base,X_week,p,clusters_articles_df)
    dict_cat_articles=top_df_to_dict(top12_cat)
    return dict_cust_cat, dict_cat_articles

def baseline0(segment,X_week,q): #supprimer tdat et restituer les valeurs plutot que df
    # q est le nbre de weeks sur lesquels on veut définir les articles_id de la baseleine
    segment_base= build_segment_base(segment)
    Xq_week_achats=build_segment_horizon_transactions(segment_base,X_week,q)
    Xq_week_achats.drop(columns='t_dat', inplace=True)
    Xq_week_achats['counter']=1
    segment_top12=Xq_week_achats.groupby(['article_id'],as_index=False).sum().sort_values(by='counter', ascending=False).head(12)
    segment_baseline=segment_top12['article_id'].values
    return  segment_baseline

def build_pred_base(dict_cust_cat, dict_cat_articles, segment_baseline):
    # paires (diversité client : nb de liste articlesID à chercher)
 
    # buyers_default_strategy : si les clients avec achats sur l'horizon choisi n'ont pas le nbre de catégories correspondant
    # au niveau de diversité désiré
    # cold_start_default_strategy : quelle baseline donner aux clients sas acahts sur l'horizon choisi 
    # (Baseline0 calculée sur quels mois)
    #dict_cust_cat, dict_cat_articles=fit_recommender(segment_df,clusters_articles_df,X_week,horizon,p,diversity)
    
    # 1. customers avec achats dans l'horizon choisi
    dict_cust_articles_pers={}
    for customer,cat_list in dict_cust_cat.items():
        nb_cat_to_predict=min(len(cat_list),12)
        nb_articles_per_cat=int(12/nb_cat_to_predict)
        modulo=12 % nb_cat_to_predict
        articles_arr=[[]]
        if nb_cat_to_predict==0:
            articles_arr= segment_baseline
        elif modulo==0 and nb_cat_to_predict==1:
            cat=cat_list[0]
            articles_arr=np.r_[dict_cat_articles[cat][:6],segment_baseline[:6]]# on force la diveristé en mettant du baseline0
        else: # modulo positif ou nul
            from_baseline=0
            for cat in cat_list:
                nb_articles_in_cat=len(dict_cat_articles[cat])
                if nb_articles_in_cat<nb_articles_per_cat:
                    start_index=from_baseline
                    end_index= start_index+nb_articles_per_cat-nb_articles_in_cat                   
                    articles_arr=np.r_[dict_cat_articles[cat][:nb_articles_in_cat],segment_baseline[start_index:end_index]]
                    from_baseline=from_baseline+(nb_articles_per_cat-nb_articles_in_cat)
                else :
                    articles_arr=np.r_[articles_arr,dict_cat_articles[cat][:nb_articles_per_cat]]
        if modulo>0 :# modulo positif donc à compléter avec du baseline
            start_index=from_baseline
            end_index= start_index+modulo
            articles_arr=np.r_[articles_arr,segment_baseline[start_index:end_index]]
        dict_cust_articles_pers[customer]=articles_arr
    return dict_cust_articles_pers

def pred(segment,X_week,q): 
    segment_to_predict=segment['customer_id'].values
    segment_baseline= baseline0(segment,X_week,q)
    dict_cust_articles_pers={} #pour e moment je passe un dict vide car ma fonction build_pred_base ne fonctionne pas encore
    # chercher si customer(s) est/sont dans dict_cust_articles et si oui lui/leur donner la liste d'articles correspondante
    # sinon attribuer la baseline
    segment_result_dict={}
    for customer in segment_to_predict:
        pred=dict_cust_articles_pers.get(customer, None)
        if pred==None:
            pred=segment_baseline
        segment_result_dict[customer]=pred
    return segment_result_dict

# Paramètres communs à tous les segments:

clusters_articles_df=
X_week=


################### faire ici une boucle pour chaque segment ###################################################
segment=
segment_base=

# Définition des paramètres qu'il est possible de choisir pour chaque segment:
horizon=
p=
cat_threshold=
q=

#1. Calcul de la baseline0
segment_baseline=(segment,X_week,q)
#Export de la baseline en fichier text
segment_baseline_file=          #nom du fichier à exporter
np.savetxt(segment_baseline_file,segment_baseline,fmt='%d')
#2. Fit recommender sur chaque segment:
segment_dict_cust_cat, segment_dict_cat_articles= fit_recommender(segment_base,clusters_articles_df,X_week,horizon,p,cat_threshold)
#3. Création du dictionnaire des recommandations
segment_recs_pers=build_pred_base(segment_dict_cust_cat, segment_dict_cat_articles,segment_baseline)
#Export du dictionnaire en fichier text
segment_recs_pers = pred(segment,X_week,q)
with open('data.json', 'wb') as fp:
    pickle.dump(segment_recs_pers, fp)

