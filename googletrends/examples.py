# %%
import googletrends as googletrends

# %% Linked-in example
searchwords = ['corona','covid-19','Wuhan']
geo = ['NL','italy']
date_start = '01-12-2019'

# Temporal
results_temp = googletrends.temporal(searchwords, geo=geo, date_start=date_start)
googletrends.plot(results_temp, color_by_searchword=True, group_by_searchword=False)

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
googletrends.plot(results, color_by_searchword=False, group_by_searchword=False)
googletrends.plot(results, color_by_searchword=True, group_by_searchword=False)
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
geo_names = googletrends.get_geo_names()

# worldmap.county2code('hong kong')[0][0]
# worldmap.county2code('china')[0][0]


# %%



# %%
import joypy
from matplotlib import cm

from sklearn import datasets
iris = datasets.load_iris(return_X_y=False)
df = pd.DataFrame(iris['data'], columns=iris['feature_names'])
fig, axes = joypy.joyplot(df, by="Name", ylim='own')


dfnew = [df[['bitcoin','year']], df[['sars','year']]]
dfnew = pd.concat(dfnew)
dfnew[np.isnan(dfnew)]=0
fig, axes = joypy.joyplot(dfnew, column=['sars','bitcoin'], by="year", figsize=(12,8), legend=True, alpha=0.9, grid="y", linewidth=1,  ylim='own')


dfnew = pd.DataFrame()
dfnew['bitcoin'] = df[['bitcoin','year']]

df = results['df']
df['year'] = df['date'].dt.year.astype(str)
df['corona'][df['corona']==0]=0.001
fig, axes = joypy.joyplot(df, column=['sars','bitcoin'], by="year", figsize=(12,8), legend=True, alpha=0.9, grid="y", linewidth=1,  ylim='own')
fig, axes = joypy.joyplot(df, column=['corona'], by="year", figsize=(12,8), legend=True, alpha=0.9, grid="y", linewidth=1,  ylim='own')
fig, axes = joypy.joyplot(df, column=['year'], by='bitcoin', figsize=(12,8), legend=True, alpha=0.9, grid="y", linewidth=1,  ylim='own')


labels = df['year'].unique()
# labels=[y if y%10==0 else None for y in list(df['year'].unique())]
fig, axes = joypy.joyplot(df, by="corona", column="corona", labels=labels, range_style='own', 
                          grid="y", linewidth=1, legend=True, figsize=(6,5),
                          title="Corona",
                          colormap=cm.autumn_r)

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import clusteval
from scipy.interpolate import make_interp_spline

out = googletrends.for_time(searchwords, geo=map_codes[0][0].upper(), date_start='01-06-2019', date_stop='18-01-2020')['df_trends']
out['spatio']=map_codes[0][0]
for i in range(1,len(map_codes[0])):
    df = googletrends.for_time(searchwords, geo=map_codes[0][i].upper(), date_start='01-06-2019', date_stop='18-03-2020')['df_trends']
    
    if not df.empty:
        df['spatio']=map_codes[1][i]
        out = pd.concat([out, df], axis=0, sort=False)


# out = pd.read_csv('D://stack//TOOLBOX_PY//REPOSITORIES//googletrends//googletrends//data//corona_all_countries.zip', sep=';')
N=200
Xdata=[]
uicountries = np.unique(out['spatio'])
plt.subplots(figsize=(20,8))
for spatio in uicountries:
    tmpdf=out.loc[out['spatio']==spatio,:]
    X = tmpdf[searchwords].sum(axis=1)
    plt.plot(tmpdf['date'], X, label=spatio, lw=0.8)

    # Make smooth line
    # Xinterp = np.linspace(0, len(tmpdf['search_sum']), N)
    # spl = make_interp_spline(np.arange(0,tmpdf.shape[0]), tmpdf['search_sum'].values, k=3)
    # power_smooth = spl(Xinterp)
    # plt.plot(Xinterp, power_smooth)
    # if len(Xdata)==0:
    #     Xdata = Xinterp
    # else:
    #     Xdata = np.c_[Xdata, Xinterp]

plt.grid(True)
plt.legend()

import clusteval

# %%
out = googletrends.for_related_topics(searchwords, geo='NL', date_start='01-01-2017', date_stop='18-01-2020')
googletrends.plot(out)


# %%
searchwords=['iphone', 'iphone release', 'iphone X', 'samsung', 'samsung release']
out = googletrends.geo(searchwords, date_start='01-01-2011', date_stop='04-10-2018')
out = googletrends.trends(searchwords,'01-01-2011','26-02-2018', geo='NL')
out = googletrends.trends(searchwords,timeframe='today 1-m', geo='NL')

# %%
searchwords=['kpn', 'kpn storing', 'xs4all storing']
searchwords=['xs4all storing', 'kpn storing', 'telfort storing']
searchwords=['telfort storing']
out = googletrends.trends(searchwords,'01-01-2011','04-10-2018', geo='NL')
out = googletrends.trends(searchwords, timeframe='now 7-d', geo='NL')
out = googletrends.trends(searchwords, timeframe='now 1-H', geo='NL')

# %%
searchwords=['Bitcoin']
out = googletrends.trends(searchwords,'01-01-2011', geo=None)
out = googletrends.trends(searchwords,'01-01-2011','10-09-2018', geo='NL')
out = googletrends.trends(searchwords,timeframe='now 7-d', geo='')
out = googletrends.trends(searchwords,timeframe='now 7-d', geo='NL')
out = googletrends.trends(searchwords,timeframe='today 6-m', geo='NL')

searchwords; date_start='01-01-2011'; date_stop='10-09-2018'; timeframe=''; width=15; height=8; geo=''; showfig=False; verbose=True; cmap=['#ff0000']


# %%
# Initialize the FacetGrid object
import seaborn as sns
df = results['df']
df = df['NL']

g = sns.FacetGrid(df, row="corona", hue="corona", aspect=5, height=3)

# # Draw the densities in a few steps
g.map(sns.kdeplot, "corona", shade=True, alpha=1, lw=3.5, bw=.2)
g.map(sns.kdeplot, "corona", color="w", lw=2, bw=.2)
g.map(plt.axhline, y=0, lw=2)

# # Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, color=color, ha="left", va="center", transform=ax.transAxes)
g.map(label, "corona")

# Set the subplots to overlap
g.fig.subplots_adjust(hspace=-.25)

# # Remove axes details that don't play well with overlap
g.set_titles("")
g.set(yticks=[])
g.despine(bottom=True, left=True)

# %%