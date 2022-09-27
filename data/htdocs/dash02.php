<?php

require_once(dirname(__FILE__).'/lib/config.php');

error_reporting (E_ALL ^ E_NOTICE);

//상단 메뉴
include_once('menu.php');

//이미지 유사도 표시 상한선
$img_level = '';
$img_level = $_GET['img'];
if(isset($img_level) == True){
} else {
    $img_level = 100;
}

//データ検索
/* 
$sql = "SELECT a.*, b.*, timestampdiff(minute, b.url_lastest_check_dt, now()) as diff_time 
FROM `tb_monitor` as a 
left outer join tb_url as b 
on a.url_no = b.url_no 
where a.mon_img_match1 <= '$img_level' 
order by a.mon_no 
desc limit 10";


$sql ="SELECT c.grp_short_title, a.*, b.*, timestampdiff(minute, b.url_lastest_check_dt, now()) as diff_time 
FROM `tb_monitor` as a 
left outer join tb_url as b 
on a.url_no = b.url_no 
left outer join tb_group as c 
on c.grp_no = b.grp_no 
where a.mon_img_match1 <= '$img_level' 
order by a.mon_no desc limit 10";
*/

$sql = "select * from tb_monitor where mon_img_match1 <= '$img_level' order by mon_no desc limit 10";

// echo $sql ;
$mysql = $pdo->query($sql);

//データ割り当て
$result = array();
$arr_row = array();

$i = 1;
while ($data = $mysql->fetch(PDO::FETCH_ASSOC)) {

    // getGRP_title($data[''])

    $arr_url = getUrlinfo($data['url_no']);

    # 응답 속도
    $mon_response_time = $data['mon_response_time'];
    if($mon_response_time > 5 && $mon_response_time < 10){
        $mon_response_time_color = 'warning';
    } else if ($mon_response_time >= 10) {
        $mon_response_time_color = 'danger';
    } else {
        $mon_response_time_color = 'success';
    }

    # 상태 코드
    $status_code = $data['status_code'];
    if($status_code == 200){
        $status_code_color = 'success';
    } else {
        $status_code_color = 'danger';
    }

    # 이미지 유사도
    if($data['mon_img_match1'] == '-1'){
        $data['mon_img_match1'] = '원본없음';
        $mon_img_match1_color = 'secondary';
    } else if($data['mon_img_match1'] == '-2'){
        $data['mon_img_match1'] = '캡쳐안됨';
        $mon_img_match1_color = 'secondary';
    } else if($data['mon_img_match1'] < 100 && $data['mon_img_match1'] > 60){
        $mon_img_match1_color = 'success';
    } else if ($data['mon_img_match1'] <= 60) {
        $mon_img_match1_color = 'danger';
    } else {
        $mon_img_match1_color = 'success';
    }
    
    # HTML 유사도
    if($data['mon_html_match1'] == '-1'){
        $data['mon_html_match1'] = '원본없음';
        $mon_html_match1_color = 'secondary';
    // } else if($data['mon_html_match1'] == '-2'){
    //     $data['mon_html_match1'] = '캡쳐안됨';
    //     $mon_html_match1_color = 'secondary';
    } else if($data['mon_html_match1'] < 100 && $data['mon_html_match1'] > 60){
        $mon_html_match1_color = 'success';
    } else if ($data['mon_html_match1'] <= 60) {
        $mon_html_match1_color = 'danger';
    } else {
        $mon_html_match1_color = 'success';
    }

    
    $diff_time = checkPriod($data['diff_time']);

    #결과 출력용
    $arr_row[] = array(
        'grp_title' => $arr_url['grp_short_title'],
        'mon_no' => $data['mon_no'],
        'url_title' => $arr_url['url_title'],
        'url_addr' => $arr_url['url_addr'],
        'url_no' => $arr_url['url_no'],
        'mon_dt' => $data['mon_dt'],
        'mon_response_time' => $data['mon_response_time'],
        'mon_response_time_color' =>  $mon_response_time_color,
        'status_code' => $data['status_code'],
        'status_code_color' => $status_code_color,
        'diff_time' => $diff_time,
        'html_file' => $data['html_file'],
        'mon_img_match1' => $data['mon_img_match1'],
        'mon_img_match1_color' => $mon_img_match1_color,
        'mon_html_match1' => $data['mon_html_match1'],
        'mon_html_match1_color' => $mon_html_match1_color,
        'mon_html_diff_output' => $data['mon_html_diff_output'],
        // 'mon_dt' => $data['mon_dt'],
    );

    if($i == 1){
        $lastest_no = $data['mon_no'];    
    }
    
    // array_push($arr_groups, $arr_urls);
    //array_push($result, $arr_row);


    $i++;


}
// $smarty->debugging = true;
$smarty->assign('result', $arr_row);
$smarty->assign('mon_no', $lastest_no);


// $smarty->debugging = true;
//template파일 설정
$smarty->display('dash02.html');

//DB 접속종료
$pdo = null;
?>