This XBMC plugin enables (Ireland only):
  * the playing of TV catchup content from the RTE Player, TV3 website and TG4 website
  * Watching Live RTE TV feeds
  * Watching Magnet WebTV (http://www.magnetwebtv.ie)
  * Watching An Lár TV (http://www.anlar.tv/)

It needs the latest versions of XBMC.



# Wanted! #
  * If anybody interested in contributing a logo for VODie please dont hesitate to contribute.

# Plugin Demo #

[Screenshots](Screenshots.md)

## Video ##
<a href='http://www.youtube.com/watch?feature=player_embedded&v=Rh0MrnUK78M' target='_blank'><img src='http://img.youtube.com/vi/Rh0MrnUK78M/0.jpg' width='425' height=344 /></a>

# Plugin Uninstallation #

## For Linux/OSX/Windows/AppleTV XBMC (xbmc.org) ##
  * Remove the folder plugin.video.vodie from
    * On linux
      * $HOME/.xbmc/addons/
      * $HOME/.xbmc/userdata/addon\_data
    * On Mac
      * $HOME/Library/Application Support/XBMC/addons
      * $HOME/Library/Application Support/XBMC/userdata/addon\_data
    * On Apple TV1
      * /mnt/Scratch/Users/frontrow/Library/Application Support/XBMC/addons
      * /mnt/Scratch/Users/frontrow/Library/Application Support/XBMC/userdata/addon\_data
    * On Apple TV2 should be the same as Apple TV1 need to check
    * On Windows ???

# Plugin Installation #

  * Download the [plugin.video.vodie\_1.1.3.zip](http://code.google.com/p/xbmc-vodie/downloads/detail?name=plugin.video.vodie-1.1.3.zip&can=2&q=)

## For XBMC4XBOX ##
  * Follow the [XBMC4XBOX plugin installation instructions](http://www.xbmc4xbox.org/wiki/index.php?title=HOW-TO_install_and_use_plugins_in_XBMC)

## For Linux/OSX/Windows/AppleTV XBMC (xbmc.org) ##
  * If already installed with previous version, Uninstall plugin following the steps in [#Plugin\_Uninstallation](#Plugin_Uninstallation.md)
  * Unpack the zip and copy the plugin.video.vodie folder to your XBMC addons folder.
    * On linux it is found in $HOME/.xbmc/addons/
    * On Mac it is found in $HOME/Library/Application Support/XBMC/addons
    * On Apple TV1 it is found in /mnt/Scratch/Users/frontrow/Library/Application Support/XBMC/addons
    * On Apple TV2 should be the same as Apple TV1 need to check
    * On Windows ???

# Configuring Magnet WebTV #
  * In the VODie Add-on settings
  * In the Magnet Web TV section, enter your Username and Password
  * Launching or Relaunching VODie should enable the Magnet WebTV menu

# Plugin Issues #
If you are having a problem with the plugin or just have a query please do read the documentation and do a search on the XBMC plugin forum thread before posting.

If you believe you have found a bug or would like to request a feature then create a new issue.

Please make sure you post a Debug Log with your report

# Plugin Limitations #
  * This plugin doesn't work outside of the Republic of Ireland. The RTE, TV3 and TG4 Player website ensures that only Irish IP addresses can access content.
  * This plugin requires an up to date version of XBMC with libRTMP support to work. For the XBOX (XBMC4XBOX) you need at least [revision 30413](https://code.google.com/p/xbmc-vodie/source/detail?r=30413) or later. For Linux/Windows/OSX you will need the Dharma release (or newer).