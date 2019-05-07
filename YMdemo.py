from selenium import webdriver
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import traceback

def openWeb():
    path = './chromedriver.exe'
    driver = webdriver.Chrome(path)
    url = 'https://www.wjx.top/m/36553538.aspx'  # url需要为手机上查看的
    try:
        driver.get(url)
    except (TimeoutError, ConnectionError):
        driver.get(url)

    # 获取所有的input输入框
    textinput = driver.find_element_by_class_name('fieldset').find_elements_by_tag_name('input')
    # 获取所有的单选框
    urchoice = driver.find_element_by_class_name('fieldset').find_elements_by_class_name('ui-radio')
    # 获取提交按钮
    submit = driver.find_element_by_id('ctlNext')
    for i in textinput:
        id = i.get_attribute('id')
        is_time_choice = i.get_attribute('data-role')
        print(id)
        # 判断，如果有一个问题中有两个input时，就判断为非正常输入框跳过。
        if '_' not in id and is_time_choice is None:
            name = i.get_attribute('verify')
            # 判断如果输入框的校验名字为姓名、手机、身份证号
            if name == '姓名':
                i.send_keys('张瑜')
            elif name == '手机':
                i.send_keys('18358441721')
            elif name == '身份证号':
                i.send_keys('33028219960225006X')
        # 判断如果输入框为时间输入框，则移除readonly属性
        elif is_time_choice == 'datebox':
            js = f"document.getElementById('{id}').removeAttribute('readonly')"
            driver.execute_script(js)
            i.send_keys('1996-02-25')
    # 判断如果单选框，如果性别是选择的，咋选择性别为女，有其它选择时记得增加条件
    for item in urchoice:
        if item.text == '女':
            item.click()
        elif item.text == '选项1':
            item.click()
    submit.click()
    # driver.close()


def print_time():
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"当前时间为：{time_now}")


def print_date():
    time_now = time.strftime("%Y-%m-%d", time.localtime())
    print(time_now)


if __name__ == '__main__':
    # openWeb()z
    # 设置定时任务\
    scheduler = BlockingScheduler()
    scheduler.add_job(print_time, 'interval', seconds=1)
    # scheduler.add_job(print_date, 'interval', seconds=3)
    scheduler.add_job(openWeb, 'date', run_date='2019-3-27 14:02:00')
    scheduler.start()
