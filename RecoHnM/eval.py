# import des métriques


def y_true(segment_base,y_week,t):
    #segment_base= build_segment_base(segment)
    y_week_achats=build_segment_horizon_transactions(segment_base,y_week,t)
    y_week_achats.drop(columns='t_dat', inplace=True)
    y_week_achats['counter']=1
    segment_ytrue_df=y_week_achats.groupby(['customer_id','article_id'],as_index=False).sum().sort_values(by='counter', ascending=False)
    segment_ytrue_dict=df_to_dict(segment_ytrue_df,'customer_id','article_id')
    return segment_ytrue_dict
