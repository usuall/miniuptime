<?php

require_once(dirname(__FILE__).'/lib/config.php');


$query = "select a.grp_no, grp_short_title, count(a.url_no) as cnt
            from tb_url as a
            left outer join tb_group as b
            on a.grp_no= b.grp_no
            where url_fg = 1
            group by grp_no
            order by grp_short_title";
$stmt = $pdo->prepare($query);
$stmt->execute();
$menu = $stmt->fetchAll();

$smarty->assign('menu', $menu);




?>