from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import generic
from .forms import StudentForm
from .models import Student, StudentGroup, Teacher, Discipline, GroupDiscipline, Mark

def check_perm(request):
    if request.user.is_superuser:
        return redirect('../squads/')
    else:
        return redirect("/student_stat/")

def student_stat(request):
    surname = request.user.studentmodel.surname
    name = request.user.studentmodel.name
    patronymic = request.user.studentmodel.patronymic

    squad = request.user.studentmodel.squad
    disciplines = squad.squaddiscipline_set.all()
    marks = Mark.objects.filter(discipline__in=disciplines, student=request.user.studentmodel)
    dates = marks.dates("date", "day")
    table = []
    title = ["Дисциплины"]
    for date in dates:
        title.append(str(date))
    for discipline in disciplines:
        dis_report = []
        dis_report.append(discipline.discipline.name)
        for date in dates:
            mark = marks.filter(date= date,discipline= discipline)[0]
            dis_report.append(mark.ball)
        table.append(dis_report)

    context = {"titles": title, "reports": table, "surname": surname, "name": name,"patronymic": patronymic, "squad": squad.number}
    return render(request, "student_info.html", context)

def squad_study_raiting(request, pk):
    if request.method == "GET":
        squad = StudentGroup.objects.get(id=pk)
        students = Student.objects.filter(squad=squad)
        discipline = Discipline.objects.get(name="дополнительные обязанности")
        squad_disciplines = GroupDiscipline.objects.filter(squad=squad)
        squad_disciplines = squad_disciplines.exclude(discipline= discipline)
        raiting_list = []
        for student in students:
            cnt_ball = 0
            cur_ball = 0
            for discipline in squad_disciplines:
                cur_marks = Mark.objects.filter(student=student, discipline=discipline)
                for mark in cur_marks:
                    if mark.ball != -1:
                        cnt_ball += 1
                        cur_ball += mark.ball
            cur_student = [str(student), cur_ball/cnt_ball]
            raiting_list.append(cur_student)
        raiting_list.sort(key=lambda x: x[1])
        raiting_list.reverse()
        raiting_list = map(lambda x: [x[0], float('%.2f'%x[1])], raiting_list)
        titles = ["ФИО", "Средная оценка"]
        context = {"students": raiting_list, "squadmodel": squad, "titles": titles}
        return  render(request, "ejournal/squad_raiting.html",context)

def squad_visiting_raiting(request, pk):
    if request.method == "GET":
        squad = StudentGroup.objects.get(id=pk)
        students = Student.objects.filter(squad=squad)
        squad_disciplines = GroupDiscipline.objects.filter(squad=squad)
        raiting_list = []
        for student in students:
            cnt_pass = 0
            for discipline in squad_disciplines:
                cur_marks = Mark.objects.filter(student=student, discipline=discipline)
                for mark in cur_marks:
                    if mark.ball == -1:
                        cnt_pass += 1
            cur_student = [student, cnt_pass]
            raiting_list.append(cur_student)
        raiting_list.sort(key=lambda x: x[1])
        #raiting_list = map(lambda x: x[0], raiting_list)
        titles = ["ФИО", "Количество пропусков"]
        context = {"students": raiting_list, "squadmodel": squad, "titles": titles}
        return  render(request, "ejournal/squad_raiting.html",context)

def squad_addres_raiting(request, pk):
    if request.method == "GET":
        squad = StudentGroup.objects.get(id=pk)
        students = Student.objects.filter(squad=squad)
        discipline = Discipline.objects.get(name="дополнительные обязанности")
        squad_disciplines = GroupDiscipline.objects.filter(squad=squad, discipline=discipline)
        raiting_list = []
        for student in students:
            cur_ball = 0
            for discipline in squad_disciplines:
                cur_marks = Mark.objects.filter(student=student, discipline=discipline)
                for mark in cur_marks:
                    if mark.ball != -1:
                        cur_ball += mark.ball
            cur_student = [student, cur_ball]
            raiting_list.append(cur_student)
        raiting_list.sort(key=lambda x: x[1])
        raiting_list.reverse()
        #raiting_list = map(lambda x: x[0], raiting_list)
        titles = ["ФИО", "Дополнительная активность"]
        context = {"students": raiting_list, "squadmodel": squad, "titles": titles}
        return  render(request, "ejournal/squad_raiting.html",context)

