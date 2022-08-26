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
$mysql = $pdo->prepare('SELECT * FROM tb_group where grp_fg = 1 and grp_no = :id ORDER BY grp_title');
$mysql->bindValue(':id', $grp_no);
$mysql->execute();
//データ割り当て
// $groups = array();
$result = array();
$arr_groups = array();
$arr_urls = array();

$i = 1;
while ($data = $mysql->fetch(PDO::FETCH_ASSOC)) {

    if ($i != 1){
        $arr_urls = array();
        $arr_groups = array();
    }    
  
    $mysql2 = $pdo->prepare('SELECT * FROM tb_url where grp_no = :id and url_fg = 1');
    $mysql2->bindValue(':id', $data['grp_no']);
    $mysql2->execute();
    while ($data2 = $mysql2->fetch(PDO::FETCH_ASSOC)) {

        $urls = array(
            'url_no' => $data2['url_no'],
            'url_title' => $data2['url_title'],
            'url_addr' => $data2['url_addr'],
            'url_redirected' => $data2['url_redirected'],
            'url_status' => $data2['url_status'],
            'url_lastest_check_dt' => $data2['url_lastest_check_dt'],
            'url_img_match1' => $data2['url_img_match1'],            
        );

        array_push($arr_urls, $urls);
    }
    
    #결과 출력용
    $arr_groups = array(
        'grp_no' => $data['grp_no'],
        'grp_title' => $data['grp_title'],
        'grp_short_title' => $data['grp_short_title'],
        'urls' => $arr_urls,
    );

    // array_push($arr_groups, $arr_urls);
    array_push($result, $arr_groups);


    $i++;


}

// var_dump($result);
$smarty->assign('result', $result);


//template파일 설정



//データ検索
$sql = "SELECT a.*, b.* FROM `tb_monitor` as a left outer join tb_url as b on a.url_no = b.url_no 
where a.mon_img_match1 <= '$img_level' 
and b.grp_no = '$grp_no' order by a.mon_no desc limit 20";
// echo $sql;

$mysql = $pdo->query($sql);

//データ割り当て
$result2 = array();
$arr_row2 = array();

// $result = $mysql->fetchAll(PDO::FETCH_ASSOC);

$i = 1;
while ($data = $mysql->fetch(PDO::FETCH_ASSOC)) {

    $status_code_color = 'text-dark bg-white';
    if($data['status_code'] != 200){
        $status_code_color = 'strong text-pink bg-white';
    }

    $mon_img_match1_color = 'text-dark bg-white';
    if($data['mon_img_match1'] == '-1'){
        $data['mon_img_match1'] = '원본없음';
        $mon_img_match1_color = 'strong text-pink bg-white';
    } else if($data['mon_img_match1'] < 100 && $data['mon_img_match1'] > 60){
        $mon_img_match1_color = 'text-indigo bg-white';
    } else if ($data['mon_img_match1'] <= 60) {
        $mon_img_match1_color = 'strong text-pink bg-white';
    }
    
    $mon_html_match1_color = 'text-dark bg-white';
    if($data['mon_html_match1'] == '-1'){
        $data['mon_html_match1'] = '원본없음';
        $mon_html_match1_color = 'strong text-pink bg-white';
    } else if($data['mon_html_match1'] < 100 && $data['mon_html_match1'] > 60){
        $mon_html_match1_color = 'text-indigo bg-white';
    } else if ($data['mon_html_match1'] <= 60) {
        $mon_html_match1_color = 'strong text-pink bg-white';
    }

    


    #결과 출력용
    $arr_row2 = array(
        'mon_no' => $data['mon_no'],
        'url_title' => $data['url_title'],
        'url_addr' => $data['url_addr'],
        'url_no' => $data['url_no'],
        'mon_dt' => $data['mon_dt'],
        'mon_response_time' => $data['mon_response_time'],
        'status_code' => $data['status_code'],
        'status_code_color' => $status_code_color,
        'html_file' => $data['html_file'],
        'mon_img_match1' => $data['mon_img_match1'],
        'mon_img_match1_color' => $mon_img_match1_color,
        'mon_html_match1' => $data['mon_html_match1'],
        'mon_html_match1_color' => $mon_html_match1_color,
        'mon_html_diff_output' => $data['mon_html_diff_output'],
        // 'mon_dt' => $data['mon_dt'],
    );

    // array_push($arr_groups, $arr_urls);
    array_push($result2, $arr_row2);


    $i++;


}
$smarty->assign('result2', $result2);

$smarty->debugging = true;

$smarty->display('dash03.html');

//DB 접속종료
$pdo = null;
?>