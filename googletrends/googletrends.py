""" This function returns a dataframe with google trends results of the input search

	A=trends(searchwords, date_start, date_stop, <optional>)

 INPUT:
   searchwords:     String or array with strings
                   'bitcoin'
                   ['bitcoin','ripple','crypto']
                   
 OPTIONAL

   date_start:     String: Start date to count frequency of searchwords
                   "01-01-2011"
                   
   date_stop:      String: Stop date to count frequency of searchwords
                   "22-08-2018"
                                      
   geo:            String: Filter on geo-graphical location
                   ''   (No filter: World)(default)
                   'NL' (only netherlands)

   timeframe:      String: Timeframe from today
                   '' (default)
                   'today #-Y'
                   'today #-m'
                   'now 7-d'  
                   'now 1-H'  

   showfig:        Boolean [True,False]: Line-plot, wordcloud and geographical plot
                   True: Yes (default)
                   False: No 

   verbose:        Boolean [0,1] or [True,False]
                   True: Yes (default)
                   False: No 

 OUTPUT
	pandas dataframe

        
 EXAMPLE

"""

# -------------------------------------------------------
# Name        : googletrends.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# github      : https://github.com/erdogant/googletrends
# Licence     : MIT
# -------------------------------------------------------

# Libraries
from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.preprocessing import MinMaxScaler
import googletrends.utils.check_connection as check_connection
from scipy.interpolate import make_interp_spline
import colourmap
import worldmap


# %%
def _set_dates(date_start, date_stop, verbose=3):
    # Set defaults
    if date_start is None:
        raise Exception('[googletrends] date_start must be filled in.')
    if date_stop is None:
        date_stop = time.strftime("%d-%m-%Y")

    date_start = pd.to_datetime(date_start, format="%d-%m-%Y")
    date_stop = pd.to_datetime(date_stop, format="%d-%m-%Y")
    date_range = ['%s %s' % (str(date_start.date()), str(date_stop.date()))]

    if verbose>=3: print('[googletrends] %s - %s' %(date_start.strftime("%d %B %Y"), date_stop.strftime("%d %B %Y")))

    return date_start, date_stop, date_range


# %%
def _initialize(searchwords, date_start, date_stop, geo, method, cat=0, include_suggestions=False, verbose=3):
    # https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories
    # cat=0  : All categories
    # cat=47 : Autos & Vehicles
    # method : Can be 'images', 'news', 'youtube' or 'froogle' (for Google Shopping results)

    # Convert name to code
    if geo is None:geo = ''
    if len(geo)>3:
        geo=worldmap.county2code(geo)[0][0]
    geo = geo.upper()
    # Set dates
    date_start, date_stop, date_range = _set_dates(date_start, date_stop, verbose=verbose)
    # Set up the trend fetching object
    pytrends = TrendReq(hl='en-US', tz=360)

    # Include google suggestions
    if include_suggestions:
        suggested_words = []
        for word in searchwords:
            suggested_words = suggested_words + list(pd.DataFrame(pytrends.suggestions(word))['title'].values)
        searchwords = searchwords + suggested_words
        if verbose>=3: print('[googletrends] [%d] suggestions included.' %(len(suggested_words)))

    if date_start!=date_stop:
        if geo=='':
            pytrends.build_payload(searchwords, cat=cat, timeframe=date_range[0], gprop=method)
        else:
            pytrends.build_payload(searchwords, geo=geo, cat=cat, timeframe=date_range[0], gprop=method)
    else:
        raise Exception('Start and stop time must be different.')
        # pytrends.build_payload(searchwords, geo=geo, cat=0, timeframe=timeframe, gprop=method)

    return(pytrends, geo)


