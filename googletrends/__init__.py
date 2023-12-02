from googletrends.googletrends import (
    plot,
    plot_worldmap,
    plot_trending,
    plot_spatio,
    plot_temporal,
    spatio,
    temporal,
    trending,
    get_geo_names,
)

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '0.1.2'

# module level doc-string
__doc__ = """
googletrends
=====================================================================

Description
-----------
Python package to examine trending, spatio and temporal google searching for input queries.

Example
-------
>>>
>>> # Trending results
>>> result = googletrends.trending(['corona','covid-19'], geo=['nl','italy'], date_start='01-12-2019')
>>> googletrends.plot(result)
>>>
>>> # Results on geogrpahical locations
>>> result = googletrends.spatio(['corona','covid-19'], geo=['nl','italy'], date_start='01-12-2019')
>>> googletrends.plot(result)
>>>
>>> # Results over time
>>> result = googletrends.temporal(['corona','covid-19'], geo=['nl','italy'], date_start='01-12-2019')
>>> googletrends.plot(result)

References
----------
* https://github.com/erdogant/googletrends
* https://mancap314.github.io/googletrends-py.html
* https://www.karinakumykova.com/2019/03/calculate-search-interest-with-pytrends-api-and-python/


"""
