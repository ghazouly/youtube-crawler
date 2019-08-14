import re
import time
import requests
from bs4 import BeautifulSoup
import urllib

from flask import render_template


class YoutubeAdaptor:

    def __init__(self, stream_url):
        self.stream_url = stream_url

    def get_stream_list(self):

        # TODO: Regex validation over other urls
        # pattern = re.compile(r"^(https?\:\/\/)?((www\.)?youtube\.com|youtu\.?be)\/.+$")
        # pattern.search(self.stream_url):

        # parsing html page
        try:
            stream_title = []
            stream_views = []
            stream_duration = []
            stream_video_url = []
            stream_img_thumb = []
            stream_img_original = []

            # do playlist stuff
            if not self.stream_url.find('list') == -1:

                # case the link represent a single video in a playlist, get the playlist URL
                if not self.stream_url.find('watch') == -1:
                    self.stream_url = "https://www.youtube.com/playlist?" + self.stream_url.split('&')[1]

                request_markup = requests.get(self.stream_url)
                soup = BeautifulSoup(request_markup.content, features="html.parser")

                # crawl video title and url
                for title_url in soup.find_all('tr', {"class": "pl-video yt-uix-tile"}):
                    stream_title.append(title_url['data-title'])
                    stream_video_url.append('watch?v=' + title_url['data-video-id'])

                # crawl video duration
                for duration in soup.find_all('div', {"class": "timestamp"}):
                    stream_duration.append(duration.text)
                    # just a placeholder, youtube doesn't reveal views per video on playlist page
                    stream_views.append('')

                # crawl video image thumb and original
                for img in soup.find_all('img', {"width": "72"}):
                    thumb_name = "%s.webp" % int(round(time.time() * 1000))
                    urllib.urlretrieve(img['data-thumb'], "flaskr/static/thumb/%s" % thumb_name)
                    stream_img_thumb.append(thumb_name)
                    # TODO: Get base_url for youtube original image to be saved as well
                    stream_img_original.append(img['src'])

            # do channel stuff
            else:

                request_markup = requests.get(self.stream_url)
                soup = BeautifulSoup(request_markup.content, features="html.parser")

                # crawl video title and url
                for title_url in soup.find_all('a', {"class": "yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2"}):
                    stream_title.append(title_url['title'])
                    stream_video_url.append(title_url['href'])

                # crawl video views
                for view in soup.find_all('ul', {"class": "yt-lockup-meta-info"}):
                    # TODO: Enhance this more
                    stream_views.append(view.text)

                # crawl video duration
                for duration in soup.find_all('span', {"class": "video-time"}):
                    stream_duration.append(duration.text)

                # crawl video image thumb and original
                for img in soup.find_all('img', {"width": "196"}):
                    thumb_name = "%s.webp" % int(round(time.time() * 1000))
                    urllib.urlretrieve(img['data-thumb'], "flaskr/static/thumb/%s" % thumb_name)
                    stream_img_thumb.append(thumb_name)
                    # TODO: Get base_url for youtube original image to be saved as well
                    stream_img_original.append(img['src'])

            # Mapping all crawled data extracted for database loading
            stream = [
                {
                    'title': a,
                    'video_url': b,
                    'views': c,
                    'duration': d,
                    'img_thumb': e,
                    'img_original': f,
                }
                for a, b, c, d, e, f in zip(
                    stream_title,
                    stream_video_url,
                    stream_views,
                    stream_duration,
                    stream_img_thumb,
                    stream_img_original
                )
            ]

            return stream

        # TODO: Detailed handling for crawling errors
        except requests.exceptions.ConnectionError:
            return []
