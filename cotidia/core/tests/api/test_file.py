# import os
# import shutil

# from pathlib import Path

# from django.template.defaultfilters import filesizeformat
# from django.urls import reverse
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import Permission

# from rest_framework import status
# from rest_framework.test import APITestCase
# from rest_framework.authtoken.models import Token

# from cotidia.account.models import User
# from cotidia.core.utils.doc import Doc
# from cotidia.file.utils.generator import (
#     generate_pdf_file,
#     generate_text_file,
#     generate_image_file
# )
# from cotidia.file.models import File
# from cotidia.file.factory import FileFactory
# from cotidia.file.conf import settings
# from cotidia.file.tests.models import GenericItem


# class FileAPITests(APITestCase):

#     maxDiff = None
#     display_doc = False

#     def setUp(self):
#         self.doc = Doc()

#         # Test settings
#         settings.FILE_MAX_UPLOAD_SIZE = 1600  # 1.6kb

#         # Create a generic item to test the generic foreign key
#         self.item = GenericItem.objects.create()

#         self.normal_user = User.objects.create(
#             username="normal",
#             email="normal@test.com",
#             is_active=True)
#         self.normal_user_token, created = Token.objects.get_or_create(
#             user=self.normal_user)

#         self.admin_user = User.objects.create(
#             username="admin",
#             email="admin@test.com",
#             is_active=True,
#             is_staff=True)
#         self.admin_user_token, created = Token.objects.get_or_create(
#             user=self.admin_user)

#         self.admin_user_permitted = User.objects.create(
#             username="admin.permitted",
#             email="admin.permitted@test.com",
#             is_active=True,
#             is_staff=True)
#         self.admin_user_permitted_token, created = Token.objects.get_or_create(
#             user=self.admin_user_permitted)

#         content_type = ContentType.objects.get_for_model(File)
#         permission = Permission.objects.get(
#             content_type=content_type, codename='add_file')
#         self.admin_user_permitted.user_permissions.add(permission)

#     def tearDown(self):
#         if Path(settings.FILE_UPLOAD_PATH).is_dir():
#             shutil.rmtree(settings.FILE_UPLOAD_PATH)

#     def test_upload_file_permission_restricted(self):
#         """Test that a user without the necessary permissions is restricted."""

#         url = reverse('file-api:upload')

#         pdf_file = generate_pdf_file()

#         data = {
#             'f': pdf_file
#         }

#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)

#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.admin_user_token.key)

#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_upload_file_permission_user_permitted(self):
#         """Test that an admin user with the right permission can upload."""

#         url = reverse('file-api:upload')

#         pdf_file = generate_pdf_file()

#         data = {
#             'f': pdf_file
#         }

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key)

#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_upload_file(self):
#         """Test if we can upload a file."""

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key)

#         url = reverse('file-api:upload')

#         pdf_file = generate_pdf_file()

#         data = {
#             'f': pdf_file
#         }

#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["name"], "test.pdf")
#         self.assertEqual(response.data["mimetype"], "application/pdf")
#         self.assertEqual(response.data["size"], pdf_file.getbuffer().nbytes)

#         if self.display_doc:
#             payload = data.copy()
#             payload['f'] = "test.pdf"
#             content = {
#                 'title': "Upload file",
#                 'url': url,
#                 'http_method': 'POST',
#                 'payload': payload,
#                 'response': response.data
#             }
#             self.doc.display_section(content)

#     def test_upload_file_with_generic_relation(self):
#         """Test if we can upload a file with content type."""

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key)

#         url = reverse('file-api:upload')

#         pdf_file = generate_pdf_file()
#         content_type_id = ContentType.objects.get_for_model(self.item).id

#         data = {
#             'f': pdf_file,
#             'content_type': content_type_id,
#             'object_id': self.item.id
#         }

#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["name"], "test.pdf")
#         self.assertEqual(response.data["mimetype"], "application/pdf")
#         self.assertEqual(response.data["content_type"], content_type_id)
#         self.assertEqual(response.data["object_id"], self.item.id)

#         if self.display_doc:
#             payload = data.copy()
#             payload['f'] = "test.pdf"
#             content = {
#                 'title': "Upload file with generic relation",
#                 'url': url,
#                 'http_method': 'POST',
#                 'payload': payload,
#                 'response': response.data
#             }
#             self.doc.display_section(content)

#     def test_upload_file_public(self):
#         """Test if we can upload a file with a public permission for S3."""

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key)

#         url = reverse('file-api:upload')

#         pdf_file = generate_pdf_file()

#         data = {
#             'f': pdf_file,
#             'public': True
#         }

#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["name"], "test.pdf")
#         self.assertEqual(response.data["mimetype"], "application/pdf")
#         self.assertEqual(response.data["size"], pdf_file.getbuffer().nbytes)

