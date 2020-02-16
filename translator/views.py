import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.utils import safe_request_post
from translator.vendors.papago import PapagoRequests
from translator.vendors.kakao import KakaoRequests

class TranslatorView(APIView):

    __translators = {
        'kakao': KakaoRequests,
        'papago': PapagoRequests
    }

    def params(self, request):
        params = {
            'source_language': safe_request_post(request, 'source_language'),
            'target_language': safe_request_post(request, 'target_language'),
            'vendor': safe_request_post(request, 'vendor'),
            'contents': safe_request_post(request, 'contents'),
        }

        for key in ['source_language', 'target_language', 'contents']:
            if params[key] is not None:
                continue

            if key in request.data:
                params[key] = request.data[key]
            else:
                return Response({
                    'status': False,
                    'message': f'Request Parameter: {key} is required'
                }, status=status.HTTP_400_BAD_REQUEST)

        return params

    def post(self, request):
        params = self.params(request)
        if type(params).__name__ == 'Response':
            return params

        result = []
        for key in self.__translators:
            translator = self.__translators[key]()
            translator.set_data(**params)
            response = translator.translate()
            data = response.to_dict()
            data['vendor'] = key
            result.append(data)

        return Response({
            'status': 'success',
            'data': result
        })