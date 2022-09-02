<?php

//홈디렉토리 설정(htdocs)
define('MY_WEB_DIR', dirname(__FILE__)."/../"); 
define('IMG_CAPTURE_PATH', MY_WEB_DIR.'capture/'); 

//DB설정#1
define("DBTYPE1", "mysql");
define("DBNAME1", "uptimemini");
define("DBHOST1", "localhost");
define("DBUSER1", "root");
define("DBPASS1", "");

$dbtype1 = DBTYPE1; $dbname1 = DBNAME1; $dbhost1 = DBHOST1; $dbuser1 = DBUSER1; $dbpass1 = DBPASS1;

//MySQL 접속
try {
    $dsn = "{$dbtype1}:host={$dbhost1};dbname={$dbname1}";
    $pdo = new PDO($dsn,$dbuser1,$dbpass1);
} catch (PDOException $e) {
    print "Error!: " . $e->getMessage();
    die();
}


//라이브러리 경로
require 'vendor/autoload.php';
$smarty = new Smarty();
$smarty->error_reporting = E_ALL & ~E_NOTICE;

//Smarty 객체 생성 및 경로 설정
$smarty->setTemplateDir(MY_WEB_DIR. '/smarty/templates/');
$smarty->setCompileDir( MY_WEB_DIR. '/smarty/templates_c/');
$smarty->setConfigDir(  MY_WEB_DIR. '/smarty/config/');
$smarty->setCacheDir(   MY_WEB_DIR. '/smarty/cache/');
$smarty->setCacheDir(   MY_WEB_DIR. '/smarty/cache/');


require_once(dirname(__FILE__).'/library.php');

?>