<?php
/*
Maak een IFTTT applet:
Koppel 'Android Notification' aan 'Webhook':
If Notification received, then Make a web request

url: https://domein.com/notifications/
Method: post
Content type: application/x-www-form-urlencoded
body: NotificationMessage= {{NotificationMessage}}&NotificationTitle= {{NotificationTitle}}&AppName= {{AppName}}&ReceivedAt= {{ReceivedAt}}

*/
if (isset($_REQUEST["NotificationMessage"])) {
	if (trim($_REQUEST["NotificationMessage"]) != "" && trim($_REQUEST["AppName"]) == "WhatsApp") {
		$notifications = json_decode(file_get_contents('/geheimeplek/notifications.json'), true);
		
		$time=time();
		$notifications[$time]["NotificationTitle"] = trim($_REQUEST["NotificationTitle"]);
		$notifications[$time]["NotificationMessage"] = trim($_REQUEST["NotificationMessage"]);
		$notifications[$time]["AppName"] = trim($_REQUEST["AppName"]);
		$notifications[$time]["ReceivedAt"] = trim($_REQUEST["ReceivedAt"]);
		
		if(file_put_contents('/geheimeplek/notifications.json', json_encode($notifications, JSON_PRETTY_PRINT))) {
			echo 'ok';
		} else {
			echo 'error';
		}
	}
}
?>