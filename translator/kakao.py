from dotenv import load_dotenv
import os, sys
import requests
from .utils import Language
from .utils import BaseRequestData
from .utils import BaseResponseData
from .utils import BaseRequest
import urllib

KAKAO_APP_KEY = os.getenv('KAKAO_APP_KEY')

KAKAO_LANGUAGE = {
    Language.ko.name: 'kr',
    Language.en.name: 'en',
    Language.cn.name: 'cn',
    Language.jp.name: 'jp',
}


class RequestData(BaseRequestData):

    def to_dict(self):
        return {
            'target_lang': self.target_language,
            'src_lang': self.source_language,
            'query': self.contents,
        }


class ResponseData(BaseResponseData):
    msg: str = ''

    def to_dict(self):
        return {
            'result': self.result,
            'translated_text': self.translated_text,
            'messsage': self.msg,
        }


class KakaoRequests(BaseRequest):
    url = 'https://kapi.kakao.com/v1/translation/translate'
    headers = {
        'Authorization': f'KakaoAK {KAKAO_APP_KEY}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    method = 'post'
    accepted_lang = KAKAO_LANGUAGE
    data = RequestData
    request_data_handler = RequestData
    response_data_handler = ResponseData


    def valid_data(self):
        if self.data.target_language not in self.accepted_lang:
            raise ValueError(f'{self.data.target_language} is not in accepted_lang')
        else:
            self.data.target_language = self.accepted_lang[self.data.target_language]

        if self.data.source_language not in self.accepted_lang:
            raise ValueError(f'{self.data.source_language} is not in accepted_lang')
        else:
            self.data.source_language = self.accepted_lang[self.data.source_language]

        return self.data.to_dict()


if __name__ == "__main__":
    kakao = KakaoRequests()
    kakao.set_data(
        target_language='en',
        source_language='ko',
        contents='hahahah')
    response = kakao.request_translate()
    print(response)