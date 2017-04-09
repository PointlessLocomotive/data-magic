import numpy as np

from . import AT


def political_analysis(cluster):
    analysis = {
        'sentiment': np.mean([tweet.sentiment for tweet in cluster]),
        'topic1': np.mean([tweet.topic1 for tweet in cluster]),
        'topic2': np.mean([tweet.topic2 for tweet in cluster]),
        'topic3': np.mean([tweet.topic3 for tweet in cluster]),
        'topic4': np.mean([tweet.topic4 for tweet in cluster]),
        'topic5': np.mean([tweet.topic5 for tweet in cluster]),
        'green': np.mean([tweet.green for tweet in cluster]),
        'libertarian': np.mean([tweet.libertarian for tweet in cluster]),
        'liberal': np.mean([tweet.liberal for tweet in cluster]),
        'conservative': np.mean([tweet.conservative for tweet in cluster]),
        'cluster_size': len(cluster)
    }
    return analysis
