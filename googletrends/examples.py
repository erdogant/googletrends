# %%
import googletrends as googletrends
print(dir(googletrends))
print(googletrends.__version__)

# %%
searchwords=['corona','covid-19','sars','mers','bitcoin']
# searchwords=['bitcoin']
searchwords=['corona']
searchwords=['corona','covid-19']

# %%
import worldmap
county_names = worldmap.list_county_names()
# worldmap.list_map_names()[0]
worldmap.county2code('hong kong')[0][0]

# %% Temporal analysis
results = googletrends.temporal(searchwords, geo='nl', date_start='01-10-2011')
googletrends.plot(results)

results = googletrends.temporal(searchwords, geo='', date_start='01-10-2011')
googletrends.plot(results)

results = googletrends.temporal(searchwords, geo='', date_start='01-01-2020')
googletrends.plot(results)

results = googletrends.temporal(searchwords, geo='NL', date_start='01-01-2020')
googletrends.plot(results)

results = googletrends.temporal(searchwords, geo=['NL','japan','hong kong','italy'], date_start='01-12-2019')
googletrends.plot(results)


# %% Geographical analysis
results = googletrends.spatio(searchwords, geo='NL', date_start='01-01-2020')
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
results = googletrends.related_topics(searchwords[0], geo='', date_start='01-01-2020')
googletrends.plot(results)


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
