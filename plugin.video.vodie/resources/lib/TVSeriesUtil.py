#!/usr/bin/python

"""
    VODie
    kitesurfing@kitesurfing.ie
"""

import re
import sys
from BeautifulSoup import SoupStrainer, MinimalSoup as BeautifulSoup, BeautifulStoneSoup
import urllib, urllib2, cookielib

GET_SERIES_URL    = 'http://www.thetvdb.com/api/GetSeries.php?seriesname=%s'
SERIE_DETAILS_URL = 'http://cache.thetvdb.com/api/1D62F2F90030C444/series/%s/banners'

BANNER_URL = 'http://cache.thetvdb.com/banners/%s'

KNOWN_SHOWS = {
               "Castle" : {"TVDBName":"Castle (2009)",},
               }

class Util:
    
    def saveSerieDetail(self, serieName, serie):
        if not serieName in KNOWN_SHOWS.keys():
            KNOWN_SHOWS[serieName] = {"TVDBName":serieName}

        KNOWN_SHOWS[serieName]['id'] = str(serie.id.string)
        KNOWN_SHOWS[serieName]['banner'] = str(BANNER_URL % (serie.banner.string))
        
        self.getDetailsForSerieByID(serieName, KNOWN_SHOWS[serieName]['id'])
        
    def getSeriesDetailsByName(self, serieName):
        if serieName in KNOWN_SHOWS.keys():
            url = GET_SERIES_URL % (urllib.quote(KNOWN_SHOWS[serieName]['TVDBName']))
        else:
            url = GET_SERIES_URL % (urllib.quote(serieName))
        
        try:
            # Load and read the URL
            f    = urllib2.urlopen(url)
            soup = BeautifulStoneSoup(f)
            f.close()
            
            if len(soup.findAll('series')) == 1:
                self.saveSerieDetail(serieName, soup.series) 
            else:
                for serie in soup.findAll('series'):
                    if serie.seriesname.string == serieName:
                        self.saveSerieDetail(serieName, serie)
            
            if serieName in KNOWN_SHOWS.keys():
                return KNOWN_SHOWS[serieName]
            return None
        except:
            print 'Error'
            return None
        
    def getDetailsForSerieByID(self, serieName, serieID):
        url = SERIE_DETAILS_URL % (urllib.quote(serieID))

        # Change the User Agent
        USER_AGENT = 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10'
                
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)

        resp = opener.open(req)
        
        soup = BeautifulStoneSoup(resp.read())
        resp.close()
        
        for banner in soup.banners.findAll('banner'):
            if banner.language.string == 'en':
                if not 'Fanart' in KNOWN_SHOWS[serieName].keys() and banner.bannertype.string == 'fanart':
                    KNOWN_SHOWS[serieName]['Fanart'] = str(BANNER_URL % (banner.bannerpath.string))
                    if banner.thumbnailpath:
                        KNOWN_SHOWS[serieName]['FanartThumb'] = str(BANNER_URL % (banner.thumbnailpath.string))
                elif not 'Poster' in KNOWN_SHOWS[serieName].keys() and banner.bannertype.string == 'poster':
                    KNOWN_SHOWS[serieName]['Poster'] = str(BANNER_URL % (banner.bannerpath.string))
                    if banner.thumbnailpath:
                        KNOWN_SHOWS[serieName]['PosterThumb'] = str(BANNER_URL % (banner.thumbnailpath.string))
                elif not 'Season' in KNOWN_SHOWS[serieName].keys() and banner.bannertype.string == 'season':
                    KNOWN_SHOWS[serieName]['Season'] = str(BANNER_URL % (banner.bannerpath.string))
                    if banner.thumbnailpath:
                        KNOWN_SHOWS[serieName]['SeasonThumb'] = str(BANNER_URL % (banner.thumbnailpath.string))
                elif not 'Series' in KNOWN_SHOWS[serieName].keys() and banner.bannertype.string == 'series':
                    KNOWN_SHOWS[serieName]['Series'] = str(BANNER_URL % (banner.bannerpath.string))
                    if banner.thumbnailpath:
                        KNOWN_SHOWS[serieName]['SeriesThumb'] = str(BANNER_URL % (banner.thumbnailpath.string))

if __name__ == '__main__':
    #print KNOWN_SHOWS
    
    print Util().getSeriesDetailsByName('Home and Away')
    #print Util().getSeriesDetailsByName('Castle')
    #print Util().getSeriesDetailsByName('Casualty')
    print Util().getSeriesDetailsByName('Desperate Housewives')
    
    #print KNOWN_SHOWS
