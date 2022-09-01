<?php

require_once(dirname(__FILE__).'/lib/config.php');


//이미지 유사도 표시 상한선
$img_level = '';
$img_level = $_GET['img'];
if(isset($img_level) == True){
} else {
    $img_level = 100;
}

$mon_no = $_POST['mon_no'];
//データ検索
// $mysql = $pdo->query("SELECT max(mon_no) as mon_no from tb_monitor");
// $data = $mysql->fetch(PDO::FETCH_ASSOC);
// $mon_no = $data['mon_no'] - 1;

$sql = "SELECT a.*, b.*, timestampdiff(minute, b.url_lastest_check_dt, now()) as diff_time 
        FROM `tb_monitor` as a 
        LEFT OUTER JOIN tb_url as b on a.url_no = b.url_no 
        where a.mon_img_match1 <= '$img_level' 
        and a.mon_no > '$mon_no'
        ORDER BY a.mon_no desc";

$mysql = $pdo->query($sql);

//データ割り当て
// $groups = array();
$result = array();
$arr_groups = array();
$arr_urls = array();

$arr_row = array();

$i = 1;
while ($data = $mysql->fetch(PDO::FETCH_ASSOC)) {

    $status_code_color = 'text-dark';
    if($data['status_code'] != 200){
        $status_code_color = 'strong text-pink';
    }

    $mon_img_match1_color = 'text-dark';
    if($data['mon_img_match1'] == '-1'){
        $data['mon_img_match1'] = '원본없음';
        $mon_img_match1_color = 'strong text-pink';
    } else if($data['mon_img_match1'] < 100 && $data['mon_img_match1'] > 60){
        $mon_img_match1_color = 'text-indigo';
    } else if ($data['mon_img_match1'] <= 60) {
        $mon_img_match1_color = 'strong text-pink';
    }
    
    $mon_html_match1_color = 'text-dark';
    if($data['mon_html_match1'] == '-1'){
        $data['mon_html_match1'] = '원본없음';
        $mon_html_match1_color = 'strong text-pink';
    } else if($data['mon_html_match1'] < 100 && $data['mon_html_match1'] > 60){
        $mon_html_match1_color = 'text-indigo';
    } else if ($data['mon_html_match1'] <= 60) {
        $mon_html_match1_color = 'strong text-pink';
    }

    
    $diff_time = checkPriod($data['diff_time']);

    #결과 출력용
    $arr_row[] = array(
        'mon_no' => $data['mon_no'],
        'url_title' => $data['url_title'],
        'url_addr' => $data['url_addr'],
        'url_no' => $data['url_no'],
        'mon_dt' => $data['mon_dt'],
        'mon_response_time' => $data['mon_response_time'],
        'status_code' => $data['status_code'],
        'status_code_color' => $status_code_color,
        'diff_time' => $diff_time,
        'html_file' => $data['html_file'],
        'mon_img_match1' => $data['mon_img_match1'],
        'mon_img_match1_color' => $mon_img_match1_color,
        'mon_html_match1' => $data['mon_html_match1'],
        'mon_html_match1_color' => $mon_html_match1_color,
        'mon_html_diff_output' => $data['mon_html_diff_output'],
        'sql' => $sql,
    );

    


    $i++;


}

// var_dump($result);


header('Content-type: application/json');
echo json_encode($arr_row);


$smarty->debugging = true;

/**/


//DB 접속종료
$pdo = null;
?>