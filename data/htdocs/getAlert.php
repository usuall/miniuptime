<?php

require_once(dirname(__FILE__).'/lib/config.php');


//유사도 이상 건수
$sql = "SELECT count(*) as cnt FROM `tb_url` where 1=1 and url_fg = 1 and ((url_img_match1 BETWEEN 0 AND 50) and (url_html_match1 BETWEEN 0 AND 50))";
$mysql = $pdo->query($sql);
$status_cnt = $mysql->fetch(PDO::FETCH_ASSOC);

if($status_cnt['cnt'] == 0){
    $alert_output = '';
} else {
    $alert_output = $status_cnt['cnt'];
}


header('Content-type: application/json');
echo json_encode($alert_output);

//DB 접속종료
$pdo = null;
?>