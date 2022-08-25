<?php

require_once(dirname(__FILE__).'/lib/config.php');


$grp_no = $_GET['grp_no'];

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
  
    $mysql2 = $pdo->prepare('SELECT * FROM tb_url where grp_no = :id');
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

// $smarty->debugging = true;

//template파일 설정
$smarty->display('dash03.html');

//DB 접속종료
$pdo = null;
?>