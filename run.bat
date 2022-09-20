REM (윈도우, 가상환경 스크립트 실행) 
REM https://stackoverflow.com/questions/34622514/run-a-python-script-in-virtual-environment-from-windows-task-scheduler

REM .venv\Scripts\activate.bat && python run.py

@echo off
set CUR_YYYY=%date:~10,4%
set CUR_MM=%date:~4,2%
set CUR_DD=%date:~7,2%
set CUR_HH=%time:~0,2%
if %CUR_HH% lss 10 (set CUR_HH=0%time:~1,1%)

set CUR_NN=%time:~3,2%
set CUR_SS=%time:~6,2%
set CUR_MS=%time:~9,2%

set SUBFILENAME=%CUR_YYYY%%CUR_MM%%CUR_DD%-%CUR_HH%%CUR_NN%%CUR_SS%

.venv\Scripts\activate.bat && pythonw -u run.py > data/logs/run_%SUBFILENAME%.log 2>&1

