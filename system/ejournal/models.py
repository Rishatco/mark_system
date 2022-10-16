from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.urls import reverse


# модель Студент
class Student(models.Model):
    # surname - фамилия
    surname = models.CharField(max_length=80, verbose_name="фамилия")
    # name - имя
    name = models.CharField(max_length=80, verbose_name='имя')
    # patronymic - отчество
    patronymic = models.CharField(max_length=80, verbose_name='отчество')
    # group - учебная группа
    group = models.ForeignKey(to="StudentGroup", on_delete=models.CASCADE, verbose_name='учебная группа')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'surname', 'patronymic'], name='unique fio student')
        ]
        ordering = ["surname", "name", "patronymic"]
        db_table = "student"

    def __str__(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic


# модель учебной группы
class StudentGroup(models.Model):
    # номер группы
    number = models.IntegerField(unique=True)
    # специлизация
    specialization = models.CharField(max_length=200)

    class Meta:
        ordering = ['number']
        db_table = "studentGroup"

    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        return reverse('group-detail', args=[str(self.id)])

    def get_edit_url(self):
        return reverse('group-edit', args=[str(self.id)])

    def get_del_url(self):
        return reverse('group-delete', args=[str(self.id)])

    def get_rating_url(self):
        return reverse('rating', args=[str(self.id)])

    def get_study_rating_url(self):
        return reverse('group-study-rating', args=[str(self.id)])

    def get_visiting_rating_url(self):
        return reverse('group-visiting-rating', args=[str(self.id)])

    def get_add_res_rating_url(self):
        return reverse('group-add-res-rating', args=[str(self.id)])

    def get_total_rating(self):
        return reverse('group-total-rating', args=[str(self.id)])



# модель преподавателя
class Teacher(models.Model):
    # имя
    name = models.CharField(max_length=20, verbose_name="Имя")
    # фамилия
    surname = models.CharField(max_length=30, verbose_name="Фамилия")
    # отчество
    patronymic = models.CharField(max_length=30, verbose_name="Отчество")

    def __str__(self):
        return self.surname+" "+self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'surname', 'patronymic'], name='unique fio teacher')
        ]
        ordering = ["surname", "name", "patronymic"]
        db_table = "teacher"

    def get_absolute_url(self):
        return reverse('teacher-detail', args=[str(self.id)])

    def get_edit_url(self):
        return reverse('teacher-edit', args=[str(self.id)])

    def get_del_url(self):
        return reverse('teacher-delete', args=[str(self.id)])


# модель Дисциплина
class Discipline(models.Model):
    TYPE_EXAM = [
        ('N', ''),
        ('Z', 'зачёт'),
        ('O', 'зачёт с оценкой'),
        ('E', 'экзамен')
    ]

    name = models.CharField(max_length=400, verbose_name="Название", unique=True)
    short_name = models.CharField(max_length=10, verbose_name="Аббревиатура", blank=True)
    teacher = models.ForeignKey(to="Teacher", on_delete=models.CASCADE, verbose_name="Преподаватель", blank=True,
                                null=True)
    course = models.IntegerField(verbose_name="Курс", blank=True, null=True)
    hours = models.IntegerField(verbose_name="Количество часов", blank=True, null=True)

    type_exam = models.CharField(max_length=1, choices=TYPE_EXAM, verbose_name="Тип экзамена")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique name discipline')
        ]
        ordering = ["name"]
        db_table = "discipline"

    def get_absolute_url(self):
        return reverse('discipline-detail', args=[str(self.id)])

    def get_edit_url(self):
        return reverse('discipline-edit', args=[str(self.id)])

    def get_del_url(self):
        return reverse('discipline-delete', args=[str(self.id)])


# модель оценки
class Mark(models.Model):
    student = models.ForeignKey(to="Student", on_delete=models.CASCADE, verbose_name="Студент")

    discipline = models.ForeignKey(to="GroupDiscipline", on_delete=models.CASCADE, verbose_name="Дисциплина")

    date = models.DateField(verbose_name="Дата")

    ball = models.IntegerField()

    class Meta:
        ordering = ["date", "student"]
        db_table = "mark"


# модель дисциплины группы
class GroupDiscipline(models.Model):
    group = models.ForeignKey(to="StudentGroup", on_delete=models.CASCADE, verbose_name="Взвод")
    discipline = models.ForeignKey(to="Discipline", on_delete=models.CASCADE, verbose_name="Дисциплина")

    class Meta:
        db_table = "groupDiscipline"
