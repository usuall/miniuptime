from tabnanny import process_tokens
from mini.config import get_Config
import mini.model as model
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import time
import urllib3
import requests
from loguru import logger
import sys
from image_match.goldberg import ImageSignature
from PIL import Image
from html_similarity import style_similarity, structural_similarity, similarity   # 소스 유사도 검사
from pathlib import Path
from difflib import HtmlDiff


# 환경 설정값 취득
properties = get_Config()
config_sys = properties['SYSTEM']
config_log = properties['LOG']
config_db = properties['DATABASE']

# 각종 디렉토리 경로 지정
project_path = os.path.abspath(os.getcwd()) + '\\'
lib_path = project_path + config_sys['LIB_PATH'] + '\\'  # 라이브러리 경로
data_path = project_path + config_sys['DATA_PATH'] + '\\' 
web_path = data_path + config_sys['WEB_PATH'] + '\\'   # apache_htdocs 경로
img_path = web_path + config_sys['IMG_PATH'] + '\\'   # screenshot 경로
img_origin_path = img_path + '\\' + config_sys['IMG_ORIGIN_PATH'] + '\\'
img_daily_path = img_path + '\\' + config_sys['IMG_DAILY_PATH'] + '\\'
img_diff_path = img_path + '\\' + config_sys['IMG_DIFF_PATH'] + '\\'

html_path = data_path + config_sys['HTML_PATH'] + '\\'     # html 경로
logs_path = data_path + config_sys['LOGS_PATH'] + '\\'     # 각종로그 경로
html_origin_path = html_path + config_sys['HTML_ORIGIN_PATH'] + '\\'
html_daily_path = html_path + config_sys['HTML_DAILY_PATH'] + '\\'
html_diff_path = web_path + config_sys['HTML_DIFF_PATH'] + '\\'
skip_unchanged = config_sys['HTML_DIFF_SKIP_UNCHANGED']
set_delete_days = config_sys['SET_DELETE_DAYS']
remain_file_cnt = config_sys['REMAIN_FILE_CNT']
unit_cnt = config_sys['UNIT_CNT']


# 실행환경
user_agent = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'

at_now = datetime.now().strftime('%y%m%d_%H%M%S')

# 각종 로그 출력 설정
LOG_rotation = config_sys['LOG_ROTATION']
LOG_retention = int(config_sys['LOG_RETENTION'])
# logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
# logger.add(logs_path + "uptime_" + at_now + ".log", rotation=LOG_rotation, retention=LOG_retention ) # rotation='100 MB' (로그 사이즈), retantion=10 (10세대분 보유)
# logger.add(logs_path + "uptime_err_" + at_now + ".log", rotation=LOG_rotation, retention=LOG_retention, level='WARNING')  # rotation='100 MB' (로그 사이즈), retantion=10 (10세대분 보유), level=로그레벨

# logger.info('<SYSTEM> Init ------------------------- ')
# logger.info('<SYSTEM> LIBRARY PATH : ' + lib_path)
# logger.info('<SYSTEM> DATA PATH : ' + data_path)
# logger.info('<SYSTEM> IMG PATH : ' + img_path)
# logger.info('<SYSTEM> HTML PATH : ' + html_path)
# logger.info('<SYSTEM> LOGS PATH : ' + logs_path)
# logger.info('<SYSTEM> LOG_ROTATION : ' + config_sys['LOG_ROTATION'])
# logger.info('<SYSTEM> LOG_RETENTION : ' + config_sys['LOG_RETENTION'])

#현재시각
def get_sysdate():
    sysdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(sysdate)


def before_main():
    
    # 저장 디렉토리 존재 확인 및 생성
    isExist_dir(data_path)
    isExist_dir(web_path)
    isExist_dir(img_path)
    isExist_dir(img_origin_path)
    isExist_dir(img_daily_path)
    isExist_dir(img_diff_path)     
    isExist_dir(html_path)
    isExist_dir(html_origin_path)
    isExist_dir(html_daily_path)
    isExist_dir(html_diff_path)
    isExist_dir(logs_path)
    
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    logger.add(logs_path + "uptime_" + at_now + ".log", rotation=LOG_rotation, retention=LOG_retention ) # rotation='100 MB' (로그 사이즈), retantion=10 (10세대분 보유)
    logger.add(logs_path + "uptime_err_" + at_now + ".log", rotation=LOG_rotation, retention=LOG_retention, level='WARNING')  # rotation='100 MB' (로그 사이즈), retantion=10 (10세대분 보유), level=로그레벨

    logger.info('<SYSTEM> Init ------------------------- ')
    logger.info('<SYSTEM> LIBRARY PATH : ' + lib_path)
    logger.info('<SYSTEM> DATA PATH : ' + data_path)
    logger.info('<SYSTEM> IMG PATH : ' + img_path)
    logger.info('<SYSTEM> HTML PATH : ' + html_path)
    logger.info('<SYSTEM> LOGS PATH : ' + logs_path)
    logger.info('<SYSTEM> LOG_ROTATION : ' + config_sys['LOG_ROTATION'])
    logger.info('<SYSTEM> LOG_RETENTION : ' + config_sys['LOG_RETENTION'])
    

    
def isExist_dir(path):    
    isExist = os.path.exists(path)
    if(isExist == False):
        os.makedirs(path)
        