#         if self.display_doc:
#             payload = data.copy()
#             payload['f'] = "test.pdf"
#             content = {
#                 'title': "Upload file",
#                 'url': url,
#                 'http_method': 'POST',
#                 'payload': payload,
#                 'response': response.data
#             }
#             self.doc.display_section(content)

#     def test_upload_file_public_no_public_storage_setup(self):
#         """Test if we can upload public without public storage setup."""

#         del settings.PUBLIC_FILE_STORAGE

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key)

#         url = reverse('file-api:upload')

#         pdf_file = generate_pdf_file()

#         data = {
#             'f': pdf_file,
#             'public': True
#         }

#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_file_type_validation(self):
#         """Test if we get a validation error for invalid file types."""

#         with self.settings(FILE_ALLOWED_TYPES=['application/pdf']):

#             self.client.credentials(
#                 HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key
#             )

#             url = reverse('file-api:upload')

#             text_file = generate_text_file()

#             data = {
#                 'f': text_file
#             }

#             response = self.client.post(url, data, format='multipart')
#             self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#             self.assertEqual(
#                 response.data['f'],
#                 ['File type (text/plain) is invalid.']
#             )

#     def test_file_filesize_validation(self):
#         """Test if we get a validation error for large files."""

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key)

#         url = reverse('file-api:upload')

#         # Make a larger image so it exceeds the file size limit on purpose
#         pdf_file = generate_pdf_file(content="Some text " * 5000)

#         data = {
#             'f': pdf_file
#         }

#         max_upload_size_fmt = filesizeformat(settings.FILE_MAX_UPLOAD_SIZE)

#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             response.data['f'],
#             [
#                 'File size too large. It must be less than {}'.format(
#                     max_upload_size_fmt)
#             ]
#         )

#     def test_upload_file_with_taxonomy(self):
#         """Test if we can upload a file with taxonomy."""

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key)

#         url = reverse('file-api:upload')

#         pdf_file = generate_pdf_file()

#         data = {
#             'f': pdf_file,
#             'taxonomy': "gallery"
#         }

#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["name"], "test.pdf")
#         self.assertEqual(response.data["taxonomy"], "gallery")
#         self.assertEqual(response.data["mimetype"], "application/pdf")

#         if self.display_doc:
#             payload = data.copy()
#             payload['f'] = "test.pdf"
#             content = {
#                 'title': "Upload file with taxonomy",
#                 'url': url,
#                 'http_method': 'POST',
#                 'payload': payload,
#                 'response': response.data
#             }
#             self.doc.display_section(content)

#     def test_upload_file_with_generic_relation_and_taxonomy(self):
#         """Test if we can upload a file with content type and taxonomy."""

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key)

#         url = reverse('file-api:upload')

#         pdf_file = generate_pdf_file()
#         content_type_id = ContentType.objects.get_for_model(self.item).id

#         data = {
#             'f': pdf_file,
#             'content_type': content_type_id,
#             'object_id': self.item.id,
#             'taxonomy': "floorplan"
#         }

#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["name"], "test.pdf")
#         self.assertEqual(response.data["taxonomy"], "floorplan")
#         self.assertEqual(response.data["mimetype"], "application/pdf")
#         self.assertEqual(response.data["content_type"], content_type_id)
#         self.assertEqual(response.data["object_id"], self.item.id)

#         if self.display_doc:
#             payload = data.copy()
#             payload['f'] = "test.pdf"
#             content = {
#                 'title': "Upload file with generic relation and taxonomy",
#                 'url': url,
#                 'http_method': 'POST',
#                 'payload': payload,
#                 'response': response.data
#             }
#             self.doc.display_section(content)

#     def test_upload_file_public(self):
#         """Test a sub class of the upload view with no permissions required.

#         The view will also handle the content_type itself.
#         """

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key)

#         url = reverse('file-upload-public')

#         pdf_file = generate_pdf_file()
#         content_type_id = ContentType.objects.get_for_model(self.item).id

#         data = {
#             'f': pdf_file,
#             'object_id': self.item.id,
#             'taxonomy': "floorplan"
#         }

#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["name"], "test.pdf")
#         self.assertEqual(response.data["taxonomy"], "floorplan")
#         self.assertEqual(response.data["mimetype"], "application/pdf")
#         self.assertEqual(response.data["content_type"], content_type_id)
#         self.assertEqual(response.data["object_id"], self.item.id)

#         if self.display_doc:
#             payload = data.copy()
#             payload['f'] = "test.pdf"
#             content = {
#                 'title': "Upload file without permission required",
#                 'url': url,
#                 'http_method': 'POST',
#                 'payload': payload,
#                 'response': response.data
#             }
#             self.doc.display_section(content)

#     def test_upload_file_with_image_variations(self):
#         """Test if we can upload a file with image variations."""

