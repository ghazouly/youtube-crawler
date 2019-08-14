import abc


class IChannelRecognizer:

    def __init__(self, channel, stream_url):
        self.channel = channel
        self.stream_url = stream_url

    def handle(self):
        pass
