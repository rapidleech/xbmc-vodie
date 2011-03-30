#!/usr/bin/python

"""
    VODie
    kitesurfing@kitesurfing.ie
"""

import re
import sys
from BeautifulSoup import SoupStrainer, MinimalSoup as BeautifulSoup, BeautifulStoneSoup
import urllib, urllib2
import MenuConstants

# Url Constants
TV3_URL      = 'http://www.tv3.ie/'
MAINURL      = TV3_URL + 'includes/ajax/video_all_shows.php'
EPISODE_URL  = TV3_URL + 'videos.php?locID=%s'

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
               'Title'       : 'TV3',
               'Director'    : 'TV3',
               'Genre'       : 'TV3',
               'Plot'        : 'TV3',
               'PlotOutline' : 'TV3',
               'id'          : '1093567',
               'url'         : '%s playpath=%s' % (metabase, videosrc)
               }

    def getMainMenu(self):

        # Load and read the URL
        f    = urllib2.urlopen(MAINURL)
        text = f.read()
        f.close()

        REGEXP = '<a class="whiteLink" href="videos.php\?openshows=1\&locID=(.*?)">(.*?)<\/a>'    
        for mymatch in re.findall(REGEXP, text):
            yield {'Channel' : CHANNEL,
                   'Thumb'   : TV3LOGO,
                   'url'     : mymatch[0],
                   'Title'   : urllib.unquote( urllib.quote( mymatch[1] ).replace( '%92' , "'" ) ),
                   'mode'    : MenuConstants.MODE_GETEPISODES}
            
    def getEpisodes(self, showID):
        # Load and read the URL
        f = urllib2.urlopen(EPISODE_URL % (showID))
        text = f.read()
        f.close()
        
        REGEXP = '^<a class="whiteLink" href="(videos.php\?video=.*?&date=(\d\d\d\d-\d\d-\d\d)&date_mode=&page=1&show_cal=\d*&newspanel=&showspanel=&web_only=&full_episodes=)">\s+<img src=(.*?) height="84" alt="(.*?)" title="(.*?)"'
        for mymatch in re.findall(REGEXP, text, re.MULTILINE):
            # Default values
            description = 'None'
            link        = 'None'

            # ListItem properties
            img   = mymatch[2]
            title = mymatch[3]
            date  = mymatch[1]
            
            # Look for the higher resolution image 
            img = img.replace('thumbnail.jpg','preview_vp.jpg')
            
            # Format the date
            date = "%s-%s-%s" % ( date[ 8 : 10], date[ 5 : 7 ], date[ : 4 ])
            year = int("%s"%(date[6:10]))

            # Load the URL for this episode
            f2    = urllib2.urlopen(TV3_URL + mymatch[0])
            text2 = f2.read()
                        
            # Get description
            descre = '<\/strong><br \/><br \/>\s+(.*)'
            for mymatch2 in re.findall(descre, text2, re.MULTILINE):
                description = mymatch2.strip()

            # Get link for the mp4
            mp4re = 'url: \"(.*?mp4)\"'
            for mymatch2 in re.findall(mp4re, text2, re.MULTILINE):
                link = mymatch2
            
            yield {'Channel'      : CHANNEL,
                    'Thumb'       : img,
                    'url'         : link,
                    'Title'       : title,
                    'mode'        : MenuConstants.MODE_PLAYVIDEO,
                    'Plot'        : description,
                    'plotoutline' : title,
                    'Date'        : date,
                    'Year'        : year,
                    'Studio'      : CHANNEL
                    }

if __name__ == '__main__':

    items = TV3().getMainMenu()
    
    for item in items:
        print item
        episodes = TV3().getEpisodes(item['url'])
        for episode in episodes:
            print episode
            print TV3().getVideoDetails(episode['url'])
