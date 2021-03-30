import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import datetime
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select


def main():
    UserName='########' # ########替换为学号
    Password='********' # ********替换为密码
    url = "http://ehall.xidian.edu.cn/xsfw/sys/ssxfapp/*default/index.do#/indexpagenew"
    dateToday = datetime.date.today().strftime("%Y-%m-%d")
    openTime = dateToday + " 9:00:00"

    # 创建浏览器对象
    chromeOptions = Options()
    # 关闭Chrome上部提示语 "Chrome正在受到自动软件的控制"
    chromeOptions.add_experimental_option(
        "excludeSwitches", ['enable-automation'])
    # 允许浏览器重定向，Framebusting requires same-origin or a user gesture
    chromeOptions.add_argument("disable-web-security")
    driver = webdriver.Chrome(os.path.join(
        "./chromeDriver", "chromedriver.exe"), chrome_options=chromeOptions)

    driver.get(url)
    inputUserName = driver.find_elements_by_id('username')
    inputUserName[0].send_keys(UserName)  
    inputPassword = driver.find_elements_by_id('password')
    inputPassword[0].send_keys(Password)  
    driver.find_element_by_css_selector(
        "[class='auth_login_btn primary full_width']").click()

    try:
        print(driver.find_element_by_css_selector(
            '[class="auth_error"]').text)
        exit()
    except Exception:
        pass

    while True:
        try:
            driver.find_element_by_css_selector(
                '[data-action="selectRoom"]').click()
            break
        except Exception:
            print("找不到正式选房按钮")
            if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') < openTime:
                localTime = datetime.datetime.strptime(
                    openTime, "%Y-%m-%d %H:%M:%S")
                print('预约未开始，离开始还有', (localTime-datetime.datetime.now()))
            else:
                print('预约开始')

    try:
        WebDriverWait(driver, 60, 0.1).until(
            lambda x: x.find_element_by_id('oneKeyChooseBtn'))
        driver.find_element_by_id('oneKeyChooseBtn').click()

    except Exception:
        print(url, '服务器超时，或其他原因！')


if __name__ == '__main__':
    main()
    print('按任意键结束...')
    os.system('pause>>nul')
