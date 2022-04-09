#***************************************************************************************************************
#
#                Cherche les meilleurs paramètres des modèles Kmeans sur
#                  les categories d'articles afin d'évaluer la qualité
#                                   de la prédiction
#
#***************************************************************************************************************

# paramètres :

#recherche du nbre de clusters optimum pour la segmentation des articles:
cat_nb=[25, 30, 35, 40, 45, 50, 55, 60]

# définition des points des numéros de semaines à considérer:
Xweek=103
yweek=104 # semaine à prédire
horizons=[0, 1, 2] # nbre de weeks considérées pour trouver les fréquences d'achat par cat, 0= on considère uniquement la période Xweek,
                   # 102: on considère toutes les périodes

# dataframes passés en input de la segmentation
article_history=history(Xweek,horizon) # dépend de l'horizon temporel passé en paramètre, pour le moment je n'ai que de 101 à 103
segments=[S1,S2]                       # customer_id et segment_id


def best_parameters(segments,cat_nb,Xweek,horizon,yweek):
    results={}
    for segment in segments:
        for nb in cat_nb:
            cat=build_categories(nb) # donne un df : article_id et cat_id
            for horizon in horizons
                build_matrix(segment,cat,article_history,Xweek,horizon,yweek)
                predict()
                precision = evaluate(segment,yweek)
                key=f'{segment}' + '-' + f'{nb}' +  '-' + f'{horizon}'
                results={ key : precision } # si on ne peut pas mettre de tuple on passe en string
    return results #résultat des différents modèles de kmeans selon horizon et le nbre de cat
