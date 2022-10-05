<?php
require_once(dirname(__FILE__).'/lib/config.php');

//상단 메뉴
include_once('menu.php');

$url_no = $_POST['url_no'];
$grp_no = $_POST['grp_no'];
$url_title = $_POST['url_title'];
$url_addr = $_POST['url_addr'];
$url_fg = $_POST['url_fg'];

// var_dump($_POST);
// echo ">>>>>>>".
$option_javascript_disabled = $_POST['javascript_disabled'];
$option_browser_bg_execute = $_POST['browser_bg_execute'];
$option_delay_seconds = $_POST['delay_seconds'];


if($url_fg == 'on'){
    $url_fg = 1;
} else {
    $url_fg = 0;
}

if($option_javascript_disabled == 'on'){
    $option_javascript_disabled = 1;
} else {
    $option_javascript_disabled = 0;
}

if($option_browser_bg_execute == 'on'){
    $option_browser_bg_execute = 1;
} else {
    $option_browser_bg_execute = 0;
}


if($url_no == ''){
    $mysql = $pdo->prepare('INSERT INTO `tb_url` (grp_no, url_title, url_addr, url_fg, option_javascript_disabled, option_browser_bg_execute, option_delay_seconds ) VALUES ( ?, ?, ?, ?, ?, ?, ?) ');

    $mysql->bindValue(1, $grp_no);
    $mysql->bindValue(2, $url_title);
    $mysql->bindValue(3, $url_addr);
    $mysql->bindValue(4, $url_fg);
    $mysql->bindValue(5, $option_javascript_disabled);
    $mysql->bindValue(6, $option_browser_bg_execute);
    $mysql->bindValue(7, $option_delay_seconds);
    
    $mysql->execute();
    
    // echo $mysql->queryString; # 실행SQL 확인
    // echo ">>>> ".$pdo->lastInsertId(); # 최신 등록ID

    // 신규 입력이 정상적으로 되었을때 사용하는 구문
    $count = $mysql->rowCount();
    if($count>0){
        alert('등록 완료', '/url_config.php?url_no='.$pdo->lastInsertId());
    }else{
        alert('등록 실패');
    }

    
} else {
    $mysql = $pdo->prepare('UPDATE `tb_url` /* url_config 수정 */ SET grp_no = ?, url_title = ?, url_addr = ?, url_fg = ?, option_javascript_disabled = ?, option_browser_bg_execute = ?, option_delay_seconds =? where url_no = ? ');

    echo ">>>>>".$grp_no;
    $mysql->bindValue(1, $grp_no);
    $mysql->bindValue(2, $url_title);
    $mysql->bindValue(3, $url_addr);
    $mysql->bindValue(4, $url_fg);
    $mysql->bindValue(5, $option_javascript_disabled);
    $mysql->bindValue(6, $option_browser_bg_execute);
    $mysql->bindValue(7, $option_delay_seconds);
    $mysql->bindValue(8, $url_no);
    $mysql->execute();

    //echo $mysql->queryString;

    // 신규 입력이 정상적으로 되었을때 사용하는 구문
    // $count = $mysql->rowCount();
    // if($count>0){
    //     echo "성공";
    // }else{
    //     echo "실패";
    // }

    // sleep(3);
    alert('수정완료');
}

//DB 접속종료
$pdo = null;
?>