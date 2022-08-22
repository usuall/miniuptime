<?php

//require_once(dirname(__FILE__).'/lib/config.php');
require_once(dirname(__FILE__).'/../smarty/config/config.php');

        
//디버그 모드
//$smarty->debugging = true;

/*
CREATE TABLE `test01` (
  `col1` int(10) NOT NULL,
  `col2` varchar(255) NOT NULL,
  `col3` varchar(255) NOT NULL,
  `col4` varchar(255) NOT NULL
);

ALTER TABLE `test01`
  ADD PRIMARY KEY (`col1`);

ALTER TABLE `test01`
  MODIFY `col1` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

INSERT INTO `test01` (`col1`, `col2`, `col3`, `col4`) VALUES (NULL, 'test1', 'test11', 'test111');
INSERT INTO `test01` (`col1`, `col2`, `col3`, `col4`) VALUES (NULL, 'test2', 'test22', 'test222');
INSERT INTO `test01` (`col1`, `col2`, `col3`, `col4`) VALUES (NULL, 'test3', 'test33', 'test333');
INSERT INTO `test01` (`col1`, `col2`, `col3`, `col4`) VALUES (NULL, 'test4', 'test44', 'test444');
*/


//데이터 조회
$result = $mysql->prepare("select * from test01"); 
$result->execute(); 
$result->setFetchMode(PDO::FETCH_LAZY); 
$smarty->assign('result',$result); 



//데이터 조회(결과 없는 경우)
$result2 = $mysql->prepare("select * from test01 where col1='55' "); 
$result2->execute(); 
$result2->setFetchMode(PDO::FETCH_LAZY); 
$smarty->assign('result2',$result2); 


//template파일 설정
$smarty->display('db1.html');


?>