class Student_Stat():
    def __init__(self):
        self.fio = None
        self.study_ball = 0
        self.addres_ball = 0
        self.cnt_pass = 0

def squad_total_raiting(request, pk):
    if request.method == "GET":
        squad = StudentGroup.objects.get(id=pk)
        students = Student.objects.filter(squad=squad)
        discipline = Discipline.objects.get(name="дополнительные обязанности")
        squad_disciplines = GroupDiscipline.objects.filter(squad=squad)
        squad_disciplines_addres = squad_disciplines.get(discipline=discipline)
        squad_disciplines = squad_disciplines.exclude(discipline=discipline)
        raiting_list = []
        for student in students:
            cnt_pass = 0
            cur_ball = 0
            addres_ball =0
            student_stat = Student_Stat()
            for discipline in squad_disciplines:
                cur_marks = Mark.objects.filter(student=student, discipline=discipline)
                for mark in cur_marks:
                    if mark.ball != -1:
                        cur_ball += mark.ball
                    else:
                        cnt_pass += 1
            cur_marks = Mark.objects.filter(student=student, discipline=squad_disciplines_addres)
            for mark in cur_marks:
                if mark.ball != -1:
                    addres_ball += mark.ball

            student_stat.addres_ball = addres_ball
            student_stat.study_ball =cur_ball
            student_stat.cnt_pass = cnt_pass
            student_stat.fio = str(student)
            raiting_list.append(student_stat)
        max_study =0
        max_addres =0
        max_pass =0
        for x in raiting_list:
            max_study = max(max_study, x.study_ball)
            max_addres = max(max_addres, x.addres_ball)
            max_pass = max(max_pass, x.cnt_pass)
        for x in raiting_list:
            x.study_ball = x.study_ball/max_study*60
            x.addres_ball = x.addres_ball/max_addres*25
            x.cnt_pass = (max_pass-x.cnt_pass)/max_pass*15
        raiting = []
        for x in raiting_list:
            raiting.append([x.fio, float('%.2f'%x.study_ball),float('%.2f'%x.addres_ball),
                            float('%.2f'%x.cnt_pass), float('%.2f'%(x.study_ball+x.addres_ball+x.cnt_pass))])
        raiting.sort(key= lambda x: x[1]+x[2]+x[3])
        raiting.reverse()
        titles = ["ФИО", "Баллы за учебу", "Баллы за доп активность","Баллы за посещение", "Суммарный балл"]
        context = {"students": raiting, "squadmodel": squad, "titles": titles}
        return  render(request, "ejournal/squad_raiting.html",context)



def rating_log(request, pk):
    if request.method == "GET":
        curDis = request.GET.get("choose_discipline")
        if curDis == None:
            squad = StudentGroup.objects.get(id=pk)
            context = {"squad": squad}
            return render(request, "ejournal/raiting_log.html", context)
        else:
            discipline = Discipline.objects.get(name=curDis)
            squad = StudentGroup.objects.get(id=pk)
            squadDiscipline = GroupDiscipline.objects.get(discipline=discipline, squad=squad)
            students = Student.objects.filter(squad=squad)
            curMarks = Mark.objects.filter(discipline=squadDiscipline)
            studentsMark =curMarks.filter(student__in=students)
            dates =set(curMarks.values_list('date',flat=True))
            strDate =sorted( list(map(lambda x: x.strftime("%Y-%m-%d"), dates)))
            marks = []
            for student in students:
                marks.append({"student": student, "marks":[]})
                for date in strDate:
                    if Mark.objects.filter(student=student, date=date,discipline=squadDiscipline).exists():
                        curMark = Mark.objects.get(student=student, date=str(date), discipline=squadDiscipline)
                        if curMark.ball == -1:
                            marks[-1]["marks"].append('н')
                        else:
                            marks[-1]["marks"].append(curMark.ball)
                    else:
                        marks[-1]["marks"].append(0)
            context = {"squad": squad, "students": students, "marks": curMarks, "dates": strDate, "stmarks": marks, "cur_discipline": discipline}

            return render(request, "ejournal/raiting_log.html", context)
    else:
        curDis = request.GET.get("choose_discipline")
        dates = request.POST.getlist("data")
        ocenkas = request.POST.getlist('ocenka')
        squad = StudentGroup.objects.get(id=pk)
        discipline = Discipline.objects.get(name=curDis)
        squadDiscipline = GroupDiscipline.objects.get(discipline=discipline, squad=squad)
        students =list(Student.objects.filter(squad=squad))
        curMarks = Mark.objects.filter(discipline=squadDiscipline)
        studentsMark = curMarks.filter(student__in=students)
        studentsMark.delete()
        i =1
        j=0
        curStudent= students[j]
        for ocenka in ocenkas:
            if ocenka == '' or dates[i-1] == '':
                continue
            mark = Mark()
            mark.student = curStudent
            if ocenka == 'н':
                mark.ball = -1
            else:
                mark.ball = ocenka
            mark.date =dates[i-1]
            mark.discipline = squadDiscipline
            mark.save()
            if i == len(dates):
                j +=1
                if(j==len(students)):
                    break
                curStudent= students[j]
                i=1
            else:
                i += 1

        return redirect(squad)



