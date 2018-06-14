from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from django.contrib.auth.models import Group
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^$',TemplateView.as_view(template_name='homepage.html'),name="homepage"),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/',TemplateView.as_view(template_name='accounts/index.html')),
    url(r'^v1/', include('snippets.urls')),
    url(r'^login/', obtain_jwt_token),
]
