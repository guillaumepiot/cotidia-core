from rest_framework import permissions
from rest_framework.views import exception_handler


def drf_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None and \
            context['request'].method not in permissions.SAFE_METHODS:
        context['request']._request.POST = context['request'].data

    return response
