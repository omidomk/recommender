from dbconnect import connection
import pandas as pd
import numpy as np


a, config = connection()

rating = 'SELECT * FROM ratings'
ratings = pd.read_sql(rating, config)
ratings.head()

del ratings['timestamp']


article = 'SELECT * FROM articles'
articles = pd.read_sql(article, config)
articles.head()

user = 'SELECT * FROM users'
users = pd.read_sql(user, config)
users.head()

ratings_df = pd.merge(ratings, articles, on='article_id')[['user_id', 'title', 'article_id','ratings']]

ratings_mrtx_df = ratings_df.pivot_table(values='ratings', index='user_id', columns='title')
ratings_mrtx_df.fillna(0, inplace=True)

article_index = ratings_mrtx_df.columns


ratings_mrtx_df.head()

corr_matrix = np.corrcoef(ratings_mrtx_df.T)
corr_matrix.shape


def get_similar_articles(article_title):
    '''Returns correlation vector for a article'''
    article_idx = list(article_index).index(article_title)
    return corr_matrix[article_idx]

def get_article_recommendations(user_articles):
    '''given a set of articles, it returns all the articles sorted by their correlation with the user'''
    article_similarities = np.zeros(corr_matrix.shape[0])
    for article_id in user_article:
        article_similarities = article_similarities + get_similar_articles(article_id)


        similar_articles_df = pd.DataFrame({
            'title': article_index,
            'sum_similarity': article_similarities
        })
        
    similar_articles_df = similar_articles_df.sort_values(by=['sum_similarity'], ascending=False)
   
    return similar_articles_df



def get_user_rec(smpl_user):
    ratings_df[ratings_df.user_id==smpl_user].sort_values(by=['ratings'], ascending=False)

    smpl_user_articles = ratings_df[ratings_df.user_id==smpl_user].title.tolist()
    recommendations = get_article_recommendations(smpl_user_articles)
    l= 20

    #We get the top 20 recommended articles
    innerl = l+24
    rec = recommendations.title.head(innerl)[l:]
#
    reviews = []

    for item in rec:
        a.execute('SELECT img from articles WHERE title =%s', (str(item)))
        img = a.fetchone()
        a.execute('SELECT article_id from articles WHERE title =%s', (str(item)))
        aid = a.fetchone()
        a.execute('SELECT arxivid from links WHERE article_id =%s', (int(mid[0])))
        arxiv = a.fetchone()

       

        reviews.append((int(arxiv[0]), item, img[0], str(x)))


    return reviews



