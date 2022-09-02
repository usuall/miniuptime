<?php

require_once(dirname(__FILE__).'/lib/config.php');

//상단 메뉴
include_once('menu.php');

$grp_no = $_GET['grp_no'];

//이미지 유사도 표시 상한선
$img_level = '';
$img_level = $_GET['img'];
if(isset($img_level) == True){
} else {
    $img_level = 100;
}

//データ検索
$mysql = $pdo->prepare('select *, timestampdiff(minute, url_lastest_check_dt, now()) as diff_time from tb_url where grp_no =:id order by url_title ');
$mysql->bindValue(':id', $grp_no);
$mysql->execute();
//データ割り当て
// $groups = array();
$result = array();
$arr_groups = array();
$arr_urls = array();

$i = 1;

while ($data = $mysql->fetch(PDO::FETCH_ASSOC)) {
    
    if($data['url_fg'] == 1){
        $url_fg = 'Y';
    } else {
        $url_fg = 'N';
    }

    $diff_time = checkPriod($data['diff_time']);

    $urls = array(
        'url_no'            => $data['url_no'],
        'url_title'         => $data['url_title'],
        'url_addr'          => $data['url_addr'],
        'url_redirected'    => $data['url_redirected'],
        'url_response_time' => $data['url_response_time'],        
        'url_status'        => $data['url_status'],
        'url_lastest_check_dt' => $data['url_lastest_check_dt'],
        'diff_time'         => $diff_time,
        'url_img_match1'    => $data['url_img_match1'],
        'url_html_match1'   => $data['url_html_match1'],
        'url_html_diff_output'   => $data['url_html_diff_output'],            
        'url_fg'            => $url_fg,
    );

    array_push($arr_urls, $urls);
}


$smarty->assign('result', $arr_urls);




//graph01
$sql = "SELECT mon_dt, mon_response_time, status_code FROM `tb_monitor` WHERE url_no = 1 order by mon_dt desc limit 30";
$mysql2 = $pdo->query($sql);

//データ割り当て
$result = array();
$arr_row = array();

$i = 1;
while ($data = $mysql2->fetch(PDO::FETCH_ASSOC)) {

    #결과 출력용
    $arr = array(
        'mon_dt'            => substr($data['mon_dt'], 10,6),
        'mon_response_time' => $data['mon_response_time'],
        'status_code'       => $data['status_code'],
    );

    array_push($arr_row, $arr);
    $i++;


}

$smarty->assign('graph', array_reverse($arr_row));


// $smarty->debugging = true;
$smarty->display('dash03.html');

//DB 접속종료
$pdo = null;
?>