<?php

require_once(dirname(__FILE__).'/lib/config.php');

error_reporting (E_ALL ^ E_NOTICE);

//상단 메뉴
include_once('menu.php');

//이미지 유사도 표시 상한선
$code_status = '';
$code_status = $_GET['code'];
if(isset($code_status) == True){
} else {
    $code_status = '';
}

//データ検索
/* 
$sql = "SELECT a.*, b.*, timestampdiff(minute, b.url_lastest_check_dt, now()) as diff_time 
FROM `tb_monitor` as a 
left outer join tb_url as b 
on a.url_no = b.url_no 
where a.url_img_match1 <= '$img_level' 
order by a.url_no 
desc limit 10";
*/

//서비스 지연 건수
$sql = "SELECT count(*) as cnt FROM `tb_url` WHERE 1=1 and url_fg = 1 and url_response_time >= 10";
$mysql = $pdo->query($sql);
$response_cnt = $mysql->fetch(PDO::FETCH_ASSOC);
$smarty->assign('response_cnt', $response_cnt);

//상태 코드 이상 건수
$sql = "SELECT count(*) as cnt FROM `tb_url` where 1=1 and url_fg = 1 and (url_status <> 200 or url_status is null)";
$mysql = $pdo->query($sql);
$status_cnt = $mysql->fetch(PDO::FETCH_ASSOC);
$smarty->assign('status_cnt', $status_cnt);

//HTML 유사도 이상 건수
$sql = "SELECT count(*) as cnt FROM `tb_url` where 1=1 and url_fg = 1 and (url_html_match1 BETWEEN 0 AND 60)";
$mysql = $pdo->query($sql);
$status_cnt = $mysql->fetch(PDO::FETCH_ASSOC);
$smarty->assign('html_cnt', $status_cnt);

//원본 미설정 건수
$sql = "SELECT count(*) as cnt FROM `tb_url` WHERE 1=1
and url_fg = 1 and (url_img_match1 = -1 or url_html_match1 = -1)";
$mysql = $pdo->query($sql);
$origin_not_cnt = $mysql->fetch(PDO::FETCH_ASSOC);
$smarty->assign('origin_not_cnt', $origin_not_cnt);


$sql ="SELECT b.*, c.grp_short_title
        FROM tb_url as b
        left outer join tb_group as c
        on b.grp_no = c.grp_no
        where 1=1 
        and url_fg = 1
        and ";

if($code_status == ''){
    $sql .= "( 
            (b.url_status <> 200 or b.url_status is NULL) OR 
            (b.url_img_match1 <= 40 or b.url_html_match1 <= 40) OR 
            (b.url_img_match1 = -1 or b.url_html_match1 = -1) OR
            (b.url_response_time >= 10)
            )
        ";
} else if($code_status == 'delay'){
    $sql .= " (b.url_response_time >= 10) ";
} else if($code_status == 'status'){
    $sql .= " (b.url_status <> 200 or b.url_status is NULL) ";
} else if($code_status == 'img'){
    $sql .= " (b.url_img_match1 <= 40 or b.url_html_match1 <= 40) ";
} else if($code_status == 'origin'){
    $sql .= " (b.url_img_match1 = -1 or b.url_html_match1 = -1) ";
}










$mysql = $pdo->query($sql);

//データ割り当て
$result = array();
$arr_row = array();

$i = 1;
while ($data = $mysql->fetch(PDO::FETCH_ASSOC)) {

    # 응답 속도
    $url_response_time = $data['url_response_time'];
    if($url_response_time > 5 && $url_response_time < 10){
        $url_response_time_color = 'warning';
    } else if ($url_response_time >= 10) {
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
    } else if ($data['url_img_match1'] <= 60) {
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

    
    $diff_time = checkPriod($data['diff_time']);

    #결과 출력용
    $arr_row[] = array(
        'grp_title' => $data['grp_short_title'],
        'url_no' => $data['url_no'],
        'url_title' => $data['url_title'],
        'url_addr' => $data['url_addr'],
        'url_no' => $data['url_no'],
        'url_dt' => $data['url_dt'],
        'url_response_time' => $data['url_response_time'],
        'url_response_time_color' =>  $url_response_time_color,
        'status_code' => $status_code,
        'status_code_color' => $status_code_color,
        'diff_time' => $diff_time,
        'html_file' => $data['html_file'],
        'url_img_match1' => $data['url_img_match1'],
        'url_img_match1_color' => $url_img_match1_color,
        'url_html_match1' => $data['url_html_match1'],
        'url_html_match1_color' => $url_html_match1_color,
        'url_html_diff_output' => $data['url_html_diff_output'],
        'url_dt' => $data['url_dt'],
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
$smarty->display('dash04.html');

//DB 접속종료
$pdo = null;
?>