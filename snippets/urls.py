from django.conf.urls import url
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^api/$', views.SnippetList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)$', views.SnippetDetail.as_view()),
    url(r'^api/login/', obtain_jwt_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)
