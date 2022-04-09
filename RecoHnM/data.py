import pandas as pd

def get_data (csv_file):
    df = pd.read_csv('../raw_data/' + f'{csv_file}')
    return df

# attention la fonctio suivante n'efface pas le df précédent qd on la relance .... c'est dnc sujet à erreur car les dummies restent
def week_raw_to_dummy(transactions_df,X_week,y_week, horizon): #horizon=nbre de weeks utilisées, 1= 1 seule, la semaine Xweek
    week_min= X_week-horizon+1
    week_max= X_week
    tmp=transactions_df
    for w in range(week_min,week_max+1):
        inweek='in' + f'{w}'
        tmp[inweek]= tmp['t_dat'].apply(lambda x: 1 if x==w else 0)
        transactions_df=tmp
    return transactions_df