def button_activate(window, activate):
    
    # 화면 요소ID
    obj_list = ('-GRP_LIST-', '-DISABLED-', '-URL_LIST-', '-URL_NO-', '-SITE_TITLE-', '-SITE_URL-', '-REPEAT-', '-ERROR_URL-', '-BUTTON_START-', '-RANDOM-')
    #obj_list = ('-GRP_LIST-', '-TIMEOUT1-', '-TIMEOUT2-', '-TIMEOUT3-', '-TIMEOUT4-', '-TIMEOUT5-', '-TIMEOUT6-', '-DISABLED-', '-URL_LIST-', '-URL_NO-', '-SITE_TITLE-', '-SITE_URL-', '-REPEAT-', '-ERROR_URL-', '-BUTTON_START-', '-RANDOM-')
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

    # if(values['-TIMEOUT1-'] == True ):
    #     timeout_term = 5
    # elif(values['-TIMEOUT2-'] == True ):
    #     timeout_term = 10
    # elif(values['-TIMEOUT3-'] == True ):
    #     timeout_term = 15
    # elif(values['-TIMEOUT4-'] == True ):
    #     timeout_term = 20
    # elif(values['-TIMEOUT5-'] == True ):
    #     timeout_term = 25
    # elif(values['-TIMEOUT6-'] == True ):
    #     timeout_term = 30
    # else:
    #     timeout_term = 12
        
    timeout_term = 12

    # window['-OUTPUT-'].update(value='- 실행시간 : ' + str1 + '\n', append=True)
    window['-OUTPUT-'].update(value='--------- <검색조건> ---------\n', append=True)
    window['-OUTPUT-'].update(value='- 카테고리 : ' + values['-GRP_LIST-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- URL범위 : ' + values['-URL_LIST-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- URL번호 : ' + values['-URL_NO-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- 사이트명 : ' + values['-SITE_TITLE-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- URL명 : ' + values['-SITE_URL-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- 반복 점검 : ' + str(values['-REPEAT-']) + '\n', append=True)
    window['-OUTPUT-'].update(value='- 비활성화 URL포함. : ' + str(values['-DISABLED-']) + '\n', append=True)
    #window['-OUTPUT-'].update(value='- 백그라운드 실행 : ' + str(values['-BG_EXE-']) + '\n', append=True)
    window['-OUTPUT-'].update(value='- 랜덤 실행 : ' + str(values['-RANDOM-']) + '\n', append=True)    
    #window['-OUTPUT-'].update(value='- OLD 체크 : ' + str(values['-OLDEST-']) + '\n', append=True)    
    # window['-OUTPUT-'].update(value='- 이미지 유사도 검증 : ' + str(values['-IMAGE_MATCH-']) + '\n', append=True)
    # window['-OUTPUT-'].update(value='- HTML 유사도 검증 : ' + str(values['-HTML_MATCH-']) + '\n', append=True)
    window['-OUTPUT-'].update(value='- ERROR URL 검사 : ' + str(values['-ERROR_URL-']) + '\n', append=True)
    window['-OUTPUT-'].update(value='- 타임아웃 설정 : ' + str(timeout_term) + '초\n', append=True)
    # window['-OUTPUT-'].update(value='-------------------------------------------\n', append=True)

    #검색 조건 저장
    keyword = { 'GRP_LIST':     values['-GRP_LIST-'], 
                'URL_LIST':     values['-URL_LIST-'], 
                'URL_NO':       values['-URL_NO-'], 
                'SITE_TITLE':   values['-SITE_TITLE-'], 
                'SITE_URL':     values['-SITE_URL-'], 
                'REPEAT':       values['-REPEAT-'], 
                'DISABLED':     values['-DISABLED-'], 
                #'BG_EXE':       values['-BG_EXE-'],
                'RANDOM':       values['-RANDOM-'],
                #'OLDEST':       values['-OLDEST-'],
                # 'IMAGE_MATCH':  values['-IMAGE_MATCH-'], 
                # 'HTML_MATCH':   values['-HTML_MATCH-'], 
                'ERROR_URL':    values['-ERROR_URL-'], 
                'TIME_OUT':     timeout_term }
    
    logger.info('--------- <모니터링 시작> ---------')
    logger.info('카테고리 : ' + values['-GRP_LIST-'])
    logger.info('URL범위 : ' + values['-URL_LIST-'])
    logger.info('URL번호 : ' + values['-URL_NO-'])
    logger.info('사이트명 : ' + values['-SITE_TITLE-'])
    logger.info('URL명 : ' + values['-SITE_URL-'])
    logger.info('반복 점검 : ' + str(values['-REPEAT-']))
    logger.info('비활성화 URL포함. : ' + str(values['-DISABLED-']))
    logger.info('백그라운드 실행 : ' + str(values['-RANDOM-']))
    #logger.info('OLD 체크 실행 : ' + str(values['-OLDEST-']))
    # logger.info('이미지 유사도 검증 : ' + str(values['-IMAGE_MATCH-']))
    # logger.info('HTML 유사도 검증 : ' + str(values['-HTML_MATCH-']))
    logger.info('ERROR URL 검사 : ' + str(values['-ERROR_URL-']))
    logger.info('타임아웃 설정 : ' + str(timeout_term) + '초')

    # for k in keyword.values():
    #     print('>>>',k)

    return keyword


# 검색결과 모니터링
def get_monitoring(window, keyword):    
    
    global driver
    global _step_
    global html_output
    global process_stop
     
    stime = time.time()
        
    cnt = 0    
    result = model.get_grp_url_list(keyword)
    window['-OUTPUT-'].update(value='- 조회시간 : ' + get_sysdate() +'\n', append=True)

    # print('resutl ',type(result), len(result))
    total_cnt = len(result) # 조회 건수
    logger.info('☞  조회결과 : '+ str(total_cnt) + '건')
    window['-OUTPUT-'].update(value='☞ 조회결과 : '+ str(total_cnt) +'건\n', append=True)
    window['-OUTPUT-'].update(value='------------------------------\n', append=True)
    
    # 조회결과가 있을때만 브라우져 기동
    if(total_cnt > 0):
        # 브라우저 환경 설정 취득
        BG_EXE = keyword.get('BG_EXE') # 백그라운드 실행
        # driver = set_browser_option(BG_EXE)
    
    total_step = 8
    process_stop = False
    for row in result:
        
        # window['-TIMESTAMP-'].update(value=get_sysdate(), append=False)
        window['-TIMESTAMP-'].update(get_sysdate())
        
        # 사이트별 브라우져 설정 읽기
        driver = set_browser_option_url(browser_option=row)
        
        if(process_stop == True):
            return 
        
        cnt += 1
        _step_ = 0
        
        tb_url = {}
        tb_monitor = {}
        
        window['-OUTPUT-'].update(value='\n', append=True)
        window.refresh() 
        
        pertime = time.time() # 개별작업시간
        # 작업시간 출력
        logger.info('---- URL Health Check Start' + ' ['+ str(cnt) + '/' + str(total_cnt) + '] ----')
        str1 = '[' + get_sysdate() + ']\n['+ str(cnt) + '/' + str(total_cnt) + '] ' + row['url_addr'] + ' (NO:' + str(row['url_no'])  +')'
        window['-OUTPUT-'].update(value=str1+'\n', append=True)
        window.refresh() 

        # 브라우져 URL 탐색
        # web_url = row['url_type']+row['url_addr']
        web_url = row['url_addr']
        
        # 브라우져 무한로딩시 timeout 회피(jnpolice.go.kr 사례) / 해결하는데 5일 걸림
        TIME_OUT = keyword.get('TIME_OUT') #디폴트 10초
        driver.set_page_load_timeout(TIME_OUT)
        outtime = time.time()
        
        logger.info(step_add(total_step) + 'URL_GET(1/2) ' + web_url + diff_time(outtime))
        try:
            driver.get(web_url)
            
            # 응답시간 취득 
            # domComplete 시간이 취득안되는 경우가 있어 보류
            # resp_time = getResponseTime(driver)
            
            
            
            #브라우져 비율 조정(이미지 사이즈 다운)
            # driver.execute_script("document.body.style.zoom='80%'")            
            
            # c1 = driver.find_elements(By.CSS_SELECTOR("input[type='checkbox']"))
            # c2 = c1.count()
            # print ('checkbox --> ', c1, c2)
            
            try:
                # alert 창의 '확인'을 클릭
                driver.switch_to.alert.accept()
            except NoAlertPresentException:
                # logger.info('NoAlertPresentException ... pass ')
                pass
            
            # # 응답시간 취득
            # resp_time = str(round(time.time()-outtime, 2))
            
            # logger.info(step_add(total_step) + 'URL_GET(2/2) '+ 'URL Loading'+ resp_time)
            
        except TimeoutException:
            logger.exception('URL_GET / time_out exception : '+ web_url)
            pass
        except Exception:  # 기타 오류 발생시 처리 정지
            logger.exception('URL_GET Exception Occured ')
            #break
            pass
        
        # 응답시간 취득
        resp_time = str(round(time.time()-outtime, 2))

        redirected_url = driver.current_url            
        
        #팝업 레이어 
        # driver.execute_script("document.getElementsByClassName('popup-container').style.display='none';")
        
        
        logger.info(step_add(total_step) + 'URL redirected : '+ redirected_url + diff_time(pertime))
        window['-OUTPUT-'].update(value='→ (redirected) '+redirected_url + diff_time(pertime)+'\n', append=True)
        window.refresh() # 작업내용 출력 반영
        
        # 이미지 캡쳐 (브라우져 크기 설정후 캡쳐 사이즈 지정 필요)
        # redirect 된 url로 이미지 캡쳐 필요
        #img_str = str(row['url_no'])+ "__" + row['url_addr'] + ".png"
        
        #img_str = str(row['url_no'])+ "_site.png"        
        img_str = str('{0:04}'.format(row['url_no']))+ "_site.png"
        
        #time.sleep(2) # 화면캡쳐 전 2초대기
        
        
        
        
        # 화면 캡쳐
        try:
            # 특정 사이즈 저장
            # driver.save_screenshot(img_daily_path + img_str)
            
            
            # 이미지 캡쳐 전 daily 파일삭제
            '''
            existDailyImage = os.path.isfile(img_daily_path + img_str)
            if(existDailyImage == True):
                os.remove(img_daily_path + img_str)
                logger.info('delete ===> ' + img_daily_path + img_str)
            '''
            
            # 화면캡쳐 전 대기시간(default=2초)
            if(row['option_delay_seconds'] > 0):
                delay_time = row['option_delay_seconds']
            else:
                delay_time = 2
                
            time.sleep(delay_time)
            
            logger.info('option_delay_seconds : '+ str(delay_time))
            
            # 작업중...
            now_time = datetime.now().strftime('%Y%m%d%H%M%S%f')
            new_img = str('{0:04}'.format(row['url_no'])) + "_" + str(now_time) + "_site.png"
            
            # 오래된 이미지 자료 삭제
            remove_old_screenshot(row['url_no'])
            
            # Full 스크린 저장
            fullpage_screenshot(driver, img_daily_path + new_img)
            
            # Daily 이미지 생성 체크
            existDailyImage = os.path.isfile(img_daily_path + new_img)
            if(existDailyImage == False):
                logger.warning('화면캡쳐 생성 에러 : ' + img_daily_path + new_img)
            
            
        except TimeoutException as e:
            logger.warning('Screenshot Timout')
            pass
        except Exception as e:  # 기타 오류 발생시 처리 정지
            logger.critical('SCREENSHOT Exception Occured : '+ str(e))
            break
        
        logger.info(step_add(total_step) + 'Screenshot' + diff_time(pertime))
        window['-OUTPUT-'].update(value='→ Screenshot'+ diff_time(pertime)+'\n', append=True)
        # origin_img = img_origin_path + img_str
        # new_img = img_daily_path + img_str
        
        # 이미지 유사도 검증
        # IMAGE_MATCH = keyword.get('IMAGE_MATCH')
        IMAGE_MATCH = True
        
        if(IMAGE_MATCH == True):
            origin_img = img_str
            # new_img = img_str
            
            img_matching_point = image_match(origin_img, new_img)
            if(img_matching_point == -99.99):
                logger.info(step_add(total_step) + 'image_match skipped(file is not exist.) ' + diff_time(pertime))
            else:
                if(img_matching_point >= 40):
                    img_match = '(OK) '
                else:
                    img_match = '(NG) '
                logger.info(step_add(total_step) + 'image_match '+ img_match + str(round(img_matching_point,3)) + diff_time(pertime))
        else:
            logger.info(step_add(total_step) + 'image_match skipped(search option) ' + diff_time(pertime))
        
        window['-OUTPUT-'].update(value='→ Image Simlarity', append=True)
        window['-OUTPUT-'].update(value=diff_time(pertime), append=True)        
        window['-OUTPUT-'].update(value='\n', append=True)
                

        
        window.refresh() 

        # HTML 저장 및 검증 ----------------------------------- #
        # HTML 소스코드 취득
        try:
            # 소스파일 취득시 에러발생 회피( 에러 : "안전한 사용을 위해 키보드보안 보안솔루션(라온시큐어) 설치페이지로 이동합니다.")
            html_source = driver.page_source # redirected 최종 URL의 소스를 취득
            
            # 로그를 보기좋게 정리(prettfy)
            html_source = BeautifulSoup(html_source, 'html.parser').prettify
            
            # HTML 저장 ------------------------------------------- #
            html_file = save_html(row['url_no'], html_source)
            
            logger.info(step_add(total_step) + 'HTML Save'+ diff_time(pertime))
            window['-OUTPUT-'].update(value='→ HTML Save' + diff_time(pertime)+'\n', append=True)
            window.refresh()
            
            # HTML 비교
            html_output = {}
            org_html = str('{0:04}'.format(row['url_no'])) + '.html'
            # html_rate, html_diff_output = diff_html(org_html, html_file, row['url_no'])
            diff_st_time = time.time()
            html_output = diff_html(org_html, html_file, row['url_no'])
        
        except:
            pass
        
        
        # HTML 비교 소요시간
        mon_html_diff_time = str(round(time.time()-diff_st_time, 2))
        logger.info('HTML Simlarity '+ mon_html_diff_time)
        window['-OUTPUT-'].update(value='→ HTML Simlarity', append=True)
        window['-OUTPUT-'].update(value=' ('+ mon_html_diff_time + 's)', append=True)        
        window['-OUTPUT-'].update(value='\n', append=True)
        # print(html_output)
        
        # logger.info('HTML 유사도 : ' + str(html_output['s4']) )

        # Request Code 취득 ----------------------------------- #
        # (200 : ok, 404 : page not found)
        try:
            req_code = get_request_code(redirected_url)
            logger.info(step_add(total_step) + 'Status : '+ str(req_code) + diff_time(pertime))
        except Exception as e:  # 기타 오류 발생시 처리 정지
            logger.critical('Request Code Exception Occured : '+ str(e))
            req_code = 'FAILED'
            pass  
        
        t_color='#333333'
        if(req_code != 200):
            t_color='Red'
        # http Status code 
        window['-OUTPUT-'].update(value='→ Status ' + str(req_code) + diff_time(pertime)+'\n' , append=True, text_color_for_value=t_color)
        window.refresh()

        # HTML 유사도 검증 ------------------------------------- #
        # 
                
                
        # 새창 닫기
        
        close_new_tabs(driver)
        logger.info(step_add(total_step) + 'New Tab Closed' + diff_time(pertime))
        window['-OUTPUT-'].update(value='→ New Tab Closed', append=True)
        window['-OUTPUT-'].update(value=' ('+str(round(time.time()-pertime, 2)) + 's)', append=True)        
        window['-OUTPUT-'].update(value='\n', append=True)
        window.refresh() # 작업내용 출력 반영

        # img_matching_point = image_match( img_str , img_str) # 이미지 유사도
        
        mon_html_match1 = html_output.get('s4')
        mon_html_diff_output = html_output.get('mon_html_diff_output')
        tb_monitor['url_no'] = row['url_no']
        tb_monitor['mon_response_time'] = resp_time
        tb_monitor['status_code'] = req_code
        tb_monitor['html_file'] = html_file
        tb_monitor['mon_image'] = new_img   # img_daily_path + img_str
        tb_monitor['mon_img_match1'] = img_matching_point
        tb_monitor['mon_html_match1'] = mon_html_match1
        tb_monitor['mon_html_diff_output'] = mon_html_diff_output
        tb_monitor['mon_html_diff_time'] = mon_html_diff_time

        tb_url['url_no'] = row['url_no']
        tb_url['url_redirected'] = redirected_url
        tb_url['url_status'] = req_code
        tb_url['url_response_time'] = resp_time
        tb_url['url_img_match1']  = img_matching_point
        tb_url['url_html_match1'] = mon_html_match1
        tb_url['url_html_diff_output'] = mon_html_diff_output
        
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

    # 작업종료후 브라우져 닫기
    if(total_cnt > 0):
        driver.close() 
        driver.quit() # Headless 실행시 chromedriver.exe 실행되고 작업종료 후 prompt창 닫기


    deleted_cnt = delete_Old_HTML_File(html_diff_path)
    print (deleted_cnt)
    
    #처리건수 리턴
    return cnt

def stop_Signal():
    # 정지 신호
    global process_stop
    process_stop = True
    
  
    
def browser_Close():
    global driver
    driver.close() 
    driver.quit()

# 소스파일 비교용(변경되지 않은 행을 제외)
def trim_unchanged(lines:list[str]) -> list[str]:

    # tr の部分とその前後で分ける
    pre = lines[:7]
    trs = lines[7:-2]
    post = lines[-2:]

    # 省略部分を示すフィラー
    filler = '<tr class="filler"><td class="diff_next"></td><td class="diff_header"></td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header"></td><td nowrap="nowrap"></td></tr>'

    minimal_lines = []
    for i, line in enumerate(trs):

        if ('class="diff_chg"' in line) or ('class="diff_sub"' in line) or ('class="diff_add"' in line):
            # 表示する行とそのインデックスを控えていく
            minimal_lines.append([-1, filler])
            minimal_lines.append([i, line])
            if i == 0:
                # 先頭の行が変更されていた場合は冒頭にフィラー不要
                minimal_lines.pop(-2)
            if len(minimal_lines) > 2 and minimal_lines[-3][0] + 1 == i:
                # 2つ前の行番号と今の行番号が1つしか違わない、すなわち行が連続している場合もフィラー不要
                minimal_lines.pop(-2)

    return pre + [x[1] for x in minimal_lines] + post

def html_diff_output(from_file, to_file, html_diff_output_file, template_path, css_path):
    
    global skip_unchanged
    # import argparse
    # from pathlib import Path
    # from difflib import HtmlDiff

    f_path = Path(from_file)
    t_path = Path(to_file)
    f = f_path.read_text("utf-8").splitlines()
    t = t_path.read_text("utf-8").splitlines()

    # 差分を html table に変換
    df = HtmlDiff()
    logger.info('html_diff_output  1 (성능개선 필요, 1행에 대량의 코드가 있는 경우, mob.hometax.go.kr 5분 소요')
    markup_lines = df.make_table(f, t, fromdesc=f_path.name, todesc=t_path.name).splitlines()
    logger.info('html_diff_output  2')
    if skip_unchanged:
        markup_lines = trim_unchanged(markup_lines)
    markup_table = "\n".join(markup_lines)

    # テンプレートの html 読み込み
    template = Path(template_path).read_text("utf-8")

    # css 読み込み
    style_sheet = Path(css_path).read_text("utf-8")

    # 整形してファイルに書き込み
    html_page = template.replace(
        "<style></style>", "<style>\n{}\n</style>".format(style_sheet)
    ).replace(
        '<div class="main"></div>', '<div class="main">\n{}\n</div>'.format(markup_table)
    )
    #Path(out_path).write_text(html_page, "utf-8")
    
    
    f = open(html_diff_output_file, 'w', encoding='UTF-8')
    f.write(str(html_page))
    f.close()
    
    
def diff_html(org_html, html_file, url_no):
    
    global html_output
    
    #todo.
    org_html  = html_path + 'orign\\' +  org_html 
    daily_html = html_path + 'daily\\' + html_file

    logger.info('(org_html) ' + org_html)
    logger.info('(daily_html) '  + daily_html)
    
    
    # 원본파일 로딩
    try:
        f = open(org_html, "r", encoding='utf-8')
        reader1 = f.read()
        
    except:
        logger.warning("Origin file is not existed : %s\n" % org_html)
        html_output['s4'] = '-1'
        return html_output

    # 대상파일 로딩
    try:
        f2 = open(daily_html, "r", encoding='utf-8')
        reader2 = f2.read()        
    except:
        logger.warning("Daily file is not existed : %s\n" % daily_html)
        html_output['s4'] = '-1'
        return html_output

    # 유사도 검사       
    s1 = style_similarity(reader1, reader2)
    s2 = structural_similarity(reader1, reader2)
    s3 = similarity(reader1, reader2)

    # 복합 유사도 검사
    # Using k=0.3 give use better results. 
    # The style similarity gives more information about the similarity rather than the structural similarity.
    k = 0.3 
    s4 = k * structural_similarity(reader1, reader2) + (1 - k) * style_similarity(reader1, reader2)
    
    logger.info ('(style_similarity) ' +  str(s1))
    logger.info ('(structural_similarity) ' + str(s2))
    logger.info ('(similarity) ' + str(s3))
    logger.info ('(Joint Similarity) ' + str(s4))
    
    # 파일 닫기
    f.close()
    f2.close()
    
    
    
    #############################################
    # 유사도 검사 

    # 100분율 환산    
    html_output['s1'] = s1 * 100
    html_output['s2'] = s2 * 100
    html_output['s3'] = s3 * 100
    html_output['s4'] = s4 * 100

    # 소수점 2자리까지 절삭
    html_output['s4'] = round(html_output['s4'], 2)
    # diff_save_html()
    html_output['mon_html_diff_output'] = 'None'
    
    
    if(s4 < 100):
        logger.info('(Joint Similarity < 100) ')
        # first_file_lines = Path(org_html).read_text('utf-8').splitlines()
        # second_file_lines = Path(daily_html).read_text('utf-8').splitlines()

        # output = difflib.HtmlDiff().make_file(first_file_lines, second_file_lines)
        # html_diff_path = html_path + 'diff\\'
        
        # sysdate = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        # html_diff_output = html_diff_path + str('{0:04}'.format(url_no)) + '_' + str(sysdate) +'_diff.html'
        # Path(html_diff_output).write_text(output, encoding = 'utf-8')
        
        template_path = lib_path + 'diff_template.html'
        css_path = lib_path + 'diff_wrap.css'
        
        sysdate = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        
        file_name = str('{0:04}'.format(url_no)) + '_' + str(sysdate) +'_diff.html'
        html_diff_output_file = html_diff_path + file_name
        html_diff_output(org_html, daily_html, html_diff_output_file, template_path, css_path)
        
       
        html_output['mon_html_diff_output'] = file_name
    elif(s4 == 100):
        logger.info('Joint Similarity is 100')
    else:
        logger.info('Joint Similarity > 100 !! ')
    
    # print (html_output)
    
    # daily file 삭제
    # time.sleep(5)
    # del_File(file_name=daily_html)
    
    return html_output
    
# 임시 파일 삭제용
def del_File(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        logger.info('(Delte file) ' +  file_name)
    
# 응답시간 취득
def getResponseTime(driver):
    
    """
    Use Selenium to Measure Web Timing
    Performance Timing Events flow
    navigationStart -> redirectStart -> redirectEnd -> fetchStart -> domainLookupStart -> domainLookupEnd
    -> connectStart -> connectEnd -> requestStart -> responseStart -> responseEnd
    -> domLoading -> domInteractive -> domContentLoaded -> domComplete -> loadEventStart -> loadEventEnd
    """
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")

    # domComplete 시간이 취득안되는 경우가 있어 보류
    
    backendPerformance = responseStart - navigationStart
    frontendPerformance = domComplete - responseStart
    resp_time = domComplete - navigationStart

    logger.info ("Back End: %s" % backendPerformance)
    logger.info ("Front End: %s" % frontendPerformance)
    logger.info ("Response Time: %s" % resp_time)
    
    return resp_time


def set_browser_option_url(browser_option):
    
    # 크롬 브라우저 오픈
    options = webdriver.ChromeOptions()
    # USER_Agent 지정
    options.add_argument(user_agent)
    options.add_argument("disable-gpu")

    #자바스크립트 disable
    if(browser_option['option_javascript_disabled'] == True):
        logger.info('option_javascript_disabled .....')
        options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    
    # '시스템에 부착된 장치가 작동하지 않습니다' 오류 제거
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    # Bypass to "Your connection is not private"
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    # windows의 경우, command prompt 뜨지 않게
    args = ["--hide_console--", ]

    '''
    service.py : 72 line 
    path = .venv\Lib\site-packages\selenium\webdriver\common\service.py
    
    if any("--hide_console--" in arg for arg in self.command_line_args()):
                print ('invisible prompt ... chromedriver.exe')
                self.process = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, creationflags=0x08000000)
            else:
                print ('(default) visible prompt ... chromedriver.exe')
                self.process = subprocess.Popen(cmd, env=self.env, 
                                                close_fds=system() != 'Windows', 
                                                stdout=self.log_file, 
                                                stderr=self.log_file, 
                                                stdin=PIPE)
    '''

    if (browser_option['option_browser_width'] > 0) and (browser_option['option_browser_height'] > 0):
        # 사용자 지정 사이즈
        option_browser_width = browser_option['option_browser_width']
        option_browser_height = browser_option['option_browser_height']
    else:
        # 디폴트 사이즈
        option_browser_width = 1280
        option_browser_height = 1000
    
    # 자바스크립트 비활성화
    # options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})

    # 브라우져 창 최소화 유무
    if (browser_option['option_browser_bg_execute'] == True):
        logger.info('headless.....')
        # 백그라운드 실행
        options.add_argument("--headless")
        
        # headless 실행시 윈도우 사이즈 줄여야함(width: -16, height : -137)
        browser_size = '--window-size='+ str(option_browser_width - 16)+','+str(option_browser_height - 137)
        options.add_argument(browser_size)
        
        # headless 탐지막기 
        # https://beomi.github.io/gb-crawling/posts/2017-09-28-HowToMakeWebCrawler-Headless-Chrome.html
        # options.headless = True

    else:
        
        logger.info('foreground .....')
        # 디폴트 사이즈
        browser_size = '--window-size='+ str(option_browser_width)+','+str(option_browser_height)
        options.add_argument(browser_size)
        #options.add_argument("--start-maximized")
    
    # 브라우져 옵션 설정
    driver = webdriver.Chrome(lib_path + 'chromedriver.exe', options=options, service_args=args) 
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) # deprecated option

    # 명시적으로 대기(10초) 
    driver.implicitly_wait(time_to_wait=10)    
    
    # InsecureRequestWarning  메시지 제거
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    return driver
    
    
    
# 브라우저 기본 설정
def set_browser_option(BG_EXE):
    
    # 크롬 브라우저 오픈
    options = webdriver.ChromeOptions()
    # USER_Agent 지정
    options.add_argument(user_agent)
    options.add_argument("disable-gpu")

    #자바스크립트 disable
    options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})


    
    # '시스템에 부착된 장치가 작동하지 않습니다' 오류 제거
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    # Bypass to "Your connection is not private"
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    # windows의 경우, command prompt 뜨지 않게
    args = ["--hide_console--", ]

    '''
    service.py : 72 line 
    path = .venv\Lib\site-packages\selenium\webdriver\common\service.py
    
    if any("--hide_console--" in arg for arg in self.command_line_args()):
                print ('invisible prompt ... chromedriver.exe')
                self.process = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, creationflags=0x08000000)
            else:
                print ('(default) visible prompt ... chromedriver.exe')
                self.process = subprocess.Popen(cmd, env=self.env, 
                                                close_fds=system() != 'Windows', 
                                                stdout=self.log_file, 
                                                stderr=self.log_file, 
                                                stdin=PIPE)
    '''

    # 자바스크립트 비활성화
    # options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})

    # 브라우져 창 최소화 유무
    if (BG_EXE == True):
        # 백그라운드 실행
        # headless 실행시 윈도우 사이즈 줄여야함(width: -16, height : -137)
        options.add_argument('--window-size=1264,863')
        options.add_argument("--headless")
        # headless 탐지막기 
        # https://beomi.github.io/gb-crawling/posts/2017-09-28-HowToMakeWebCrawler-Headless-Chrome.html
        # options.headless = True

    else:
        # 사이즈 변경하지 말것
        options.add_argument('--window-size=1280,1000')

        #options.add_argument("--start-maximized")
    
    # 브라우져 옵션 설정
    driver = webdriver.Chrome(lib_path + 'chromedriver.exe', options=options, service_args=args) 
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) # deprecated option

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
    # print ('11',type(result))
    # if(type(result) == "<class 'NoneType'>"):
    #     print ('22',type(result))
    #if result 
    try:
        
        for row in result:
            #org_list.append(row['org_title']+'['+row['org_no']+']')
            grp_list.append(row['grp_title'])

        return grp_list

    except Exception as e:
        logger.error(e)
        logger.exception(e)
        raise

def my_grp_list_checkbox():
    
    grp_list = ['전 체']
    result = model.get_grp_list()
    
    # # DB조회결과 없는 경우
    # if( type(result) != 'list'):
    #     return False
    # print ('11',type(result))
    # if(type(result) == "<class 'NoneType'>"):
    #     print ('22',type(result))
    #if result 
    try:
        
        for row in result:
            #org_list.append(row['org_title']+'['+row['org_no']+']')
            grp_list[row['grp_no']] = row['grp_title']

        return grp_list

    except Exception as e:
        logger.error(e)
        logger.exception(e)
        raise
    
    
def list_combo():
    
    url_list = ['----']
    result_cnt = model.get_url_list_cnt()
    
    # print(type(result_cnt))
    # print('>>>>', result_cnt['cnt'])
    
    unit = int(unit_cnt)
    
    try:
        per = ( result_cnt['cnt'] / unit) + 1
        
        # print (per)
        print('>>>>', range(1, round(per)))
        i = 1
        ranges = i
        for i in range(1, round(per)):
            
            print ('list -> ', str(ranges) + ' ~ ' + str(ranges + unit - 1))
            
            url_list.append(str(ranges) + ' ~ ' + str(ranges + unit - 1))
            ranges = ranges + unit
        
        # grp_list.append(i)
        
        # for row in result:
            #org_list.append(row['org_title']+'['+row['org_no']+']')
            # grp_list.append(row['cnt'])

        return url_list

    except Exception as e:
        logger.error(e)
        logger.exception(e)
        raise

@logger.catch 
def save_org_html(url_no, src_text):
    
    html_file = str('{0:04}'.format(url_no))+'.html'
    
    #원본 저장경로    
    full_path_name = html_path + 'orign\\' + html_file
    
    f = open(full_path_name, 'w', encoding='UTF-8')
    # print(type(src_text))
    f.write(str(src_text))
    f.close()

    return html_file
    # DB insert

@logger.catch 
def save_html(url_no, src_text):
    
    sysdate = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    # print(html_path + str(url_no)+'_'+str(sysdate)+'.html')

    
    # html_file = str('{0:04}'.format(url_no))+'_'+str(sysdate)+'.html'
    # URL별로 한개만 생성하도록 변경
    html_file = str('{0:04}'.format(url_no)) + '.html'
    
    full_path_name = html_path + 'daily\\' + html_file
    # print(full_path_name)
    
    f = open(full_path_name, 'w', encoding='UTF-8')
    # print(type(src_text))
    f.write(str(src_text))
    f.close()

    return html_file
    # DB insert

@logger.catch    
def get_request_code(web_url):
    
    global user_agent
    headers = {'User-Agent': user_agent}
    
    # print(headers)
    
    status = None
    try:
        response = requests.get(web_url, headers=headers, verify=False) # verify=False (SSLerror 오류 발생 회피)
        
        
        # 상태코드 수신 대기
        loop_cnt = 0
        # print ('loop_cnt1-->', loop_cnt, response.status_code)
        # while response.status_code == 'None':
        #     if(loop_cnt < 10 ):
        #         time.sleep(1)
        #         loop_cnt += 1
        #     else:
        #         break
            
        #     print ('loop_cnt2-->', loop_cnt, response.status_code)
                    
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

    logger.info('(org_img) ' + img_origin_path + origin_img)
    logger.info('(new_img) ' + img_daily_path + new_img)
    file1 = img_origin_path + origin_img 
    file2 = img_daily_path + new_img
    
    gis = ImageSignature()
    
    if os.path.isfile(file1) and os.path.isfile(file2):
        a = gis.generate_signature(file1)
        b = gis.generate_signature(file2)
    
        # 0.4% 이하 유사도 높음
        result = gis.normalized_distance(a, b)
        
        # 100% 비율로 환산(0.4% 이하 => 60% 이상 유사도 높음)
        result = round((100-(result * 100)),2)
        return result
    else:
        if(os.path.isfile(file1) == False):
            logger.info('Original image is nothing ... Image_matching skipped')
            result = -1 # 스킵(상태) = -1
        elif(os.path.isfile(file2) == False):
            logger.info('Daily image is nothing ... Image_matching skipped')
            result = -2 # 스킵(상태) = -1
            
        return result


def fullpage_screenshot_test(driver, file):
    # from selenium import webdriver

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=chrome_options)
    #driver.get("http://naver.com")
    #width = driver.execute_script("return document.body.scrollWidth") #스크롤 할 수 있는 최대 넓이
    width = driver.execute_script("return document.body.clientWidth")
    height = driver.execute_script("return document.body.scrollHeight") #스크롤 할 수 있는 최대 높이
    driver.set_window_size(width, height) #스크롤 할 수 있는 모든 부분을 지정
    driver.save_screenshot(file)



@logger.catch    
def fullpage_screenshot(driver, file):

        # print("Starting chrome full page screenshot workaround ...")
        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = driver.execute_script("return document.body.clientWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        logger.info("FullpageScreenshot_Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height, viewport_width, viewport_height))
        rectangles = []

        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height

            if top_height > total_height:
                top_height = total_height

            while ii < total_width:
                top_width = ii + viewport_width

                if top_width > total_width:
                    top_width = total_width

                #print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
                rectangles.append((ii, i, top_width,top_height))

                ii = ii + viewport_width

            i = i + viewport_height

        stitched_image = Image.new('RGB', (total_width, total_height))
        previous = None
        part = 0

        for rectangle in rectangles:
            if not previous is None:
                driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                #print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
                time.sleep(0.2)

            #file_name = "part_{0}.png".format(part)
            nowdt = datetime.now().strftime('%y%m%d_%H%M%S%f')
            file_name = nowdt+".png"
            
            print("full screenshot... {0} {1} ..." + str(file_name))

            driver.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

            # print("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
            stitched_image.paste(screenshot, offset)

            del screenshot
            os.remove(file_name)
            part = part + 1
            previous = rectangle

        stitched_image.save(file)
        # print("Finishing chrome full page screenshot workaround...")
        return True
    

