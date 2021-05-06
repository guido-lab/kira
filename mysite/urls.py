from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from core import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('upload/', views.upload, name='upload'),
    path('download/<str:file>/', views.download_file, name='download_file'),
    path('files/', views.file_list, name='file_list'),
    path('files/upload/', views.upload_book, name='upload_book'),

    path('avro/', views.avro_schema, name='avro'),
    path('upsert/', views.upsert, name='upsert'),

    path('files/<str:file>/', views.delete_file, name='delete_file'),

    path('class/books/', views.BookListView.as_view(), name='class_book_list'),
    path('class/books/upload/', views.UploadBookView.as_view(), name='class_upload_book'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
