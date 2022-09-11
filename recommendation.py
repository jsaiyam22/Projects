# -*- coding: utf-8 -*-
"""recommendation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qQ1DN52x2mdbSDd9pKQJDpEMgk4B5DTt
"""

import pandas as pd
import numpy as np

movies=pd.read_csv('/content/movies.csv')
ratings=pd.read_csv('/content/ratings.csv')

movies.head()

ratings.head()

m_rat=movies.merge(ratings,on='movieId')

m_rat.head()

m_rat=m_rat[['movieId','userId','title','genres','rating']]

m_rat.head()

m_rat.isnull().sum()

m_rat.dropna(axis=0,subset=['title'])

m_rat.duplicated().sum()

m_rat.groupby('title')['rating'].count().sort_values(ascending=False).head()

avg_rat= pd.DataFrame(m_rat.groupby('title')['rating'].mean())
avg_rat.head()

avg_rat['no_of_ratings'] = pd.DataFrame(m_rat.groupby('title')['rating'].count())
avg_rat.head()

total_movie_count = m_rat.merge(avg_rat,on = 'title')

total_movie_count.head()

min = 100
popular_movie= total_movie_count.query('no_of_ratings >= @min')
popular_movie.head()

matrix = popular_movie.pivot_table(index='title',columns='userId',values='rating_x').fillna(0)
matrix.head()

from scipy.sparse import csr_matrix

sparse_matrix= csr_matrix(matrix.values)

from sklearn.neighbors import NearestNeighbors


knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
knn.fit(sparse_matrix)

movie_index = np.random.choice(matrix.shape[0])
print(movie_index)
distances, indices = knn.kneighbors(matrix.iloc[index,:].values.reshape(1, -1), n_neighbors = 5)

matrix.head()

for i in range(0, len(distances.flatten())):
    if i == 0:
        print('Recommendations for {0}:\n'.format(matrix.index[movie_index]))
    else:
        print('{0}:{1}, with distance of {2}:'.format(i, matrix.index[indices.flatten()[i]], distances.flatten()[i]))