# %%
def related_topics(searchwords, date_start=None, date_stop=None, geo=None, method='news', verbose=3):
    if not check_connection.internet():
        raise Exception('No internet connection')
    if isinstance(searchwords, str):
        searchwords=[searchwords]
    if geo is None:
        raise Exception('parameter [geo] must be provided.')

    # Initialize
    pytrends, geo = _initialize(searchwords, date_start, date_stop, geo, method, verbose=verbose)

    # Retrieve the interest over time
    related_queries = pytrends.related_queries()
    trending_searches = pytrends.trending_searches(pn=worldmap.code2county(geo)[1].lower())

    out = {}
    out['method'] = 'related_topics'
    out['df_related_queries'] = related_queries
    out['df_trending_searches'] = trending_searches
    out['geo'] = geo
    out['searchwords'] = searchwords
    return(out)


# %%
def temporal(searchwords, date_start=None, date_stop=None, geo=None, method='news', verbose=3):
    # If you choose a time period that is 3 months or shorter you get daily data, otherwise you get weekly data.
    # If the time period is 3 years or longer, the monthly data is plotted, otherwise it is weekly data.

    if not check_connection.internet():
        raise Exception('No internet connection')
    if isinstance(searchwords, str):
        searchwords=[searchwords]
    if isinstance(geo, str):
        geo=[geo]
    if verbose>=3:
        print('[googletrends] Collecting trends over time for geographically: %s' %(geo))

    # Get data range and message
    dsart, dstop, date_range = _set_dates(date_start, date_stop, verbose=verbose)

    # Collect data per searchword
    df_geo = {}
    for geo_name in geo:
        dftmp = []
        for searchword in searchwords:
            if verbose>=3: print('[googletrends] [%s] Working on %s..' %(geo_name, searchword))
            pytrends, geo_name = _initialize([searchword], date_start, date_stop, geo_name, method, verbose=0)
            data_time = pytrends.interest_over_time()
            # data_time = pytrends.get_historical_interest([searchword], year_start=dsart.year, month_start=dsart.month, day_start=dsart.day, hour_start=0, year_end=dstop.year, month_end=dstop.month, day_end=dstop.day, hour_end=0, cat=0, geo=geo, gprop=method, sleep=0)
            if not data_time.empty:
                data_time.sort_values('date', inplace=True)
                dftmp.append(data_time[[searchword]])

        # Combine data in 1 dataframe
        dftmp = pd.concat(dftmp, axis=1)
        dftmp.reset_index(inplace=True, drop=False)
        df_geo[geo_name]={}
        df_geo[geo_name]=dftmp

    out = {}
    out['method'] = 'time_interval'
    out['df'] = df_geo
    out['geo'] = geo
    out['searchwords'] = searchwords
    out['date_range'] = date_range
    return(out)


# %%
def spatio(searchwords, geo='', date_start=None, date_stop=None, method='news', include_suggestions=False, verbose=3):
    if not check_connection.internet():
        raise Exception('No internet connection')
    if isinstance(searchwords, str):
        searchwords=[searchwords]

    # Get data range and message
    _, _, date_range = _set_dates(date_start, date_stop, verbose=verbose)

    # Collect data per searchword
    df_city = []
    df_country = []
    for searchword in searchwords:
        if verbose>=3: print('[googletrends] Working on %s..' %(searchword))
        data_per_city, data_per_country = _country_per_searchword([searchword], geo=geo, date_start=date_start, date_stop=date_stop, method=method, include_suggestions=include_suggestions, verbose=0)
        df_city.append(data_per_city)
        df_country.append(data_per_country)

    # Combine data in 1 dataframe
    df_city = pd.concat(df_city, axis=1)
    df_country = pd.concat(df_country, axis=1)

    # Fin
    out = {}
    out['method'] = 'geo'
    out['df'] = df_city
    out['country'] = df_country
    out['geo'] = geo
    out['date_range'] = date_range
    out['searchwords'] = searchwords
    return(out)


