# from django.contrib.contenttypes.models import ContentType

# from cotidia.file.views.api.file import Upload
# from cotidia.file.tests.models import GenericItem


# class PublicUpload(Upload):
#     permission_classes = ()

#     def perform_create(self, serializer):
#         """Automatically assign the content type."""
#         content_type = ContentType.objects.get_for_model(GenericItem)
#         serializer.save(content_type=content_type)
