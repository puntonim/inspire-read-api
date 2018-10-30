"""
URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path

from . import views


urlpatterns = [
    path('api/health/', views.health, name='health'),
    path('api/unhealth/', views.unhealth, name='unhealth'),

    re_path(r'^api/literature/(?P<pid_value>[\w]+)/$', views.LiteratureDetail.as_view(),
            name='literature-detail'),
    re_path(r'^api/authors/(?P<pid_value>[\w]+)/$', views.AuthorDetail.as_view(),
            name='author-detail'),
    re_path(r'^api/authors/$', views.AuthorsList.as_view(),
            name='authors-list'),

    # DJRF browsable APIs auth views.
    path('api-auth/', include('rest_framework.urls')),
    # Django Admin.
    path('admin/', admin.site.urls),
]
