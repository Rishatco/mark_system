from django.contrib import admin
from .models import StudentModel, SquadModel, DepartamentModel
# Register your models here.

admin.site.register(StudentModel)
admin.site.register(SquadModel)
admin.site.register(DepartamentModel)
