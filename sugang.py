from selenium import webdriver
from bs4 import BeautifulSoup
import os
import sys
import time

# 수강 꾸러미에 담겨져 있을 때 자리가 나면 자동으로 수강신청 해주는 파이선 파일

def enrolment() :
    chromedriver = os.path.abspath('chromedriver.exe')

    #옵션 지정
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    #options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument('lang=ko_KR')    # 언어 설정
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome(executable_path=chromedriver, options=options)

    #입력 받은 인자로 get
    driver.get('https://sugang.knu.ac.kr/Sugang/comm/support/login/loginForm.action?redirUrl=%2FSugang%2Fcour%2FlectReq%2FonlineLectReq%2Flist.action')
    driver.implicitly_wait(3)

    stuNumber = driver.find_element_by_css_selector('#user\.stu_nbr')
    stuNumber.send_keys('') # 학번입력
    id = driver.find_element_by_css_selector('#user\.usr_id')
    id.send_keys('') # id 입력
    password = driver.find_element_by_css_selector('#user\.passwd')
    password.send_keys('') #password 입력

    driver.find_element_by_css_selector('#loginForm > table > tbody > tr:nth-child(4) > td > button.login').click()
    driver.find_element_by_css_selector('#lectPackReqGrid_3 > td.button').click()

def getDataFromMyKnu():
    # chromdriver의 위치 지정
    chromedriver = os.path.abspath('chromedriver.exe')

    #옵션 지정
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    #options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument('lang=ko_KR')    # 언어 설정
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    
    # 옵션 적용
    driver = webdriver.Chrome(executable_path=chromedriver, options=options)

    #입력 받은 인자로 get
    driver.get('http://my.knu.ac.kr/stpo/stpo/cour/lectReqCntEnq/list.action')
    driver.implicitly_wait(3)

    classCode = driver.find_element_by_css_selector('#search_subj_class_cde')
    classCode.send_keys('ELEC323006') # 교과목 코드 입력
    try:
        f = open("log.txt", 'r')
    except Exception:
        f = open("log.txt", 'w')

    f.close()
    
    while True:
        driver.find_element_by_css_selector('#contents > div > div > table.search.form > tbody > tr > td > button').click()

        total = driver.find_element_by_css_selector('#contents > div > div > table.resultT.form > tbody:nth-child(2) > tr > td.lect_quota').text
        reqCnt = driver.find_element_by_css_selector('#contents > div > div > table.resultT.form > tbody:nth-child(2) > tr > td.lect_req_cnt').text
        
        f = open("log.txt", 'a')
    
        now = time.localtime()
        f.write("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))

        if(int(total) == int(reqCnt)) :
            f.write('꽉 참\n')
        elif(int(total) > int(reqCnt)) :
            enrolment()
            print(total, reqCnt)
            f.write("사람 빠짐\n")  
            break
        
        f.close()
        time.sleep(5)

    print(total, reqCnt)
    
    driver.close()
    driver.quit()

if __name__ == '__main__':
    getDataFromMyKnu()
    #print(sys.argv[1])
