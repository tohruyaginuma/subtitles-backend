from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {
            'data': data,
            'error': None
        }

        response = renderer_context.get('response', None)
        if response and not str(response.status_code).startswith('2'):
            response_data['data'] = None
            response_data['error'] = data

        return super().render(response_data, accepted_media_type, renderer_context)