# %%
def _country_per_searchword(searchword, geo='', date_start=None, date_stop=None, method='news', include_suggestions=False, verbose=3):
    # Initialize
    pytrends, _ = _initialize(searchword, date_start, date_stop, geo, method, include_suggestions=include_suggestions, verbose=verbose)

    # Results on GEO-location
    try:
        if verbose>=3: print('[googletrends] Collecting trends over geographical location.')
        trends_GEO_CITY = pytrends.interest_by_region(resolution='CITY', inc_low_vol=True, inc_geo_code=False)
        trends_GEO_COUNTRY = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
        # trends_GEO_DMA = pytrends.interest_by_region(resolution='DMA', inc_low_vol=True, inc_geo_code=False)
        # trends_GEO_REGION  = pytrends.interest_by_region(resolution='REGION')
    except Exception as e:
        print(e)
        if verbose>=3: print('[googletrends] Google Search for GEO Trend retrieval failed.')
        trends_GEO_CITY=None
        trends_GEO_COUNTRY=None
        # trends_GEO_DMA=None
    
    return trends_GEO_CITY, trends_GEO_COUNTRY


# %%
def _make_colors(results, cmap, color_by_searchword):
    if color_by_searchword:
        colors = colourmap.generate(len(results['searchwords']), cmap=cmap, method='seaborn')
        alpha=0.1
    else:
        colors = colourmap.generate(len(results['df']), cmap=cmap, method='seaborn')
        alpha=0.2
    
    return(colourmap.rgb2hex(colors), alpha)


# %%
def _make_plots(results, group_by_searchword, figsize):
    if group_by_searchword:
        nrplots = len(results['searchwords'])
    else:
        nrplots = len(results['df'])

    if figsize=='auto':
        figsize=(20,10)
        fig, ax = plt.subplots(nrplots, 1, figsize=(figsize[0]*np.floor(nrplots/2),figsize[1]*np.floor(nrplots/2)))
    else:
        fig, ax = plt.subplots(nrplots, 1, figsize=figsize)
    
    return fig, ax


# %%
def _make_smooth_line(xs, ys, smooth_factor=3):
    # Make smooth line
    # xs = df['date'].values
    xnew = np.linspace(0, len(xs), len(xs) * smooth_factor)
    # ys = df[searchword].values
    spl = make_interp_spline(range(0,len(xs)), ys, k=2)
    ynew = spl(xnew)
    ynew[ynew<0]=0
    return xnew, ynew


# %%
def plot_temporal(results, figsize='auto', cmap='Set1', color_by_searchword=True, group_by_searchword=False, verbose=3):
    window=5
    linestyles = ['-', '--', '-.', ':']
    linewidths = [0.5, 1, 1.5, 2, 2.5]

    # Make subplots
    fig, ax = _make_plots(results, group_by_searchword, figsize)
    # Make colors
    colors, alpha = _make_colors(results, cmap, color_by_searchword)

    # Walk across maps
    for i, key in enumerate(results['df'].keys()):
        if not results['df'][key].empty:
            # df = pd.DataFrame()
            df = results['df'][key].rolling(window, min_periods=1).mean()
            xs = results['df'][key]['date']

            linestyle = linestyles[np.mod(i, len(linestyles))]
            linewidth = linewidths[np.mod(i, len(linewidths))]

            # Walk across searchwords
            for k, searchword in enumerate(results['searchwords']):
                # Set colors and graph nr.
                if searchword not in df.columns: df[searchword]=0
                color = colors[k] if color_by_searchword else colors[i]
                pi = np.mod(k, len(results['searchwords'])) if group_by_searchword else np.mod(i, len(results['df']))
                # Make smooth line
                ys = df[searchword]
                xnew, ynew = _make_smooth_line(xs.values, ys.values)
                # Draw the line
                ax[pi].plot(xnew, ynew, color=color, ls=linestyle, lw=linewidth, label=key + ' ' + searchword)
                ax[pi].fill_between(range(0,len(xs)), ys, where=ys>=np.zeros(len(xs)), interpolate=True, color=color, alpha=alpha)

    idx = np.arange(0,len(xs),step=5)
    xsnew = np.array(list(map(lambda x: x.strftime('%d-%m-%Y'), xs)))
    ax[0].set_title('Date: ' + results['date_range'][0] + '\nGeographically: ' + ', '.join(results['geo']))
    for i in range(0,len(ax)):
        ax[i].legend()
        ax[i].grid(True)
        ax[i].set_xticklabels(xsnew[idx], rotation=20)
        ax[i].set_ylabel('Normalized Google searches')

    return fig, ax


