"""Python package to examine trending, spatio and temporal google searching for input queries."""

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


# %% Trending google searches
def trending(searchwords, geo=None, date_start=None, date_stop=None, method='news', verbose=3):
    """ Gather data for trending google searches.

    Description
    -----------
    If you choose a time period that is 3 months or shorter you get daily data, otherwise you get weekly data.
    If the time period is 3 years or longer, the monthly data is plotted, otherwise it is weekly data.

    Parameters
    ----------
    searchwords : list
        Lookup each input word and return the (normalized) frequency of google searches.
        Example: ['Corona','earth quake']
    geo : list, optional
        Filter on geographical locations.
        'NL' (only netherlands),
        ['NL','germany','IT'],
        'world' to examine all countries
    date_start : str [dd-mm-yyyy]
        String: Start date for counting.
    date_stop : str [dd-mm-yyyy], optional
        String: Stop date for counting. If nothing is filled in, date of today is used.
    method : str, optional
        Type of google search. The default is 'news'.
        Choose on of those: 'images','news','youtube','froogle'
    verbose : int, optional
        Print message to screen. The default is 3.

    Raises
    ------
    Exception
        code 429: Too Many google requests in a given amount of time ("rate limiting").

    Returns
    -------
    dict containing results.

    Examples
    --------
    >>> result = googletrends.spatio(['corona','covid-19'], geo=['nl','italy'], date_start='01-12-2019')
    >>> googletrends.plot(result)
    >>> # Plot only on the worldmap
    >>> googletrends.plot_worldmap(result)

    """
    if not check_connection.internet():
        raise Exception('No internet connection')
    if isinstance(searchwords, str):
        searchwords=[searchwords]
    if isinstance(geo, str):
        geo=[geo]
    if geo is None:
        raise Exception('parameter [geo] must be provided.')
    if geo=='world':
        geo = get_geo_names()['code'].values

    # Convert to country name to code
    for i in range(0,len(geo)):
        if len(geo[i])>3:
            geo[i]=worldmap.county2code(geo[i])[0][0].upper()
    # Get data range and message
    _, _, date_range = _set_dates(date_start, date_stop, verbose=verbose)

    # Collect data per searchword
    df, df_rising, df_top = {},{},{}
    if verbose>=3: print('[googletrends]')
    for geo_name in geo:
        df[geo_name], df_rising[geo_name],df_top[geo_name] = {},{},{}
        dftmp, dftmp1, dftmp2=[],[],[]

        if verbose>=3: print('--------[%s]--------' % geo_name)

        for searchword in searchwords:
            try:
                # Initialize
                pytrends, _ = _initialize([searchword], date_start, date_stop, geo_name, method, verbose=0)
                # Trending
                trending_searches = pytrends.trending_searches(pn=worldmap.code2county(geo_name)[1].lower())
                trending_searches['searchword']=searchword
                dftmp.append(trending_searches)
                # Top
                related_queries = pytrends.related_queries()
                tmptop = pd.DataFrame(related_queries[searchword]['top'])
                if not tmptop.empty:
                    tmptop['searchword']=searchword
                    dftmp1.append(tmptop)
                # Rising
                tmprising=pd.DataFrame(related_queries[searchword]['rising'])
                if not tmprising.empty:
                    tmprising['searchword']=searchword
                    dftmp2.append(tmprising)

                if verbose>=3: print('[%s]\n   Top: %.0f\n   Rising: %.0f\n   Trending: %.0f' %(searchword, tmptop.shape[0], tmprising.shape[0], trending_searches.shape[0]))
            except:
                print('[googletrends] [%s][%s]: Warning: Could not retrieve informatie. Maybe wrong geo or searchword?' %(geo_name,searchword))

        # Combine data in 1 dataframe
        if len(dftmp1)>0:
            dftmp1 = pd.concat(dftmp1, axis=0)
            dftmp1.sort_values(by='value',ascending=False).reset_index(drop=True, inplace=True)
            df_top[geo_name]=dftmp1
        if len(dftmp2)>0:
            dftmp2 = pd.concat(dftmp2, axis=0)
            dftmp2.sort_values(by='value',ascending=False).reset_index(drop=True, inplace=True)
            df_rising[geo_name]=dftmp2
        if len(dftmp)>0:
            dftmp = pd.concat(dftmp, axis=0)
            dftmp.reset_index(drop=True, inplace=True)
            df[geo_name] = dftmp

    out = {}
    out['method'] = 'trending'
    out['trending'] = df
    out['rising'] = df_rising
    out['top'] = df_top
    out['geo'] = geo
    out['searchwords'] = searchwords
    out['date_range'] = date_range
    return(out)


