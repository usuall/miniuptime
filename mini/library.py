from mini.config import get_Config
import mini.model as model
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import time
import urllib3
import requests
from loguru import logger
import sys
from image_match.goldberg import ImageSignature


# 환경 설정값 취득
properties = get_Config()
config_sys = properties['SYSTEM']
config_log = properties['LOG']
config_db = properties['DATABASE']

# 각종 디렉토리 경로 지정
project_path = os.path.abspath(os.getcwd()) + '\\'
lib_path = project_path + config_sys['LIB_PATH'] + '\\'  # 라이브러리 경로
data_path = project_path + config_sys['DATA_PATH'] + '\\' 
img_path = data_path + config_sys['IMG_PATH'] + '\\'   # screenshot 경로
img_origin_path = img_path + '\\' + config_sys['IMG_ORIGIN_PATH'] + '\\'
img_daily_path = img_path + '\\' + config_sys['IMG_DAILY_PATH'] + '\\'
img_resize_path = img_path + '\\' + config_sys['IMG_RESIZE_PATH'] + '\\'
html_path = data_path + config_sys['HTML_PATH'] + '\\'     # html 경로
logs_path = data_path + config_sys['LOGS_PATH'] + '\\'     # 각종로그 경로

# 실행환경
user_agent = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'

# 각종 로그 출력 설정
LOG_rotation = config_sys['LOG_ROTATION']
LOG_retention = int(config_sys['LOG_RETENTION'])
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add(logs_path + "uptime.log", rotation=LOG_rotation, retention=LOG_retention ) # rotation='100 MB' (로그 사이즈), retantion=10 (10세대분 보유)
logger.add(logs_path + "uptime_err.log", rotation=LOG_rotation, retention=LOG_retention, level='WARNING')  # rotation='100 MB' (로그 사이즈), retantion=10 (10세대분 보유), level=로그레벨

logger.info('<SYSTEM> Init ------------------------- ')
logger.info('<SYSTEM> LIBRARY PATH : ' + lib_path)
logger.info('<SYSTEM> DATA PATH : ' + data_path)
logger.info('<SYSTEM> IMG PATH : ' + img_path)
logger.info('<SYSTEM> HTML PATH : ' + html_path)
logger.info('<SYSTEM> LOGS PATH : ' + logs_path)
logger.info('<SYSTEM> LOG_ROTATION : ' + config_sys['LOG_ROTATION'])
logger.info('<SYSTEM> LOG_RETENTION : ' + config_sys['LOG_RETENTION'])

#현재시각
def get_sysdate():
    sysdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(sysdate)


def before_main():
    
    # 저장 디렉토리 존재 확인
    isExist_dir(data_path)
    isExist_dir(img_path)
    isExist_dir(img_origin_path)
    isExist_dir(img_daily_path)
    isExist_dir(img_resize_path)
    isExist_dir(html_path)
    isExist_dir(logs_path)

    
def isExist_dir(path):    
    isExist = os.path.exists(path)
    if(isExist == False):
        os.makedirs(path)
        
def button_activate(window, activate):
    
    # 화면 요소ID
    obj_list = ('-GRP_LIST-', '-TIMEOUT1-', '-TIMEOUT2-', '-TIMEOUT3-', '-TIMEOUT4-', '-TIMEOUT5-', '-TIMEOUT6-', '-DISABLED-', '-SITE_TITLE-', '-SITE_URL-', '-REPEAT-', '-BG_EXE-', '-BUTTON_START-')
    #obj_list = ('-GRP_LIST-', '-TIMEOUT1-', '-TIMEOUT2-', '-TIMEOUT3-', '-TIMEOUT4-', '-TIMEOUT5-', '-TIMEOUT6-', '-DISABLED-', '-SITE_TITLE-', '-SITE_URL-', '-REPEAT-', '-BG_EXE-', '-BUTTON_START-', '-BUTTON_EXIT-')
    
    # 버튼 활성화 전환
    if activate == 0:
        window['-OUTPUT-'].update(value='', append=False)
        window['-BUTTON_STOP-'].update(disabled=False)
        for key in obj_list:
            window[key].update(disabled=True)
    else:
        window['-BUTTON_STOP-'].update(disabled=True)
        for key in obj_list:
            window[key].update(disabled=False)
            
            

