import time
import pandas as pd
import requests


# 下载歌词
def download_lrc(index, song_id, img_url):
    time.sleep(0.5)
    try:
        with open('E:\\web\\taihe\\img\\' + str(song_id) + '.png', 'wb') as f:
            f.write(requests.get(img_url).content)
            print('第%s个歌曲图片id：%s, 地址：%s' % (index, song_id, img_url))
    except FileNotFoundError:
        pass
    except OSError:
        pass


if __name__ == '__main__':
    df = pd.read_excel(r'taihe_song_infos.xls')
    img_urls = df['图片'].values
    song_ids = df['song_id'].values
    lens = len(song_ids)
    for num in range(lens):
        download_lrc(num, song_ids[num], img_urls[num])
