import pandas as pd

def get_data (csv_file):
    df = pd.read_csv('../raw_data/' + f'{csv_file}')
    return df

def encode_categories_articles(clusters_articles_df):  #df doit avoir les champs format ['article_id','catID']
    # création de dummies pour chaque catégorie de produits
    cluster_name=clusters_articles_df.columns[1]
    ohe = OneHotEncoder(sparse=False)# Instanciate encoder
    cat_encoded=pd.DataFrame(ohe.fit_transform(clusters_articles_df[[cluster_name]]))
    cat_names=ohe.categories_
    return pd.concat([articles_hetm[['article_id']],cat_encoded], axis=1) 

def build_segment_base(segment): # ce df contient toutes les transactions des individus du segment 
    return segment[['customer_id']].merge(transact_history)


############################ Création des bases utilisées par le recommender #####################################

# Lecture du fichier de transactions avec le champ 'week'
transactions_file='transaction_train_week_101_104.csv'
transactions_file_path=f'../raw_data/{transactions_file}'
transact_history=get_data(transactions_file_path)

# Récupértaion de segments clients issus du Kmeans
# faire une boucle qui récupère les fichiers et crée la base segment associée
# for i in range (1, N) #N étant le nbre de segments
S1=get_data('customers_age_16_17.csv')
S1_base=build_segment_base(S1)
#.....

# Récupértaion des catégories articles issues du Kmeans et transformation en dummies
clusters_articles_df = get_data('../raw_data/articles.csv')
articles_categories=encode_categories_articles(clusters_articles_df)


