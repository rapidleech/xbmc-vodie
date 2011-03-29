#!/usr/bin/python

"""
    VODie
    kitesurfing@kitesurfing.ie
"""

import re
import sys
from BeautifulSoup import BeautifulStoneSoup
import urllib, urllib2
import MenuConstants

# Player Constants
SWFURL = 'http://www.rte.ie/player/assets/player_439.swf'
PAGEURL = 'http://www.rte.ie/player/'

# URL Constants
PROGRAMME_URL = 'http://dj.rte.ie/vodfeeds/feedgenerator/programme/?id='
SHOW_BY_TYPE_URL = 'http://dj.rte.ie/vodfeeds/feedgenerator/%s/'
FEATURES   = 'features'
LATEST     = 'latestfront'
LASTCHANCE = 'lastchancefront'
GENRELIST  = 'genrelist'
LIVE       = 'live'

# Channel Constants
CHANNEL = 'RTE'
LOGOICON = 'http://www.rte.ie/iptv/images/logo.gif'

# Main Menu Items
LIVEMENU =      {'Thumb'    : LOGOICON,
                 'Channel'  : CHANNEL,
                 'Title'    : 'Live',
                 'url'      : LIVE,
                 'mode'     : MenuConstants.MODE_CREATEMENU ,
                 'Plot'     : 'Watch Live'
                 }
FEATMENU =      {'Thumb'    : LOGOICON,
                 'Channel'  : CHANNEL,
                 'Title'    : 'Features'            ,
                 'url'      : FEATURES      ,
                 'mode'     : MenuConstants.MODE_CREATEMENU ,
                 'Plot'     : 'Features'
                 }
LTSTMENU =      {'Thumb'    : LOGOICON,
                 'Channel'  : CHANNEL,
                 'Title'    : 'Latest',
                 'url'      : LATEST,
                 'mode'     : MenuConstants.MODE_CREATEMENU ,
                 'Plot'     : 'Latest'
                 }
LASTMENU =      {'Thumb'    : LOGOICON,
                 'Channel'  : CHANNEL,
                 'Title'    : 'Last Chance',
                 'url'      : LASTCHANCE,
                 'mode'     : MenuConstants.MODE_CREATEMENU ,
                 'Plot'     : 'Last Chance'
                 }
ATOZMENU =      {'Thumb'    : LOGOICON,
                 'Channel'  : CHANNEL,
                 'Title'    : 'Search by A-Z',
                 'url'      : MenuConstants.MODE_ATOZ,
                 'mode'     : MenuConstants.MODE_CREATEMENU ,
                 'Plot'     : 'Search by A to Z'
                 }
CATYMENU =      {'Thumb'    : LOGOICON,
                 'Channel'  : CHANNEL,
                 'Title'    : 'Search by Category',
                 'url'      : MenuConstants.MODE_CATEGORY ,
                 'mode'     : MenuConstants.MODE_CREATEMENU ,
                 'Plot'     : 'Search by Category'
                 }