# %% Google searches over time
def temporal(searchwords, geo=None, date_start=None, date_stop=None, method='news', verbose=3):
    """ Gather data for google searches over time.

    Parameters
    ----------
    searchwords : list
        Lookup each input word and return the (normalized) frequency of google searches.
        Example: ['Corona','earth quake']
    geo : list, optional
        Filter on geographical locations.
        'NL' (only netherlands)
        ['NL','germany','IT']
    date_start : str [dd-mm-yyyy]
        String: Start date for counting.
    date_stop : str [dd-mm-yyyy], optional
        String: Stop date for counting. If nothing is filled in, date of today is used.
    method : str, optional
        Type of google search. The default is 'news'.
        Choose on of those: 'images','news','youtube','froogle'
    verbose : int, optional
        Print message to screen. The default is 3.

    Raises
    ------
    Exception
        code 429: Too Many google requests in a given amount of time ("rate limiting").

    Returns
    -------
    dict containing results.
    
    Examples
    --------
    >>> result = googletrends.temporal(['corona','covid-19'], geo=['nl','italy'], date_start='01-12-2019')
    >>> googletrends.plot(result)

    """
    if not check_connection.internet():
        raise Exception('No internet connection')
    if isinstance(searchwords, str):
        searchwords=[searchwords]
    if geo=='world':
        geo = get_geo_names()['code'].values
    if isinstance(geo, str):
        geo=[geo]

    if verbose>=3:
        print('[googletrends] Collecting trends over time for geographically: %s' %(geo))

    # Get data range and message
    _, _, date_range = _set_dates(date_start, date_stop, verbose=verbose)
    # Convert to country name to code
    for i in range(0,len(geo)):
        if len(geo[i])>3:
            geo[i]=worldmap.county2code(geo[i])[0][0].upper()

    # Collect data per searchword
    df_geo = {}
    for geo_name in geo:
        dftmp = []
        for searchword in searchwords:
            try:
                if verbose>=3: print('[googletrends] [%s] Working on %s..' %(geo_name, searchword))
                pytrends, geo_name = _initialize([searchword], date_start, date_stop, geo_name, method, verbose=0)
                data_time = pytrends.interest_over_time()
                if not data_time.empty:
                    data_time.sort_values('date', inplace=True)
                    dftmp.append(data_time[[searchword]])
            except:
                if verbose>=2: print('[googletrends] [%s] Failed %s..' %(geo_name, searchword))

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


