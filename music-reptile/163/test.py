# coding:utf-8
from html.parser import HTMLParser

import requests
import re
import time
import xlrd
from xlutils.copy import copy
from lxml import etree  # xpath

headers = {
    'Referer': 'https://music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}


def get_page(url, index):
    res = requests.get(url, headers=headers)
    data = re.findall('<a title="(.*?)" href="/playlist\?id=(\d+)" class="msk"></a>', res.text)
    for item in data:
        index = get_songs(item, index)
        index += 1
    return index


def get_songs(data, index):
    playlist_url = 'https://music.163.com/playlist?id=%s' % data[1]

    res = requests.get(playlist_url, headers=headers)
    obj_nodes = etree.HTML(res.text)
    node_texts = obj_nodes.xpath('//div[@id="song-list-pre-cache"]//a/@href')
    if len(node_texts) > 0:
        for nodeText in node_texts:
            re.findall(r'id=(\d+)', nodeText)
            if 'id=' in nodeText:
                temp_text = nodeText.split('id=')
                get_music_info(temp_text[1], index, data[1])
                index += 1
    return index


def get_music_info(song_id, index, playlist_id):
    music_url = 'https://music.163.com/song?id=%s' % song_id
    res = requests.get(music_url, headers=headers)

    obj_nodes = etree.HTML(res.text)
    img = obj_nodes.xpath('//img/@data-src')
    title = obj_nodes.xpath('//em[@class="f-ff2"]/text()')
    author = obj_nodes.xpath('//div[@class="cnt"]//span/@title')
    # lrc = obj_nodes.xpath('//div[@id="lyric-content"]')[0]
    # lrc = etree.tostring(lrc, encoding='utf-8')
    # print(lrc)
    print('正在导入%s下的id:%s,歌曲是：%s的%s，图片是%s的数据: %s' % (playlist_id, song_id, author, title, img, index))

    xlsx = xlrd.open_workbook(filename='../excel/music.xls', formatting_info=True)
    wb = copy(xlsx)
    ws = wb.get_sheet(0)

    ws.write(index, 0, song_id)
    ws.write(index, 1, title)
    ws.write(index, 2, author)
    ws.write(index, 3, img)
    # ws.write(index, 4, str(lrc))

    wb.save("music.xls")


if __name__ == '__main__':
    startTime = time.time()
    limit = 35
    index = 1
    for num in range(0, 38):
        offset = num * limit
        hot_url = 'https://music.163.com/discover/playlist/?order=hot&cat=全部&limit=%s&offset=%s' % (limit, offset)
        index = get_page(hot_url, index)
        index += 1
    time.time() - startTime
    print("爬取数据成功，用时%s" % (time.time() - startTime))
