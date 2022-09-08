<?php
require_once(dirname(__FILE__).'/lib/config.php');

//상단 메뉴
include_once('menu.php');

$url_no = $_POST['url_no'];
$grp_no = $_POST['grp_no'];

if(trim($url_no) == '' && trim($grp_no) == ''){    
    alert('잘못된 실행입니다.');
} else {
    $mysql = $pdo->prepare('DELETE FROM `tb_url` WHERE url_no = ? ');
    $mysql->bindValue(1, $url_no);
    $mysql->execute();

    alert('삭제 완료', 'dash03.php?grp_no='.$grp_no);
}

//DB 접속종료
$pdo = null;
?>