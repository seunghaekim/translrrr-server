import os, sys
import requests
from translator.utils import Language
from translator.vendors.base_request_data import BaseRequestData
from translator.vendors.base_response_data import BaseResponseData
from translator.vendors.base_request import BaseRequest
from translator.vendors.base_vendor_data import BaseVendorData
import urllib
import itertools
from dotenv import load_dotenv

load_dotenv()

VENDOR = BaseVendorData(key="kakao")

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
            'target_lang': KAKAO_LANGUAGE[self.target_language],
            'src_lang': KAKAO_LANGUAGE[self.source_language],
            'query': self.contents,
        }


class ResponseData(BaseResponseData):
    msg: str = ''

    def to_dict(self):
        return {
            'vendor': VENDOR.key,
            'result': self.result,
            'translated_text': self.get_translated_text(),
            'messsage': self.msg,
        }

    def get_translated_text(self):
        return " ".join(list(itertools.chain.from_iterable(self.translated_text)))


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
    vendor = VENDOR


    def valid_data(self):
        if self.data.target_language not in self.accepted_lang:
            raise ValueError(f'{self.data.target_language} is not in accepted_lang')

        if self.data.source_language not in self.accepted_lang:
            raise ValueError(f'{self.data.source_language} is not in accepted_lang')

        return self.data.to_dict()
