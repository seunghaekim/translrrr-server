from enum import Enum
from dataclasses import dataclass
import sys
import requests


class Language(Enum):
    ko = 'ko'
    en = 'en'
    cn = 'cn'
    jp = 'jp'


@dataclass
class BaseRequestData:
    target_language: str
    source_language: str
    contents: str

    def to_dict(self):
        return {
            'target_language': self.target_language,
            'source_language': self.source_language,
            'contents': self.contents,
        }

    def valid(self):
        if self.contents is None:
            raise ValueError('contents value cannot be None')
        return True


@dataclass
class BaseResponseData:
    translated_text: str = ''
    result: bool = False
    message: str = ''

    def to_dict(self):
        return {
            'translated_text': self.translated_text,
            'result': self.result,
            'message': self.message
        }


class BaseRequest:
    url: str
    headers: dict
    method: str
    accepted_lang: dict
    data: BaseRequestData
    request_data_handler = BaseRequestData
    response_data_handler = BaseResponseData

    def set_data(self, **kwargs):
        if 'vendor' in kwargs:
            del kwargs['vendor']
        self.data = self.request_data_handler(**kwargs)

    def valid_data(self):
        return self.data.to_dict()

    def request_params(self):
        params = {}
        if bool(self.headers) is not False:
            params['headers'] = self.headers

        valid_data = self.valid_data()
        if bool(valid_data) is not False:
            params['params'] = valid_data

        return params

    def request_translate(self):
        params = self.request_params()
        try:
            response = getattr(requests, self.method)(
                self.url, **params
            )
        except:
            print(sys.exc_info()[0])
            raise
        return self.response(response)

    def response(self, response):
        json = response.json()
        response_data = {'result': True}
        if response.status_code != 200:
            response_data['result'] = False
            response_data['message'] = json['msg']
        else:
            response_data['translated_text'] = json['translated_text']

        return self.response_data_handler(**response_data)