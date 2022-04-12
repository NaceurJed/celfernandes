
# Two main metrics are implemented:

#1) Look at the list of prediction as a set, thus order does not matter when you compare the prediction with the actual purchases.
#2) The metric that is proposed in the Kaggle competition, that is, it takes into account the order etc.
# For more details, see https://www.kaggle.com/code/nandeshwar/mean-average-precision-map-k-metric-explained-code/notebook

import numpy as np

import collections

def convert_dico_actual_predicted(dict_actual,dict_pred):
    
    #First, reduce the dictionnaries to the keys, values for which the keys are in both dicts
    dict_actual_filtered = {key:dict_actual[key] for key in dict_actual if key in dict_pred }
    dict_pred_filtered = {key:dict_pred[key] for key in dict_pred if key in dict_actual }

    #Now, order the dictionnaries accordingly to the keys
    dict_actual_filtered_ordered = dict(collections.OrderedDict(sorted(dict_actual_filtered.items())))
    dict_pred_filtered_ordered = dict(collections.OrderedDict(sorted(dict_pred_filtered.items())))

    #Since they are well ordrered and contain the same keys, we only need to convert into lists.
    actual= [dict_actual_filtered_ordered.get(key,0) for key in dict_actual_filtered_ordered]
    pred = [dict_pred_filtered_ordered.get(key,0) for key in dict_pred_filtered_ordered]
    return actual, pred

#1)
#Compute the metric for two arrays of items: predicted and actual. This gives the ratio of correct predictions: the closer to 1, the better.
def metric_no_order(array_items_actual,array_items_pred):
    n = len(array_items_actual)
    if n == 0:
        return 0.0
    set_actual = set(array_items_actual)
    set_pred = set(array_items_pred)
    return 1- len(set_actual - set_pred) / n

#metric applied to the full dictionnaries
def metric_no_order_global(dict_actual,dict_pred, k=12):
    actual, pred = convert_dico_actual_predicted(dict_actual,dict_pred)
    n = len(actual)
    return np.mean([metric_no_order(actual[i],pred[i]) for i in range(n)])


