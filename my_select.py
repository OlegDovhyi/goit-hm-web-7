from sqlalchemy import func
from models import Group, Subject, Student, Teacher, Grade
from connect_db import session

def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів
    top_students = (
        session.query(Student.name, func.avg(Grade.grade).label('average_grade'))
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    return top_students

def select_2(subject_name):
    # Знайти студента із найвищим середнім балом з певного предмета
    top_student = (
        session.query(Student.name, func.avg(Grade.grade).label('average_grade'))
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(1)
        .first()
    )
    return top_student

def select_3(subject_name):
    # Знайти середній бал у групах з певного предмета
    avg_group_scores = (
        session.query(Group.group_number, func.avg(Grade.grade).label('average_grade'))
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.group_number)
        .order_by(func.avg(Grade.grade).desc())
        .all()
    )
    return avg_group_scores

def select_4():
    # Знайти середній бал на потоці (по всій таблиці оцінок)
    average_score = (
        session.query(func.round(func.avg(Grade.grade), 2))
        .scalar()
    )
    return average_score

def select_5(teacher_name):
    # Знайти курси, які читає певний викладач
    courses_taught = (
        session.query(Subject.name)
        .join(Teacher, Subject.id == Teacher.subject_id)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    return [course[0] for course in courses_taught]

def select_6(group_number):
    # Знайти список студентів у певній групі
    students_in_group = (
        session.query(Student.name)
        .join(Group, Student.group_id == Group.id)
        .filter(Group.group_number == group_number)
        .all()
    )
    return [student[0] for student in students_in_group]

def select_7(subject_name, group_number):
    # Знайти оцінки студентів у окремій групі з певного предмета
    student_grades = (
        session.query(Student.name, Grade.date_of, Grade.grade)
        .join(Group, Student.group_id == Group.id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .filter(Group.group_number == group_number)
        .all()
    )
    return student_grades

def select_8(teacher_name):
    # Знайти середній бал, який ставить певний викладач зі своїх предметів
    teacher_average_scores = (
        session.query(Subject.name, func.round(func.avg(Grade.grade), 2))
        .join(Teacher, Subject.id == Teacher.subject_id)
        .join(Grade, Subject.id == Grade.subject_id)
        .filter(Teacher.name == teacher_name)
        .group_by(Subject.name)
        .all()
    )
    return teacher_average_scores

def select_9(student_name):
    # Знайти список курсів, які відвідує певний студент
    student_courses = (
        session.query(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .filter(Student.name == student_name)
        .distinct()  # Видаляємо дублікати
        .all()
    )
    return [course[0] for course in student_courses]


def select_10(student_name, teacher_name):
    # Знайти список курсів, які певний студент відвідує з певним викладачем
    student_teacher_courses = (
        session.query(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .join(Student, Grade.student_id == Student.id)
        .join(Teacher, Subject.id == Teacher.subject_id)
        .filter(Student.name == student_name)
        .filter(Teacher.name == teacher_name)
        .distinct()  
        .all()
    )
    return [course[0] for course in student_teacher_courses]

if __name__ == "__main__":
    # print("Запит 1:")
    # print(select_1())

    # subject_name = "Math"
    # print(f"Запит 2 (Предмет: {subject_name}):")
    # print(select_2(subject_name))

    # subject_name = "Physics"
    # print(f"Запит 3 (Предмет: {subject_name}):")
    # print(select_3(subject_name))

    # print("Запит 4:")
    # print(select_4())

    # teacher_name = "David Taylor"
    # print(f"Запит 5 (Викладач: {teacher_name}):")
    # print(select_5(teacher_name))

    # group_number = 4  # Приклад номеру групи
    # print(f"Запит 6 (Група: {group_number}):")
    # print(select_6(group_number))

    # subject_name = "Computer Science"
    # group_number = 54
    # print(f"Запит 7 (Предмет: {subject_name}, Група: {group_number}):")
    # print(select_7(subject_name, group_number))

    # teacher_name = "Daniel Hoover"
    # print(f"Запит 8 (Викладач: {teacher_name}):")
    # print(select_8(teacher_name))

    student_name = "Sarah Clark"
    print(f"Запит 9 (Студент: {student_name}):")
    print(select_9(student_name))

    teacher_name = "Jessica Johnson"
    student_name = "Julie Ruiz"
    print(f"Запит 10 (Студент: {student_name}, Викладач: {teacher_name}):")
    print(select_10(student_name, teacher_name))
