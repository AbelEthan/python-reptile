import time

import pandas as pd
import requests


# 下载歌词
def download_lrc(index, songid, lrc_url):
    time.sleep(0.5)
    try:
        with open('E:\\web\\taihe\\lrc\\' + str(songid) + '.lrc', 'wb') as f:
            f.write(requests.get(lrc_url).content)
            print('第%s个,歌词id：%s, 地址：%s' % (index, songid, lrc_url))
    except FileNotFoundError:
        pass
    except OSError:
        pass


if __name__ == '__main__':
    df = pd.read_excel(r'taihe_song_infos.xls')
    lrc_urls = df['歌词'].values
    song_ids = df['song_id'].values
    lens = len(song_ids)
    for num in range(lens):
        download_lrc(num, song_ids[num], lrc_urls[num])
