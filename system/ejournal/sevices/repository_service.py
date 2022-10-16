from typing import Optional, Iterable, List
from django.db.models import QuerySet
from ..models import Student, StudentGroup, Mark, Discipline, GroupDiscipline, Departament,Teacher

def get_stundets_by_group(group: Group) -> QuerySet:
    return Student.objects.filter(group=group)

def create_group(number: int, specilization: str) -> None:
    group =StudentGroup.objets.create(number= number, specilization = specilization)
    group.save()

def create_student(surname: str, name: str, patronymic: str, group: StudentGroup, user: user) -> None:
    student = Student.objects.create(user= user, surname= surname, name= name, patronymic= patronymic, group= group)
    student.save()

def update_student_group_by_id(id:int, group: StudentGroup)-> None:
    student = get_student_by_id(id=id)
    student.group = group
    student.save()

def get_student_by_id(id: int)-> Optional[Student]:
    return  Student.objects.get(id=id)

def delete_student_by_id(id: int) -> None:
    get_student_by_id(id).delete()

def get_group_by_number(number: int) -> Optional[StudentGroup]:
    group = StudentGroup.objects.get(number= number);
    return group

def delete_group_by_number(number: int) -> None:
    get_group_by_number(number).delete()