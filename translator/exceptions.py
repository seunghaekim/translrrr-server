class TranslatorExeptions(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ContentsHashNotExists(TranslatorExeptions):

    def __init__(self, msg="Contents Cache not exists"):
        super().__init__(msg)


class ContentsCacheNotExists(TranslatorExeptions):

    def __init__(self, msg="Contents Cache not exists"):
        super().__init__(msg)


class ContentsCacheExpired(TranslatorExeptions):

    def __init__(self, msg="Contents Cache not exists"):
        super().__init__(msg)