# %% Google searches for specific countries and counties
def spatio(searchwords, geo='', date_start=None, date_stop=None, method='news', include_suggestions=False, verbose=3):
    """Gather data for google searches over geographical locations and time.

    Parameters
    ----------
    searchwords : list
        Lookup each input word and return the (normalized) frequency of google searches.
        Example: ['Corona','earth quake']
    geo : list, optional
        Filter on geographical locations.
        'NL' (only netherlands)
        ['NL','germany','IT']
    date_start : str [dd-mm-yyyy]
        String: Start date for counting.
    date_stop : str [dd-mm-yyyy], optional
        String: Stop date for counting. If nothing is filled in, date of today is used.
    method : str, optional
        Type of google search. The default is 'news'.
        Choose on of those: 'images','news','youtube','froogle'
    include_suggestions : bool, optional
        Include suggestions. The default is False.
    verbose : int, optional
        Print message to screen. The default is 3.

    Raises
    ------
    Exception
        code 429: Too Many google requests in a given amount of time ("rate limiting").

    Returns
    -------
    dict containing results.
    
    Examples
    --------
    >>> result = googletrends.spatio(['corona','covid-19'], geo=['nl','italy'], date_start='01-12-2019')
    >>> googletrends.plot(result)

    """
    if not check_connection.internet():
        raise Exception('No internet connection')
    if isinstance(searchwords, str):
        searchwords=[searchwords]
    if geo=='':
        raise Exception('geo should be a string')
    if geo=='world':
        geo = get_geo_names()['code'].values
    if isinstance(geo, str):
        geo=[geo]

    # Get data range and message
    _, _, date_range = _set_dates(date_start, date_stop, verbose=verbose)
    # Convert to country name to code
    for i in range(0,len(geo)):
        if len(geo[i])>3: geo[i]=worldmap.county2code(geo[i])[0][0].upper()

    # Search for searchwords
    out = {}
    for geo_name in geo:
        out[geo_name] = _spatio_per_searchword(searchwords, geo=geo_name, date_start=date_start, date_stop=date_stop, method=method, include_suggestions=include_suggestions, verbose=verbose)

    # Fin
    out['method'] = 'geo'
    out['date_range'] = date_range
    out['searchwords'] = searchwords
    out['geo'] = geo
    # return
    return(out)


# %%
def _spatio_per_searchword(searchwords, geo='', date_start=None, date_stop=None, method='news', include_suggestions=False, verbose=3):
    if geo=='':
        raise Exception('geo should be a string')
    if isinstance(geo, list):
        raise Exception('geo should be a string and can not be of type list.')
    if isinstance(searchwords, str):
        searchwords=[searchwords]

    # Get data range and message
    _, _, date_range = _set_dates(date_start, date_stop, verbose=verbose)

    # Collect data per searchword
    df_city = []
    for searchword in searchwords:
        if verbose>=3: print('[googletrends] [%s] Working on %s..' %(geo, searchword))
        data_per_city = _country_per_searchword([searchword], geo=geo, date_start=date_start, date_stop=date_stop, method=method, include_suggestions=include_suggestions, verbose=0)
        df_city.append(pd.DataFrame(data_per_city))

    # Combine data in 1 dataframe
    df_city = pd.concat(df_city, axis=1)

    # Fin
    out = {}
    out['method'] = 'geo'
    out['df'] = df_city
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
        # trends_GEO_COUNTRY = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
        # trends_GEO_DMA = pytrends.interest_by_region(resolution='DMA', inc_low_vol=True, inc_geo_code=False)
        # trends_GEO_REGION  = pytrends.interest_by_region(resolution='REGION')
    except Exception as e:
        print(e)
        if verbose>=3: print('[googletrends] Google Search for GEO Trend retrieval failed.')
        trends_GEO_CITY=None

    return trends_GEO_CITY


