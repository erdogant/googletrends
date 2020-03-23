""" This function returns a dataframe with google trends results of the input search
    Search for search term in google news
    Show related queries, rising related queries

	A=get_google_trends(searchword, date_start, date_stop, <optional>)

 INPUT:
   searchword:     String or array with strings
                   'bitcoin'
                   ['bitcoin','ripple','crypto']
                   
 OPTIONAL

   date_start:     String: Start date to count frequency of searchword
                   "01-01-2011"
                   
   date_stop:      String: Stop date to count frequency of searchword
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

 DESCRIPTION
   Returns a pandas dataframe containing the frequency of searchword per day in the date-range
   Search for search term in google news
   Show related queries, rising related queries
   https://mancap314.github.io/googletrends-py.html
   https://pypi.org/project/pytrends/
   
        
 EXAMPLE
   %reset -f
   import sys, os, importlib
   import startup; startup.startup(pydir='')
   import get_google_trends as eta
   importlib.reload(eta)
   %matplotlib auto

   searchword=['iphone', 'iphone release', 'iphone X', 'samsung', 'samsung release']
   out = eta.get_google_trends(searchword,'01-01-2011','04-10-2018', showfig=True)
   out = eta.get_google_trends(searchword,'01-01-2011','26-02-2018', geo='NL', showfig=True)
   out = eta.get_google_trends(searchword,timeframe='today 1-m', geo='NL', showfig=True)

   searchword=['kpn', 'kpn storing', 'xs4all storing']
   searchword=['xs4all storing', 'kpn storing', 'telfort storing']
   searchword=['telfort storing']
   out = eta.get_google_trends(searchword,'01-01-2011','04-10-2018', geo='NL', showfig=True)
   out = eta.get_google_trends(searchword, timeframe='now 7-d', geo='NL', showfig=True)
   out = eta.get_google_trends(searchword, timeframe='now 1-H', geo='NL', showfig=True)

   searchword=['Bitcoin']
   out = eta.get_google_trends(searchword,'01-01-2011','10-09-2018', geo='', showfig=True)
   out = eta.get_google_trends(searchword,'01-01-2011','10-09-2018', geo='NL', showfig=True)
   out = eta.get_google_trends(searchword,timeframe='now 7-d', geo='', showfig=True)
   out = eta.get_google_trends(searchword,timeframe='now 7-d', geo='NL', showfig=True)
   out = eta.get_google_trends(searchword,timeframe='today 6-m', geo='NL', showfig=True)


"""
#print(__doc__)

#--------------------------------------------------------------------------
# Name        : get_google_trends.py
# Version     : 1.0
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Aug. 2018
#--------------------------------------------------------------------------
# searchword; date_start='01-01-2011'; date_stop='10-09-2018'; timeframe=''; width=15; height=8; geo=''; showfig=False; verbose=True; cmap=['#ff0000']

#%%
def get_google_trends(searchword, date_start='', date_stop='', timeframe='', width=15, height=8, geo='', cmap=['#ff0000'], showfig=False, verbose=True):
	#%% DECLARATIONS
    Param = {}
    Param['searchword']  = searchword
    Param['verbose']     = verbose
    Param['date_start']  = date_start
    Param['date_stop']   = date_stop
    Param['showfig']     = showfig
    Param['width']       = width
    Param['height']      = height
    Param['geo']         = geo # 'NL'
    Param['cmap']        = cmap
    Param['timeframe']   = timeframe

    #%% Libraries
    from pytrends.request import TrendReq
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import time

    out                = dict()
    trends             = []
    related_queries    = []
    trends_GEO_CITY    = []
    trends_GEO_COUNTRY = []
    trends_GEO_DMA     = []
    
    #%% Convert to pandas datetime for indexing dataframe
    if 'str' in str(type(Param['searchword'])):
        Param['searchword']=[Param['searchword']]
    #end
    
    if Param['date_start']=='':
        Param['date_start'] = time.strftime("%d/%m/%Y")
    if Param['date_stop']=='':
        Param['date_stop'] = time.strftime("%d/%m/%Y")
    #end
    
    Param['date_start'] = pd.to_datetime(Param['date_start'], infer_datetime_format=True)
    Param['date_stop']  = pd.to_datetime(Param['date_stop'], infer_datetime_format=True)
    date_range = ['%s %s' % (str(Param['date_start'].date()), str(Param['date_stop'].date()))]
    maxyears = np.minimum(pd.datetime.now().year-Param['date_start'].year, 5)

    if timeframe=='':
        timeframe = 'today '+str(maxyears)+'-y'
    #end
    
    #%% Set up the trend fetching object
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list  = Param['searchword']

    #%% RESULTS ON GEOGRAPHICAL LOCATION
    try:
        if Param['verbose']: print('[GOOGLE TRENDS] Collecting trends over geographical locations.')
        if Param['date_start']!=Param['date_stop']:
            pytrends.build_payload(kw_list, geo=Param['geo'], cat=0, timeframe=date_range[0], gprop='news')
        else:
            pytrends.build_payload(kw_list, geo=Param['geo'], cat=0, timeframe=timeframe, gprop='news')
        #end
            
        trends_GEO_CITY    = pytrends.interest_by_region(resolution='CITY')
        trends_GEO_COUNTRY = pytrends.interest_by_region(resolution='COUNTRY')
        trends_GEO_DMA     = pytrends.interest_by_region(resolution='DMA')
