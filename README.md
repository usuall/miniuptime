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
pip install gtts  
pip install playsound  
