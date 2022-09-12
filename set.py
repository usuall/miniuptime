import mini.set_library as mini
import mini.model as model
#from mini.config import get_Config
import PySimpleGUI as sg
import threading
import os
import time
from threading import Event
from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException

# 환경 설정값 취득
properties = mini.get_Config()
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


def main():
    
    global driver
    
    # GUI 실행
    sg.theme('TanBlue')
    
    
    grp_list = mini.my_grp_list_combo()  
        
    layout = [
        [sg.Image(filename=logo, key='key1', pad=((5, 0), (10, 10)))],
        [sg.Text('Setting Agent', size=(30, 1), font=("Helvetica", 25))],
        # [sg.Text('Uptime Stream is URL Health Check Manager')],
        # [sg.InputText('', key='in1')],
        # [category_box],
        [sg.Text('카테고리'), sg.Combo(values=(grp_list), default_value='전 체', size=(30, 1), key='-GRP_LIST-', enable_events=False, tooltip='카테고리를 선택해주세요.'),
         sg.Text('URL번호'), sg.InputText('', key='-URL_NO-', size=(7, 1), tooltip='URL 번호')],
        # [sg.Listbox(values=(org_list), size=(30, 1), key='-ORG_LIST-', enable_events=True)],
        [sg.Text('사이트명'), sg.InputText('', key='-SITE_TITLE-', size=(20, 1), tooltip='사이트명을 입력하세요.'),
         sg.Text('  URL명'), sg.InputText('', key='-SITE_URL-', size=(20, 1), tooltip='도메인(URL)을 입력하세요.')],
        [sg.CBox('반복 점검', key='-REPEAT-', default=False, tooltip='체크 대상을 반복하여 점검합니다.'),
         sg.CBox('비활성화 URL 포함', key='-DISABLED-'), sg.CBox('백그라운드 실행', key='-BG_EXE-', default=False, tooltip='크롬 브라우져의 실행화면이 표시되지 않음'),
         sg.CBox('랜덤 실행', key='-RANDOM-')],
         #sg.Radio('랜덤 실행', group_id="RADIO2", default=True, key='-RANDOM-'), sg.Radio('OLD 체크', group_id="RADIO2", default=False, key='-OLDEST-')],
        [sg.CBox('이미지 유사도 검증', key='-IMAGE_MATCH-', disabled=True), sg.CBox('HTML 유사도 검증', key='-HTML_MATCH-', disabled=True)],
        [sg.Text('타임아웃'), sg.Radio('5초', group_id="RADIO1", key='-TIMEOUT1-'),
                            sg.Radio('10초', group_id="RADIO1", key='-TIMEOUT2-'),
                            sg.Radio('15초', group_id="RADIO1", key='-TIMEOUT3-'),
                            sg.Radio('20초', group_id="RADIO1", key='-TIMEOUT4-'),
                            sg.Radio('25초', group_id="RADIO1", key='-TIMEOUT5-'),
                            sg.Radio('30초', group_id="RADIO1", default=True, key='-TIMEOUT6-')],
        [sg.MLine(default_text='', font=('Dotum',11), size=(60, 15), key='-OUTPUT-', autoscroll=True, disabled=True)],        
        [sg.Button('종 료', key='-BUTTON_EXIT-', button_color=('white', 'firebrick3')),
         sg.Button('도움말', key='-BUTTON_HELP-', button_color=('white', 'firebrick3')),
         sg.Text('  ' * 30), sg.Button('     실 행     ', key='-BUTTON_START-'), sg.Button('중 지', key='-BUTTON_STOP-', disabled=True, button_color=('black', 'lightblue'))]
    ]
    
    #window = sg.Window('Uptime Manager for NIRS', layout, default_element_size=(40, 1), grab_anywhere=False, location=sg.user_settings_get_entry('-LOCATION-', (None, None)))
    window = sg.Window('Uptime Stream for NIRS', layout, default_element_size=(40, 1), grab_anywhere=False, icon=ico)

    # stop_event = Event()
    cnt = 0

    while True:
        event, value = window.read()
        print('while loop...', event, value)
        
        if event == '-BUTTON_START-':
            logger.info(' --- BUTTON_START --- ')

            # 조건 저장
            keyword = mini.getCondition(window, value)
            
            # 검색
            result = model.get_grp_url_list(keyword)
            total_cnt = len(result) # 조회 건수
            logger.info('☞  조회결과 : '+ str(total_cnt) + '건')
            window['-OUTPUT-'].update(value='☞ 조회결과 : '+ str(total_cnt) +'건\n', append=True)
            window['-OUTPUT-'].update(value='------------------------------\n', append=True)
            
            cnt = 1
            for row in result:
                tb_url = {}
                tb_monitor = {}
                
                window['-OUTPUT-'].update(value=' ---------------- URL NO : ' + str(row['url_no']) + '\n', append=True)
                window.refresh() 
                
                    
                BG_EXE = keyword.get('BG_EXE') # 백그라운드 실행
                driver = mini.set_browser_option(BG_EXE)
                TIME_OUT = keyword.get('TIME_OUT') #디폴트 10초
                driver.set_page_load_timeout(TIME_OUT)
                
                yes_no = sg.popup_ok_cancel("["+ str(cnt) +"] URL 초기 설정 시작?", title="Next Step")
                if(yes_no == 'OK'):                
                    # 원본이미지 존재 확인
                    img_str = str('{0:04}'.format(row['url_no']))+ "_site.png"
                    existFile = os.path.isfile(img_origin_path + img_str)
                    logger.info("파일 존재 유무 : " + img_origin_path + img_str)        
                    window['-OUTPUT-'].update(value="IMG 파일 존재 유무 "+ img_origin_path + img_str  +' \n', append=True)
                    window.refresh() 
                
                    # 원본 HTML 존재 확인
                    org_html = str('{0:04}'.format(row['url_no']))+ ".html"
                    existFile2 = os.path.isfile(html_origin_path + org_html)
                    logger.info("파일 존재 유무 : " + html_origin_path + org_html +' \n')
                    window['-OUTPUT-'].update(value="HTML 파일 존재 유무 "+ html_origin_path + org_html  +' \n', append=True)
                    window.refresh() 
                
                    
                    if(existFile != True or existFile2 != True):
                        if( existFile != True ):
                            logger.info ('이미지 파일 미존재')
                            window['-OUTPUT-'].update(value="이미지 파일 미존재 \n", append=True)
                            
                        if( existFile2 != True ):
                            logger.info ('HTML 파일 미존재')
                            window['-OUTPUT-'].update(value="HTML 파일 미존재 \n", append=True)

                        window.refresh() 
                        
                        pertime = time.time() # 개별작업시간
                        
                        web_url = row['url_addr']
                        
                        # 브라우져 무한로딩시 timeout 회피(jnpolice.go.kr 사례) / 해결하는데 5일 걸림
                        TIME_OUT = keyword.get('TIME_OUT')
                        
                        outtime = time.time()
                        
                        #logger.info(step_add(total_step) + 'URL_GET(1/2) ' + web_url + diff_time(outtime))
                        try:
                            driver.get(web_url)
                            
                            try:
                                driver.switch_to.alert.accept()
                            except NoAlertPresentException:
                                logger.info('NoAlertPresentException ... pass ')
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
                                
                        time.sleep(5) # 화면캡쳐 전 2초대기
                        
                        
                        # 화면 캡쳐
                        try:
                            # 특정 사이즈 저장
                            # driver.save_screenshot(img_daily_path + img_str)

                            # Full 스크린 저장
                            yes_no = sg.popup_ok_cancel("이미지 캡쳐할까요?", title="Next Step")
                            if(yes_no == 'OK'):   
                                mini.fullpage_screenshot(driver, img_origin_path + img_str)
                        except TimeoutException as e:
                            logger.warning('Screenshot Timout')
                            pass    
                        except Exception as e:  # 기타 오류 발생시 처리 정지
                            logger.critical('SCREENSHOT Exception Occured : '+ str(e))
                            break
                        
                        # logger.info(step_add(total_step) + 'Screenshot' + diff_time(pertime))

                        # HTML 저장 및 검증 ----------------------------------- #
                        # HTML 소스코드 취득
                        html_source = driver.page_source # redirected 최종 URL의 소스를 취득
                        
                        # 로그를 보기좋게 정리(prettfy)
                        html_source = BeautifulSoup(html_source, 'html.parser').prettify
                        
                        # HTML 저장 ------------------------------------------- #
                        html_file = mini.save_org_html(row['url_no'], html_source)

                    else:
                        logger.info ('이미지, HTML 파일 존재')
                
                # 취소시 종료
                else: 
                    window.close()
                    break
                    
                # 새창 닫기        
                mini.close_new_tabs(driver)
                
                cnt += 1
            
        
        if event is None:
            break

    window.close()


def init_process():
    global logo, ico
    
    properties = mini.get_Config()
    config_sys = properties['SYSTEM']
    
    # 각종 디렉토리 경로
    project_path = os.path.abspath(os.getcwd()) + '\\'
    data_path = project_path + config_sys['DATA_PATH'] + '\\'
    logo = data_path + 'uptime_s2.png'
    ico = data_path + 'logo.ico'

if __name__ == '__main__':
    init_process()
    main()
    