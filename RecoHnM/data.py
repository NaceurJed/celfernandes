import pandas as pd

def get_data(csv_file, df):
    df = pd.read_csv('../raw_data/f'{csv_file}')
    return df

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
df=transactions_101_104.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'price', 'sales_channel_id'])
