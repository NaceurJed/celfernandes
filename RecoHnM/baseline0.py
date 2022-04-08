#****************************   Build Customer x Article matrixes   ********************************************
# One matrix per customers segment
#***************************************************************************************************************

import pandas as pd

def get_data (csv_file, df):
    df = pd.read_csv('../raw_data/f'{csv_file}')
    return df

def week_raw_to_dummy(df, week_list):
    for week in week_list:
        inweek="in" + f'{week}'
        article_history['inweek']=article_history['t_dat'].apply(lambda x: 1 if x==week else 0)
    return article_history


def Baseline_0 (segment,transact_history,X_week,y_week): # exemple: week104name ='in104' dans l'historique des transactions

    X_week_dummy="in" + f'{X_week}'
    y_week_dummy="in" + f'{y_week}'

    filtre_Xweek=transact_history[X_week_dummy]==1
    filtre_yweek=transact_history[y_week_dummy]==1

    X_achats=segment[['customer_id']].merge(transact_history[filtre_Xweek][['customer_id','article_id',X_week_dummy]])
    y_achats=segment[['customer_id']].merge(transact_history[filtre_yweek][['customer_id','article_id',y_week_dummy]])

    # calcul des plus populaires sur la dernière semaine des X = baseline0
    articles= X_achats.groupby(['article_id']).sum()
    Top12_arr=articles.sort_values(by=X_week_dummy, ascending=False).head(12)
    Top12=""
    for i in range (0, 12):
        if i==0 :
            Top12=str(Top12_arr.index[i])
        else:
            Top12=Top12 + " "+ str(Top12_arr.index[i])

    #je donne à tous mes customers de mon segment le baseline top12 calculé ci-dessus
    segment['Baseline0']=Top12

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

    segment_BS=segment.merge(Baseline0_precision, how = 'left', on='customer_id')

    return segment_BS


# Récupértaion de segments clients de Naceur selon l'âge
# note du 06042022: à ce stade de l'analyse les customers sans information sur l'âge ne sont pas inclus
get_data('customers_age_16_17.csv','S1')
get_data('customers_age_18_19.csv','S2')
get_data('customers_age_20_21.csv','S3')
get_data('customers_age_22_23.csv','S4')
get_data('customers_age_24_25.csv','S5')
get_data('customers_age_26_27.csv','S6')
get_data('customers_age_28_29.csv','S7')
get_data('customers_age_30_34.csv','S8')
get_data('customers_age_35_39.csv','S9')
get_data('customers_age_40_44.csv','S10')
set_data('customers_age_45_49.csv','S11')
get_data('customers_age_50_54.csv','S12')
get_data('customers_age_55_59.csv','S13')
get_data('customers_age_60.csv','S14')

# Récupération du fichiers de transactions "test" contenant semaines 101 à 104:
get_data('transaction_train_week_101_104','transaction_101_104')
transactions_101_104.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'price', 'sales_channel_id'])
week_list=[101,102,103,104]
week_raw_to_dummy(transactions_101_104, week_list)
Baseline_0(S1,article_history,103,104)
