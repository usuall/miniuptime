<?php

require_once(dirname(__FILE__).'/lib/config.php');

//변수 할당
$smarty->assign('name','usuall');

$smarty->assign('firstname', 'Doug');
$smarty->assign('lastname', 'Evans');
$smarty->assign('meetingPlace', 'New York');


$smarty->assign('Contacts',
    array('fax' => '555-222-9876',
          'email' => 'zaphod@slartibartfast.example.com',
          'phone' => array('home' => '555-444-3333',
                           'cell' => '555-111-1234')
                           )
         );
         
//디버그 모드
//$smarty->debugging = true;

//template파일 설정
$smarty->display('test4.html');


?>