import  django_tables2 as tables
from django_tables2 import A

from .models import StudentModel

class StudentTable(tables.Table):
    delete = tables.LinkColumn('main:delete_item', args=[A('pk')], attrs={
    'a': {'class': 'btn'}})
    class Meta:
        model = StudentModel
        attrs = {'class': 'paleblue'}
        fields = ("surname","name", "patronymic")
