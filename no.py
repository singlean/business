from selenium import webdriver
from threading import Thread
import re,json


def get_content(self):
    # 创建一个无界面谷歌浏览器
    opt = webdriver.ChromeOptions()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=opt)
    while True:
        song_url_list = self.song_url_queue.get()
        for url_dict in song_url_list:
            url = url_dict["song_list_url"]
            # 获取url，发送请求，获取响应内容
            print(url)
            driver.get(url)
            # 切换到需要获取信息的iframe中
            driver.switch_to_frame("g_iframe")
            # 　分组，对每一组进行处理
            tr_list = driver.find_elements_by_xpath(".//table[@class='m-table ']/tbody/tr")
            # 需要保存的信息
            content_list = []
            page_info = {}
            page_info["page_title"] = url_dict["song_list_title"]
            try:
                page_info["introduce"] = driver.find_element_by_xpath(
                    ".//div[@class='cntc']/p[@class='intr f-brk']").text
            except:
                page_info["introduce"] = None
            page_info["song_list_collect"] = driver.find_element_by_xpath(
                ".//a[@class='u-btni u-btni-fav ']").get_attribute("data-count")
            i_list = driver.find_elements_by_xpath(".//div[@class='tags f-cb']/a[@class='u-tag']")
            desc = []
            for i in i_list:
                i = i.find_element_by_xpath("./i").text
                desc.append(i)
            page_info["song_list_label"] = desc
            page_info["play-count"] = driver.find_element_by_xpath(".//strong[@id='play-count']").text
            page_info["song_count"] = driver.find_element_by_xpath(
                ".//span[@class='sub s-fc3']/span[@id='playlist-track-count']").text

            content_list.append(page_info)
            # 使用xpath循环获取信息
            for tr in tr_list:
                item = {}
                item["rank_num"] = tr.find_element_by_xpath(".//span[@class='num']").text
                item["title"] = tr.find_element_by_xpath(".//span[@class='txt']/a/b").get_attribute("title")
                item["time"] = tr.find_element_by_xpath(".//span[@class='u-dur ']").text
                item["author_name"] = tr.find_element_by_xpath(".//div[@class='text']").get_attribute("title")
                item["music"] = tr.find_element_by_xpath(".//span[@class='txt']/a").get_attribute("href")
                item["author_musics"] = tr.find_element_by_xpath(".//a[@hidefocus='true']").get_attribute("href")
                content_list.append(item)
            # 返回数据内容
            self.content_list_queue.put(content_list)
        self.song_url_queue.task_done()


def save_content(self):
    while True:
        content_list = self.content_list_queue.get()
        title = content_list[0]["page_title"]
        title = re.sub(r"/", ":", title)
        with open("/home/python/Desktop/musicdata/" + title + ".json", "w")as f:
            f.write(json.dumps(content_list, ensure_ascii=False, indent=2))
        print("保存成功")
        self.content_list_queue.task_done()


def run(self):
    # 获取所有分类的url地址
    self.get_type_url()
    # 获取所有歌单的url地址
    thread_list = []
    for i in range(3):
        t_song_url = Thread(target=self.get_song_list_url)
        thread_list.append(t_song_url)
    # 获取每个歌单的数据
    for i in range(5):
        t_content = Thread(target=self.get_content)
        thread_list.append(t_content)
    # 保存获取到底数据
    for i in range(3):
        t_save = Thread(target=self.save_content)
        thread_list.append(t_save)

    for t in thread_list:
        t.setDaemon(True)
        t.start()

    for q in [self.type_url_queue, self.song_url_queue, self.content_list_queue]:
        q.join()

    print("{}程序完成{}".format("*" * 10, "*" * 10))