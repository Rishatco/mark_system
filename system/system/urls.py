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

from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.conf.urls import include
from django.contrib.auth import views
from ejournal.views import groupList, rating_log,group_study_raiting,group_visiting_raiting,group_addres_raiting,group_total_raiting,student_stat
from ejournal.views import groupDetailView, check_perm
from ejournal.views import groupUpdateView
from ejournal.views import save_student,DisciplineDetailView
from ejournal.views import groupCreateView,TeacherDetailView
from  ejournal.views import TeachersList, DisciplinesList, TeacherCreateView, TeacherEditView, TeacherDeleteView
from ejournal.views import groupDeleteView,DisciplineCreateView, DisciplineEditView, DisciplineDeleteView

urlpatterns = [
    path("admin/", admin.site.urls),
   # path("", groupList.as_view(), name='groups'),
    path('groups/', groupList.as_view(), name='groups'),
    path('teachers/', TeachersList.as_view(), name='teachers'),
    path('disciplines/', DisciplinesList.as_view(), name='disciplines'),
    re_path(r'^group/(?P<pk>\d+)$', groupDetailView.as_view(), name="group-detail"),
    re_path(r'^group-edit/(?P<pk>\d+)$', groupUpdateView.as_view(), name="group-edit" ),
    path('groups/create', groupCreateView.as_view(), name="group-create"),
    re_path(r'^group-delete/(?P<pk>\d+)$', groupDeleteView.as_view(), name="group-delete" ),
    path('teacher/create', TeacherCreateView.as_view(), name="teacher-create"),
    re_path(r'^teacher-edit/(?P<pk>\d+)$', TeacherEditView.as_view(), name="teacher-edit"),
    re_path(r'^teacher-detele/(?P<pk>\d+)$', TeacherDeleteView.as_view(), name="teacher-delete" ),
    re_path(r'^teacher/(?P<pk>\d+)$', TeacherDetailView.as_view(), name="teacher-detail"),
    path('discipline/create', DisciplineCreateView.as_view(), name="disсipline-create"),
    re_path(r'^discipline-edit/(?P<pk>\d+)$', DisciplineEditView.as_view(), name="discipline-edit"),
    re_path(r'^discipline-detele/(?P<pk>\d+)$', DisciplineDeleteView.as_view(), name="discipline-delete"),
    re_path(r'^discipline/(?P<pk>\d+)$', DisciplineDetailView.as_view(), name="discipline-detail"),
    path('group/rating/<int:pk>/', rating_log, name='rating'),
    path('group/group-study-rating/<int:pk>/', group_study_raiting, name='group-study-rating'),
    path('group/group-visiting-rating/<int:pk>/', group_visiting_raiting, name='group-visiting-rating'),
    path('group/group-addres-rating/<int:pk>/', group_addres_raiting, name='group-add-res-rating'),
    path('group/group-total-rating/<int:pk>/', group_total_raiting, name='group-total-rating'),
    path('', views.LoginView.as_view(), name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('student_stat/', student_stat, name="student_stat"),
    path('chech_perm/', check_perm, name="check_perm")
   # path('accounts/profile/', student_stat)


]