def save_student(request, id):
    try:
        student =Student.objects.get(id)
        if request.method == "POST":
            student.name = request.POST.get("name")
            student.surname = request.POST.get("surname")
            student.patronymic = request.POST.get("patronymic")
            student.save()
        return HttpResponseRedirect(f"squad-edit/{student.squad.id}")
    except Student.DoesNotExist:
        raise Http404('Такого студента не существует')


def squad_update_view(request, id):
    if request.method=="GET":
     try :
        data = StudentGroup.object.get(id=id)
     except StudentGroup.DoesNotExist:
        raise Http404('такого взвода не сущетвует')
        return render(request, 'squadmodel_form.html', {})

class SquadList(generic.ListView):
    model = StudentGroup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            data = Discipline.objects.get(name="дополнительные обязанности")
        except Discipline.DoesNotExist:
            disp = Discipline()
            disp.name = "дополнительные обязанности"
            disp.type_exam = disp.TYPE_EXAM[0]
            disp.save()
        return context


class SquadDetailView(generic.DetailView):
    model = StudentGroup

class SquadUpdateView(generic.UpdateView):
    model = StudentGroup
    fields = ["number", "departament", "specialization"]


    def get_context_data(self, *args, **kwargs):
        context = super(SquadUpdateView, self).get_context_data(**kwargs)
        disciplines = Discipline.objects.exclude(name="дополнительные обязанности" )
        try:
            GroupDiscipline.objects.get(discipline= Discipline.objects.get(name="дополнительные обязанности"), squad=self.object)
        except:
            discipline = GroupDiscipline()
            discipline.discipline = Discipline.objects.get(name="дополнительные обязанности")
            discipline.squad = self.object
            discipline.save()
        context['disciplines'] =disciplines
        return context


    def post(self, request, *args, **kwargs):
        # получение значений студентов
        id = request.POST.getlist('id')
        name = request.POST.getlist('name')
        surname =request.POST.getlist('surname')
        patronymic = request.POST.getlist("patronymic")
        # получение текущего взвода
        squad = StudentGroup.objects.get(id=kwargs['pk'])
        # получение id существующих студентов, так как клиент для новых студентов возвращает пустую строку как id
        id_upd = list(filter(lambda x: x!='',id))
        students =Student.objects.filter(squad=squad)
        students_upd =students.filter(id__in= id_upd)
        # id всех студентов
        students_id = map(lambda x: x.id,students )
        # id студентов, информацию о которых надо обновить
        students_upd_id = map(lambda x: x.id, students_upd)
        del_students = set(students_id).difference(set(students_upd_id))
        for student_id in del_students:
            student = Student.objects.get(id=student_id)
            student.delete()
        for x in range(len(id)):
            # изменение уже сущетсвующих элементов
            if(id[x]!=''):
                student = Student.objects.get(id=id[x])
                student.name = name[x]
                student.surname = surname[x]
                student.patronymic = patronymic[x]
                student.save()
            else:
                student = Student()
                student.name = name[x]
                student.surname = surname[x]
                student.patronymic = patronymic[x]
                student.squad=squad
                student.save()

        disciplines = request.POST.getlist("discipline") # список названий дисциплин
        discipline_pk = request.POST.getlist("discipline_pk")[1:] # спискок их id
        Addres_pk = GroupDiscipline.objects.get(discipline= Discipline.objects.get(name="дополнительные обязанности"), squad=squad).pk # id дисциплны доп обяз
        # получение id существующих дисциплин, так как клиент для новых дисциплин возвращает пустую строку как id
        id_discp_upd = list(filter(lambda x: x != '' and x !=str(Addres_pk), discipline_pk))
        squadDiscipline = GroupDiscipline.objects.filter(squad=squad)
        squadDiscipline = GroupDiscipline.objects.exclude(discipline= Discipline.objects.get(name="дополнительные обязанности"))
        squad_dicp_upd = GroupDiscipline.objects.filter(id__in=id_discp_upd)
        # id всех дисциплин
        discipline_id = map(lambda x: x.id, squadDiscipline)
        # id дисциплин, информацию о которых надо обновить
        discipline_upd_id = map(lambda x: x.id, squad_dicp_upd)
        del_discipline = set(discipline_id).difference(set(discipline_upd_id))
        # удаление
        for disc_id in del_discipline:
            discipline = GroupDiscipline.objects.get(id=disc_id)
            discipline.delete()

        for x in range(len(discipline_pk)):
            # изменение уже сущетсвующих элементов
            if (discipline_pk[x] != '' and discipline_pk[x] != str(Addres_pk)):
                discipline = GroupDiscipline.objects.get(id=discipline_pk[x])
                discipline.squad = squad
                dirDiscp = Discipline.objects.get(name=disciplines[x])
                discipline.discipline =dirDiscp
                discipline.save()
            elif (discipline_pk[x] != str(Addres_pk)):
                discipline = GroupDiscipline()
                discipline.squad = squad
                dirDiscp = Discipline.objects.get(name=disciplines[x])
                discipline.discipline = dirDiscp
                discipline.save()

        return super().post(request, *args, **kwargs)