def after_main():
    global driver
    
    try:
        # 작업종료후 브라우져 닫기
        driver.close()
        driver.quit()
        # print("작업 종료 ..  =>",type(driver))
        logger.info("Chrome Browser Closed")
    except:
        # 시작하지 않고 종료시 driver 변수 에러 방지(NameError: name 'driver' is not defined)
        pass
    

def image_diff_opencv(src, dest):
    
    from PIL import ImageChops
    import cv2    
        
    diff = ImageChops.difference(src, dest)
    diff.save(img_diff_path + 'diff.png')
    
    # 파일생성 대기
    while not os.path.exists(img_diff_path + 'diff.png'):
        time.sleep(1)
        
        
        
    
    src_img = cv2.imread(src)
    dest_img = cv2.imread(dest)
    diff_img = cv2.imread(img_diff_path + 'diff.png')
    
    grey = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    COLOR = (0, 200, 0)
    
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            x, y, width, height = cv2.boundingRect(cnt)
            cv2.rectangle(src_img, (x, y), (x + width, y + height), COLOR, 2)
            cv2.rectangle(dest_img, (x, y), (x + width, y + height), COLOR, 2)
            cv2.rectangle(diff_img, (x, y), (x + width, y + height), COLOR, 2)
        
   
    cv2.imshow('src', src_img)
    cv2.imshow('dest', dest_img)
    cv2.imshow('diff', diff_img)
    
