#***************************************************************************************************************
#                           Build Baseline0 - default value
#***************************************************************************************************************

from data import *


#from baseline0.py

def Baseline_0(segment,transact_history,X_week,y_week,horizon): # exemple: week104name ='in104' dans l'historique des transactions

    X_week_dummy="in" + f'{X_week}'
    y_week_dummy="in" + f'{y_week}'

    filtre_Xweek=transact_history[X_week_dummy]==1
    #filtre_yweek=transact_history[y_week_dummy]==1

    X_achats=segment[['customer_id']].merge(transact_history[filtre_Xweek][['customer_id','article_id',X_week_dummy]])
    # pour précision : y_achats=segment[['customer_id']].merge(transact_history[filtre_yweek][['customer_id','article_id',y_week_dummy]])

    # calcul des 12 plus populaires du segment:
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

    #segment_BS=segment.merge(Baseline0_precision, how = 'left', on='customer_id')

    return segment



# Récupértaion de segments clients de Naceur selon l'âge
# note du 06042022: à ce stade de l'analyse les customers sans information sur l'âge ne sont pas inclus
S1=get_data('customers_age_16_17.csv','S1')
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
transactions_101_104 = get_data('../raw_data/transaction_train_week_101_104.csv')
transactions_101_104.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'price', 'sales_channel_id'], inplace=True)
article_history=week_raw_to_dummy(transactions_101_104, 103,104,1)
Baseline_0(S1,article_history,103,104,1)
