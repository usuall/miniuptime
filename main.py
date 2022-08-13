import mini.library as mini
import mini.model as model
import PySimpleGUI as sg
from pickle import TRUE
# from webdriver_manager.chrome import ChromeDriverManager
import os

'''
    URL healthcheck dashboard introduction...
    ....
    .... copyright usuall@gmail.com
    .... mini project
'''



def main():
    
    #모니터링 실시
    
    #카테고리 취득
    org_list = mini.my_org_list_combo()

    # GUI 실행
    sg.theme('TanBlue')
    layout_left = [[sg.Button('종 료', key='-BUTTON_EXIT-', button_color=('white', 'firebrick3'))]]
    layout_right =[[sg.Button('     실 행     ', key='-BUTTON_START-'), sg.Button('중 지', key='-BUTTON_STOP-', disabled=True, button_color=('black', 'lightblue'))]]
    layout = [
        [sg.Text('URL Health-Check Manager', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('URL 모니터링 툴입니다. 조건을 선택하고 실행하세요'),sg.Text('URL 모니터링 툴입니다. 조건을 선택하고 실행하세요')],
        # [sg.InputText('', key='in1')],
        # [sg.Listbox(values=(org_list), size=(30, 1), key='-ORG_LIST-', enable_events=True)],
        [sg.Text('카테고리'), sg.Combo(values=(org_list), default_value='전 체', size=(30, 1), key='-ORG_LIST-', enable_events=False, tooltip='카테고리를 선택해주세요.')],
        [sg.Text('사이트명'), sg.InputText('', key='-SITE_TITLE-', size=(30, 1), tooltip='사이트명을 입력하세요.'),
         sg.Text('  URL명'), sg.InputText('', key='-SITE_URL-', size=(30, 1), tooltip='도메인(URL)을 입력하세요.')],
        [sg.CBox('반복 점검', key='-REPEAT-', default=False, tooltip='체크 대상을 반복하여 점검합니다.'), 
         sg.CBox('비활성화 URL 포함', key='-DISABLED-'), sg.CBox('백그라운드 실행', key='-BG_EXE-', default=True, tooltip='임시 비활성화 URL 대상까지 검색')],
        [sg.CBox('AP작업 포함', key='-AP_WORK-', default=TRUE, tooltip='AP작업중 URL.....'), 
         sg.CBox('추가 항목', key='-ADD1-'), sg.CBox('추가 항목2', key='-ADD2-', default=True)],
        [sg.MLine(default_text='', font='Gothic', size=(80, 20), key='-OUTPUT-', autoscroll=True, disabled=True)],
        [sg.Text('타임아웃'), sg.Radio('5초',  group_id="RADIO1", key='-TIMEOUT1-'),
                            sg.Radio('10초', group_id="RADIO1", default=True, key='-TIMEOUT2-'),
                            sg.Radio('15초', group_id="RADIO1", key='-TIMEOUT3-'),
                            sg.Radio('20초', group_id="RADIO1", key='-TIMEOUT4-'),
                            sg.Radio('25초', group_id="RADIO1", key='-TIMEOUT5-'),
                            sg.Radio('30초', group_id="RADIO1", key='-TIMEOUT6-')],
        # [sg.Combo(('Combobox 1', 'Combobox 2'), key='combo', size=(20, 1)),sg.Slider(range=(1, 100), orientation='h', size=(34, 20), key='slide1', default_value=85)],
        # [sg.Combo(('Combobox 1', 'Combobox 2'), key='combo', size=(20, 1))],
        # [sg.OptionMenu(('Menu Option 1', 'Menu Option 2', 'Menu Option 3'), key='optionmenu')],

        # [sg.Text('Choose A Folder', size=(35, 1))],
        # [sg.Text('Your Folder', size=(15, 1), justification='right'),
        # sg.InputText('Default Folder', key='folder'), sg.FolderBrowse()],
        # [sg.Col(layout_left, p=0), sg.Col(layout_right, p=0)],
        [sg.Button('종 료', key='-BUTTON_EXIT-', button_color=('white', 'firebrick3')),
         sg.Button('도움말', key='-BUTTON_HELP-', button_color=('white', 'firebrick3')),
         sg.Text('  ' * 30), sg.Button('     실 행     ', key='-BUTTON_START-'), sg.Button('중 지', key='-BUTTON_STOP-', disabled=True, button_color=('black', 'lightblue'))]
    ]

    
    #window = sg.Window('Uptime Manager for NIRS', layout, default_element_size=(40, 1), grab_anywhere=False, location=sg.user_settings_get_entry('-LOCATION-', (None, None)))
    window = sg.Window('Uptime Manager for NIRS', layout, default_element_size=(40, 1), grab_anywhere=True )

    
    while True:
        event, values = window.read()
        # 각종 버튼에 대한 이벤트 처리
        if event == '-BUTTON_START-':
                        
            cnt = 1
            # 버튼 비활성화 전환
            mini.button_activate(window, 0)

            # 조회조건 출력
            keyword = mini.getCondition(window, values)
            
            # 모니터링 중
            mon_status = 1
            
            # 모니터링 작업
            while True:
                # print ('repeat -->', keyword.get('REPEAT'))
                # 반복작업 선택시
                if (keyword.get('REPEAT') == True or cnt == 1):
                    url_cnt = mini.get_monitoring(window, keyword)
                    if(url_cnt == 0):
                        print('--- Working Completed(cnt=0) ---')
                        break
                    cnt += 1

                else:
                    print('--- Working Completed.(REPEAT=False) ---')
                    break
            
        elif event == '-BUTTON_STOP-':
            print('중지')
            # 버튼 활성화 전환
            mini.button_activate(window, 1)
            
        elif event == '-BUTTON_HELP-':
            
            help_text = '''Uptime Connectly는 URL Health Check Manager 입니다.
            
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

        elif event in ('-BUTTON_EXIT-', 'Escape:27', sg.WIN_CLOSED):
            # 재실행시 종료한 위치에 실행됨
            sg.user_settings_set_entry('-LOCATION-', window.current_location())
            # Todo : browser & dbconnection close.
            print('exit....')
            break

    window.close()
    
if __name__ == '__main__':
    print('__main__')
    
    mini.before_main()
    main()
    
         
