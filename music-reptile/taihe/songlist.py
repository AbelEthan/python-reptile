# -*-coding:utf-8-*-
import json
import random
import re
import time
import requests
import xlrd
import os
from lxml import etree
from xlutils.copy import copy
from taihe.SongInfo import SongInfo

user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",

]

headers = {
    'User-Agent': random.choice(user_agent)
}

path = 'http://music.taihe.com/'


# 获取歌单分类链接
def get_song_list_tag(url, list):
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    div = etree.HTML(res.text)
    song_list_urls = div.xpath('//p[@class="text-title"]/a/@href')
    for song_list_url in song_list_urls:
        list = get_song_list(song_list_url, list)
    return list


# 获取分类歌曲链接
def get_song_list(song_list_url, list):
    url = path + song_list_url
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    html = etree.HTML(res.text)
    song_urls = html.xpath('//span[@class="songname"]/a/@href')
    for song_url in song_urls:
        if '/song/' in song_url:
            list = download_mp3(song_url, list)
    return list


# 获取歌曲详细信息
def get_song_info(song_url, index):
    url = path + song_url
    res = requests.get(url, headers=headers)
    time.sleep(0.1)
    res.encoding = "utf-8"
    html = etree.HTML(res.text)
    img = html.xpath('//img[@class="music-song-ing"]/@src')
    title = html.xpath('//span[@class="name"]/text()')
    artist = html.xpath('//span[@class="author_list"]/@title')
    album = html.xpath('//p[@class="album desc"]/a/text()')
    publish = html.xpath('//p[@class="publish desc"]/text()')
    company = html.xpath('//p[@class="company desc"]/text()')
    lrc = html.xpath('//div[@id="lyricCont"]/@data-lrclink')
    try:
        print('%s这首歌是由%s于%s发行,%s的%s专辑里面的，图片%s,歌词%s. %s' % (
            title[0], company[0], publish[0], artist[0], album[0], img[0], lrc[0], index))
        index += 1
    except FileNotFoundError:
        pass
    except OSError:
        pass
    except IndexError:
        pass
    return index


# 下载歌曲信息
def download_mp3(song_url, list):
    time.sleep(2)
    # song_id = song_url.split('/song/')[1]
    # params = "callback=jQuery172009464779806914603_%s&songid=%s&from=web&_=%s" % (
    #     str(round(time.time() * 1000)), song_url, str(round(time.time() * 1000)))
    # url = "http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&%s" % params
    url = path + '/data/tingapi/v1/restserver/ting?method=baidu.ting.song.baseInfo&songid=%s&from=web' % song_url
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    # data = re.findall(r'\((.*?)\)\;$', res.text)
    try:
        data = json.loads(res.text)
        # file_link = data['bitrate']['file_link']
        # with open('E:\\web\\taihe\\music\\' + song_id + '.mp3', 'wb') as f:
        #     f.write(requests.get(file_link, headers=headers).content)
        title = data['content']['title']
        artist = data['content']['author']
        pic = data['content']['pic_big'].split('@')[0]
        lrc = data['content']['lrclink']
        album = data['content']['album_title']
        company = data['content']['si_proxycompany']
        song_info = SongInfo(song_url, title, artist, pic, lrc, album, company)
        print('正在存储第%s首[%s]的[%s]专辑的[%s]歌曲' % (len(list), artist, album, title))
        list.append(song_info)
    except KeyError:
        print('KeyError')
        pass
    except IndexError:
        print('IndexError')
        pass
    except FileNotFoundError:
        print('FileNotFoundError')
        pass
    except OSError:
        print('OSError')
        pass
    except RuntimeError:
        pass
    return list


# 导入信息到excel
def export_excel(data):
    xlsx = xlrd.open_workbook(r'taihe_song_infos.xls', formatting_info=True)
    wb = copy(xlsx)
    ws = wb.get_sheet(0)
    for info in data:
        num = data.index(info) + 1
        ws.write(num, 0, info.song_id)
        ws.write(num, 1, info.title)
        ws.write(num, 2, info.artist)
        ws.write(num, 3, info.pic)
        ws.write(num, 4, info.lrc)
        ws.write(num, 5, info.album)
        ws.write(num, 6, info.company)
    wb.save('taihe_song_infos.xls')


if __name__ == '__main__':
    start_time = time.time()
    limit = 20
    list = []
    filelist = os.listdir('E:\\web\\taihe\\music')
    # for num in range(1, 122):
    #     offset = limit * num
    #     url = path + 'songlist/tag/华语?orderType=1&offset=%s&third_type=' % offset
    #     list = get_song_list_tag(url, list)
    print(len(filelist))
    for file in filelist:
        song_id = file.split('.')[0]
        list = download_mp3(song_id, list)
    export_excel(list)
    print("請求用時：%s" % (time.time() - start_time))
