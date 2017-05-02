import json
from statistics.popularity_measures import wilson_score
from statistics.weekfilter import week_filter
import psycopg2

WEEKS = [
    ('20170329'),
    ('20170329', '20170404'),
    ('20170405', '20170411'),
    ('20170412', '20170418'),
    ('20170419', '20170425'),
    ('20170426', '20170502'),
    ('20170503', '20170510'),
]


class DataAnalysis:
    def __init__(self, candidates):
        self.candidates = candidates
        self.db = psycopg2.connect(
            database='pointloc',
            user='pointloc',
            password='pointloc',
            host='10.40.60.191',
            port="5432"
        )
        self.cursor = self.db.cursor()

    def candidate_profile(self):
        query = (
            "SELECT text, text_analysis "
            "FROM tweets "
        )
        results = list()
        for candidate in self.candidates:
            where_clause = "WHERE author_id='%s'" % candidate['user_id']
            custom_query = query + where_clause
            self.cursor.execute(custom_query)
            rows = self.cursor.fetchall()
            tweet_count = 0
            positive = 0
            negative = 0
            political = {
                'Liberal': 0,
                'Libertarian': 0,
                'Conservative': 0
            }
            for data in rows:
                data = data[1]
                # tweet count
                if len(data) == 0:
                    continue
                tweet_count += 1
                # positive count
                if data['sentiment'] >= 0.55:
                    positive += 1
                else:
                    negative += 1
                political['Liberal'] += data['political']['Liberal']
                political['Libertarian'] += data['political']['Libertarian']
                political['Conservative'] += data['political']['Conservative']
            # order
            labels = sorted(political, key=political.__getitem__, reverse=True)
            tw_url = "http://twitter.com/%s" % candidate["screen_name"][1:]
            results.append({
                "name": candidate["key_words"][0],
                "banner-pic": candidate["banner"],
                "profile-pic": candidate["profile"],
                "url_twitter": tw_url,
                "url_wikipedia": candidate['wikipedia'],
                "political-party": candidate["political_party"],
                "total-tweets": tweet_count,
                "positive-tweets": positive,
                "negative-tweets": negative,
                "orientation": labels[0]
            })
            with open('candidates2.json', 'w') as outfile:
                json.dump(results, outfile)
        return results

    def weekly_tweet_score(self, week_number):
        keyword_set = [c['key_words'] for c in self.candidates]
        results = list()
        if week_number == 0:
            query = (
                "SELECT text, text_analysis "
                "FROM tweets "
                "WHERE text_analysis::text!='{}'::text AND "
                "created_at < '%s' AND ("
            ) % WEEKS[week_number]
        else:
            query = (
                "SELECT text, text_analysis "
                "FROM tweets "
                "WHERE text_analysis::text!='{}'::text AND "
                "created_at >= '%s' AND created_at <= '%s' AND ("
            ) % WEEKS[week_number]
        vote_count = [[0, 0] for _ in range(len(keyword_set))]
        for i, kset in enumerate(keyword_set):
            from_clause = ''
            for k in kset[:-1]:
                from_clause += " text LIKE '%%%s%%' OR" % k
            from_clause += " text LIKE '%%%s%%')" % kset[-1]
            candidate_query = query + from_clause
            self.cursor.execute(candidate_query)
            rows = self.cursor.fetchall()
            for data in rows:
                # empty text_analysis
                if len(data[1]) == 0:
                    continue
                if data[1]['sentiment'] >= 0.55:
                    vote_count[i][0] += 1
                else:
                    vote_count[i][1] += 1
            if sum(vote_count[i]) == 0:
                score = 0
            else:
                score = wilson_score(vote_count[i][0], vote_count[i][1])[0]
            results.append({
                "party": self.candidates[i]['political_party'],
                "score": score,
            })
        return results

    def tweet_score(self):
        results = {
            'PRI': list(),
            'PAN': list(),
            'PRD': list(),
            'PT': list(),
            'MORENA': list(),
        }
        for i in range(len(WEEKS)-1):
            week_result = self.weekly_tweet_score(i+1)
            for data in week_result:
                results[data['party']].append(data['score'])
        return results

    def weekly_voter_score(self, week_number):
        parties = [c['political_party'] for c in self.candidates]
        party_count = [0 for c in self.candidates]
        party_count.append(0)
        parties.append('undecided')
        keyword_set = [c['key_words'] for c in self.candidates]
        results = list()
        if week_number == 0:
            query = (
                "SELECT author_id, text_analysis "
                "FROM tweets "
                "WHERE text_analysis::text!='{}'::text AND "
                "created_at < '%s' AND ("
            ) % WEEKS[week_number]
        else:
            query = (
                "SELECT author_id, text_analysis "
                "FROM tweets "
                "WHERE text_analysis::text!='{}'::text AND "
                "created_at >= '%s' AND created_at <= '%s' AND ("
            ) % WEEKS[week_number]
        vote_count = [[0, 0] for _ in range(len(keyword_set))]
        vote_count = dict()
        for i, kset in enumerate(keyword_set):
            from_clause = ''
            for k in kset[:-1]:
                from_clause += " text LIKE '%%%s%%' OR" % k
            from_clause += " text LIKE '%%%s%%')" % kset[-1]
            candidate_query = query + from_clause
            self.cursor.execute(candidate_query)
            rows = self.cursor.fetchall()
            for data in rows:
                user = data[0]
                if user not in vote_count.keys():
                    vote_count[user] = [[0, 0]
                                        for _ in range(len(keyword_set))]
                if len(data[1]) == 0:
                    continue
                if data[1]['sentiment'] >= 0.55:
                    vote_count[user][i][0] += 1
                else:
                    vote_count[user][i][1] += 1
        for user_id in vote_count.keys():
            for i, votes in enumerate(vote_count[user_id]):
                if votes[0] > votes[1]:
                    vote_count[user_id][i] = votes[0]
                else:
                    vote_count[user_id][i] = -1
            if sum(vote_count[user_id]) != -5:
                max_index = vote_count[user_id].index(max(vote_count[user_id]))
                party_count[max_index] += 1
            # all were -1
            else:
                # undecides
                party_count[-1] += 1
        places = zip(parties[:-1], party_count[:-1])
        places = sorted(places, key=lambda x: x[1], reverse=True)
        return WEEKS[week_number][0], party_count[-1], places

    def voter_score(self):
        results = list()
        for i in range(len(WEEKS) - 1):
            date, undecided, week_result = self.weekly_voter_score(i+1)
            results.append({'date': date})
            for index, data in enumerate(week_result):
                results[i][data[0]] = index + 1
            results[i]['undecided'] = undecided
        return results

