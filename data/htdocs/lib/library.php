<?php

$g5['title'] = 'notice';

function checkPriod($minute){
    //점검시간
    if($minute > 60 ){
        $time1 = (int)($minute / 60);
        $time2 = $minute % 60;
        $diff_time = $time1 .'h ' . $time2 .'m';
    } else {
        $diff_time = $minute.'m'; 
    }

    return $diff_time;
}

function alert($msg='', $url='', $error=true, $post=false){

    //run_event('alert', $msg, $url, $error, $post);

    $msg = $msg ? strip_tags($msg, '<br>') : '올바른 방법으로 이용해 주십시오.';

    $header = '';
    if (isset($g5['title'])) {
        $header = $g5['title'];
    }
    include_once('alert.php');
    exit;
}


// 경고메세지 출력후 창을 닫음
function alert_close($msg, $error=true){
    // global $g5, $config, $member, $is_member, $is_admin, $board;
    
    //run_event('alert_close', $msg, $error);

    $msg = strip_tags($msg, '<br>');

    $header = '';
    if (isset($g5['title'])) {
        $header = $g5['title'];
    }
    include_once('alert_close.php');
    exit;
}


?>