# %%
import googletrends as googletrends

# %% Get country names
geo_names = googletrends.get_geo_names()

# %% Linked-in example
# searchwords = ['corona', 'covid', 'Wuhan']
searchwords = ['bitcoin', 'ethereum']
geo = ['NL', 'united kingdom']
date_start = '01-12-2012'

# Temporal
results = googletrends.temporal(searchwords, geo=geo, date_start=date_start)
googletrends.plot(results, color_by_searchword=True, group_by_searchword=False)

#  spatio
results_spatio = googletrends.spatio(searchwords, geo=geo, date_start=date_start)
googletrends.plot(results_spatio)

# Trending
results_trending = googletrends.trending(searchwords, geo=geo, date_start=date_start)
googletrends.plot(results_trending)

# %% Gather temporal searches
results = googletrends.temporal(['corona','covid-19'], geo=['NL','DE','italy','BE'], date_start='01-01-2020')
# Make plot
googletrends.plot(results)

# %% Color and make different subgroups for the results.
googletrends.plot(results, color_by_searchword=True, group_by_searchword=False)
googletrends.plot(results, color_by_searchword=False, group_by_searchword=False)
googletrends.plot(results, color_by_searchword=False, group_by_searchword=True)
googletrends.plot(results, color_by_searchword=True, group_by_searchword=True)

# %% Gather searches over geographical locations
results = googletrends.spatio(['corona','covid-19'], geo=['NL','DE','italy','BE'], date_start='01-01-2020')
# Make plot
googletrends.plot(results)

# %% Make worldmap plot
googletrends.plot_worldmap(results)

# %% Gather searches over geographical locations
results = googletrends.trending(['corona','covid-19'], geo=['NL','DE','italy','ES','BE'], date_start='01-01-2020')
# Make plot
googletrends.plot(results)

# %% Results across all countries
results = googletrends.spatio(['corona','covid-19'], geo='world', date_start='01-01-2020')
# Make plot
googletrends.plot_worldmap(results_spatio)





# %% ----------------------------------------------------------------------
searchwords=['corona','covid-19','virus']
geo=['NL','DE','italy','ES','BE']
# searchwords=['Rijkswaterstaat','NFI']
# geo=['NL']
date_start='01-01-2020'

results = googletrends.trending(searchwords, geo=geo, date_start=date_start)
googletrends.plot(results)

results_temporal = googletrends.temporal(searchwords, geo=geo, date_start=date_start)
googletrends.plot(results_temporal)

results_spatio = googletrends.spatio(searchwords, geo=geo, date_start=date_start)
googletrends.plot(results_spatio)


# %%
results_trending = googletrends.trending(searchwords, geo=geo, date_start='27-03-2020')
googletrends.plot(results_trending)

results_temporal = googletrends.temporal(searchwords, geo=geo, date_start='23-03-2020')
googletrends.plot(results_temporal)

# %%
searchwords=['corona']
geo=['NL']
results = googletrends.trending(searchwords, geo=geo, date_start='01-01-2020', date_stop='29-03-2020')
googletrends.plot(results)

results = googletrends.trending(searchwords, geo=geo, date_start='01-01-2019', date_stop='29-03-2019')
googletrends.plot(results)

# %%
searchwords=['corona','covid-19','sars','mers']
searchwords=['corona']
searchwords=['corona','covid-19']

# %%
results = googletrends.temporal(searchwords, geo=['NL','china','hong kong','italy','US'], date_start='01-12-2019')

googletrends.plot(results, color_by_searchword=False, group_by_searchword=False)
googletrends.plot(results, color_by_searchword=True, group_by_searchword=False)
googletrends.plot(results, color_by_searchword=False, group_by_searchword=True)
googletrends.plot(results, color_by_searchword=True, group_by_searchword=True)

# %% Across all geo
searchwords='bitcoin'
geo=''
results = googletrends.temporal(searchwords, geo=geo, date_start='01-01-2010')
googletrends.plot(results, color_by_searchword=True, group_by_searchword=False, verbose=4)

# %% World
results = googletrends.spatio(searchwords, geo='NL', date_start='01-01-2010')
googletrends.plot(results)

# %% Geographical analysis
results = googletrends.spatio(searchwords, geo='NL', date_start='01-01-2010')
googletrends.plot(results)

results = googletrends.spatio(searchwords, geo='NL', date_start='01-01-2020', date_stop='01-02-2020')
googletrends.plot(results)

results = googletrends.spatio(searchwords, geo='NL', date_start='01-02-2020', date_stop='01-03-2020')
googletrends.plot(results)

results = googletrends.spatio(searchwords, geo='NL', date_start='01-03-2020')
googletrends.plot(results)

results = googletrends.spatio(searchwords, geo='NL', date_stop='01-02-2020')
googletrends.plot(results)

# %%