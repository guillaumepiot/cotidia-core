from django.conf import settings


def absolute_url(url):
    if url.startswith('http') and url.startswith('//'):
        return url
    else:
        return settings.SITE_URL + url
