<?php


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

?>