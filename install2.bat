REM ( PIP upgrading .....  )
python -m pip install --upgrade pip

REM ( Image-match installing .... )
git clone https://github.com/ascribe/image-match.git

cd image-match
pip install numpy
pip install scipy
pip install .

REM ( Image-match drectory deleting.... )
cd ..
rmdir /S /Q image-match

REM ( html-similarity installing....  )
pip install html-similarity

REM ( etc package installing....  )
pip install PySimpleGUI
pip install pymysql
pip install selenium
pip install requests
pip install pillow
pip install webdriver-manager
pip install urllib3
pip install BeautifulSoup4
pip install loguru

REM ( Install project ....  )
git clone https://github.com/usuall/miniuptime.git

REM ---- Installation Completed ----