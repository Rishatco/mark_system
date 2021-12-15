"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView

from firstapp.views import SquadList
from firstapp.views import create_view, student_detail_view, student_view

from firstapp.views import SquadDetailView

from firstapp.views import SquadUpdateView

from firstapp.views import save_student

urlpatterns = [
    path("admin/", admin.site.urls),
    path("create/", create_view),
    path("", student_view),
    path('<int:id>/', student_detail_view),
    path('squads/', SquadList.as_view(), name='squads'),
    re_path(r'^squad/(?P<pk>\d+)$', SquadDetailView.as_view(), name="squad-detail"),
    re_path(r'^squad-edit/(?P<pk>\d+)$', SquadUpdateView.as_view(), name="squad-edit" ),
    path('squad-edit/save-student/<int:id>/', save_student)

]