class SquadCreateView(generic.CreateView):
    template_name = "squadmodel_create.html"
    fields = ["number", "departament", "specialization"]
    model = StudentGroup

    def post(self, request, *args, **kwargs):
        squad = super().post(request, *args, **kwargs)

        return squad

class SquadDeleteView(generic.DeleteView):
    model = StudentGroup

    success_url = reverse_lazy('squads')
    def post(self, request, *args, **kwargs):
        squad = StudentGroup.objects.get(id=kwargs['pk'])
        students = Student.objects.filter(squad=squad)
        students.delete()
        return self.delete(request, *args, **kwargs)

class TeachersList(generic.ListView):
    model = Teacher

class TeacherCreateView(generic.CreateView):
    model = Teacher
    fields = ["surname", "name", "patronymic", "departament", "rank"]
    template_name = "teacher_create.html"

class TeacherEditView(generic.UpdateView):
    model = Teacher
    fields = ["surname", "name", "patronymic", "departament", "rank"]
    template_name = "teacher_update.html"

class TeacherDeleteView(generic.DeleteView):
    model = Teacher
    success_url = reverse_lazy('teachers')

class TeacherDetailView(generic.DetailView):
    model = Teacher


class DisciplinesList(generic.ListView):
    model = Discipline

class DisciplineCreateView(generic.CreateView):
    model = Discipline
    fields = ["name", "short_name", "departament", "teacher", "course", "hours", "type_exam"]
    template_name = "discipline_create.html"

class DisciplineEditView(generic.UpdateView):
    model = Discipline
    fields = ["name", "short_name", "departament", "teacher", "course", "hours", "type_exam"]
    template_name = "discipline_update.html"

class DisciplineDeleteView(generic.DeleteView):
    model = Discipline
    success_url = reverse_lazy('disciplines')

class DisciplineDetailView(generic.DetailView):
    model =  Discipline