# %%
def plot_temporal(results, figsize='auto', cmap='Set1', color_by_searchword=True, group_by_searchword=False, verbose=3):
    """Plot the temporal results.

    Parameters
    ----------
    results : dict
        results are derived from the temporal() function.
    figsize : tuple, optional
        Figure size (height, width). The default is 'auto'.
    cmap : str, optional
        colormap. The default is 'Set1'.
    color_by_searchword : bool, optional
        Color lines by searchwords. The default is True.
    group_by_searchword : TYPE, optional
        Make subplots based on searchwords. The default is False.
    verbose : int, optional
        Print message to screen. The default is 3.

    Returns
    -------
    fig : object
        Figure.
    ax : object
        Axis.

    Examples
    --------
    >>> result = googletrends.temporal(['corona','covid-19'], geo=['nl','italy'], date_start='01-12-2019')
    >>> googletrends.plot_temporal(result)

    """
    fig, ax = None, None
    window=5
    if group_by_searchword:
        linestyles = ['-', '--', '-.', ':']
        linewidths = [0.5, 1, 1.5, 2, 2.5]
    else:
        linestyles = ['-']
        linewidths = [1.5]

    # Make subplots
    fig, ax, fontsize = _make_plots(results, group_by_searchword, figsize, verbose=verbose)
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
                try:
                    xnew, ynew = _make_smooth_line(xs.values, ys.values)
                except:
                    xnew, ynew = np.arange(0, len(xs)), ys
                # Draw the line
                ax[pi].plot(xnew, ynew, color=color, ls=linestyle, lw=linewidth, label=key + ' ' + searchword)
                ax[pi].fill_between(range(0,len(xs)), ys, where=ys>=np.zeros(len(xs)), interpolate=True, color=color, alpha=alpha)

    # Set axis
    for i in np.arange(0, len(ax)):
        idx = list(np.arange(0,len(xs),step=10)) + [len(xs) - 1]
        ax[i].set_ylim([0,100])
        ax[i].set_xticks(idx)

        # labels on only bottom figure
        if i==(len(ax) - 1):
            xsnew = np.array(list(map(lambda x: x.strftime('%d-%m-%Y'), xs)))
            ax[i].set_xticklabels(xsnew[idx], rotation=30, fontsize=fontsize)
        else:
            ax[i].set_xticklabels('')

        ax[i].set_ylabel('Normalized Searches', fontsize=fontsize)
        ax[i].legend(loc='upper left', prop={'size': fontsize})
        ax[i].grid(True, axis='x', which='major', linestyle='--')
        ax[i].spines['top'].set_visible(False)
        ax[i].spines['right'].set_visible(False)
        ax[i].spines['bottom'].set_visible(False)
        ax[i].spines['left'].set_visible(False)

    ax[0].set_title('Date: ' + results['date_range'][0] + '\nGeographically: ' + ', '.join(results['geo']), fontsize=fontsize)

    return fig, ax


# %%
def plot_spatio(results, figsize=(15,8), showfig=True, verbose=3):
    """Plot the spatio results.

    Parameters
    ----------
    results : dict
        results are derived from the temporal() function.
    figsize : tuple, optional
        Figure size (height, width). The default is 'auto'.
    showfig : bool, optional
        When True, auto open the map figures in your browser. The default is 'True'.
    verbose : int, optional
        Print message to screen. The default is 3.

    Returns
    -------
    ax : object
        Axis.
    out_map : dict
        DataFrame containing map data.

    Examples
    --------
    >>> result = googletrends.spatio(['corona','covid-19'], geo=['nl','italy'], date_start='01-12-2019')
    >>> googletrends.plot_spatio(result)

    """
    ax, out_map = None, None
    # Plot stacked-bar plot
    if not results['df'].empty:
        ax = results['df'].plot(kind='bar', stacked=True, figsize=figsize, grid=True)
        ax.set_ylabel('Normalized Google searches')
        ax.set_title('Date: ' + results['date_range'][0] + '\nGeographically: ' + results['geo'])
        # Plot map
        out_map = _plot_map(results, showfig=showfig)
    # Return
    return ax, out_map


