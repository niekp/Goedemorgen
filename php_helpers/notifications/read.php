<?php
if (isset($_REQUEST["KEY"])) {
	if ($_REQUEST["KEY"] == "") {
		header('Content-Type: application/json');
		echo file_get_contents('/geheimeplek/notifications.json');
	}
	else {
		header('Content-Type: application/json');
		echo "{}";
	}
}
?>