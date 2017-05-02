import json
import random
import psycopg2
import numpy as np

from pprint import pprint

from sklearn.cluster import DBSCAN
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import AgglomerativeClustering

from machine_learning import AT
from machine_learning.cluster_analysis import political_analysis


def cluster_indices(clustNum, labels_array):
    return np.where(labels_array == clustNum)[0]


X = list()
labels = [
    'sentiment',
    'topic1',
    'topic2',
    'topic3',
    'topic4',
    'topic5'
    'conservative',
    'green',
    'liberal',
    'libertarian',
]

db = psycopg2.connect(
    database='pointloc',
    user='pointloc',
    password='pointloc',
    host='10.40.60.191',
    port="5432"
)

cursor = db.cursor()
query = (
    "SELECT text, text_analysis FROM tweets "
)

cursor.execute(query)
rows = cursor.fetchall()

for item in random.sample(rows, 1):
    data = item[1]
    if len(data) == 0:
        continue
    # topic value
    topic = sorted(data['text_tags'].values(), reverse=True)[0:5]
    # topic name
    keywords = sorted(
        data['text_tags'],
        key=data['text_tags'].__getitem__,
        reverse=True
    )[0:5]
    print item[0]
    pprint(data['text_tags'])
    pprint(topic)
    pprint(keywords)
    exit()
    vector = (
        # data['sentiment'],
        topic[0],
        topic[1],
        topic[2],
        topic[3],
        topic[4],
        data['political']['Conservative'],
        data['political']['Green'],
        data['political']['Liberal'],
        # data['political']['Libertarian']
    )
    # print vector
    X.append(vector)

# Minibatch K means
mbk = MiniBatchKMeans(
    init='k-means++', n_clusters=6, batch_size=30,
    n_init=10, max_no_improvement=10, verbose=0, compute_labels=True
)

# Affinity propagation
af = AffinityPropagation(preference=-50)

# Ward
ward = AgglomerativeClustering(n_clusters=6, linkage='ward')

# DBSCAN
db = DBSCAN(eps=0.005, min_samples=5)

clust = [
    (mbk, 'MiniBatchKMeans'),
    # (af, 'AffinityPropagation'),
    (ward, 'AgglomerativeClustering'),
    # (db, 'DBSCAN')
]

for c_n in clust:
    c = c_n[0]
    c.fit(X)
    print(c_n[1])
    c_labels = set(c.labels_)
    print('Clusters: ', len(c_labels))
    for l in c_labels:
        indices = cluster_indices(l, c.labels_)
        cluster = list()
        for i in indices:
            cluster.append(AT(*X[i]))
        print(political_analysis(cluster))