#         variations = {
#             "thumbnail": ["crop", 75, 75],
#             "small": ["resize", 50, 50]
#         }

#         with self.settings(FILE_IMAGE_VARIATIONS=variations):

#             self.client.credentials(
#                 HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key
#             )

#             url = reverse('file-api:upload')

#             img_file = generate_image_file(size=(200, 200))

#             data = {
#                 'f': img_file
#             }

#             response = self.client.post(url, data, format='multipart')
#             self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#             self.assertEqual(response.data["name"], "test.PNG")
#             self.assertEqual(response.data["mimetype"], "image/png")
#             self.assertEqual(
#                 response.data["size"],
#                 img_file.getbuffer().nbytes
#             )
#             self.assertEqual(response.data["width"], 200)
#             self.assertEqual(response.data["height"], 200)

#             f = File.objects.latest("id")
#             # Check that the variations exist
#             for variation in variations.keys():
#                 path = f.build_variation_path(variation)
#                 self.assertTrue(Path(path).is_file())

#     def test_non_raster_image_variations(self):
#         """Test if we upload a non raster image no variations is created."""

#         variations = {
#             "thumbnail": ["crop", 100, 100],
#             "small": ["resize", 100, 100]
#         }

#         raster_image_formats = [
#             "image/gif"
#         ]

#         with self.settings(
#                 FILE_IMAGE_VARIATIONS=variations,
#                 FILE_RASTER_IMAGE_FORMATS=raster_image_formats
#         ):
#             self.client.credentials(
#                 HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key
#             )

#             url = reverse('file-api:upload')

#             img_file = generate_image_file()

#             data = {
#                 'f': img_file
#             }

#             response = self.client.post(url, data, format='multipart')
#             self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#             self.assertEqual(response.data["name"], "test.PNG")
#             self.assertEqual(response.data["mimetype"], "image/png")

#             f = File.objects.latest("id")
#             # Check that the variations exist
#             for variation in variations.keys():
#                 path = f.build_variation_path(variation)
#                 self.assertFalse(Path(path).is_file())

#     def test_reorder_files(self):
#         """Test if we can reorder a file list."""

#         test_files = [FileFactory() for i in range(5)]
#         uuids = list(map(lambda x: x.uuid, test_files))

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key)

#         url = reverse('file-api:order')

#         # Shuffles the data
#         data = {
#             'data': [uuids[2], uuids[4], uuids[3], uuids[1], uuids[0]]
#         }

#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Ensure we have the latest version of the file from the db
#         for f in test_files:
#             f.refresh_from_db()

#         # Checks the correct order id has been set
#         self.assertEqual(test_files[2].order_id, 1)
#         self.assertEqual(test_files[4].order_id, 2)
#         self.assertEqual(test_files[3].order_id, 3)
#         self.assertEqual(test_files[1].order_id, 4)
#         self.assertEqual(test_files[0].order_id, 5)

#         if self.display_doc:
#             payload = data.copy()
#             payload['f'] = "test.pdf"
#             content = {
#                 'title': "Upload file",
#                 'url': url,
#                 'http_method': 'POST',
#                 'payload': payload,
#                 'response': response.data
#             }
#             self.doc.display_section(content)

#     def test_reorder_files_wrong_uuid(self):
#         """Test if we can reorder a file list."""

#         test_files = [FileFactory() for i in range(5)]
#         uuids = list(map(lambda x: x.uuid, test_files))

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key)

#         url = reverse('file-api:order')

#         # Shuffles the data
#         data = {
#             'data': ["ab3e6952-aaaa-aaaa-a726-2579206ee961", uuids[4], uuids[3], uuids[1], uuids[0]]
#         }

#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#         if self.display_doc:
#             payload = data.copy()
#             payload['f'] = "test.pdf"
#             content = {
#                 'title': "Upload file",
#                 'url': url,
#                 'http_method': 'POST',
#                 'payload': payload,
#                 'response': response.data
#             }
#             self.doc.display_section(content)

#     def test_reorder_files_invalid_uuid(self):
#         """Test if we can reorder a file list."""

#         test_files = [FileFactory() for i in range(5)]
#         uuids = list(map(lambda x: x.uuid, test_files))

#         self.client.credentials(
#             HTTP_AUTHORIZATION='Token ' + self.admin_user_permitted_token.key)

#         url = reverse('file-api:order')

#         # Shuffles the data
#         data = {
#             'data': ["ab3e6952-aaa-aaaa-a726-2579206ee961", uuids[4], uuids[3], uuids[1], uuids[0]]
#         }

#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#         if self.display_doc:
#             payload = data.copy()
#             payload['f'] = "test.pdf"
#             content = {
#                 'title': "Upload file",
#                 'url': url,
#                 'http_method': 'POST',
#                 'payload': payload,
#                 'response': response.data
#             }
#             self.doc.display_section(content)
