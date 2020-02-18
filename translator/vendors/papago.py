from dotenv import load_dotenv
import os, sys
import requests
from translator.utils import Language
from translator.vendors.base_response_data import BaseResponseData
from translator.vendors.base_request import BaseRequest
from translator.vendors.base_request_data import BaseRequestData
from translator.vendors.base_vendor_data import BaseVendorData
import urllib
from dotenv import load_dotenv

load_dotenv()

VENDOR = BaseVendorData(key='papago')

PAPAGO_CLIENT_ID = os.getenv('PAPAGO_CLIENT_ID')
PAPAGO_CLIENT_SECRET = os.getenv('PAPAGO_CLIENT_SECRET')

PAPAGO_LANGUAGE = {
    Language.ko.name: 'ko',
    Language.en.name: 'en',
    Language.cn.name: 'cn',
    Language.jp.name: 'jp',
}


class RequestData(BaseRequestData):

    def to_dict(self):
        return {
            'source': self.source_language,
            'target': self.target_language,
            'text': self.contents,
        }


class ResponseData(BaseResponseData):
    translatedText: str = ''

    def to_dict(self):
        return {
            'vendor': VENDOR.key,
            'result': self.result,
            'translated_text': self.translated_text,
            'message': self.message
        }


class PapagoRequests(BaseRequest):
    url = 'https://openapi.naver.com/v1/papago/n2mt'
    headers = {
        'X-Naver-Client-Id': PAPAGO_CLIENT_ID,
        'X-Naver-Client-Secret': PAPAGO_CLIENT_SECRET,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    method = 'post'
    accepted_lang = PAPAGO_LANGUAGE
    data = RequestData
    request_data_handler = RequestData
    response_data_handler = ResponseData
    vendor = VENDOR

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

    def request_params(self):
        params = {}
        if bool(self.headers) is not False:
            params['headers'] = self.headers

        valid_data = self.valid_data()
        if bool(valid_data) is not False:
            params['data'] = urllib.parse.urlencode(valid_data, encoding='UTF-8', doseq=True)

        return params

    def response(self, response):
        json = response.json()
        response_data = {'result': True}
        if response.status_code != 200:
            response_data['result'] = False
            response_data['message'] = "%s(errorCode: %s)"%(json['errorMessage'], json['errorCode'])
        else:
            response_data['translated_text'] = json['message']['result']['translatedText']

        responsedata_obj = self.response_data_handler(**response_data)
        if response_data['result'] is True:
            self.save_cache(responsedata_obj)
        return responsedata_obj
