<?php
if (isset($_REQUEST["KEY"])) {
	if ($_REQUEST["KEY"] == "") {

		if (isset($_REQUEST["CLEAR"])) {
			file_put_contents('/geheimeplek/notifications.json', "{}");
			echo "ok";
		} else {
			header('Content-Type: application/json');
			echo file_get_contents('/geheimeplek/notifications.json');
		}

	}
	else {
		header('Content-Type: application/json');
		echo "{}";
	}
}
?>