def CBtn(sg, BoxText):
    strlen = len(BoxText)
    strlen = strlen + 3
    return sg.Checkbox(BoxText, size=(strlen, 1), default=False)

def delete_Old_HTML_File(path):
    
    global set_delete_days
    
    import datetime

    file_names = os.listdir(path)
    cnt = 0
    for file in file_names:
        
        today = datetime.datetime.now() # 오늘
        delete_days = today - datetime.timedelta(days = int(set_delete_days)) # 삭제 기준일
        delete_days = delete_days.strftime('%Y%m%d') # yyyymmdd 형식으로 변환
        
        # print(today.strftime('%y%m%d'), before_1week.strftime('%y%m%d'))
        
        
        # print (file_array[1] )
        
        # 파일명에서 년월일 추출 ( 0340_20220919_103234_044251_diff.html )
        file_array = file.split('_')
        file_yyyymmdd = file_array[1] # 20220919
        
        
        if(file_yyyymmdd < delete_days):

            if os.path.isfile(path + file):
                
                # 오류 발생시 pass 되도록 개선( 에러내용 : "PermissionError: [WinError 5] 액세스가 거부되었습니다")
                try:
                    os.remove(path + file)
                    print(file_yyyymmdd , delete_days)
                    print ('deleted.', cnt)
                    cnt += 1
                except:
                    pass
                    
            else:
                print ('not deleted.')
        
        
        # 100개만 삭제하고 중지 (수행시간 단축위해)
        if(cnt == 100):
            print ('Old File deleted CNT ... ', cnt )
            return cnt
            break
                
        
    print ('Old File deleted CNT ... ', cnt )
    
    return cnt

def remove_old_screenshot(url_no):
    
    import glob
    
    #print (img_daily_path + str('{0:04}'.format(url_no)) + '_*.png')
    files = glob.glob(img_daily_path + str('{0:04}'.format(url_no)) + '_*.png')
    # print (files)
    
    # 역순으로 sort
    files.sort(reverse=True)
    
    
    cnt = 0
    deleted = 0
    
    for file in files:
        base = os.path.basename(file)
        file_name = img_daily_path + os.path.splitext(base)[0] + '.png'
        # print(file_name)
        
        # 10개 이상 삭제
        if(cnt >= 10):
            if os.path.isfile(file_name):
                os.remove(file_name)
                deleted += 1
        
        cnt += 1
        
        # print(os.path.splitext(base)[0])
    logger.info('이미지 삭제된 파일 : ' + str(deleted))
