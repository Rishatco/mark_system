from django.contrib import admin
from .models import StudentModel, SquadModel, DepartamentModel, Teacher,Discipline,Mark
# Register your models here.

admin.site.register(StudentModel)
admin.site.register(SquadModel)
admin.site.register(DepartamentModel)
admin.site.register(Teacher)
admin.site.register(Discipline)
admin.site.register(Mark)