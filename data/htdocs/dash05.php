<?php

require_once(dirname(__FILE__).'/lib/config.php');

error_reporting (E_ALL ^ E_NOTICE);

//상단 메뉴
include_once('menu.php');

//이미지 유사도 표시 상한선
$img_level = '';
$img_level = $_GET['min'];
if(isset($img_level) == True){

} else {
    $img_level = 10;
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

$sql = "SELECT * FROM `tb_url` WHERE url_lastest_check_dt <= DATE_ADD(NOW(), INTERVAL -$img_level MINUTE) order by url_lastest_check_dt";


// echo $sql ;
$mysql = $pdo->query($sql);

//データ割り当て
$result = array();
$arr_row = array();

$i = 1;
while ($data = $mysql->fetch(PDO::FETCH_ASSOC)) {

    $grp_short_title = getGRP_short_title($data['grp_no']);

    // $arr_url = getUrlinfo($data['url_no']);

    # 응답 속도
    $url_response_time = $data['url_response_time'];
    if($url_response_time > 5 && $url_response_time < 10){
        $url_response_time_color = 'warning';
    } else if ($url_response_time >= 10 || $url_response_time == '') {
        $url_response_time_color = 'danger';
    } else {
        $url_response_time_color = 'success';
    }

    # 상태 코드
    $status_code = $data['url_status'];
    if($status_code == 200){
        $status_code_color = 'success';
    } else {
        $status_code_color = 'danger';
    }

    # 이미지 유사도
    if($data['url_img_match1'] == '-1'){
        $data['url_img_match1'] = '원본없음';
        $url_img_match1_color = 'secondary';
    } else if($data['url_img_match1'] == '-2'){
        $data['url_img_match1'] = '캡쳐안됨';
        $url_img_match1_color = 'secondary';
    } else if($data['url_img_match1'] < 100 && $data['url_img_match1'] > 60){
        $url_img_match1_color = 'success';
    } else if ($data['url_img_match1'] <= 60 || $data['url_img_match1'] == '') {
        $url_img_match1_color = 'danger';
    } else {
        $url_img_match1_color = 'success';
    }
    
    # HTML 유사도
    if($data['url_html_match1'] == '-1'){
        $data['url_html_match1'] = '원본없음';
        $url_html_match1_color = 'secondary';
    // } else if($data['url_html_match1'] == '-2'){
    //     $data['url_html_match1'] = '캡쳐안됨';
    //     $url_html_match1_color = 'secondary';
    } else if($data['url_html_match1'] < 100 && $data['url_html_match1'] > 60){
        $url_html_match1_color = 'success';
    } else if ($data['url_html_match1'] <= 60) {
        $url_html_match1_color = 'danger';
    } else {
        $url_html_match1_color = 'success';
    }

    
    // $diff_time = checkPriod($data['diff_time']);

    if($data['url_fg'] == 1){
        $url_fg = 'primary';        
    } else {
        $url_fg = 'danger';
    }

    #결과 출력용
    $arr_row[] = array(
        'grp_title' => $grp_short_title,
        'url_title' => $data['url_title'],
        'url_addr' => $data['url_addr'],
        'url_no' => $data['url_no'],
        'url_lastest_check_dt' => $data['url_lastest_check_dt'],
        'url_response_time' => $data['url_response_time'],
        'url_response_time_color' =>  $url_response_time_color,
        'url_status' => $data['url_status'],
        'status_code_color' => $status_code_color,
        'diff_time' => $diff_time,
        'html_file' => $data['html_file'],
        'url_img_match1' => $data['url_img_match1'],
        'url_img_match1_color' => $url_img_match1_color,
        'url_html_match1' => $data['url_html_match1'],
        'url_html_match1_color' => $url_html_match1_color,
        'url_html_diff_output' => $data['url_html_diff_output'],
        'url_fg' => $url_fg,
    );

    if($i == 1){
        $lastest_no = $data['url_no'];    
    }
    
    // array_push($arr_groups, $arr_urls);
    //array_push($result, $arr_row);


    $i++;


}
// $smarty->debugging = true;
$smarty->assign('result', $arr_row);
$smarty->assign('url_no', $lastest_no);


// $smarty->debugging = true;
//template파일 설정
$smarty->display('dash05.html');

//DB 접속종료
$pdo = null;
?>