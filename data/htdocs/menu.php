<?php

require_once(dirname(__FILE__).'/lib/config.php');


$query = "SELECT * from tb_group where grp_fg=1 order by grp_title";
$stmt = $pdo->prepare($query);
$stmt->execute();
$menu = $stmt->fetchAll();

$smarty->assign('menu', $menu);




?>