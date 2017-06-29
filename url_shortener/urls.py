from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from url_shortener import views

urlpatterns = [
    url(r'^new/?$', views.URLNew.as_view()),
    url(r'^(?P<short_id>[^/]+)$', views.URLDetails.as_view()),
]
