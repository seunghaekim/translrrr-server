import hashlib
from dataclasses import dataclass

@dataclass
class BaseRequestData:
    target_language: str
    source_language: str
    contents: str

    def to_dict(self):
        return {
            'target_language': self.target_language.strip(),
            'source_language': self.source_language.strip(),
            'contents': self.contents.strip(),
        }

    def valid(self):
        if self.contents is None:
            raise ValueError('contents value cannot be None')
        return True

    def contents_hash(self):
        return hashlib.sha1(self.contents.encode('utf-8')).hexdigest()