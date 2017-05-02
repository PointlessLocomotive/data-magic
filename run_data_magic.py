import json
from statistics import DataAnalysis
from pprint import pprint
from pymongo import MongoClient

# client = MongoClient('localhost', 27017)
# db = client.tmnt

candidates = json.load(open('candidates.json'))
da = DataAnalysis(candidates)

candidates
candidates = db.candidates
candidates_data = da.candidate_profile()
candidates.delete_many({})
candidates.insert_many(candidates_data)

weeks
weeks = db.weeks
weeks_data = da.tweet_score()
weeks.delete_many({})
weeks.insert_one(weeks_data)

places
places = db.places
places_data = da.voter_score()
places.delete_many({})
places.insert_many(places_data)

