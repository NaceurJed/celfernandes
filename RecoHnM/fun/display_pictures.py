#This .py allows to render the pictures corresponding to a list of article_ids.

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def display_pictures_list_of_articles(list_of_articles):
    for article_id in list_of_articles:
        folder = '0'+str(article_id)[0:2]
        #WARNING, possible problems with the path if you move things around
        img = mpimg.imread('../../raw_data/images/'+folder+'/0' + str(article_id) +'.jpg')
        imgplot = plt.imshow(img)
        plt.show()

