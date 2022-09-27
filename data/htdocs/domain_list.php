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
$mysql = $pdo->prepare('SELECT url_no, url_group, url_title1, url_title2, url_addr, url_level, check_date, valid_from, 
                        valid_till, days_left, creation_date, substr(expiration_date, 1, 10) as expiration_date, domain_name 
                        FROM `tb_domain_list` as a
                        ORDER BY `expiration_date` ASC');

$mysql->execute();

//データ割り当て
$result = array();

$i = 1;

while ($data = $mysql->fetch(PDO::FETCH_ASSOC)) {
    
    // if($data['url_fg'] == 1){
    //     $url_fg = 'Y';
    // } else {
    //     $url_fg = 'N';
    // }
    $check_date = $data['check_date'];

    // $diff_time = checkPriod($data['diff_time']);
    
    

    $result[] = array(
        'url_no'            => $data['url_no'],
        'url_group'         => $data['url_group'],
        'url_title1'        => $data['url_title1'],
        'url_title2'        => $data['url_title2'],
        'url_addr'          => $data['url_addr'],
        'url_level'         => $data['url_level'],
        'check_date'        => $data['check_date'],
        'valid_from'        => $data['valid_from'],        
        'valid_till'        => $data['valid_till'],
        'days_left'         => $data['days_left'],
        'creation_date'     => substr($data['creation_date'],0, 10),
        'expiration_date'   => substr($data['expiration_date'],0, 10),
        'domain_name'       => $data['domain_name'],            
    );
}

function isNull($str){
    if($str == ''){
        return '인증서없음';
    } else {
        return $str;
    }
        
}

function isNull2($str){
    if($str == ''){
        return '도메인없음';
    } else {
        return $str;
    }
        
}

$smarty->assign('check_date', $check_date);
$smarty->assign('result', $result);


// $smarty->debugging = true;
$smarty->display('domain_list.html');

//DB 접속종료
$pdo = null;
?>