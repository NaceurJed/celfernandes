import baseline0
from sklearn.preprocessing import OneHotEncoder


def encode_cat_articles(df):# création de dummies pour chaque catégorie de produits
    df=df[['article_id','garment_group_name']]
    ohe = OneHotEncoder(sparse=False) # Instanciate encoder
    garment_encoded=ohe.fit_transform(df[['garment_group_name']])
    cat_names=ohe.categories_

def Baseline_plus (segment,transact_history,X_week, y_week):
    # segment et transact_history sont des df
    # X_week (fin de la période d'observation des transactions), y_week sont des numéros de semaine (target)

    X_week_dummy="in" + f'{X_week}'
    y_week_dummy="in" + f'{y_week}'

    filtre_Xweek=transact_history[X_week_dummy]==1
    filtre_yweek=transact_history[y_week_dummy]==1

    #je récupère les catégories, ici les dummies serviront pour une étape ultérieure (ex filtrage collaboratif etc)
    X_achats=segment[['customer_id']].merge(transact_history[filtre_Xweek][['customer_id','article_id',X_week_dummy]]).merge(articles_categories)
    y_achats=segment[['customer_id']].merge(transact_history[filtre_yweek][['customer_id','article_id',y_week_dummy]]).merge(articles_categories)


    #je fais un groupby par clients, sans le sort car j'ai ensuite besoin de refaire un tri par valeur de in104 derrière et j'ai
    # a nouveau besoin de refaire le tri par client pour cela donc gain de teps de calcul car on suppose que sort_values est plus rapide que le
    # sort de groupby
    achats_cat_srt=X_achats.groupby(['customer_id','garment_group_name'],as_index=False, sort=False).sum().sort_values(by=['customer_id',X_week_dummy],ascending=False)

    #je supprime les doublons pour garder que la catégorie max d'achats
    achats_cat_max=achats_cat_srt.drop_duplicates(subset=['customer_id'],inplace=False)

    #définition du Top12 par catégorie: à la valeur de garment j'associe la valeur TOP12 associée
    #calcul du Top12 par catégorie stocké sou forme de dictionnaire
    achats_cat_art=y_achats.groupby(['garment_group_name','article_id'], as_index=False, sort=False).sum().sort_values(by=['garment_group_name', y_week_dummy], ascending=False)
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


    achats_cat_max.loc[:,'Baseline1']=achats_cat_max.loc[:,'garment_group_name'].apply(lambda c: Top12_cat[c])


    #*************** Calcul précision **************************************************************
    cust_baseline=achats_cat_max[['customer_id','Baseline1']]
    achats_et_baseline1=achats[['customer_id','article_id']].merge(cust_baseline1, on='customer_id')

    # si l'articleID acheté est dans la TOP12 (1 si oui, O sinon)
    achats_et_baseline1['inBaseline1']=achats_et_baseline1['article_id'].apply(lambda x: 1 if str(x) in achats_et_baseline1['Baseline1'] else 0)
    sortie=achats_et_baseline1.groupby(['customer_id']).sum().rename(columns={'inBaseline1':'Precision'})

    #segment_BS=segment.merge(Baseline0_precision, how = 'left', on='customer_id')
    return achats_cat_max#cust_baseline1# achats_cat_max.head(10)#return segment #ici segment contient toutes ces colonnes passées en input



get_data('articles.csv','articles_hetm')
encode_cat_articles('articles_hetm')
