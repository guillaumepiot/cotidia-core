from django.urls import include, path

from cotidia.account.views.admin import dashboard

# from .views import PublicUpload

urlpatterns = [
    # url(r'^api/file/', include('cotidia.file.urls.api.file',
    #     namespace="file-api")),
    # url(r'^api/file/upload-public$', PublicUpload.as_view(),
    #     name="file-upload-public"),
    # url(r'^admin/file/', include('cotidia.file.urls.admin',
    #     namespace="file-admin")),
    path(
        "admin/account/",
        include("cotidia.account.urls.admin", namespace="account-admin"),
    ),
    path("admin/mail/", include("cotidia.mail.urls", namespace="mail-admin")),
    path(
        "admin/generic/", include("cotidia.admin.urls.admin", namespace="generic-admin")
    ),
    path("admin/", dashboard, name="dashboard"),
]
