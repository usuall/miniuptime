<?php

require_once(dirname(__FILE__).'/lib/config.php');
$base_dir = dirname(__FILE__);



$url_no = $_GET['url_no'];
$mysql = $pdo->query("SELECT * from tb_url where url_no = '{$url_no}'");
$result = $mysql->fetch(PDO::FETCH_ASSOC);

// $smarty->debugging = true;

$smarty->assign('result', $result);
$smarty->display('img_diff.html');


?>