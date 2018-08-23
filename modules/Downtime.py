from modules import Module
import urllib, json, time

class Downtime(Module):
	def __init__(self, config):
		self.hasText = False
		self.text = "";

		# Op deze URL verwacht het script een JSON file met minimaal: { "server": { "ping": timestamp } }
		response = urllib.urlopen(config["url"]);
		ping = json.loads(response.read());

		# Pak de laatste ping
		lastPing = ping[config["server"]]["ping"]

		# Vergelijk deze met de timestamp van nu
		now = round(time.time())
		diff = now - lastPing;
		diffHour = (diff / 60 / 60)

		# Is dit langer dan [uur] geleden, signaleren
		if (diffHour >= int(config["uur"])):
			self.hasText = True
			self.text = "De backup raspberry pi is al " + str(round(diffHour, 2)) + " uur offline."


	def HasText(self):
		return super(Downtime, self).HasText()

	def GetText(self):
		return super(Downtime, self).GetText()


"""
##### De server
ping.sh - Op de server/raspberry pi in de cronjob zetten:

# apparaat.txt in de homedirectory maken met hierin de naam van het apparaat

# IP opslaan in een txt file
/sbin/ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' > /home/niek/ip.txt

# Uptime opslaan in een txt
echo "Uptime: " >/home/niek/extra.txt
/usr/bin/uptime | grep -ohe 'up .*' | sed 's/,//g' | awk '{ print $2" "$3 }' >> /home/niek/extra.txt

# Beschikbare schijfruimte naar txt
echo "Free diskspace: " >> /home/niek/extra.txt
/bin/df -h | tr -s ' ' $'\t' | grep /dev/root | cut -f4 >> /home/niek/extra.txt

# Ping versturen naar de server
curl -d "apparaat=$(cat /home/niek/apparaat.txt)&extra=$(cat /home/niek/extra.txt)&ip=$(cat /home/niek/ip.txt)" -X POST https://.... php file

-------------------------------------------------------
##### De PHP file
<?php
header('Content-Type: application/json');
if (isset($_REQUEST["apparaat"])) {
	
	$ping = json_decode(file_get_contents('ping.json'), true);
	$apparaat = strtolower($_REQUEST["apparaat"]);
	$ping[$apparaat]["ip"] = $_REQUEST["ip"];

	if (isset($_REQUEST["extra"]))
		$ping[$apparaat]["extra"] = $_REQUEST["extra"];
	
	$ping[$apparaat]["ping"] = time();
	
	if(file_put_contents('ping.json', json_encode($ping, JSON_PRETTY_PRINT))) {
		echo '{ "ret": "pong" }';
	} else {
		echo '{ "ret": "error" }';
	}
}
?>
"""