class RTE:    

    def getChannelDetail(self):
        return {'Channel': CHANNEL,
                'Thumb':LOGOICON,
                'Title':'RTE',
                'mode':MenuConstants.MODE_MAINMENU,
                'Plot':'RTE'}

    def getStringFor(self, parent, tagName, attrName = None, default = 'None'):
        if parent.find(tagName):
            if attrName is None:
                return str(parent.find(tagName).string).strip()
            else:
                return str(parent.find(tagName)[attrName])
        else:
            print "Error: Cannot find tagName: %s in %s"%(tagName, parent)
            return default
        
    def getVideoDetails(self, url, includeAds = True):
        print url
        page = urllib2.urlopen(url)
        soup = BeautifulStoneSoup(page, selfClosingTags=['link','category','media:player','media:thumbnail','rte:valid', 'rte:duration', 'rte:statistics'])
        
        entry = soup.find('entry')
        
        published  = self.getStringFor(entry, 'published')
        plot       = self.getStringFor(entry, 'content')
        duration   = self.getStringFor(entry, 'rte:duration','formatted')
        rating     = self.getStringFor(entry, 'media:rating')
        copyright  = self.getStringFor(entry, 'media:copyright')
        title      = self.getStringFor(entry, 'title')        
        id         = self.getStringFor(entry, 'id')

        categories = entry.findAll('category')
        categories_str = u''
        for category in categories:
            categories_str = categories_str + u', ' + category['term']
                
        contents = entry.findAll('media:content')
        for content in contents:
            if content['rte:format'] == 'content':
                # Build the RTMP url for XBMC to play the Stream
                RTE_RTMPE_SERVER = str(content['rte:server'])
                RTE_APP = 'rtevod/'
                mp4url = '%s app=%s swfUrl=%s swfVfy=1 playpath=%s'%(RTE_RTMPE_SERVER, RTE_APP, SWFURL, str(content['url'])[len(RTE_RTMPE_SERVER):])
                
                # Grab the Part number to add it to the Title.
                # Streams are split into parts due to ads break
                partre = '\_part(\d)\_'
                partMatches = re.findall(partre, mp4url)
                if len(partMatches) > 0:
                    newtitle = '%s - Part %s' % (title, partMatches[0])
                else:
                    newtitle = title
                
                # Return this show
                yield {'Channel'      : CHANNEL,
                       'TVShowTitle'  : newtitle,
                       'Title'        : newtitle,
                       'MPAA'         : rating,
                       'Director'     : copyright,
                       'Duration'     : duration,
                       'Genre'        : categories_str,
                       'Plot'         : plot,
                       'PlotOutline'  : plot,
                       'id'           : id,
                       'url'          : mp4url,
                       'Date'         : "%s-%s-%s" % ( published[ 8 : 10], published[ 5 : 7 ], published[ : 4 ], )}
            # Direct Links
            elif content['rte:format'] == 'string' and includeAds:
                yield {'Channel'      : CHANNEL,
                       'TVShowTitle'  : content['url'],
                       'Title'        : content['url'],
                       'Plot'         : '',
                       'PlotOutline'  : '',
                       'id'           : id,
                       'url'          : content['url'] }
            # Live Shows
            elif content['rte:format'] == 'live':
                RTE_RTMPE_SERVER = str(content['rte:server'])
                RTE_APP = 'live'
                mp4url = "%s playpath=%s swfUrl=%s swfVfy=1 app=%s pageUrl=%s live=true" % (RTE_RTMPE_SERVER, str(content['url'])[len(RTE_RTMPE_SERVER):], SWFURL, RTE_APP, PAGEURL)
                yield {'Channel'      : CHANNEL,
                       'TVShowTitle'  : content['url'],
                       'Title'        : content['url'],
                       'Plot'         : '',
                       'PlotOutline'  : '',
                       'id'           : id,
                       'url'          : mp4url }
            # FLV Advertisement
            elif content['rte:format'] == 'advertising' and includeAds:
                page = urllib2.urlopen(content['url'])
                soup = BeautifulStoneSoup(page, selfClosingTags=['CustomParameters','ISCI'])

                for bandwidth_value in ['high', 'medium', 'low']:
                    results = soup.findAll('flv', bandwidth=bandwidth_value)
                    for result in results:
                        if result.contents[0].string != ' ':
                            yield {'Channel'     : CHANNEL,
                                   'TVShowTitle' : result.contents[0].string,
                                   'Title'       : result.contents[0].string,
                                   'Plot'        : '',
                                   'PlotOutline' : '',
                                   'id'          : result.contents[0].string,
                                   'url'         : result.contents[0].string }

    def getMainMenu(self):
        return [LIVEMENU,
                FEATMENU,
                LTSTMENU,
                LASTMENU,
                ATOZMENU,
                CATYMENU] 


    def getEpisodes(self, showID):
        page = urllib2.urlopen(PROGRAMME_URL + showID)
        soup = BeautifulStoneSoup(page, selfClosingTags=['link','category','media:player','media:thumbnail'])
        
        items = soup.findAll('entry')
        for item in items:
            link = self.getStringFor(item, 'id')
            title = self.getStringFor(item, 'title')
            published = self.getStringFor(item, 'published')
            desc =  self.getStringFor(item, 'media:description')
            thumb =  self.getStringFor(item, 'media:thumbnail', 'url', LOGOICON)
            duration = str(int(self.getStringFor(item, 'rte:duration','ms'))/1000/60)

            yield {'plotoutline'   : title,
                    'Duration'     : duration,
                    'Studio'       : CHANNEL,
                    'Year'         : int("%s" % (published[ : 4 ])),
                    'Date'         : "%s-%s-%s" % ( published[ 8 : 10], published[ 5 : 7 ], published[ : 4 ]),
                    'Thumb'        : thumb,
                    'Channel'      : CHANNEL,
                    'url'          : link,
                    'Title'        : title,
                    'mode'         : MenuConstants.MODE_PLAYVIDEO,
                    'Plot'         : desc
                    }
            
    def getMenuItems(self, type, params = '', mode = MenuConstants.MODE_GETEPISODES):
        page = urllib2.urlopen(SHOW_BY_TYPE_URL%(type) + params)
        self.soup = BeautifulStoneSoup(page, selfClosingTags=['link','category','media:player','media:thumbnail'])

        items = self.soup.findAll('entry')
        for item in items:
            title = str(item.title.string).strip()
            
            pic = LOGOICON
            if item.find('media:thumbnail'):
                pic = item.find('media:thumbnail')['url']

            if type == LIVE:
                link = str(item.id.string).strip()
                yield {'Title':title,
                       'Channel': CHANNEL,
                       'Thumb':pic,
                       'mode':MenuConstants.MODE_PLAYVIDEO,
                       'url':link
                       }
            else:
                yield {'Title':title,
                       'Channel': CHANNEL,
                       'Thumb':pic,
                       'mode':mode,
                       'url':urllib.quote(title)
                       }
                        
    def SearchByCategory(self, genre = None):
        if genre == None or genre == '' or genre == 'Search by Category':
            categories = []
            for category in self.getMenuItems(type='genrelist', mode=MenuConstants.MODE_CREATEMENU):
                category['url'] = MenuConstants.MODE_CATEGORY
                categories.append(category)
            return categories
            
        else:
            return self.getMenuItems(type='genre', params='?id=%s'%(urllib.quote(genre)))

    def SearchAtoZ(self, letter = None):
        if letter == None or letter == '' or letter == 'Search by A-Z':
            for item in 'ABCDEFGHIJKLMNOPQRSTUVWXZ':
                yield {'Thumb':LOGOICON,
                       'Channel': CHANNEL,
                       'Title':item,
                       'url':MenuConstants.MODE_ATOZ,
                       'mode':MenuConstants.MODE_CREATEMENU,
                       'Plot':item}
        else:
            for item in self.getMenuItems(type='az', params='?id=%s'%(letter)):
                yield item

if __name__ == '__main__':
    # Test Main Menu
    print RTE().getMainMenu()
    
    #for letter in RTEScrapper().RTESearchAtoZ():
    #    print letter
    #    for item in RTEScrapper().RTESearchAtoZ(letter['Title']):
    #        print item

    #for category in RTEScrapper().RTESearchByCategory():
    #    print category
    #    for item in RTEScrapper().RTESearchByCategory(urllib.quote(category['Title'])):
    #        print item

    # Test Types
    for type in [FEATURES, LASTCHANCE, LATEST]:
        items = RTE().getMenuItems(type)
        for item in items:
            episodes = RTE().getEpisodes(urllib.quote(item['Title']))
            for episode in episodes:
                #print episode
                for detail in RTE().getVideoDetails(episode['url']):
                    print detail