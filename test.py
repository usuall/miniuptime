

import cv2, time, os
from PIL import ImageChops    
    
'''
    URL healthcheck dashboard introduction...
    ....
    .... copyright usuall@gmail.com
    .... mini project
    .... 
'''
def image_diff_opencv(src, dest):
    

    
    # path = 'D:\\DevOPS\\project\\miniuptime\\data\\htdocs\\capture\\'
    
    
    # src = path + 'orign\\' + src
    # dest = path + 'daily\\' + dest
    # img_diff_path = path + 'diff\\'
    img_diff_path = ''
    
    print (src, dest)
    diff = ImageChops.difference(src, dest)
    diff.save(img_diff_path + 'diff.png')
    
    # 파일생성 대기
    while not os.path.exists(img_diff_path + 'diff.png'):
        time.sleep(1)
        
        
        
    
    src_img = cv2.imread(src)
    dest_img = cv2.imread(dest)
    diff_img = cv2.imread(img_diff_path + 'diff.png')
    
    gray = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
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
    
if __name__ == '__main__':
    
    from PIL import Image
    
    file_name ='0004_site.png'
    
    src  = '0260_site1.png'
    dest = '0260_site2.png'
    # image_diff_opencv(src, dest)
    
    
    img_diff_path = ''
    
    print (src, dest)
    im1 = Image.open(src)
    im2 = Image.open(dest)
    diff = ImageChops.difference(im1, im2)
    diff.save(img_diff_path + 'diff.png')
    
    # 파일생성 대기
    while not os.path.exists(img_diff_path + 'diff.png'):
        time.sleep(1)
        
        
        
    
    src_img = cv2.imread(src)
    dest_img = cv2.imread(dest)
    diff_img = cv2.imread(img_diff_path + 'diff.png')
    
    gray = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
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
    
    
    
    
         
