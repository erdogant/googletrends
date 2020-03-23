from googletrends.googletrends import (
    plot,
    plot_map,
	spatio,
    temporal,
    related_topics,
)

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '0.1.0'

# module level doc-string
__doc__ = """
googletrends
=====================================================================

Description
-----------
googletrends is to quantify usage of search term in google and to determine related queries.


Example
-------
>>> import googletrends as google
>>> model = google.trends(X)
>>> fig,ax = google.plot(model)


References
----------
* https://github.com/erdogant/googletrends
* https://mancap314.github.io/googletrends-py.html
* https://pypi.org/project/pytrends/
* https://www.karinakumykova.com/2019/03/calculate-search-interest-with-pytrends-api-and-python/


"""
