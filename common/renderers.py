import uuid

from rest_framework.exceptions import APIException
from rest_framework.renderers import BaseRenderer
from rest_framework.settings import api_settings
from rest_framework.utils import json, encoders


class ApiRenderer(BaseRenderer):
    """Render the custom response structure for application.
    Best practice proposed by DRF is to use 'renderer' classes. A renderer manipulates and returns structured response.
    Django uses renderer's like Template Renderer and DRF benefits this feature and provides API Renderer's.
    By this action all views that extend DRF generic views will use renderer. If you needed to override setting you can
    use renderer_classes attribute for generic view classes and @renderer_classes decorator for api view functions.

    Source: https://stackoverflow.com/questions/53910545/how-overwrite-response-class-in-django-rest-framework-drf

    This will manage transformation of fields at root level.
    For error messages and success messages, They will be listed in a ResponseMessage class have static method
    get_message('MESSAGE_KEY').
    """

    media_type = "application/json"
    format = "json"
    encoder_class = encoders.JSONEncoder
    ensure_ascii = not api_settings.UNICODE_JSON
    compact = api_settings.COMPACT_JSON
    strict = api_settings.STRICT_JSON
    response_body = dict()

    @staticmethod
    def extract_error_messages(payload: any, error_messages):
        if isinstance(payload, dict):
            for key, value in payload.items():
                # format key: replace <_ underscore> with < space>
                format_key = (
                    key.replace("_", " ") if isinstance(key, str) else "{}".format(key)
                )
                format_key = format_key[0:1].upper() + format_key[1:]
                if isinstance(value, dict):
                    ApiRenderer.extract_error_messages(value, error_messages)
                if isinstance(value, list):
                    if isinstance(value[0], str):
                        error_messages += [", ".join(value).replace("This", format_key)]
                    elif isinstance(value[0], dict):
                        ApiRenderer.extract_error_messages(value[0], error_messages)
                elif isinstance(value, str):
                    error_messages += [value.format("This", format_key)]
        elif isinstance(payload, str):
            error_messages += [payload]
        elif isinstance(payload, list):
            error_messages = payload

        return error_messages

    @staticmethod
    def format_error_message(payload: any):
        """
        format error response as array of string in all cases.
        serializer converts the model in python primitives:
        Check these primitives and build array of strings
        :return:
        """
        error_messages = []
        return ApiRenderer.extract_error_messages(payload, error_messages)

    @classmethod
    def format_response(cls, http_status: int, payload: dict or str):
        """Format_response static method is responsible to structure the rest api
        If status is True then its success, otherwise false.
        http_status have http status code.

        Do Logging for exception or errors that are critical or vulnerable.

        payload have body
        :param http_status:
        :param payload:
        :return:
        """
        payload = payload.get_codes() if isinstance(payload, APIException) else payload
        status_message = True if http_status in range(200, 300) else False

        if http_status in range(200, 300):
            response_body = {
                "success": status_message,
                "code": http_status,
                "data": {"message": payload} if isinstance(payload, str) else payload,
            }
        else:
            response_body = {
                "success": status_message,
                "code": http_status,
                "error": {
                    "traceId": str(uuid.uuid4()),
                    "message": cls.format_error_message(payload),
                },
            }

        return response_body

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Render application/json with standard structure.
        :param data:
        :param accepted_media_type:
        :param renderer_context:
        :return:
        """
        response_dict = ApiRenderer.format_response(
            http_status=renderer_context.get("response").status_code, payload=data
        )
        return json.dumps(response_dict, cls=self.encoder_class)
