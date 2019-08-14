import abc
from flask import flash
from flaskr.channels import IChannelRecognizer
from flaskr.channels.youtube.YoutubeAdaptor import YoutubeAdaptor


# TODO: Passing ABC Interface IChannelRecognizer
class ChannelRecognizer:

    def __init__(self):
        pass

    available_channels = {
        1: "youtube",
    }

    def handle(self, channel, stream_url):

        error = None

        # case channel to be crawled is youtube then execute youtube stuff..
        if channel == self.available_channels.get(1):
            youtube = YoutubeAdaptor(stream_url)
            return youtube.get_stream_list()

        # TODO: Render a view to handle other channels error message
        else:
            error = 'We\'re sorry that we currently supporting Youtube only.'

        flash(error)

