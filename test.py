import time

from random import randint
from statistics.popularity_measures import wilson_score
from statistics.rank_correlation import spearman_correlation

# Wilson Score Interval

# El Pulso de la Republica
print wilson_score(20671, 815)
print '------------'
# Chumel con Chumel Torres
print wilson_score(11424, 534)

# Spearman
eng = [randint(1, 100) for _ in range(1000)]
math = [randint(1, 100) for _ in range(1000)]

print spearman_correlation(eng, math)
