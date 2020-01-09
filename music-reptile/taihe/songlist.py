# -*-coding:utf-8-*-
import json
import re
import time
import requests
import xlrd
from lxml import etree
from xlutils.copy import copy

from taihe.SongInfo import SongInfo

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
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
    song_id = song_url.split('/song/')[1]
    params = "callback=jQuery172009464779806914603_%s&songid=%s&from=web&_=%s" % (
        str(round(time.time() * 1000)), song_id, str(round(time.time() * 1000)))
    url = "http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&%s" % params

    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    data = re.findall(r'\((.*?)\)\;$', res.text)
    data = json.loads(data[0])

    try:
        file_link = data['bitrate']['file_link']
        with open('' + song_id + '.mp3', 'web') as f:
            f.write(requests.get(file_link, headers).content)
        title = data['songinfo']['title']
        artist = data['songinfo']['artist']
        pic = data['songinfo']['pic_big'].split('@')[0]
        lrc = data['songinfo']['lrclink']
        album = data['songinfo']['album_title']
        company = data['songinfo']['si_proxycompany']
        song_info = SongInfo(song_id, title, artist, pic, lrc, album, company)
        print('正在存储第%s首[%s]的[%s]专辑的[%s]歌曲' % (len(list), artist, album, title))
        list.append(song_info)
    except KeyError:
        pass
    except FileNotFoundError:
        pass
    except OSError:
        pass
    return list


# 导入信息到excel
def export_excel(data):
    xlsx = xlrd.open_workbook(r'../excel/taihe_song_info.xls', formatting_info=True)
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
    wb.save('../excel/taihe_song_info.xls')


if __name__ == '__main__':
    start_time = time.time()
    url = path + 'songlist/tag/华语?orderType=1&offset=0&third_type='
    list = []
    list = get_song_list_tag(url, list)
    export_excel(list)
    print("請求用時：%s" % (time.time() - start_time))