# %%
def plot_spatio(results, figsize=(15,8), verbose=3):
    # Plot stacked-bar plot
    if not results['df'].empty:
        ax = results['df'].plot(kind='bar', stacked=True, figsize=figsize, grid=True)
        ax.set_ylabel('Normalized Google searches')
        ax.set_title('Date: ' + results['date_range'][0] + '\nGeographically: ' + results['geo'])
        # Plot map
        plot_map(results)


# %%
def plot_related_topics(results, figsize=(15,8), verbose=3):

    getkeys=list(results['df_related_queries'].keys())
    gettext=[]

    for i in range(0, len(getkeys)):
        if 'NoneType' not in str(type(results['df_related_queries'][getkeys[i]]['top'])):
            tmptext = results['df_related_queries'][getkeys[i]]['top']['query'] + ' '
            tmptext = results['df_related_queries'][getkeys[i]]['top']['value'] * tmptext
            gettext = np.append(gettext, tmptext.str.cat())

    try:
        from wordcloud import WordCloud
        if len(gettext)>0:
            if verbose>=3: print('[googletrends] Making word-cloud.')
            gettext = str(gettext[0])
            wordcloud = WordCloud(background_color='white', margin=10, max_font_size=40, width=600, height=300).generate(gettext)
            plt.subplots(figsize=figsize)
            plt.imshow(wordcloud, interpolation="bilinear")
    except:
        if verbose>=2: print('\n[googletrends] <pip install wordcloud> for wordcloud plots.')


# %% Make plot
def plot(results, figsize=(15,8), cmap=['#ff0000'], color_by_searchword=True, group_by_searchword=False, verbose=3):
    
    if results['method']=='geo':
        plot_spatio(results, figsize=figsize, verbose=verbose)
        
    if results['method']=='time_interval':
        fig, ax = plot_temporal(results, figsize=figsize, color_by_searchword=color_by_searchword, group_by_searchword=group_by_searchword, verbose=verbose)

    if results['method']=='related_topics':
        plot_related_topics(results, figsize=figsize, verbose=verbose)

        
# %%
def plot_map(results, figsize=(15,8), cmap=['#ff0000'], verbose=3):

    # SHOW ON MAP
    if (results['method']=='geo') and (not results['df'].empty):
        if verbose>=3: print('[googletrends] Superimposing geographical results on worldmap.')

        # Worldmap
        if results['geo']=='':
            map_name='world'
        else:
            map_name = worldmap.code2county(results['geo'])[1]

        # data = results['df'].sum(axis=1)

        # scale scores between [0-1]
        shape = results['df'].shape
        data = results['df'].values.reshape(-1,1)
        # Add extra 0 to make sure scaling occurs between 0 and max value
        data = np.concatenate((data,[[0],[100]]))
        scaler = MinMaxScaler(feature_range=(0,1))
        data = scaler.fit_transform(data)
        # Remove the additional 0 and reshape
        data = data[0:-2]
        data = data.reshape(shape)

        for i in range(0,data.shape[1]):
            # Color only those with value>0
            idx = np.where(data[:,i]>0)[0]
            county_names = results['df'].iloc[idx,i].index.values
            opacity = data[idx,i]
            filename = results['df'].columns[i] + '.svg'

            # If no data, set all on black
            if len(county_names)==0:
                county_names = results['df'].index.values
                opacity = 1
                cmap = ['#D3D3D3']

            # Plot on map
            out = worldmap.plot(county_names, map_name=map_name, opacity=opacity, cmap=cmap, filename=filename)
