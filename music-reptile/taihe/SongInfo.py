# -*-coding:utf-8-*-

class SongInfo:
    def __init__(self, song_id, title, artist, pic, lrc, album, company):
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.pic = pic
        self.lrc = lrc
        self.album = album
        self.company = company

    def __str__(self):
        return 'song_id=%s, title=%s,artist=%s,pic=%s,lrc=%s,album=%s,company=%s' % (
            self.song_id, self.title, self.artist, self.pic, self.lrc, self.album, self.company)
