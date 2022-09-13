<?php
require_once(dirname(__FILE__).'/lib/config.php');

//상단 메뉴
include_once('menu.php');

$url_no = $_GET['url_no'];

# 그룹 select box
$sql ="SELECT grp_no, grp_title FROM `tb_group` order by grp_title";
$mysql = $pdo->query($sql);

$arr_row = array();
while ($data = $mysql->fetch(PDO::FETCH_ASSOC)) {
    $arr_row[$data['grp_no']] = $data['grp_title'];
}

$smarty->assign('myOptions', $arr_row);


// $sql = 'SELECT grp_no, grp_title FROM `tb_group` order by grp_title';
// $smarty->assign('myOptions',$pdo->getAssoc($sql));

# url 상세 내역
$mysql = $pdo->prepare('select * from tb_url where url_no =:url_no limit 1');
$mysql->bindValue(':url_no', $url_no);
$mysql->execute();

//データ割り当て
$result = $mysql->fetch(PDO::FETCH_ASSOC);
$smarty->assign('result', $result);

//셀렉트 박스 선택된 상태로
$smarty->assign('mySelect', $result['grp_no']);


// var_dump($result);

if($result['url_fg'] == 1){
    $url_fg = "checked='checked'";
} else {
    $url_fg = '';
}

$smarty->assign('url_fg', $url_fg);

// $smarty->debugging = true;
$smarty->display('url_config.html');

//DB 접속종료
$pdo = null;
?>