# Goedemorgen
Een goedemorgen bericht om de dag te starten. De wordt opgebouwd uit een config en een aantal beschikbare `modules`.

## Features
- Agenda evenementen van vandaag via CalDav
- Weer voorspelling van gewenste tijdstippen (bijv. huis > werk)
- Markdown todo/weekplanning. [Uitleg staat onder de code](modules/MarkdownTodo.py)
- Nieuwe album releases via [muspy](https://muspy.com/)
- Plastic/papier/.. afval bij de weg
- 'Server monitoring' > heeft een server al x uur niks van zich laten weten
- Waarschuwing bij ontkoppelde last.fm scrobbler
- Via config file instelbaar
- Bericht wordt via de mail of pushbullet afgeleverd

## Todo
- [x] Regen bij weerinformatie
- [ ] Praktische info als, jas aan, korte broek aan, met de auto/fiets/brommer
- [ ] Weer en agenda combineren
- [x] Notities / todo file vandaag, algemeen en gemist afgelopen dagen
- [ ] Downtime uitbereiden met meerdere servers (laatste succesvolle backup ping ipv de uptime) 

## Ideeen
- [ ] Top artiest last.fm gisteren
- [ ] Nieuwe TV afleveringen vandaag / trakt of sonarr
- [x] Nieuwe muziek releases op basis van spotify API of [muspy](https://muspy.com/) feed.
- [ ] Nieuwe afleveringen van podcast, of elke RSS-feed is dan mogelijk
- [ ] ANWB API, file informatie

## Dependencies
python3.6

```bash
pip3 install caldav
pip3 install pytz
pip3 install pushbullet.py
pip3 install feedparser
```