<?php

require_once(dirname(__FILE__).'/lib/config.php');
$base_dir = dirname(__FILE__);

$mon_no = $_GET['mon_no'];

// $url_no = $_GET['url_no'];
// $mysql = $pdo->query("SELECT * from tb_url where url_no = '{$url_no}'");
// $result = $mysql->fetch(PDO::FETCH_ASSOC);
// $smarty->assign('result', $result);
// // $smarty->debugging = true;


$mysql = $pdo->query("SELECT * from tb_monitor where mon_no = '{$mon_no}'");
$monitor = $mysql->fetch(PDO::FETCH_ASSOC);
// print_r($monitor);
$smarty->assign('monitor', $monitor);

$arr_url = getUrlinfo($monitor['url_no']);
$smarty->assign('arr_url', $arr_url);

$smarty->display('img_diff.html');


?>