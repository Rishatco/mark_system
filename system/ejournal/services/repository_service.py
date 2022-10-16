from typing import Optional

from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist

from ..models import Student, StudentGroup, Teacher


def get_students_by_group(group: StudentGroup) -> QuerySet:
    return Student.objects.filter(group=group)


def create_group(number: int, specialization: str) -> None:
    group = StudentGroup.objects.create(number=number, specialization=specialization)
    group.save()


def create_student(surname: str, name: str, patronymic: str, group: StudentGroup) -> None:
    student = Student.objects.create(surname=surname, name=name, patronymic=patronymic, group=group)
    student.save()


def update_student_group_by_id(id: int, group: StudentGroup) -> None:
    student = get_student_by_id(id=id)
    student.group = group
    student.save()


def get_student_by_id(id: int) -> Optional[Student]:
    try:
        return Student.objects.get(id=id)
    except ObjectDoesNotExist:
        return None

def delete_student_by_id(id: int) -> None:
    get_student_by_id(id).delete()


def get_group_by_number(number: int) -> Optional[StudentGroup]:
    try:
        group = StudentGroup.objects.get(number=number);
    except ObjectDoesNotExist:
        return  None
    return group


def delete_group_by_number(number: int) -> None:
    get_group_by_number(number).delete()


def create_teacher(surname: str, name: str, patronymic: str) -> None:
    teacher = Teacher.objects.create(surname=surname, name=name, patronymic=patronymic)
    teacher.save()


def get_teacher_id_by_fio(surname: str, name: str, patronymic: str) -> int:
    try:
        teacher = Teacher.objects.get(surname=surname, name=name, patronymic=patronymic)
    except ObjectDoesNotExist:
        return -1;
    return teacher.id


def delete_teacher_by_id(id: id) -> None:
    Teacher.objects.get(id = id).delete()

def update_group_specialization_by_number(number: int, new_specialization: str) -> None:
    group = get_group_by_number(number)
    if (group == None):
        return
    group.specialization = new_specialization
    group.save()
