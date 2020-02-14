from flask_restful import Resource
from flask_restful import reqparse
from .kakao import KakaoRequests
from .papago import PapagoRequests


class Translator(Resource):

    translators = { 
        'kakao': KakaoRequests,
        'papago': PapagoRequests
    }

    def params(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('source_language', type=str)
            parser.add_argument('target_language', type=str)
            parser.add_argument('vendor', type=str),
            parser.add_argument('contents', type=str)

            params = parser.parse_args()

            return params

        except Exception as e:
            return {
                'error': str(e)
            }

    def post(self):
        params = self.params()
        result = []
        for key in self.translators:
            translator = self.translators[key]()
            translator.set_data(**params)
            response = translator.request_translate()
            result.append(response.to_dict())

        return {
            'status': 'succes',
            'data': result
        }