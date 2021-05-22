from selenium import webdriver
from time import sleep
import datetime
from selenium.webdriver.common.keys import Keys
#ActionChainsを使う時は、下記のようにActionChainsのクラスをロードする
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup, BeautifulStoneSoup
from selenium.webdriver.chrome.options import Options
import requests
import json

# mac環境用
import chromedriver_binary

import settings

# 本番用トークンID
line_notify_token = settings.LINE_TOKEN
# LINE Notify APIのURL
line_notify_api = settings.LINE_API
ID = settings.ID
PASSWORD = settings.PWD

class JobCan:
    #初期化処理
    def __init__(self):
        self.options = Options()
        #ブラウザ立ち上げは処理が重たくなるので本番環境ではheadlessモードを採用
        # self.options.add_argument('--headless')
        self.options.add_argument('--window-size=1920,1080')

        #windows環境用
        # self.driver = webdriver.Chrome('C:\work\chromedriver_win32\chromedriver')

        #mac環境用
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def open_url(self, url):
        self.driver.get(url)

    def login(self, id, password):
        self.driver.find_element_by_xpath('//input[@id="client_manager_login_id"]').send_keys(id)
        self.driver.find_element_by_xpath('//input[@id="client_login_password"]').send_keys(password)
        self.driver.find_element_by_xpath('//*[@class="btn btn-info btn-block"]').click()

    def shift_page(self):
        self.driver.find_element_by_xpath('//*[@class="menuCenter"]').click()
        element = self.driver.find_element_by_link_text('シフト予定表').click()

    def select_dropdown(self):
        # ドロップダウンのselectのときはclickを使わないほうが良いっぽい
        dropdown = self.driver.find_element_by_id("type-combo")
        select = Select(dropdown)
        select.select_by_value('day2')

    def select_calender(self):
        #現在日時を取得して選択していく

        year = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/form/table[1]/tbody/tr[6]/td/div[2]/select[1]")
        selectyear = Select(year)
        currentyear = datetime.datetime.now().strftime('%Y')
        selectyear.select_by_value(currentyear)

        month = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/form/table[1]/tbody/tr[6]/td/div[2]/select[2]")
        selectmonth = Select(month)
        # 0埋めする。表示は05でもvalueの値は5になっている
        currentmonth = datetime.datetime.now().strftime('%-m')
        selectmonth.select_by_value(currentmonth)

        day = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/form/table[1]/tbody/tr[6]/td/div[2]/select[3]")
        selectday = Select(day)
        currentday = datetime.datetime.now()
        selectday.select_by_value(currentday)

        #表示ボタンクリック
        btn = self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div/div/div/div/div[2]/div/form/div[1]/a/div')
        btn.click()

    def get_shift_list(self):
        #htmlを調べる
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        #シフトテーブルを選択。tableタグが他にもあるので配列から特定
        shift_list = soup.find_all("table")[5]

        #trタグからスタッフ一覧のみを取得。0,1には要らない要素が隠れているので排除。
        member_lists = shift_list.find_all("tr")[2:]

        #メンバー値を取得していく
        member_text = "知るカフェシフト表（笑）"
        for member_list in member_lists:
            # arr.append(f'@{member_list.find_all("td")[0].text} :{member_list.find_all("td")[1].text}')
            member_text+=(f'{member_list.find_all("td")[0].text} :{member_list.find_all("td")[1].text}') +"\n"
            # print(f'@{member_list.find_all("td")[0].text}')
            # print(f'出勤時間:{member_list.find_all("td")[1].text}')

        message = member_text
        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + line_notify_token}  # Notify URL
        line_notify = requests.post(line_notify_api, data=payload, headers=headers)

        #処理が終わったらwindowを閉じる
        self.driver.close()
        self.driver.quit()

if __name__ == '__main__':
    driver = JobCan()
    driver.open_url('http://jobcan.jp/login/client/?client_login_id=all-SHIRUCAFE')
    driver.login(ID, PASSWORD)
    driver.shift_page()
    driver.select_dropdown()
    driver.select_calender()
    driver.get_shift_list()


