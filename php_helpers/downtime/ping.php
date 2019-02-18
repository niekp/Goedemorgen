<?php
header('Content-Type: application/json');
if (isset($_REQUEST["apparaat"])) {
	$ping = json_decode(file_get_contents('ping.json'), true);
	$apparaat = strtolower($_REQUEST["apparaat"]);
	$ping[$apparaat]["ip"] = $_REQUEST["ip"];
	if (isset($_REQUEST["extra"]))
		$ping[$apparaat]["extra"] = $_REQUEST["extra"];
	$ping[$apparaat]["ping"] = time();
	$ping[$apparaat]["date"] = date('Y-m-d H:i:s');
	
	if(file_put_contents('ping.json', json_encode($ping, JSON_PRETTY_PRINT))) {
		echo '{ "ret": "pong" }';
	} else {
		echo '{ "ret": "error" }';
	}

}
?>