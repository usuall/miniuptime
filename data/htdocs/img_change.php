<?php

require_once(dirname(__FILE__).'/lib/config.php');
$base_dir = dirname(__FILE__);

$mon_no = $_GET['mon_no'];
if(isset($mon_no) && $mon_no > 0){

    //모니터링 정보
    $arr_mon = getMonInfo($mon_no);
    // var_dump($arr_mon);

    #파일 일련번호 형식
    $url_no = sprintf('%04d', $arr_mon['url_no']);
    $move_img_fg = 0;
    $move_html_fg = 0;

    # 이미지 파일
    $filename = $url_no."_site.png";
    $daily_file = IMG_CAPTURE_PATH."daily/".$arr_mon['mon_image'];
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


}





?>