#        trends_GEO_REGION  = pytrends.interest_by_region(resolution='REGION')        
    except Exception as e:
        if Param['verbose']: print('\n[GOOGLE TRENDS] Google Search for GEO Trend retrieval failed.')
        print(e)
    #end    

    #%% RESULTS ON TIME
    try:
        # Create the search object
        if Param['verbose']: print('[GOOGLE TRENDS] Collecting trends over time.')
        pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=Param['geo'], gprop='news')
        trends1 = pytrends.interest_over_time()
        trends1['date']=trends1.index
        
        # Do the same thing but then with date_range
        if  Param['date_start']!=Param['date_stop']:
            pytrends.build_payload(kw_list, cat=0, timeframe=date_range[0], geo=Param['geo'], gprop='news')
            trends2 = pytrends.interest_over_time()
            trends2['date']=trends2.index

            # Combine trends
            trends = trends1.append([trends2], ignore_index=True)
        else:
            trends=trends1
        #end
        
        trends.index=trends.date
        trends.sort_values('date', inplace=True)
        trends.reset_index(inplace=True, drop=True)
        trends.set_index('date', inplace=True)
        trends = trends.reset_index()

        # Retrieve the interest over time
        related_queries = pytrends.related_queries()
        
        # Summarize
        trends['search_sum']  = trends[Param['searchword']].sum(axis=1)
        trends['search_mean'] = trends[Param['searchword']].mean(axis=1)
    except Exception as e:
        if Param['verbose']: print('\n[GOOGLE TRENDS] Google Search Trend retrieval failed.')
        print(e)
    #end    
    
    #%% LINE PLOT WITH TREND
    if len(trends)>0 and Param['showfig']:
        if Param['verbose']: print('[GOOGLE TRENDS] Making scatter plot.')
        plt.subplots(figsize=(Param['width'], Param['height']))
#        plt.plot(trends.date,trends[Param['searchword']+['search_mean']])
#        plt.legend(Param['searchword']+['Average across all'])
        plt.plot(trends.date,trends[Param['searchword']])
        plt.legend(Param['searchword'])
        plt.grid(True)
        plt.xlabel('Date')
        plt.ylabel('Frequency')
        plt.title('Absolute number of Google searches across time')
    #end

    #%% WORDCLOUD OF RELATED QUERIES
    if len(trends)>0 and Param['showfig']:
        if Param['verbose']: print('[GOOGLE TRENDS] Making word-cloud.')
        getkeys=list(related_queries.keys())
        gettext=[]
        for i in range(0, len(getkeys)):
            if not 'NoneType' in str(type(related_queries[getkeys[i]]['top'])):
                tmptext = related_queries[getkeys[i]]['top']['query']+' '
                tmptext = related_queries[getkeys[i]]['top']['value']*tmptext
                gettext = np.append(gettext, tmptext.str.cat())
        #end
        if len(gettext)>0:
            gettext = str(gettext[0])
    
            from wordcloud import WordCloud
            wordcloud = WordCloud(background_color='white', margin=10, max_font_size=40, width=600, height=300).generate(gettext)
            plt.subplots(figsize=(Param['width'],Param['height']))
            plt.imshow(wordcloud, interpolation="bilinear")
        #end
    #end
    
    #%% SHOW ON MAP
    if Param['showfig'] and trends_GEO_CITY.empty==False:
        if Param['verbose']: print('[GOOGLE TRENDS] Superimposing geographical results on worldmap.')
        import worldmap 
        from sklearn.preprocessing import normalize
        
        # Worldmap
        if Param['geo']=='':
            loadmap='world'
        else:
            loadmap=worldmap.code2city(Param['geo'])
        #end
    
        # scale scores between [0-1]
        getscores=normalize(trends_GEO_CITY,axis=0).sum(axis=1)
#        getscores=scale(trends_GEO_CITY, with_std=True, axis=0).sum(axis=1)
#        getscores=minmax_scale(trends_GEO_CITY, axis=0).sum(axis=1)
        # Take only names with score>0
        idx       = np.where(getscores>0)[0]
        citynames = trends_GEO_COUNTRY.iloc[idx].index.values
        cityscore = getscores[idx]
        cmap      = Param['cmap'] 

        # If no data, set all on black
        if len(citynames)==0:
            citynames = trends_GEO_COUNTRY.index.values
            cityscore = 1
            cmap      = ['#000000']
        #end
        
        # Plot on map
        worldmap.makemap(citynames, opacity=cityscore, cmap=cmap, loadmap=loadmap);
        
    #%% Interpolate the frequency
#    if Param['interpolate']:
#        trends['freq'] = trends['freq'].interpolate()
#    #end
    
    #%% OUTPUT
    out['trends']          = trends
    out['related_queries'] = related_queries
    out['CITY']            = trends_GEO_CITY
    out['COUNTRY']         = trends_GEO_COUNTRY
    out['DMA']             = trends_GEO_DMA
    
    #%% END
    return(out)