<?php

require_once(dirname(__FILE__).'/lib/config.php');
$base_dir = dirname(__FILE__);




$smarty->assign('name', 'Ned');
$smarty->display('test1.html');


?>