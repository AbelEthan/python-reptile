# -*-coding:utf-8-*-

import requests
import re
import time
import pandas as pd
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
                xlsx = xlrd.open_workbook(r'../excel/song.xls', formatting_info=True)
                wb = copy(xlsx)
                ws = wb.get_sheet(0)

                ws.write(index, 0, data[1])
                ws.write(index, 1, data[0])
                ws.write(index, 2, temp_text[1])
                wb.save("song.xls")
                print("正在写入：%s下的%s歌曲,%s" % (data[1], temp_text[1], index))
                index += 1
    return index


if __name__ == '__main__':
    startTime = time.time()
    index = 1
    limit = 35
    for num in range(0, 37):
        offset = num * limit
        hot_url = 'https://music.163.com/discover/playlist/?order=hot&cat=华语&limit=%s&offset=%s' % (limit, offset)
        index = get_page(hot_url, index)
    time.time() - startTime
    print("爬取数据成功，用时%s" % (time.time() - startTime))
