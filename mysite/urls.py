"""mysite URL Configuration

"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, register_converter

from .converters import (HexColorConverter, MaxWidthConverter,
                         MaxHeightConverter, FileFormatConverter)

from .views import HomeView, PlaceholderView
register_converter(FileFormatConverter, 'fileformat')
register_converter(HexColorConverter, 'hexcolor')
register_converter(MaxHeightConverter, 'maxheight')
register_converter(MaxWidthConverter, 'maxwidth')

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('<maxwidth:width>/', PlaceholderView, name="placeholder"),
    path('<maxwidth:width>/<fileformat:format>/', PlaceholderView, name="placeholder"),
    path('<maxwidth:width>/<hexcolor:backcolor>/', PlaceholderView, name="placeholder"),
    path('<maxwidth:width>/<hexcolor:backcolor>/<fileformat:format>/', PlaceholderView, name="placeholder"),
    path('<maxwidth:width>/<hexcolor:backcolor>/<hexcolor:forecolor>/', PlaceholderView, name="placeholder"),
    path('<maxwidth:width>/<hexcolor:backcolor>/<hexcolor:forecolor>/<fileformat:format>/', PlaceholderView, name="placeholder"),
    path('<maxwidth:width>/<maxheight:height>/', PlaceholderView, name="placeholder"),
    path('<maxwidth:width>/<maxheight:height>/<fileformat:format>/', PlaceholderView, name="placeholder"),
    path('<maxwidth:width>/<maxheight:height>/<hexcolor:backcolor>/', PlaceholderView, name="placeholder"),
    path('<maxwidth:width>/<maxheight:height>/<hexcolor:backcolor>/<fileformat:format>/', PlaceholderView, name="placeholder"),
    path('<maxwidth:width>/<maxheight:height>/<hexcolor:backcolor>/<hexcolor:forecolor>/', PlaceholderView, name="placeholder"),
    path('<maxwidth:width>/<maxheight:height>/<hexcolor:backcolor>/<hexcolor:forecolor>/<fileformat:format>/', PlaceholderView, name="placeholder"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'mysite.views.error_400_view'
handler403 = 'mysite.views.error_403_view'
handler404 = 'mysite.views.error_404_view'
handler500 = 'mysite.views.error_500_view'
