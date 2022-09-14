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
$mysql = $pdo->prepare('SELECT a.url_no, c.grp_short_title, b.url_title, b.url_addr, a.check_date, a.valid_from, a.valid_till, a.days_left, a.creation_date, a.expiration_date, a.domain_name 
                        FROM `tb_domain` as a
                        left outer join tb_url as b on a.url_no = b.url_no 
                        left outer join tb_group as c on b.grp_no = c.grp_no
                        order by a.days_left');
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
        'grp_short_title'   => $data['grp_short_title'],
        'url_title'         => $data['url_title'],
        'url_addr'          => $data['url_addr'],
        'valid_from'        => $data['valid_from'],        
        'valid_till'        => $data['valid_till'],
        'days_left'         => isNull($data['days_left']),
        'creation_date'     => substr($data['creation_date'],0, 10),
        'expiration_date'   => substr($data['expiration_date'],0, 10),
        'domain_name'       => $data['domain_name'],            
    );
}

function isNull($str){
    if($str == ''){
        return '-';
    } else {
        return $str;
    }
        
}

$smarty->assign('check_date', $check_date);
$smarty->assign('result', $result);


// $smarty->debugging = true;
$smarty->display('domain.html');

//DB 접속종료
$pdo = null;
?>