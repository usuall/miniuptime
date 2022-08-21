<?php

require_once(dirname(__FILE__).'/lib/config.php');
$smarty->assign('name','Ned');

//** 次の行のコメントをはずすと、デバッギングコンソールを表示します
//$smarty->debugging = true;

$smarty->display('test2.html');


?>