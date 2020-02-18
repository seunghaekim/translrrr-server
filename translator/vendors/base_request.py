import requests
from translator.vendors.base_request_data import BaseRequestData
from translator.vendors.base_response_data import BaseResponseData
from translator import service
from translator import exceptions
import itertools


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

    def translate(self):
        try:
            cache = self.get_cache()
        except exceptions.ContentsCacheExpired:
            return self.request_translate()

        if cache is False:
            return self.request_translate()
        return self.response_cache(cache)

    def get_cache(self):
        contentshash = self.data.contents_hash()
        contentshash_obj = service.get_contents_hash_obj(contentshash)
        if contentshash_obj is False:
            contentshash_obj = service.create_contents_hash(contentshash)

        data = {
            'contentshash_obj': contentshash_obj,
            'vendor': self.vendor.key,
            'source': self.data.source_language,
            'target': self.data.target_language
        }

        contentscache_obj = service.get_contents_cache(**data)
        if contentscache_obj is False:
            return False
        if contentscache_obj.translated_text == '':
            return False

        return contentscache_obj

    def response_cache(self, cache):
        return cache

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

        responsedata_obj = self.response_data_handler(**response_data)
        if response_data['result'] is True:
            self.save_cache(responsedata_obj)
        return responsedata_obj

    def save_cache(self, responsedata_obj):
        contentshash = self.data.contents_hash()
        contentshash_obj = service.get_contents_hash_obj(contentshash)

        cache_data = {
            'contentshash_obj': contentshash_obj,
            'vendor': self.vendor.key,
            'source': self.data.source_language,
            'target': self.data.target_language,
            'translated_text': responsedata_obj.get_translated_text()
        }

        cache_result = service.create_or_update_contents_cache(**cache_data)
        pass
