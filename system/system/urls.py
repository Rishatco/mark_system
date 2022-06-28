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
from firstapp.views import SquadList, rating_log,squad_study_raiting,squad_visiting_raiting,squad_addres_raiting,squad_total_raiting,student_stat
from firstapp.views import SquadDetailView, check_perm
from firstapp.views import SquadUpdateView
from firstapp.views import save_student,DisciplineDetailView
from firstapp.views import SquadCreateView,TeacherDetailView
from  firstapp.views import TeachersList, DisciplinesList, TeacherCreateView, TeacherEditView, TeacherDeleteView
from firstapp.views import SquadDeleteView,DisciplineCreateView, DisciplineEditView, DisciplineDeleteView

urlpatterns = [
    path("admin/", admin.site.urls),
   # path("", SquadList.as_view(), name='squads'),
    path('squads/', SquadList.as_view(), name='squads'),
    path('teachers/', TeachersList.as_view(), name='teachers'),
    path('disciplines/', DisciplinesList.as_view(), name='disciplines'),
    re_path(r'^squad/(?P<pk>\d+)$', SquadDetailView.as_view(), name="squad-detail"),
    re_path(r'^squad-edit/(?P<pk>\d+)$', SquadUpdateView.as_view(), name="squad-edit" ),
    path('squads/create', SquadCreateView.as_view(), name="squad-create"),
    re_path(r'^squad-delete/(?P<pk>\d+)$', SquadDeleteView.as_view(), name="squad-delete" ),
    path('teacher/create', TeacherCreateView.as_view(), name="teacher-create"),
    re_path(r'^teacher-edit/(?P<pk>\d+)$', TeacherEditView.as_view(), name="teacher-edit"),
    re_path(r'^teacher-detele/(?P<pk>\d+)$', TeacherDeleteView.as_view(), name="teacher-delete" ),
    re_path(r'^teacher/(?P<pk>\d+)$', TeacherDetailView.as_view(), name="teacher-detail"),
    path('discipline/create', DisciplineCreateView.as_view(), name="disсipline-create"),
    re_path(r'^discipline-edit/(?P<pk>\d+)$', DisciplineEditView.as_view(), name="discipline-edit"),
    re_path(r'^discipline-detele/(?P<pk>\d+)$', DisciplineDeleteView.as_view(), name="discipline-delete"),
    re_path(r'^discipline/(?P<pk>\d+)$', DisciplineDetailView.as_view(), name="discipline-detail"),
    path('squad/rating/<int:pk>/', rating_log, name='rating'),
    path('squad/squad-study-rating/<int:pk>/', squad_study_raiting, name='squad-study-rating'),
    path('squad/squad-visiting-rating/<int:pk>/', squad_visiting_raiting, name='squad-visiting-rating'),
    path('squad/squad-addres-rating/<int:pk>/', squad_addres_raiting, name='squad-add-res-rating'),
    path('squad/squad-total-rating/<int:pk>/', squad_total_raiting, name='squad-total-rating'),
    path('', views.LoginView.as_view(), name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('student_stat/', student_stat, name="student_stat"),
    path('chech_perm/', check_perm, name="check_perm")
   # path('accounts/profile/', student_stat)


]
