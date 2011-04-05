#!/usr/bin/python

"""
    VODie
    kitesurfing@kitesurfing.ie
"""

import re
import sys
from BeautifulSoup import SoupStrainer, MinimalSoup as BeautifulSoup, BeautifulStoneSoup
import urllib, urllib2
from TVSeriesUtil import Util
import MenuConstants
from datetime import date

# Url Constants
TV3_URL      = 'http://www.tv3.ie/'
#MAINURL      = TV3_URL + 'includes/ajax/video_all_shows.php'
MAINURL      = TV3_URL + 'index.php'

#EPISODE_URL  = TV3_URL + 'videos.php?locID=%s'
EPISODE_URL  = TV3_URL + 'shows.php?request=%s'

# Channel Constants
CHANNEL = 'TV3'
TV3LOGO = 'http://www.tv3.ie/graphics/global/image_logo_tv3_new.png'

class TV3:

    def getChannelDetail(self):
        return {'Channel'  : CHANNEL,
                'Thumb'    : TV3LOGO,
                'Title'    : 'TV3',
                'mode'     : MenuConstants.MODE_MAINMENU,
                'Plot'     : 'TV3'
                }

    def getStringFor(self, parent, tagName, attrName = None, default = 'None'):
        if parent.find(tagName):
            if attrName is None:
                return str(parent.find(tagName).string.strip())
            else:
                return str(parent.find(tagName)[attrName])
        else:
            print "Error: Cannot find tagName: %s in %s"%(tagName, entry)
            return default

    def getVideoDetails(self, url):
        # Load and read the URL
        f    = urllib2.urlopen(url)
        soup = BeautifulStoneSoup(f)
        f.close()
        
        # Grab the data we need
        metabase = self.getStringFor(soup, 'meta', 'base')
        videosrc = self.getStringFor(soup, 'video', 'src').replace('&amp;','&')

        yield {'Channel'     : CHANNEL,
               'Title'       : CHANNEL,
               'Director'    : CHANNEL,
               'Genre'       : CHANNEL,
               'Plot'        : CHANNEL,
               'PlotOutline' : CHANNEL,
               'id'          : url,
               'url'         : '%s playpath=%s' % (metabase, videosrc)
               }

    def getMainMenu(self):

        # Load and read the URL
        f    = urllib2.urlopen(MAINURL)
        text = f.read()
        f.close()

        BACKGRDREGEXP = '<div id="content" style="background-image: url(.*?)">'
        for mymatch in re.findall(BACKGRDREGEXP, text):
            print mymatch

        REGEXP = '<a class="whiteLink" href="videos.php\?openshows=1\&locID=(.*?)">(.*?)<\/a>'
        REGEXP = '<a href="(.*?)" class="dropDown" title="(.*?)">(.*?)</a>'    
        for mymatch in re.findall(REGEXP, text):
            title = str(mymatch[1])
                        
            #details = Util().getSeriesDetailsByName(title)
            #if details is None:
            #    pic = TV3LOGO
            #elif 'Poster' in details.keys():
            #    pic = details['Poster']
            #elif 'Season' in details.keys():
            #    pic = details['Season']
            #else:
            #    pic = TV3LOGO
            pic = TV3LOGO

            yield {'Channel' : CHANNEL,
                   'Thumb'   : pic,
                   'url'     : mymatch[0],
                   'Title'   : title,
                   'mode'    : MenuConstants.MODE_GETEPISODES}
            
    def getEpisodes(self, showID):
        # Load and read the URL
        f = urllib2.urlopen(EPISODE_URL % (showID))
        text = f.read()
        f.close()
        
        TITLEREGEXP = '<title>(.*?) - TV3</title>'
        for mymatch in re.findall(TITLEREGEXP, text, re.MULTILINE):
            the_title = mymatch.strip()
        
        REGEXP = '^<a class="whiteLink" href="(videos.php\?video=.*?&date=(\d\d\d\d-\d\d-\d\d)&date_mode=&page=1&show_cal=\d*&newspanel=&showspanel=&web_only=&full_episodes=)">\s+<img src=(.*?) height="84" alt="(.*?)" title="(.*?)"'
        REGEXP = '<div id="panel_video_menu_entry"onclick="window.open\(\'(.*?)\',\'_self\'\)" onMouseOver="style.cursor=\'pointer\'">\s+<p class="video_menu_entry"><img class="float_left" src="(.*?)" width="116" height="64" alt="" border="0">\s+<strong>(.*?)</strong>\s+<br />(.*?)</p>'
        for mymatch in re.findall(REGEXP, text, re.MULTILINE):
            print mymatch[0]
            # Default values
            description = 'None'
            link        = 'None'

            # ListItem properties
            img   = mymatch[1]
            datestr  = mymatch[2]
            description = mymatch[3].strip()
            
            # Look for the higher resolution image 
            img = img.replace('thumbnail.jpg','preview_vp.jpg')
            
            # Format the date
            date_array = datestr.split()
            if len(date_array) == 4:
                month = date_array[2][:-1].lower()
                if month.find('jan') > -1:
                    month = 1
                elif month.find('feb') > -1:
                    month = 2
                elif month.find('mar') > -1:
                    month = 3
                elif month.find('apr') > -1:
                    month = 4
                elif month.find('may') > -1:
                    month = 5
                elif month.find('jun') > -1:
                    month = 6
                elif month.find('jul') > -1:
                    month = 7
                elif month.find('aug') > -1:
                    month = 8
                elif month.find('sep') > -1:
                    month = 9
                elif month.find('oct') > -1:
                    month = 10
                elif month.find('nov') > -1:
                    month = 11
                elif month.find('dec') > -1:
                    month = 12
                else:
                    month = 0
                
                if month > 0:
                    datestr = "%02d-%02d-%s" % ( int(date_array[1].replace('th','').replace('st','').replace('nd','')), month, '2011')
                    title = the_title
                else:
                    title = the_title + ' - ' + datestr
                    datestr = date.today().strftime("%d-%m-%Y")
                    
            else:
                title = the_title + ' - ' + datestr
                datestr = date.today().strftime("%d-%m-%Y")
                
            year = 2011

            # Load the URL for this episode
            f2    = urllib2.urlopen(TV3_URL + mymatch[0])
            text2 = f2.read()

            # Get link for the mp4
            mp4re = 'url: \"(.*?mp4)\"'
            for mymatch2 in re.findall(mp4re, text2, re.MULTILINE):
                link = mymatch2
            
            yield {'Channel'      : CHANNEL,
                    'Thumb'       : img,
                    'Fanart_Image': img,
                    'url'         : link,
                    'Title'       : title,
                    'mode'        : MenuConstants.MODE_PLAYVIDEO,
                    'Plot'        : description,
                    'plotoutline' : title,
                    'Date'        : datestr,
                    'Year'        : year,
                    'Studio'      : CHANNEL
                    }

    def convertHTML(self, text):
        if not text == '':
            return BeautifulStoneSoup(text, 
                       convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0].encode( "utf-8" )
        else:
            return 'None'

if __name__ == '__main__':

    items = TV3().getMainMenu()
    
    for item in items:
        print item
        episodes = TV3().getEpisodes(item['url'])
        for episode in episodes:
            print episode
            print TV3().getVideoDetails(episode['url'])