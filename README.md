"# uptime mini" 
-----------------
## python 가상환경 생성
python -m venv .venv

## into the python env
$PROJECT_HOME/.venv/Scripts/activate

### pip upgrade
python -m pip install --upgrade pip
 
### image-match install
git clone https://github.com/ascribe/image-match.git

cd image-match  
pip install numpy  
pip install scipy  
pip install .  

### html-similarity 설치
pip install html-similarity  

-------------------------
### 크롬 드라이버 다운로드
https://chromedriver.chromium.org/downloads

### 관련 패키지 설치
pip install PySimpleGUI  
pip install pymysql  
pip install selenium  
pip install requests  
pip install pillow  
pip install webdriver-manager  
pip install urllib3  
pip install BeautifulSoup4  
pip install loguru  


### optional
pip install opencv-python  
pip install gtts  
pip install playsound  



ALTER TABLE `tb_url` ADD `url_html_diff_output` VARCHAR(255) NULL AFTER `url_html_match2`;  
ALTER TABLE `tb_url` DROP `url_type`;  
ALTER TABLE `tb_monitor` ADD `mon_html_diff_time` FLOAT NOT NULL COMMENT 'html 비교 소요시간' AFTER `mon_html_diff_output`;  
ALTER TABLE `tb_monitor` CHANGE `mon_html_diff_output` `mon_html_diff_output` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL;



-- URL 이상 있는 기관
SELECT b.grp_title, count(*) as cnt FROM `tb_url` as a
left outer join tb_group as b
on a.grp_no = b.grp_no
where a.url_status <> 200
and (a.url_img_match1 <= 60 
	 or a.url_html_match1 <= 60)
group by a.grp_no;


-- 이상 있는 URL
SELECT b.grp_title, a.url_no, a.url_title, a.url_addr, a.url_status, a.url_img_match1, a.url_html_match1 
FROM `tb_url` as a
left outer join tb_group as b
on a.grp_no = b.grp_no
WHERE 1=1 
and (a.url_status <> 200 or a.url_status is NULL)
and (a.url_img_match1 <= 60 or a.url_html_match1 <= 60);

-- 응답시간 5초 이상
SELECT * FROM `tb_url` 
where url_response_time >= 5 
order by url_response_time 
desc limit 100;


-- 평균 응답시간 느린순으로 표시
SELECT url_no, round(AVG(mon_response_time),3) as avg FROM `tb_monitor`
group by url_no
order by avg desc;

-- 평균 응답시간 느린순으로 표시(기관, title 표시)
SELECT c.grp_title, b.url_title, b.url_addr, a.url_no, round(AVG(mon_response_time),3) as avg 
FROM `tb_monitor` as a
left outer join tb_url as b
on a.url_no = b.url_no
left outer join tb_group as c
on b.grp_no = c.grp_no
group by a.url_no
order by avg desc;

-- HTML 비교 느린 것 찾기
SELECT c.grp_short_title, b.url_title, a.url_no, mon_response_time, status_code, mon_html_diff_time 
FROM `tb_monitor` as a
left outer join tb_url as b
on a.url_no = b.url_no
left outer join tb_group as c
on b.grp_no = c.grp_no
ORDER BY a.mon_html_diff_time DESC
limit 30;


# (Selenium) Bypass “Your connection is not private” Message
https://stackoverflow.com/questions/60247155/how-to-bypass-the-message-your-connection-is-not-private-on-non-secure-page-us


ALTER TABLE `tb_url` ADD `url_ssl_start_dt` DATETIME NULL AFTER `url_redirected`, ADD `url_ssl_end_dt` DATETIME NULL AFTER `ssl_start_dt`;


