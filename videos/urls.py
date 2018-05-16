from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from videos import views

urlpatterns = [
    url(r'^videos/$', views.VideoList.as_view()),
    url(r'^videos/(?P<pk>\d+)/$', views.VideoDetail.as_view()),
    url(r'^catalogs/$', views.CatalogacionList.as_view()),
    url(r'^catalogs/(?P<pk>\d+)/$', views.CatalogacionDetail.as_view()),
    url(r'^testigo/$', views.Testigo.as_view()),
    url(r'^analiticos/$', views.Analiticos.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)