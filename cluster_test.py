import psycopg2
import random
import json

from pprint import pprint

from machine_learning.cluster_analysis import political_analysis
from machine_learning import AT


cluster = [AT(*[random.random() for _ in range(10)])
           for i in range(random.randint(1000, 5000))]

pprint(political_analysis(cluster))

db = psycopg2.connect(
    database='pointloc',
    user='pointloc',
    password='pointloc',
    host='10.40.60.191',
    port="5432"
)

cursor = db.cursor()
cursor.execute(
    "SELECT author_id, text, mentions, favorites_number, retweets_number, replies_number, created_at from tweets")
rows = cursor.fetchall()

all_tweets = list()
for t in rows:
    all_tweets.append({
        'author_id': t[0],
        'text': t[1],
        'mentions': t[2],
        'favorites_number': t[3],
        'retweets_number': t[4],
        'replies_number': t[5],
        'created_at': t[6].strftime('%d/%m/%Y %H:%M:%S'),
    })

print 'data fetched'

with open('db_tweets.json', 'w') as outfile:
    json.dump(all_tweets, outfile)
    print 'file created'
