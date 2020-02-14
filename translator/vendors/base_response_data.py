from dataclasses import dataclass


@dataclass
class BaseResponseData:
    translated_text: str = ''
    result: bool = False
    message: str = ''

    def to_dict(self):
        return {
            'translated_text': self.get_translated_text(),
            'result': self.result,
            'message': self.message
        }

    def get_translated_text(self):
        return self.translated_text