# %%
def plot_trending(results, figsize=(15,20), cmap='Set1', verbose=3):
    """Plot the trending results.

    Parameters
    ----------
    results : dict
        results are derived from the temporal() function.
    figsize : tuple, optional
        Figure size (height, width). The default is 'auto'.
    cmap : str, optional
        colormap. The default is 'Set1'.
    verbose : int, optional
        Print message to screen. The default is 3.

    Returns
    -------
    None.

    Examples
    --------
    >>> result = googletrends.trending(['corona','covid-19'], geo=['nl','italy'], date_start='01-12-2019')
    >>> googletrends.plot_trending(result)

    """
    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})
    fontsize=16

    # Nr of plots to make per geo
    keys=[]
    nrplots=[]
    # for i in np.arange(0,len(results['geo'])):
    for geo in results['geo']:
        tmpplots=0
        df = results['trending'].get(geo,None)
        if (df is not None) and (isinstance(df, pd.DataFrame)):
            tmpplots=tmpplots + 1
        df = results['top'].get(geo,None)
        if (df is not None) and (isinstance(df, pd.DataFrame)):
            tmpplots=tmpplots + 1
        df = results['rising'].get(geo,None)
        if (df is not None) and (isinstance(df, pd.DataFrame)):
            tmpplots=tmpplots + 1
        if tmpplots>0:
            keys.append(geo)
            nrplots.append(tmpplots)

    # Make plot per GEO
    for i in np.arange(0,len(keys)):
        fignum=0
        fig, ax = plt.subplots(nrplots[i],1, figsize=figsize)
        if nrplots[i]==1: ax=[ax]

        # Plot trending in line plot
        df = results['trending'].get(keys[i],None)
        if (df is not None) and (isinstance(df, pd.DataFrame)):
            colors = colourmap.fromlist(df['searchword'], cmap='Set1')
            gettext = df.iloc[:,0].values
            gettext = ' '.join(gettext)

            if len(gettext)>10:
                try:
                    from wordcloud import WordCloud
                    wordcloud = WordCloud(background_color='white', margin=10, max_font_size=40, width=600, height=300)
                    wordcloud.generate(gettext)
                    ax[fignum].imshow(wordcloud, interpolation="bilinear")
                    ax[fignum].spines['top'].set_visible(False)
                    ax[fignum].spines['right'].set_visible(False)
                    ax[fignum].spines['bottom'].set_visible(False)
                    ax[fignum].spines['left'].set_visible(False)
                    ax[fignum].set_xticks([])
                    ax[fignum].set_yticks([])
                    ax[fignum].set_title(('Top searches' + keys[i] + '\nDate: ' + results['date_range'][0]), fontsize=fontsize)
                    ax[fignum].set_xlabel('')
                    fignum=fignum + 1
                except:
                    if verbose>=2: print('\n[googletrends] <pip install wordcloud> for trending plots.')

        # Plot trending in line plot
        df = results['top'].get(keys[i],None)
        if (df is not None) and (isinstance(df, pd.DataFrame)):
            df = df.sort_values(by=['value'], ascending=False)
            colors = colourmap.fromlist(df['searchword'], cmap=cmap)
            df.plot.bar(ax=ax[fignum], x='query', y='value', figsize=figsize, color=colors[0], fontsize=fontsize, legend=False)
            ax[fignum].set_ylabel('Trending searches', fontsize=fontsize)
            ax[fignum].set_xlabel('')
            ax[fignum].spines['top'].set_visible(False)
            ax[fignum].spines['right'].set_visible(False)
            ax[fignum].spines['bottom'].set_visible(False)
            ax[fignum].spines['left'].set_visible(False)
            ax[fignum].grid(True, axis='y', which='major', linestyle='--')
            fignum=fignum + 1

        # Plot trending in line plot
        df = results['rising'].get(keys[i],None)
        if (df is not None) and (isinstance(df, pd.DataFrame)):
            df = df.sort_values(by=['value'], ascending=False)
            colors = colourmap.fromlist(df['searchword'], cmap=cmap)
            df.plot.bar(ax=ax[fignum], x='query', y='value', figsize=figsize, color=colors[0], fontsize=fontsize, legend=False)
            ax[fignum].set_ylabel('Rising searches', fontsize=fontsize)
            ax[fignum].spines['top'].set_visible(False)
            ax[fignum].spines['right'].set_visible(False)
            ax[fignum].spines['bottom'].set_visible(False)
            ax[fignum].spines['left'].set_visible(False)
            ax[fignum].set_xlabel('')
            ax[fignum].grid(True, axis='y', which='major', linestyle='--')
            fignum=fignum + 1


