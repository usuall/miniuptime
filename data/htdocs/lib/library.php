<?php

$g5['title'] = 'notice';

function checkPriod($minute){
    //점검시간
    if($minute > 60 ){
        $time1 = (int)($minute / 60);
        $time2 = $minute % 60;
        $diff_time = $time1 .'h ' . $time2 .'m';
    } else {
        $diff_time = $minute.'m'; 
    }

    return $diff_time;
}

function alert($msg='', $url='', $error=true, $post=false){

    //run_event('alert', $msg, $url, $error, $post);

    $msg = $msg ? strip_tags($msg, '<br>') : '올바른 방법으로 이용해 주십시오.';

    $header = '';
    if (isset($g5['title'])) {
        $header = $g5['title'];
    }
    include_once('alert.php');
    exit;
}


// 경고메세지 출력후 창을 닫음
function alert_close($msg, $error=true){
    // global $g5, $config, $member, $is_member, $is_admin, $board;
    
    //run_event('alert_close', $msg, $error);

    $msg = strip_tags($msg, '<br>');

    $header = '';
    if (isset($g5['title'])) {
        $header = $g5['title'];
    }
    include_once('alert_close.php');
    exit;
}

// XSS 관련 태그 제거
function clean_xss_tags($str, $check_entities=0, $is_remove_tags=0, $cur_str_len=0, $is_trim_both=1)
{
    if( $is_trim_both ) {
        // tab('\t'), formfeed('\f'), vertical tab('\v'), newline('\n'), carriage return('\r') 를 제거한다.
        $str = preg_replace("#[\t\f\v\n\r]#", '', $str);
    }

    if( $is_remove_tags ){
        $str = strip_tags($str);
    }

    if( $cur_str_len ){
        $str = utf8_strcut($str, $cur_str_len, '');
    }

    $str_len = strlen($str);
    
    $i = 0;
    while($i <= $str_len){
        $result = preg_replace('#</*(?:applet|b(?:ase|gsound|link)|embed|frame(?:set)?|i(?:frame|layer)|l(?:ayer|ink)|meta|object|s(?:cript|tyle)|title|xml)[^>]*+>#i', '', $str);
        
        if( $check_entities ){
            $result = str_replace(array('&colon;', '&lpar;', '&rpar;', '&NewLine;', '&Tab;'), '', $result);
        }
        
        $result = preg_replace('#([^\p{L}]|^)(?:javascript|jar|applescript|vbscript|vbs|wscript|jscript|behavior|mocha|livescript|view-source)\s*:(?:.*?([/\\\;()\'">]|$))#ius',
                '$1$2', $result);

        if((string)$result === (string)$str) break;

        $str = $result;
        $i++;
    }

    return $str;
}

// 동일한 host url 인지
function check_url_host($url, $msg='', $return_url='', $is_redirect=false)
{
    if(!$msg)
        $msg = 'url에 타 도메인을 지정할 수 없습니다.';

    // if(run_replace('check_url_host_before', '', $url, $msg, $return_url, $is_redirect) === 'is_checked'){
    //     return;
    // }

    // KVE-2021-1277 Open Redirect 취약점 해결
    if (preg_match('#\\\0#', $url)) {
        alert('url 에 올바르지 않은 값이 포함되어 있습니다.');
    }

    while ( ( $replace_url = preg_replace(array('/\/{2,}/', '/\\@/'), array('//', ''), urldecode($url)) ) != $url ) {
        $url = $replace_url;
    }
    $p = @parse_url(trim($url));
    $host = preg_replace('/:[0-9]+$/', '', $_SERVER['HTTP_HOST']);
    $is_host_check = false;
    
    // url을 urlencode 를 2번이상하면 parse_url 에서 scheme와 host 값을 가져올수 없는 취약점이 존재함
    if ( $is_redirect && !isset($p['host']) && urldecode($url) != $url ){
        $i = 0;
        while($i <= 3){
            $url = urldecode($url);
            if( urldecode($url) == $url ) break;
            $i++;
        }

        if( urldecode($url) == $url ){
            $p = @parse_url($url);
        } else {
            $is_host_check = true;
        }
    }

    // if(stripos($url, 'http:') !== false) {
    //     if(!isset($p['scheme']) || !$p['scheme'] || !isset($p['host']) || !$p['host'])
    //         alert('url 정보가 올바르지 않습니다.', $return_url);
    // }

    //php 5.6.29 이하 버전에서는 parse_url 버그가 존재함
    //php 7.0.1 ~ 7.0.5 버전에서는 parse_url 버그가 존재함
    if ( $is_redirect && (isset($p['host']) && $p['host']) ) {
        $bool_ch = false;
        foreach( array('user','host') as $key) {
            if ( isset( $p[ $key ] ) && strpbrk( $p[ $key ], ':/?#@' ) ) {
                $bool_ch = true;
            }
        }
        if( $bool_ch ){
            $regex = '/https?\:\/\/'.$host.'/i';
            if( ! preg_match($regex, $url) ){
                $is_host_check = true;
            }
        }
    }

    // if ((isset($p['scheme']) && $p['scheme']) || (isset($p['host']) && $p['host']) || $is_host_check) {
    //     //if ($p['host'].(isset($p['port']) ? ':'.$p['port'] : '') != $_SERVER['HTTP_HOST']) {
    //     if (run_replace('check_same_url_host', (($p['host'] != $host) || $is_host_check), $p, $host, $is_host_check, $return_url, $is_redirect)) {
    //         echo '<script>'.PHP_EOL;
    //         echo 'alert("url에 타 도메인을 지정할 수 없습니다.");'.PHP_EOL;
    //         echo 'document.location.href = "'.$return_url.'";'.PHP_EOL;
    //         echo '</script>'.PHP_EOL;
    //         echo '<noscript>'.PHP_EOL;
    //         echo '<p>'.$msg.'</p>'.PHP_EOL;
    //         echo '<p><a href="'.$return_url.'">돌아가기</a></p>'.PHP_EOL;
    //         echo '</noscript>'.PHP_EOL;
    //         exit;
    //     }
    // }
}

function utf8_strcut( $str, $size, $suffix='...' )
{
    if( function_exists('mb_strlen') && function_exists('mb_substr') ){
        
        if(mb_strlen($str)<=$size) {
            return $str;
        } else {
            $str = mb_substr($str, 0, $size, 'utf-8');
            $str .= $suffix;
        }

    } else {
        $substr = substr( $str, 0, $size * 2 );
        $multi_size = preg_match_all( '/[\x80-\xff]/', $substr, $multi_chars );

        if ( $multi_size > 0 )
            $size = $size + intval( $multi_size / 3 ) - 1;

        if ( strlen( $str ) > $size ) {
            $str = substr( $str, 0, $size );
            $str = preg_replace( '/(([\x80-\xff]{3})*?)([\x80-\xff]{0,2})$/', '$1', $str );
            $str .= $suffix;
        }
    }

    return $str;
}

?>