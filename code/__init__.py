# -*- cording : utf-8 -*-

import requests
from lxml import html
from fake_useragent import UserAgent
import sys, os
import logging

class download:
    def filetender(url, is_subtitle=False):
        pass

    def crawling(url):
        with requests.session() as s:
            s.headers.update({'User-Agent' : str(UserAgent().chrome)})
            res = s.get(url, allow_redirects=True)
            if not res.status_code == 200:
                return False
            content = html.fromstring(res.content)
        return content

class torrentmi(download):
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
            print(title)
            if t.xpath('./td[2]/a/span[2]/span/text()')[0] in ['무자막']:
                continue
            elif t.xpath('./td[2]/a/span[2]/span/text()')[0] in ['한국영화', '자체자막']:
                is_subtitle = False
                torrentmi.child(torrentmi.crawling('https://www.torrentmi.com/' + link))
            else:
                is_subtitle = True
                torrentmi.child(torrentmi.crawling('https://www.torrentmi.com/' + link))

    def child(content):
        lists = content.xpath('//div[@class="downLoad"]')
        for i in lists:
            if any(x in i.xpath('./a/text()')[0] for x in [".smi", ".srt", ".ass"]):
                print("\t 자막 : " + i.xpath('./a/text()')[0])
            elif any(x in i.xpath('./a/text()')[0] for x in [".torrent"]):
                print("\t 씨앗 : " + i.xpath('./a/text()')[0])
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
        * Transmission 외에 다른 클라이언트 처리시 방안강구 => is_dir의 class???
'''


if __name__ == "__main__":
    torrentmi('영화', 'https://www.torrentmi.com/list.php?b_id=tmovie')