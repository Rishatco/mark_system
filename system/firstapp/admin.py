from django.contrib import admin
from .models import Student, StundetGroup, Departament, Teacher,Discipline,Mark,GroupDiscipline
# Register your models here.

admin.site.register(Student)
admin.site.register(StundetGroup)
admin.site.register(Departament)
admin.site.register(Teacher)
admin.site.register(Discipline)
admin.site.register(Mark)
admin.site.register(GroupDiscipline)