from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.views import generic
from django_tables2 import RequestConfig

from .forms import StudentForm

from .models import StudentModel, SquadModel

from .tables import StudentTable


def create_view(request):
    if request.method =="POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return  redirect("/")
    else:
        form = StudentForm()
        context = {"form": form}
        return  render(request, "create.html", context)

def save_student(request, id):
    try:
        student =StudentModel.objects.get(id)
        if request.method == "POST":
            student.name = request.POST.get("name")
            student.surname = request.POST.get("surname")
            student.patronymic = request.POST.get("patronymic")
            student.save()
        return HttpResponseRedirect(f"squad-edit/{student.squad.id}")
    except StudentModel.DoesNotExist:
        raise Http404('Такого студента не существует')


def student_view(request):
    dataset = StudentModel.objects.all()

    table =StudentTable(dataset)
    RequestConfig(request).configure(table)
    return render(request, 'listview.html', {"table" : table})

def student_detail_view(request, id):
    try:
        data = StudentModel.objects.get(id=id)
    except StudentModel.DoesNotExist:
        raise  Http404('Такого студента не существует')
    return render (request, 'detailview.html', {'data': data})

def squad_update_view(request, id):
    if request.method=="GET":
     try :
        data = SquadModel.object.get(id=id)
     except SquadModel.DoesNotExist:
        raise Http404('такого взвода не сущетвует')
        return render(request, 'squadmodel_form.html', {})

class SquadList(generic.ListView):
    model = SquadModel

class SquadDetailView(generic.DetailView):
    model = SquadModel

class SquadUpdateView(generic.UpdateView):
    model = SquadModel
    fields = ["number", "departament", "specialization"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        id = request.POST.getlist('id')
        name = request.POST.getlist('name')
        surname =request.POST.getlist('surname')
        patronymic = request.POST.getlist("patronymic")
        squad = SquadModel.objects.get(id=kwargs['pk'])
        students =StudentModel.objects.filter(squad=squad)
        students_upd =students.filter(id__in= id)
        # студенты для удаления
        del_students = students.difference(students_upd)
        for student in del_students:
            student.delete()
        for x in range(len(id)):
            # изменение уже сущетсвующих элементов
            if(id[x]!=''):
                student = StudentModel.objects.get(id=id[x])
                student.name = name[x]
                student.surname = surname[x]
                student.patronymic = patronymic[x]
                student.save()
        return super().post(request, *args, **kwargs)