##### Sipelste versie:
curl -d "apparaat=Titel" -X POST https://example.com/ping.php

##### Wat uitgebreider:

# apparaat.txt de apparaatnaam handmatig maken
# IP opslaan in een txt file.
/sbin/ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' > ~/ip.txt

# Uptime opslaan in een txt
/usr/bin/uptime | grep -ohe 'up .*' | sed 's/,//g' | awk '{ print $2" "$3 }' > ~/extra.txt 

# Ping versturen naar de server
curl -d "apparaat=$(cat ~/apparaat.txt)&extra=$(cat ~/extra.txt)&ip=$(cat ~/ip.txt)" -X POST https://example.com/ping.php