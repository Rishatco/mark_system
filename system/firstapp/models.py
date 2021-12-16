import django
from django.utils.timezone import timezone
from django.db import models

# Create your models here.
from django.urls import reverse

class StudentModel(models.Model):
    surname = models.CharField(max_length=80,verbose_name="фамилия")
    name = models.CharField(max_length=80, verbose_name='имя')
    patronymic = models.CharField(max_length=80, verbose_name='отчество')
    birthday = models.DateField(verbose_name='день рождения', default= django.utils.timezone.now())
    squad = models.ForeignKey(to="SquadModel", on_delete=models.CASCADE, verbose_name='номер взвода')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'surname', 'patronymic'], name='unique fio student')
        ]
        ordering = ["surname", "name", "patronymic"]

    def __str__(self):
        return self.surname+' '+self.name+' '+self.patronymic


# класс взвода
class SquadModel(models.Model):
    # номер взвода
    number = models.IntegerField(unique=True)
    # кафедра взвода
    departament = models.ForeignKey(to="DepartamentModel", on_delete=models.CASCADE)
    # направление подготовки
    specialization = models.CharField(max_length=200)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        return  reverse('squad-detail',args=[str(self.id)])
    def get_edit_url(self):
        return  reverse('squad-edit', args=[str(self.id)])

    def get_del_url(self):
        return  reverse('squad-delete', args=[str(self.id)])

class DepartamentModel(models.Model):
    # полное имя кафедры
    full_name = models.CharField(max_length=300, unique=True)
    # аббревиатура кафкдры
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return self.short_name

    class Meta:
        ordering =["full_name"]

class Teacher(models.Model):
    RANKS = [
        ('Ml', 'младший лейтенант'),
        ('L', 'лейтенант'),
        ('Sl', 'старший лейтенант'),
        ('C', 'капитан'),
        ('M', 'майор'),
        ('PP','подполковник'),
        ('P','полковник')
    ]

    name = models.CharField(max_length=20, verbose_name="Имя")
    surname = models.CharField(max_length=30, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=30, verbose_name="Отчество")

    departament = models.ForeignKey(to="DepartamentModel", on_delete=models.CASCADE, verbose_name="Кафедра")
    rank = models.CharField(max_length=2, choices=RANKS, verbose_name="Звание")

    def __str__(self):
        return  self.rank+' '+self.surname

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'surname', 'patronymic'], name='unique fio teacher')
        ]
        ordering = ["surname", "name", "patronymic"]

class Discipline(models.Model):

    TYPE_EXAM =[
        ('Z', 'зачёт'),
        ('O', 'зачёт с оценкой'),
        ('E', 'экзамен')
    ]

    name = models.CharField(max_length=400, verbose_name="Название")
    short_name = models.CharField(max_length=10, verbose_name="Аббревиатура")

    departament= models.ForeignKey(to="DepartamentModel", on_delete=models.CASCADE, verbose_name="Кафедра")

    teacher = models.ForeignKey(to="Teacher", on_delete=models.CASCADE, verbose_name="Преподаватель")

    course = models.IntegerField(verbose_name="Курс")

    hours = models.IntegerField(verbose_name="Количество часов")

    type_exam = models.CharField(max_length=1, choices=TYPE_EXAM, verbose_name="Тип экзамена")

    class Meta:
        ordering = ["name"]

class Mark(models.Model):

    student = models.ForeignKey(to="StudentModel", on_delete=models.CASCADE, verbose_name="Студент")

    discipline = models.ForeignKey(to="Discipline", on_delete=models.CASCADE, verbose_name="Дисциплина")

    date = models.DateField(verbose_name="Дата")

    class Meta:
        ordering =["date", "student"]
