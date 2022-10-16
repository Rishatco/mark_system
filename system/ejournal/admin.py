from django.contrib import admin
from .models import Student, StudentGroup, Teacher,Discipline,Mark,GroupDiscipline
# Register your models here.

admin.site.register(Student)
admin.site.register(StudentGroup)
admin.site.register(Teacher)
admin.site.register(Discipline)
admin.site.register(Mark)
admin.site.register(GroupDiscipline)