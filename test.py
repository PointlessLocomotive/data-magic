from statistics.popularity_measures import WilsonScoreInterval


wsi = WilsonScoreInterval(20671, 815)  # El Pulso de la Republica

upper, lower = wsi.calculate()

print lower

print '------------'

wsi = WilsonScoreInterval(11424, 534)  # Chumel con Chumel Torres

upper, lower = wsi.calculate()

print lower