CREATE TABLE `tb_domain` (
  `url_no` int(10) NOT NULL,
  `check_date` datetime DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  `issued_to` varchar(255) DEFAULT NULL,
  `issued_o` varchar(255) DEFAULT NULL,
  `issuer_c` varchar(100) DEFAULT NULL,
  `issuer_o` varchar(255) DEFAULT NULL,
  `issuer_ou` varchar(200) DEFAULT NULL,
  `issuer_cn` varchar(255) DEFAULT NULL,
  `cert_sn` varchar(255) DEFAULT NULL,
  `cert_sha1` varchar(255) DEFAULT NULL,
  `cert_alg` int(255) DEFAULT NULL,
  `cert_ver` int(255) DEFAULT NULL,
  `cert_sans` varchar(255) DEFAULT NULL,
  `cert_exp` varchar(255) DEFAULT NULL,
  `cert_valid` int(255) DEFAULT NULL,
  `valid_from` date DEFAULT NULL,
  `valid_till` date DEFAULT NULL,
  `validity_days` int(4) DEFAULT NULL,
  `days_left` int(4) DEFAULT NULL,
  `valid_days_to_expire` int(4) DEFAULT NULL,
  `tcp_port` int(4) DEFAULT NULL,
  `domain_name` varchar(255) DEFAULT NULL COMMENT '도메인 정보',
  `creation_date` datetime DEFAULT NULL COMMENT '도메인 생성일',
  `updated_date` datetime DEFAULT NULL COMMENT '도메인 갱신일',
  `expiration_date` datetime DEFAULT NULL COMMENT '도메인 만료일',
  `name_servers` varchar(255) DEFAULT NULL COMMENT 'dns 서버'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `tb_domain` ADD PRIMARY KEY (`url_no`);


CREATE TABLE `tb_url` (
  `url_no` int(12) NOT NULL COMMENT 'url 번호',
  `grp_no` int(4) NOT NULL COMMENT '그룹_번호',
  `url_title` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT 'URL 제목',
  `url_addr` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT 'URL 주소',
  `url_redirected` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '최종 URL 주소',
  `url_response_time` float DEFAULT NULL COMMENT 'url 길이',
  `url_status` int(1) DEFAULT 0 COMMENT '사이트 최종 상태(online=1, offline=0)',
  `url_lastest_check_dt` datetime DEFAULT NULL COMMENT '최종 점검일시',
  `url_img_match1` float DEFAULT NULL COMMENT '이미지 유사도 허용치',
  `url_img_match2` float DEFAULT NULL COMMENT '이미지 유사도 허용치2',
  `url_html_match1` float DEFAULT NULL COMMENT 'html 유사도 허용치',
  `url_html_match2` float DEFAULT NULL COMMENT 'html 유사도 허용치2',
  `url_html_diff_output` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `option_delay_seconds` int(1) NOT NULL DEFAULT 2,
  `option_javascript_disabled` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'javascript disable',
  `option_browser_bg_execute` tinyint(1) NOT NULL DEFAULT 1 COMMENT 'browser background execute',
  `option_browser_width` int(2) DEFAULT 0 COMMENT 'browser width size',
  `option_browser_height` int(2) DEFAULT 0 COMMENT 'browser height size',
  `url_fg` tinyint(1) NOT NULL DEFAULT 1 COMMENT 'url 사용유무(0=미사용, 1=사용)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE `tb_url` ADD PRIMARY KEY (`url_no`);
ALTER TABLE `tb_url` MODIFY `url_no` int(12) NOT NULL AUTO_INCREMENT COMMENT 'url 번호', AUTO_INCREMENT=1;



# todo list
- selenium full screenshot 이미지 깨짐 현상 개선
- url 점검시 매번 해당 url의 특성에 따라 selenium 실행(옵션 기능)
- url 점검시 javacript 비활성화 옵션으로 접속 
- selenium driver 창 안뜨게 하기 (22.09.16 완료)
  https://sijoo.tistory.com/409

# 개별 URL 테스트
- 숲나들e (252) backgroud 실행시 404로 처리됨. foreground 실행시 정상관제


