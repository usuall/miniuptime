<?php

require_once(dirname(__FILE__).'/lib/config.php');


$query = "select a.grp_no, grp_short_title, count(a.url_no) as cnt
            from tb_url as a
            left outer join tb_group as b
            on a.grp_no = b.grp_no
            where url_fg = 1
            group by grp_no
            order by grp_short_title";
$stmt = $pdo->prepare($query);
$stmt->execute();
$menu = $stmt->fetchAll();
$smarty->assign('menu', $menu);


//유사도 이상 건수
$sql = "SELECT count(*) as cnt FROM `tb_url` where 1=1 and url_fg = 1 and ((url_img_match1 BETWEEN 0 AND 50) and (url_html_match1 BETWEEN 0 AND 50))";
$mysql = $pdo->query($sql);
$status_cnt = $mysql->fetch(PDO::FETCH_ASSOC);
$smarty->assign('url_alert_cnt', $status_cnt['cnt']);








?>