# %% Make plot
def plot(results, figsize='auto', cmap=['#ff0000'], color_by_searchword=True, group_by_searchword=False, showfig=True, verbose=3):
    """Plot results generated by trending, spatio or temporal.

    Parameters
    ----------
    results : dict
        results are derived from the temporal() function.
    figsize : tuple, optional
        Figure size (height, width). The default is 'auto'.
    cmap : str, optional
        colormap. The default is 'Set1'.
    color_by_searchword : bool, optional
        Color lines by searchwords. The default is True.
    group_by_searchword : TYPE, optional
        Make subplots based on searchwords. The default is False.
    showfig : bool, optional
        When True, auto open the map figures in your browser. The default is 'True'.
    verbose : int, optional
        Print message to screen. The default is 3.

    Returns
    -------
    None.

    Examples
    --------
    >>> # Trending results
    >>> result = googletrends.trending(['corona','covid-19'], geo=['nl','italy'], date_start='01-12-2019')
    >>> googletrends.plot(result)
    >>> # Results on geogrpahical locations
    >>> result = googletrends.spatio(['corona','covid-19'], geo=['nl','italy'], date_start='01-12-2019')
    >>> googletrends.plot(result)
    >>> # Results over time
    >>> result = googletrends.temporal(['corona','covid-19'], geo=['nl','italy'], date_start='01-12-2019')
    >>> googletrends.plot(result)

    """
    out = {}

    if results['method']=='geo':
        if figsize=='auto': figsize=(15,8)
        for key in results['geo']:
            out[key] = plot_spatio(results[key], figsize=figsize, showfig=showfig, verbose=verbose)
        if len(results['geo'])>1:
            plot_worldmap(results, cmap=cmap, showfig=showfig)

    if results['method']=='time_interval':
        fig, ax = plot_temporal(results, figsize=figsize, color_by_searchword=color_by_searchword, group_by_searchword=group_by_searchword, verbose=verbose)

    if results['method']=='trending':
        if figsize=='auto': figsize=(15,20)
        plot_trending(results, figsize=figsize, verbose=verbose)


# %%
def plot_worldmap(results, cmap=['#ff0000'], showfig=True, verbose=3):
    """Plot results on the worldmap derived from googletrends.spatio().

    Parameters
    ----------
    results : dict
        results are derived from the temporal() function.
    figsize : tuple, optional
        Figure size (height, width). The default is 'auto'.
    showfig : bool, optional
        When True, auto open the map figures in your browser. The default is 'True'.
    verbose : int, optional
        Print message to screen. The default is 3.

    Returns
    -------
    dict containing results.

    Examples
    --------
    >>> # Trending results
    >>> result = googletrends.spatio(['corona','covid-19'], geo=['nl','italy'], date_start='01-12-2019')
    >>> googletrends.plot_worldmap(results_spatio)

    """
    out = None
    if verbose>=3: print('[googletrends] Superimposing geographical results on worldmap.')

    df = []
    county_names=[]
    for geo_name in results['geo']:
        dftmp = results[geo_name]['df']
        dftmp['geo']=worldmap.code2county(geo_name)[1]
        df.append(dftmp)

    # Combine data in 1 dataframe
    df = pd.concat(df, axis=0)
    df = df.groupby(by='geo').sum()
    data, colnames, idx_names = _normalize_data(df)

    for i in range(0,data.shape[1]):
        # Color only those with value>0
        idx = np.where(data[:,i]>0)[0]
        county_names = idx_names[idx]
        opacity = data[idx,i]
        filename = colnames[i] + '_worldmap.svg'

        # If no data, set all on black
        if len(county_names)==0:
            county_names = idx_names
            opacity = 1
            cmap = ['#D3D3D3']

        # Plot on map
        out = worldmap.plot(county_names, map_name='world', opacity=opacity, cmap=cmap, filename=filename, showfig=showfig)

    return(out)


