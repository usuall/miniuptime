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
