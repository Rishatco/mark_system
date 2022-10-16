from django.test import TestCase
from .services.repository_service import *
# Create your tests here.

class TestEJournalRepositoryService(TestCase):


    def test_create_group(self):
        create_group(1, "про")
        group = StudentGroup.objects.get(number = 1)
        self.assertTrue(group.specialization == "про")


    def test_get_group_by_number(self):
        create_group(1,"про")
        group = StudentGroup.objects.get(number=1)
        group2 = get_group_by_number(1)
        self.assertEqual(group, group2)


    def test_delete_group_by_number(self):
        create_group(1, "про")
        delete_group_by_number(1)
        result = get_group_by_number(1)
        self.assertIsNone(result)


    def test_update_group_specialization_by_number(self):
        create_group(1, "про")
        update_group_specialization_by_number(1, "МО")
        group = get_group_by_number(1)
        self.assertEqual(group.specialization, "МО")


    def test_create_student(self):
        create_group(1, "sdf")
        group = get_group_by_number(1)
        create_student("ivanov", "ivan", "ivanovich", group)
        student = Student.objects.get(id = 1)
        self.assertEqual(student.name, "ivan")
        self.assertEqual(student.surname, "ivanov")
        self.assertEqual(student.patronymic, "ivanovich")
        self.assertEqual(student.group, group)


    def test_get_student_by_id(self):
        create_group(1, "sdf")
        group = get_group_by_number(1)
        create_student("ivanov", "ivan", "ivanovich", group)
        student = Student.objects.get(id = 1)
        student2 = get_student_by_id(1)
        self.assertEqual(student, student2)


    def test_update_student_group_by_id(self):
        create_group(1, "sdf")
        group = get_group_by_number(1)
        create_student("ivanov", "ivan", "ivanovich", group)
        create_group(2, "asd")
        group = get_group_by_number(2)
        update_student_group_by_id(1, group)
        student = get_student_by_id(1)
        self.assertEqual(student.group, group)

    def test_delete_student(self):
        create_group(1, "sdf")
        group = get_group_by_number(1)
        create_student("ivanov", "ivan", "ivanovich", group)
        delete_student_by_id(1)
        result = get_student_by_id(1)
        self.assertIsNone(result)

    def test_get_students_by_group(self):
        create_group(1, "sdf")
        group = get_group_by_number(1)
        create_student("1", "4", "7", group)
        create_student("2", "5", "8", group)
        create_student("3", "6", "9", group)
        students = get_students_by_group(group)
        for student in students:
            print(student)
            self.assertEqual(student.group, group)


    def test_create_teacher(self):
        create_teacher("1", "2", "3")
        teacher = Teacher.objects.get(id = 1)
        self.assertEqual(teacher.name, "2")
        self.assertEqual(teacher.surname, "1")
        self.assertEqual(teacher.patronymic, "3")

    def test_get_teacher_id_by_fio(self):
        create_teacher("1", "2", "3")
        id = get_teacher_id_by_fio("1", "2", "3")
        self.assertEqual(id, 1)

    def test_delete_teacher_by_id(self):
        create_teacher("1", "2", "3")
        delete_teacher_by_id(1)
        id = get_teacher_id_by_fio("1", "2", "3")
        self.assertEqual(id, -1)
