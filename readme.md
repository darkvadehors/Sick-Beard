![preview thumb](http://i.imgur.com/OeXSAkU.png)

SickBeard VO/VF avec interface Française par Darkvadehors:
=====

Cette version est basée sur le travail de Midgetspy , mr-oranges et sarakha63 :

Elle comprend :

Langue audio français et en anglais

Changement de l'interfaces:

![preview thumb](http://i.imgur.com/C6TPDCT.png)
![preview thumb](http://i.imgur.com/2nFcEbZ.png)
![preview thumb](http://i.imgur.com/YvAepaA.png)

Recherche Nzb ajouté : binnews (with nzbindex, binsearch and nzbclub)

Recherche Torrent ajouté: t411, cpasbien, piratebay, gks, kat

![preview thumb](http://i.imgur.com/swc1lvx.png)

Gestion des Torrents avec transmission, utorrent deluge gestion, download station

![preview thumb](http://i.imgur.com/K2DoPND.png)

l'intégration subliminale

![preview thumb](http://i.imgur.com/plSD7lP.png)
![preview thumb](http://i.imgur.com/P2yTfpx.png)

le nettoyage des sous-titres

![preview thumb](http://i.imgur.com/5kG6d10.png)

torrent/nzb choix préféré

![preview thumb](http://i.imgur.com/1s7n4Lu.png)

Gestion torrent avec possibilité de partage

![preview thumb](http://i.imgur.com/NDKNgLT.png)

Système de notification multiple et importation de trakt liste

![preview thumb](http://i.imgur.com/xq3G3UI.png)
![preview thumb](http://i.imgur.com/MMtLuzm.png)
![preview thumb](http://i.imgur.com/N24lVgk.png)
![preview thumb](http://i.imgur.com/zEWzsJJ.png)
![preview thumb](http://i.imgur.com/u6GGX5P.png)
![preview thumb](http://i.imgur.com/uz5Ru1a.png)

Barre de progression multicouleur avec info-bulle

![preview thumb](http://i.imgur.com/IfrAr7b.jpg)

fuseau horaire local pour prochains épisodes

![preview thumb](http://i.imgur.com/gbQepiV.jpg)

ignorer  certain mots :

![preview thumb](http://i.imgur.com/bnkTqbY.png)

Recherhce par nom personnalisé et plus

![preview thumb](http://i.imgur.com/tSAvGcJ.png)
![preview thumb](http://i.imgur.com/5X3Vm5Y.png)
![preview thumb](http://i.imgur.com/axshXXM.png)
![preview thumb](http://i.imgur.com/ukrXA4C.png)
![preview thumb](http://i.imgur.com/ZTOCiRi.png)

et beaucoup plus tel que:

auto next available release download when failed
and much more

*Sick Beard is currently an alpha release. There may be severe bugs in it and at any given time it may not work at all.*

Sick Beard is a PVR for newsgroup users (with limited torrent support). It watches for new episodes of your favorite shows and when they are posted it downloads them, sorts and renames them, and optionally generates metadata for them. It currently supports NZBs.org, NZBMatrix, Bin-Req, NZBs'R'Us, EZTV.it, and any Newznab installation and retrieves show information from theTVDB.com and TVRage.com.

Features include:

* automatically retrieves new episode torrent or nzb files
* can scan your existing library and then download any old seasons or episodes you're missing
* can watch for better versions and upgrade your existing episodes (to from TV DVD/BluRay for example)
* XBMC library updates, poster/fanart downloads, and NFO/TBN generation
* configurable episode renaming
* sends NZBs directly to SABnzbd, prioritizes and categorizes them properly
* available for any platform, uses simple HTTP interface
* can notify XBMC, Growl, or Twitter when new episodes are downloaded
* specials and double episode support


Sick Beard makes use of the following projects:

* [cherrypy][cherrypy]
* [Cheetah][cheetah]
* [simplejson][simplejson]
* [tvdb_api][tvdb_api]
* [ConfigObj][configobj]
* [SABnzbd+][sabnzbd]
* [jQuery][jquery]
* [Python GNTP][pythongntp]
* [SocksiPy][socks]
* [python-dateutil][dateutil]
* [jsonrpclib][jsonrpclib]

## Dependencies

To run Sick Beard from source you will need Python 2.7 and Cheetah 2.1.0+. The [binary releases][googledownloads] are standalone.

## Bugs

If you find a bug please report it or it'll never get fixed. Verify that it hasn't [already been submitted][googleissues] and then [log a new bug][googlenewissue]. Be sure to provide as much information as possible.

[cherrypy]: http://www.cherrypy.org
[cheetah]: http://www.cheetahtemplate.org/
[simplejson]: http://code.google.com/p/simplejson/ 
[tvdb_api]: http://github.com/dbr/tvdb_api
[configobj]: http://www.voidspace.org.uk/python/configobj.html
[sabnzbd]: http://www.sabnzbd.org/
[jquery]: http://jquery.com
[pythongntp]: http://github.com/kfdm/gntp
[socks]: http://code.google.com/p/socksipy-branch/
[dateutil]: http://labix.org/python-dateutil
[googledownloads]: http://code.google.com/p/sickbeard/downloads/list
[googleissues]: http://code.google.com/p/sickbeard/issues/list
[googlenewissue]: http://code.google.com/p/sickbeard/issues/entry
[jsonrpclib]: https://github.com/joshmarshall/jsonrpclib
