# -*- cording : utf-8 -*-

import requests
from lxml import html
from fake_useragent import UserAgent
import sys, os
import logging
import torrent_parser
from fuzzywuzzy import fuzz

class analysis:
    def torrent_info():
        is_dir
        pass

    def media_info(title, year):
        pass

    def match_score(src, dst):
        return(fuzz.ratio(src, dst))

class download:
    def crawling(url, refer=None):
        with requests.session() as s:
            if refer:
                s.headers.update({'refer' : refer})
            s.headers.update({'User-Agent' : str(UserAgent().chrome)})
            res = s.get(url, allow_redirects=True)
            if not res.status_code == 200:
                return False
            content = html.fromstring(res.content)
        return content
    
    def savefile(content, filename):
        try:
            with open(filename, 'wb') as f:
                f.write(content)
            return True
        except:
            return False

class filetner(download):
    #http://file.filetender.com/down.php?link=
    def filetender(url):
        pass

class torrentmi(download, analysis):
    def __init__(self, dir, url):
        self.dir = dir
        self.url = url
        torrentmi.main(torrentmi.crawling(self.url))

    def main(content):
        tables = content.xpath('/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/table/tbody/tr')
        for t in tables:
            title = t.xpath('./td[2]/a/span[1]/text()')[0]
            genre = t.xpath('./td[2]/a/em/text()')[0]
            link = t.xpath('./td[2]/a/@href')[0]
            if t.xpath('./td[2]/a/span[2]/span/text()')[0] in ['무자막']:
                continue
            elif t.xpath('./td[2]/a/span[2]/span/text()')[0] in ['한국영화', '자체자막']:
                print(title)
                is_subtitle = False
                torrentmi.child(torrentmi.crawling('https://www.torrentmi.com/' + link))
            else:
                print(title)
                is_subtitle = True
                torrentmi.child(torrentmi.crawling('https://www.torrentmi.com/' + link), is_subtitle = True)

    def child(content, is_subtitle = False):
        is_extsub = False
        sub_lists = {}
        seed_lists = {}

        lists = content.xpath('//div[@class="downLoad"]')
        for i in lists:
            if any(x in i.xpath('./a/text()')[0] for x in [".torrent"]):
                # Todo : Logging
                #seed_lists[i.xpath('./a/text()')[0]] = i.xpath('./a/@href')[0]
                print(i.xpath('./a/@href')[0])
            elif any(x in i.xpath('./a/text()')[0] for x in [".smi", ".srt", ".ass"]):
                # Todo : Logging
                is_extsub = True
                #sub_lists[i.xpath('./a/text()')[0]] = i.xpath('./a/@href')[0]
                print(i.xpath('./a/@href')[0])
            else:
                # Todo : Logging
                continue
        
                
'''
#Todo
    - 자막이 여러개 일 때 처리
        1) 한 씨앗에 파일이 여러개로 나누어져 있는 경우
        2) bitrate(720p, 1080p 등)에 대한 자막이 각각 있는 경우
        3) 잘못된 자막이 있는 경우
    - 구분에서 잘못된 경우
        1) 자막파일 유무 확인
    - 씨앗에 내용이 폴더로 묶여 있는 경우
        * 씨앗파일 정보가져오기?
        * 안되는 경우 Transmissionrpc에서 정보가져오기
        * 마그넷인 경우....답 있나 -_-
        * Transmission 외에 다른 클라이언트 처리시 방안강구 => is_dir의 추상화???
'''


if __name__ == "__main__":
    torrentmi('영화', 'https://www.torrentmi.com/list.php?b_id=tmovie')
    