# Goedemorgen
Een goedemorgen bericht om de dag te starten. De wordt opgebouwd uit een config en een aantal beschikbare `modules`.

## Features
- Agenda evenementen van vandaag via CalDav of Google Calendar
- Weer voorspelling van gewenste tijdstippen (bijv. huis > werk) incl. advies
- Markdown todo/weekplanning. [Uitleg staat onder de code](modules/MarkdownTodo.py)
- Nieuwe album releases via [muspy](https://muspy.com/)
- Plastic/papier/.. afval bij de weg
- 'Server monitoring' > heeft een server al x uur niks van zich laten weten
- Melding wanneer er een aantal uren of dagen geen contact is geweest met ..
- Waarschuwing bij ontkoppelde last.fm scrobbler
- Herinnering aan een random last.fm artiest als muziek tip
- Via config file instelbaar
- Bericht wordt via de mail of pushbullet afgeleverd
- Nieuwe bestanden in syncthing folder
- Nieuwe podcasts beschikbaar in subsonic

## Todo
- [ ] Weer en agenda combineren

## Ideeen
- [ ] Top artiest last.fm gisteren
- [ ] Nieuwe TV afleveringen vandaag / trakt of sonarr
- [ ] Nieuwe afleveringen van podcast, of elke RSS-feed is dan mogelijk
- [ ] ANWB API, file informatie

## Dependencies
python3.6

```bash
pip3 install caldav
pip3 install pytz
pip3 install pushbullet.py
pip3 install feedparser
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip3 install syncthing
```