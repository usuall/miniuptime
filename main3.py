import mini.library as mini
import mini.model as model
import PySimpleGUI as sg
from pickle import TRUE
import os
import time
import threading
from threading import Event
from loguru import logger


'''
    URL healthcheck dashboard introduction...
    ....
    .... copyright usuall@gmail.com
    .... mini project
    .... 
'''


def long_function_thread(window, values):
    
    global keyword
    # 조회조건 출력
    keyword = mini.getCondition(window, values)
    url_cnt = mini.get_monitoring(window, keyword)    
    logger.info('GET_MONITORING WORK_CNT : ' + str(url_cnt)) 
    window.write_event_value('-THREAD DONE-', '') # Thread 종료 후 이벤트(반복 작업을 위해 사용)    
    

def long_function(window, values):
    threading.Thread(target=long_function_thread, args=(window, values), daemon=True).start()
    
def main():
    global keyword, logger, logo
    
    #모니터링 실시
    
    #카테고리 취득
    grp_list = mini.my_grp_list_combo()    
    
    
    # grp_list_checkbox = mini.my_grp_list_checkbox()    
    # grp_list_checkbox.items()
    
    
    # GUI 실행
    sg.theme('TanBlue')
    
    
    '''
    category_box = [
        mini.CBtn(sg, grp_list[i]) for i in range(len(grp_list))
    ] 
    '''       
        
    layout = [
        [sg.Image(filename=logo, key='key1', pad=((5, 0), (10, 10)))],
        # [sg.Text('(Uptime Mini) Health Check Agent', size=(30, 1), font=("Helvetica", 25))],
        # [sg.Text('Uptime Stream is URL Health Check Manager')],
        # [sg.InputText('', key='in1')],
        # [category_box],
        [sg.Text('카테고리'), sg.Combo(values=(grp_list), default_value='전 체', size=(30, 1), key='-GRP_LIST-', enable_events=False, tooltip='카테고리를 선택해주세요.'),
         sg.Text('URL번호'), sg.InputText('', key='-URL_NO-', size=(10, 1), tooltip='URL 번호')],
        # [sg.Listbox(values=(org_list), size=(30, 1), key='-ORG_LIST-', enable_events=True)],
        [sg.Text('사이트명'), sg.InputText('', key='-SITE_TITLE-', size=(30, 1), tooltip='사이트명을 입력하세요.'),
         sg.Text('  URL명'), sg.InputText('', key='-SITE_URL-', size=(30, 1), tooltip='도메인(URL)을 입력하세요.')],
        [sg.CBox('반복 점검', key='-REPEAT-', default=True, tooltip='체크 대상을 반복하여 점검합니다.'),
         sg.CBox('비활성화 URL 포함', key='-DISABLED-'), sg.CBox('백그라운드 실행', key='-BG_EXE-', default=False, tooltip='크롬 브라우져의 실행화면이 표시되지 않음'),
         # sg.CBox('랜덤 실행', key='-RANDOM-'),
         sg.Radio('랜덤 실행', group_id="RADIO2", default=True, key='-RANDOM-'), sg.Radio('OLD 체크', group_id="RADIO2", default=False, key='-OLDEST-')],
        [sg.CBox('이미지 유사도 검증', key='-IMAGE_MATCH-', default=True), sg.CBox('HTML 유사도 검증', key='-HTML_MATCH-', default=True)],
        [sg.Text('타임아웃'), sg.Radio('5초', group_id="RADIO1", key='-TIMEOUT1-'),
                            sg.Radio('10초', group_id="RADIO1", default=True, key='-TIMEOUT2-'),
                            sg.Radio('15초', group_id="RADIO1", key='-TIMEOUT3-'),
                            sg.Radio('20초', group_id="RADIO1", key='-TIMEOUT4-'),
                            sg.Radio('25초', group_id="RADIO1", key='-TIMEOUT5-'),
                            sg.Radio('30초', group_id="RADIO1", key='-TIMEOUT6-')],
        [sg.MLine(default_text='', font='Gothic', size=(80, 20), key='-OUTPUT-', autoscroll=True, disabled=True)],        
        [sg.Button('종 료', key='-BUTTON_EXIT-', button_color=('white', 'firebrick3')),
         sg.Button('도움말', key='-BUTTON_HELP-', button_color=('white', 'firebrick3')),
         sg.Text('  ' * 30), sg.Button('     실 행     ', key='-BUTTON_START-'), sg.Button('중 지', key='-BUTTON_STOP-', disabled=True, button_color=('black', 'lightblue'))]
    ]
    
    #window = sg.Window('Uptime Manager for NIRS', layout, default_element_size=(40, 1), grab_anywhere=False, location=sg.user_settings_get_entry('-LOCATION-', (None, None)))
    window = sg.Window('Uptime Stream for NIRS', layout, default_element_size=(40, 1), grab_anywhere=False, icon=ico)

    stop_event = Event()
    cnt = 0
    #  ---------------- Window Event Loop ---------------- #
    while True:
        event, values = window.read()
        
        if stop_event.is_set():
            return

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == '-BUTTON_START-':
            logger.info(' --- BUTTON_START --- ')
            # 버튼 비활성화 전환
            mini.button_activate(window, 0)
            
            # keyword = mini.getCondition(window, values)
            long_function(window, values)
            cnt += 1
                
        elif event == '-THREAD DONE-':
            logger.info(' --- THREAD DONE --- ')
            # 반복 점검
            if (keyword.get('REPEAT') == True):
                cnt += 1
                logger.info('--- THREAD REPEAT (' + str(cnt)+  ' times) ---')
                long_function(window, values)                
                
        elif event == '-BUTTON_EXIT-':
            mini.after_main()
            logger.info (' --- BUTTON_EXIT --- ')
            break

        elif event == '-BUTTON_STOP-':
            logger.info (' --- BUTTON_STOP --- ')
            stop_event.set()
            # break

        elif event == '-BUTTON_HELP-':
            help_text = '''Uptime Stream is URL Health Check Manager.
            
■ 기능설명
- 시뮬레이션 방식으로 브라우져가 URL을 접속하여 확인
- 최종 URL(redirect)의 이미지 캡쳐
 (정상 상태의 이미지와 비교하여 유사도 체크)
- 최종 URL의 상태코드를 확인
 (200 정상, 404 페이지 찾을수 없음 등..)
- 최종 URL의 html 소스코드를 저장
 (정상 상태의 html과 비교하여 유사도 체크)

■ 검색조건 : 카테고리, 사이트명, URL명 등 설정

■ 동작 방법
- 반복 점검 : 전체 검색결과를 반복해서 점검
- 비활성화 URL 점검 : 일시적으로 비활성화된 URL도 점검함
- 백그라운드 실행 : 브라우져가 화면에서 실행되지 않음
- 타임아웃 : 브라우져로 URL이 열리기까지의 타임아웃 시간(초)
            '''
            sg.Popup(help_text)
        else:
            print(' --- else --- ')
            break
            #print(event, values)
    
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
    
    
    # root_logger = logging.getLogger()
    # root_logger.debug("디버그")
    # root_logger.info("정보")
    # root_logger.error("오류")
    init_process()
    mini.before_main()    
    main()
    
    
         
