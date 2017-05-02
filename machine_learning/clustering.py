import json
import psycopg2
import numpy as np

from pprint import pprint

from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import AgglomerativeClustering
from cluster_analysis import political_analysis


class ClusterAnalysis:
    def __init__(self, dataset):
        self.dataset = dataset
        self.db = psycopg2.connect(
            database='pointloc',
            user='pointloc',
            password='pointloc',
            host='10.40.60.191',
            port="5432"
        )
        cursor = db.cursor()

    @staticmethod
    def cluster_indices(clustNum, labels_array):
        return np.where(labels_array == clustNum)[0]

    def clustering(self):
        pass


data_file = json.load(open('db_tweets.json', 'r'))

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

# Minibatch K means
mbk = MiniBatchKMeans(init='k-means++', n_clusters=6, batch_size=30,
                      n_init=10, max_no_improvement=10, verbose=0, compute_labels=True)

# Affinity propagation
af = AffinityPropagation(preference=-50)

# Ward
ward = AgglomerativeClustering(n_clusters=6, linkage='ward')

# DBSCAN
db = DBSCAN(eps=0.05, min_samples=10)

clust = [
    # (mbk, 'MiniBatchKMeans'),
    # (af, 'AffinityPropagation'),
    # (ward, 'AgglomerativeClustering'),
    (db, 'DBSCAN')
]

for c_n in clust:
    c = c_n[0]
    c.fit(X)
    print(c_n[1])
    pprint(dir(c))
    c_labels = set(c.labels_)
    for l in c_labels:
        indices = cluster_indices(l, c.labels_)
        cluster = list()
        for i in indices:
            cluster.append(X[i])
        pprint(political_analysis(cluster))
