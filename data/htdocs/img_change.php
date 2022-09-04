<?php

require_once(dirname(__FILE__).'/lib/config.php');
$base_dir = dirname(__FILE__);


$url_no = $_GET['url_no'];
$skip = $_GET['skip'];

if(isset($url_no) && $url_no > 0){

    #파일 일련번호 형식
    $url_no = sprintf('%04d', $url_no);
    $move_img_fg = 0;
    $move_html_fg = 0;

    # 이미지 파일
    $filename = $url_no."_site.png";
    $daily_file = IMG_CAPTURE_PATH."daily/".$filename;
    $origin_file = IMG_CAPTURE_PATH."orign/".$filename;
    if(file_exists($daily_file)){
        if(copy($daily_file, $origin_file)){
            #unlink($daily_file);
            $move_img_fg = 1;
        }	
    }

    # HTML 파일
    $filename = $url_no.".html";
    $daily_file = HTML_CAPTURE_PATH."daily/".$filename;
    $origin_file = HTML_CAPTURE_PATH."orign/".$filename;
    if(file_exists($daily_file)){
        if(copy($daily_file, $origin_file)){
            unlink($daily_file); 
            $move_html_fg = 1;
        }	
    }

    if($move_img_fg == 1 && $move_html_fg == 1){
        alert_close('적용 완료');
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