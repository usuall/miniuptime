<?php

require_once(dirname(__FILE__).'/lib/config.php');
$base_dir = dirname(__FILE__);


$url_no = $_GET['url_no'];

if(isset($url_no)){

    //todo 
    //image file move
    $url_no = sprintf('%04d', $url_no);

    $filename = $url_no."_site.png";
    echo "<br>".$daily_file = IMG_CAPTURE_PATH."daily/".$filename;
    echo "<br>".$origin_file = IMG_CAPTURE_PATH."orign/".$filename;
    if(file_exists($daily_file)){
        if(copy($daily_file, $origin_file)){
            unlink($daily_file);
            alert_close('적용 완료');
        }	
    }
    
} else {
    alert_close('해당하는 URL이 존재하지 않음');
}

// $mysql = $pdo->query("SELECT * from tb_url where url_no = '{$url_no}'");
// $result = $mysql->fetch(PDO::FETCH_ASSOC);

// $smarty->debugging = true;

// $smarty->assign('result', $result);
// $smarty->display('img_diff.html');


?>