# 검색 조건 확인
def getCondition(window, values):

    if(values['-TIMEOUT1-'] == True ):
        timeout_term = 5
    elif(values['-TIMEOUT2-'] == True ):
        timeout_term = 10
    elif(values['-TIMEOUT3-'] == True ):
        timeout_term = 15
    elif(values['-TIMEOUT4-'] == True ):
        timeout_term = 20
    elif(values['-TIMEOUT5-'] == True ):
        timeout_term = 25
    elif(values['-TIMEOUT6-'] == True ):
        timeout_term = 30
    else:
        timeout_term = 12

    # window['-OUTPUT-'].update(value='- 실행시간 : ' + str1 + '\n', append=True)
    window['-OUTPUT-'].update(value='--------- <검색조건> ---------\n', append=True)
    window['-OUTPUT-'].update(value='- 카테고리 : ' + values['-GRP_LIST-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- 사이트명 : ' + values['-SITE_TITLE-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- URL명 : ' + values['-SITE_URL-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- 반복 점검 : ' + str(values['-REPEAT-']) + '\n', append=True)
    window['-OUTPUT-'].update(value='- 비활성화 URL포함. : ' + str(values['-DISABLED-']) + '\n', append=True)
    window['-OUTPUT-'].update(value='- 백그라운드 실행 : ' + str(values['-BG_EXE-']) + '\n', append=True)
    window['-OUTPUT-'].update(value='- 타임아웃 설정 : ' + str(timeout_term) + '초\n', append=True)
    # window['-OUTPUT-'].update(value='-------------------------------------------\n', append=True)

    #검색 조건 저장
    keyword = { 'GRP_LIST':     values['-GRP_LIST-'], 
                'SITE_TITLE':   values['-SITE_TITLE-'], 
                'SITE_URL':     values['-SITE_URL-'], 
                'REPEAT':       values['-REPEAT-'], 
                'DISABLED':     values['-DISABLED-'], 
                'BG_EXE':       values['-BG_EXE-'], 
                'TIME_OUT':     timeout_term }
    
    logger.info('--------- <모니터링 시작> ---------')
    logger.info('카테고리 : ' + values['-GRP_LIST-'])
    logger.info('사이트명 : ' + values['-SITE_TITLE-'])
    logger.info('URL명 : ' + values['-SITE_URL-'])
    logger.info('반복 점검 : ' + str(values['-REPEAT-']))
    logger.info('비활성화 URL포함. : ' + str(values['-DISABLED-']))
    logger.info('백그라운드 실행 : ' + str(values['-BG_EXE-']))
    logger.info('타임아웃 설정 : ' + str(timeout_term) + '초')

    # for k in keyword.values():
    #     print('>>>',k)

    return keyword


#기관단위 모니터링
def get_monitoring(window, keyword):    
    
    global _step_
    
    
    stime = time.time()
    # 브라우저 환경 설정 취득
    bg_exec = keyword.get('BG_EXE') # 백그라운드 실행
    driver = set_browser_option(bg_exec)
        
    cnt = 0    
    result = model.get_grp_url_list(keyword)
    # print('resutl ',type(result), len(result))
    total_cnt = len(result) # 조회 건수
    logger.info('☞  조회결과 : '+ str(total_cnt) + '건')
    window['-OUTPUT-'].update(value='☞ 조회결과 : '+ str(total_cnt) +'건\n', append=True)
    window['-OUTPUT-'].update(value='------------------------------\n', append=True)
    
    total_step = 8
    for row in result:
        cnt += 1
        _step_ = 0
        
        tb_url = {}
        tb_monitor = {}
        
        window['-OUTPUT-'].update(value='\n', append=True)
        window.refresh() 
        
        pertime = time.time() # 개별작업시간
        # 작업시간 출력
        logger.info('---- URL Health Check Start' + ' ['+ str(cnt) + '/' + str(total_cnt) + '] ----')
        str1 = '[' + get_sysdate() + '] ['+ str(cnt) + '/' + str(total_cnt) + '] ' + row['url_addr'] + ' (NO:' + str(row['url_no'])  +')\n'
        window['-OUTPUT-'].update(value=str1, append=True)
        window.refresh() 

        # 브라우져 URL 탐색
        web_url = row['url_type']+row['url_addr']
        
        #브라우져 무한로딩시 timeout 으로 회피(jnpolice.go.kr 사례) / 해결하는데 5일 걸림
        get_url_timout = keyword.get('TIME_OUT') #디폴트 10초
        driver.set_page_load_timeout(get_url_timout)
        outtime = time.time()
        
        logger.info(step_add(total_step) + 'URL_GET(1/2) ' + web_url + diff_time(outtime))
        try:
            driver.get(web_url)
            logger.info(step_add(total_step) + 'URL_GET(2/2) '+ 'URL Loading'+ diff_time(outtime))
        except TimeoutException as e:
            logger.exception('URL_GET / time_out exception : '+ web_url)
            pass
        except Exception as e:  # 기타 오류 발생시 처리 정지
            logger.exception('URL_GET Exception Occured : '+ str(e))
            break
        
        redirected_url = driver.current_url
        
        
        #logger.info(step_add(total_step) + 'URL redirected : '+ redirected_url+ ' ('+ str(round(time.time()-pertime, 2))+'s)')
        logger.info(step_add(total_step) + 'URL redirected : '+ redirected_url + diff_time(pertime))
        window['-OUTPUT-'].update(value=' Redirected → '+redirected_url + diff_time(pertime), append=True)
        # print('redirected -->', driver.current_url)
        window.refresh() # 작업내용 출력 반영        
        
        # 이미지 캡쳐 (브라우져 크기 설정후 캡쳐 사이즈 지정 필요)
        # redirect 된 url로 이미지 캡쳐 필요
        #img_str = str(row['url_no'])+ "__" + row['url_addr'] + ".png"
        img_str = str(row['url_no'])+ "_site.png"
        time.sleep(2) # 화면캡쳐 전 2초대기
        
        # 화면 캡쳐
        try:
            driver.save_screenshot(img_daily_path + img_str)
        except TimeoutException as e:
            logger.warning('Screenshot Timout')
            pass    
        except Exception as e:  # 기타 오류 발생시 처리 정지
            logger.critical('SCREENSHOT Exception Occured : '+ str(e))
            break
        
        logger.info(step_add(total_step) + 'Screenshot' + diff_time(pertime))

        # origin_img = img_origin_path + img_str
        # new_img = img_daily_path + img_str
        
        origin_img = img_str
        new_img = img_str

        img_matching_point = image_match(origin_img, new_img)
        if(img_matching_point == -99.99):
            logger.info(step_add(total_step) + 'image_match skipped(file is not exist.) ' + diff_time(pertime))
        else:
            if(img_matching_point < 0.4):
                img_match = '(OK) '
            else:
                img_match = '(NG) '
            logger.info(step_add(total_step) + 'image_match '+ img_match + str(round(img_matching_point,3)) + diff_time(pertime))
        

        window['-OUTPUT-'].update(value=' → captured'+ diff_time(pertime), append=True)
        window.refresh() 
        #html 소스코드 취득
        html_source = driver.page_source # redirected 최종 URL의 소스를 취득
        #window['-OUTPUT-'].update(value=' redirected2 -> '+ driver.current_url, append=True)
        #print(html_source)
        # window['-OUTPUT-'].update(value='11111-------------------------------------------\n', append=True)
        # window['-OUTPUT-'].update(value=html_source, append=True)
        
        #로그를 보기좋게 정리(prettfy)
        html_source = BeautifulSoup(html_source, 'html.parser').prettify
        # log_output(html_source )
        
        #html 저장
        html_file = save_html(row['url_no'], row['url_no'], html_source)
        logger.info(step_add(total_step) + 'HTML Save'+ diff_time(pertime))
        window['-OUTPUT-'].update(value=' → html' + diff_time(pertime), append=True)
        window.refresh()
        
        # Request Code 취득 : (200 : ok, 404 : page not found)
        req_code = get_request_code(redirected_url)
        logger.info(step_add(total_step) + 'Status : '+ str(req_code) + diff_time(pertime))
        
        t_color='#333333'
        if(req_code != 200):
            t_color='Red'
        # http Status code 
        window['-OUTPUT-'].update(value='→ Status ' + str(req_code) + diff_time(pertime), append=True, text_color_for_value=t_color)
        window.refresh()

        # 새창 닫기
        close_new_tabs(driver)
        logger.info(step_add(total_step) + 'New Tab Closed' + diff_time(pertime))
        window['-OUTPUT-'].update(value=' → Tab', append=True)
        window['-OUTPUT-'].update(value=' ('+str(round(time.time()-pertime, 2)) + 's)', append=True)        
        window['-OUTPUT-'].update(value='\n', append=True)
        window.refresh() # 작업내용 출력 반영

        img_matching_point = image_match( img_str , img_str) # 이미지 유사도
        
        tb_monitor['url_no'] = row['url_no']
        tb_monitor['status_code'] = req_code
        tb_monitor['html_file'] = html_file
        tb_monitor['mon_image'] = img_str   # img_daily_path + img_str
        tb_monitor['mon_img_match1'] = img_matching_point
        # tb_monitor['mon_html_match1'] = 

        tb_url['url_no'] = row['url_no']
        tb_url['url_redirected'] = redirected_url
        tb_url['url_status'] = req_code

        
        
        
        #모니터링 데이터 DB(TB_MONITOR)
        model.add_monitoring(tb_monitor)
        
        #모니터링 데이터 DB(TB_URL)
        model.update_url_monitoring(tb_url)
        
        # logger.info('>>>>>>1111 ')
        # for key, value in tb_url.items():
        #     logger.info('>>>>>> ' + key + str(value))
        # logger.info('>>>>>>2222 ')  
        
    if(cnt > 0):
        endtime = time.time()
        window['-OUTPUT-'].update(value='-------------------------------------------\n', append=True)
        window['-OUTPUT-'].update(value='▶ (처리 URL) ' + str(cnt) +'건, (처리시간) '+ str(round(endtime-stime, 2)) + '초, (평균처리 시간) '+ str(round((endtime-stime)/cnt,2)) +'초 \n', append=True)
    else:
        window['-OUTPUT-'].update(value='▶ 검색 결과 없음', append=True)
    
    # 작업 종료후 버튼 활성화
    button_activate(window, 1)

      
    #처리건수 리턴
    return cnt

# 브라우저 기본 설정
def set_browser_option(bg_exec):
    
    # print ('bg_exec ',bg_exec)
    # 크롬 브라우저 오픈
    options = webdriver.ChromeOptions()
    # USER_Agent 지정
    options.add_argument(user_agent)
    options.add_argument("disable-gpu")
    # '시스템에 부착된 장치가 작동하지 않습니다' 오류 제거
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # 브라우져 창 최소화 유무
    if (bg_exec == True):
        # 백그라운드 실행
        options.add_argument('--window-size=1900,1080')
        options.add_argument("--headless")
        # options.headless = True

    else:
        # driver.set_window_size(1920, 1080)
        options.add_argument("--start-maximized")
    
    # 브라우져 옵션 설정
    # driver = webdriver.Chrome(lib_path + 'chromedriver.exe', options=options) # deprecated option
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 명시적으로 대기(10초) 
    driver.implicitly_wait(time_to_wait=10)
    
    # InsecureRequestWarning  메시지 제거
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    return driver

def my_grp_list_combo():
    
    grp_list = ['전 체']
    result = model.get_grp_list()
    
    # # DB조회결과 없는 경우
    # if( type(result) != 'list'):
    #     return False
    
    for row in result:
        #org_list.append(row['org_title']+'['+row['org_no']+']')
        grp_list.append(row['grp_title'])

    return grp_list

@logger.catch 
def save_html(url_no, mon_no, src_text):
    
    sysdate = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    # print(html_path + str(url_no)+'_'+str(sysdate)+'.html')
    html_file = str(url_no)+'_'+str(sysdate)+'.html'
    full_path_name = html_path + html_file
    # print(full_path_name)
    
    f = open(full_path_name, 'w', encoding='UTF-8')
    # print(type(src_text))
    f.write(str(src_text))
    f.close()

    return html_file
    # DB insert

@logger.catch    
def get_request_code(web_url):
    status = None
    try:
        response = requests.get(web_url, verify=False) # verify=False (SSLerror 오류 발생 회피)
        status = response.status_code
    except:
        pass

    return status

# 새창 뜨는 경우 닫기 기능
def close_new_tabs(driver):
    tabs = driver.window_handles
    while len(tabs) != 1:
        driver.switch_to.window(tabs[1])
        driver.close()
        tabs = driver.window_handles
    driver.switch_to.window(tabs[0])
    
def step_add(_total_):
    global _step_
    _step_ += 1
    return '[' + str(_step_) + '/' + str(_total_) + '] '



def diff_time(pertime, type = 0):
    if(type == 0):
        return ' (' + str(round(time.time()-pertime, 2))+'s)'
    else:
        return ' (' + str(round(time.time()-pertime, 2))+'s)/n'
    
# 이미지 유사도 체크    
def image_match(origin_img, new_img):

    # logger.info('origin_img --> ' + img_origin_path + origin_img)
    # logger.info('new_img --> ' + img_daily_path + new_img)
    file1 = img_origin_path + origin_img 
    file2 = img_daily_path + new_img
    
    gis = ImageSignature()
    
    if os.path.isfile(file1) and os.path.isfile(file2):
        a = gis.generate_signature(file1)
        b = gis.generate_signature(file2)
    
        result = gis.normalized_distance(a, b)
        return result
    else:
        logger.info('images_match skipped')
        result = -99.99
        return result