"""
S3 storage for static and public files.

Settings:

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "cotidia.core.storage.s3.StaticS3Boto3Storage"
PUBLIC_FILE_STORAGE = "cotidia.core.storage.s3.PublicS3Boto3Storage"

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "<website-name>-uploads-<production|staging>"
AWS_STORAGE_BUCKET_NAME_STATIC = "<website-name>-assets-<production|staging>"
AWS_DEFAULT_ACL = "private"
AWS_S3_ENCRYPTION = True
AWS_QUERYSTRING_AUTH = True
AWS_S3_FILE_OVERWRITE = False
AWS_S3_REGION_NAME = 'eu-west-2'  # Change to the relevant region
AWS_S3_SIGNATURE_VERSION = 's3v4'
"""

from storages.backends.s3boto3 import S3Boto3Storage

from django.conf import settings


class StaticS3Boto3Storage(S3Boto3Storage):

    file_overwrite = True
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME_STATIC
    default_acl = "public-read"
    bucket_acl = "public-read"
    encryption = False
    gzip = True
    querystring_auth = False


class PublicS3Boto3Storage(S3Boto3Storage):

    file_overwrite = True
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    default_acl = "public-read"
    bucket_acl = "public-read"
    encryption = False
    querystring_auth = False