# %%
def _plot_map(results, figsize=(15,8), cmap=['#ff0000'], showfig=True, verbose=3):
    out=None
    if (results['method']=='geo') and (not results['df'].empty):
        # get map name
        map_name = worldmap.code2county(results['geo'])[1]
        # Normalize
        data, colnames, idx_names = _normalize_data(results['df'])
        # Plot per searchword
        for i in range(0,data.shape[1]):
            # Color only those with value>0
            idx = np.where(data[:,i]>0)[0]
            # county_names = results['df'].iloc[idx,i].index.values
            county_names = idx_names[idx]
            opacity = data[idx,i]
            filename = colnames[i] + '.svg'

            # If no data, set all on black
            if len(county_names)==0:
                county_names = idx_names
                opacity = 1
                cmap = ['#D3D3D3']

            # Plot on map
            out = worldmap.plot(county_names, map_name=map_name, opacity=opacity, cmap=cmap, filename=filename, showfig=showfig)

    return out


# %% Import example dataset from github.
def get_geo_names(url='https://erdogant.github.io/datasets/country_and_code.zip', verbose=3):
    """Import dataset from github.

    Parameters
    ----------
    url : str
        url-Link to dataset.
    verbose : int, optional
        Print message to screen. The default is 3.

    Returns
    -------
    tuple containing import status and resources.

    """
    import wget
    import os
    curpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    PATH_TO_DATA = os.path.join(curpath, wget.filename_from_url(url))

    # Check file exists.
    if not os.path.isfile(PATH_TO_DATA):
        if verbose>=3: print('[googletrends] Downloading resources..')
        wget.download(url, curpath)

    # Extract and import local dataset
    df = pd.read_csv(PATH_TO_DATA)
    df['code'] = df['code'].str.upper()
    # Return
    return df


# %%
def _normalize_data(df):
    # scale scores between [0-1]
    shape = df.shape
    data = df.values.reshape(-1,1)
    # Add extra 0 to make sure scaling occurs between 0 and max value
    data = np.concatenate((data,[[0],[100]]))
    scaler = MinMaxScaler(feature_range=(0,1))
    data = scaler.fit_transform(data)
    # Remove the additional 0 and reshape
    data = data[0:-2]
    data = data.reshape(shape)
    # Add total
    data = np.c_[data, np.sum(data, axis=1)]
    colnames = list(df.columns.values)
    colnames.append('total')
    idx_names = df.index.values
    # return
    return(data, colnames, idx_names)


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
def _make_colors(results, cmap, color_by_searchword):
    if color_by_searchword:
        colors = colourmap.generate(len(results['searchwords']), cmap=cmap, method='seaborn')
        alpha=0.1
    else:
        colors = colourmap.generate(len(results['df']), cmap=cmap, method='seaborn')
        alpha=0.2

    return(colourmap.rgb2hex(colors), alpha)


# %%
def _make_plots(results, group_by_searchword, figsize, verbose=3):
    if group_by_searchword:
        nrplots = len(results['searchwords'])
    else:
        nrplots = len(results['df'])

    if figsize=='auto':
        figsize=(20,10)
        ratio=np.maximum(np.floor(nrplots / 2), 1)
        fig, ax = plt.subplots(nrplots, 1, figsize=(figsize[0] * ratio,figsize[1] * ratio))
        fontsize=13 * ratio
    else:
        fig, ax = plt.subplots(nrplots, 1, figsize=figsize)
        fontsize=10

    try:
        if len(ax)>0:
            pass
    except:
        ax = [ax]

    if verbose>=4: print(figsize)
    return fig, ax, fontsize


# %%
def _make_smooth_line(xs, ys, smooth_factor=3):
    # Make smooth line
    # xs = df['date'].values
    xnew = np.linspace(0, len(xs), len(xs) * smooth_factor)
    # ys = df[searchword].values
    spl = make_interp_spline(range(0,len(xs)), ys, k=2)
    ynew = spl(xnew)
    ynew[ynew<0]=0
    # return
    return xnew, ynew
