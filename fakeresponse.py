class FakeResponse(object):
    def __init__(self, content, hash=None, apparent_encoding=None):
        self.status_code = 200
        self.encoding = 'Cp1252'  # we overwrite this flag
        self.apparent_encoding = apparent_encoding
        self.headers = {'content-md5': hash}
        self.content = content  # is a byte string

    @property
    def text(self):
        return self.content.decode(self.encoding)
