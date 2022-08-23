<?php

require_once(dirname(__FILE__).'/lib/config.php');
$base_dir = dirname(__FILE__);



$mon_no = $_GET['mon_no'];
$mysql = $pdo->query("SELECT * from tb_monitor where mon_no = '{$mon_no}'");
$result = $mysql->fetch(PDO::FETCH_ASSOC);

// $smarty->debugging = true;

$smarty->assign('result', $result);
$smarty->display('html_diff.html');


?>