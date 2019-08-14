from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, url_for
)
from flaskr.db import get_db
from channels.ChannelRecognizer import ChannelRecognizer

app = Flask(__name__)
bp = Blueprint('crawler', __name__)


@bp.route('/')
def index():
    return render_template('crawler/create.html')


@bp.route('/<channel>', methods=['POST'])
def fetch_stream(channel):

    stream_url = request.form['url']

    error = None

    if not stream_url:
        error = 'The URL for a channel or playlist is required.'
        return render_template('crawler/404.html', error=error)

    if error is None:

        # TODO: validate the channel or playlist requested before to optimize time and avoid coupling
        old_stream = get_stream_videos(stream_url)

        if len(old_stream) > 0:
            return list_stream_videos(old_stream)

        else:
            cr = ChannelRecognizer()
            new_stream = cr.handle(channel, stream_url)

            # TODO: Render an empty view with error message if an invalid page or channel URL entered
            if len(new_stream) > 0:
                store_stream_videos(stream_url, new_stream)
                return list_stream_videos(new_stream)


def store_stream_videos(stream_url, stream):
    db = get_db()
    for i in stream:
        db.execute(
            'INSERT INTO videos (stream_url, video_url, title, views, duration, img_thumb, img_original)'
            'VALUES (?, ?, ?, ?, ? ,?, ?)',
            (stream_url, i['video_url'], i['title'], i['views'], i['duration'], i['img_thumb'], i['img_original'])
        )
        db.commit()


def get_stream_videos(stream_url):
    db = get_db()
    stream_videos = db.execute(
        'SELECT * FROM videos WHERE stream_url = ?', (stream_url,)
    ).fetchall()

    return stream_videos


def list_stream_videos(stream_videos):
    return render_template('crawler/index.html', videos=stream_videos)
