from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from models import Base, Group, Subject, Student, Teacher, Grade
from random import randint, sample
from datetime import datetime, timedelta

engine = create_engine('sqlite:///home.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

# Додавання груп
for _ in range(3):
    group = Group(group_number=fake.random_int(min=1, max=100))
    session.add(group)

# Випадковий вибір кількості предметів (від 5 до 8)
num_subjects = fake.random_int(min=5, max=8)
subjects = sample(['Math', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'English', 'Computer Science'], num_subjects)

# Додавання предметів
for subject_name in subjects:
    subject = Subject(name=subject_name)
    session.add(subject)

# Додавання студентів (від 30 до 50)
for _ in range(fake.random_int(min=30, max=50)):
    student_name = fake.name()
    group_id = fake.random_int(min=1, max=3)
    student = Student(name=student_name, group_id=group_id)
    session.add(student)

# Додавання викладачів (від 3 до 5)
num_teachers = fake.random_int(min=3, max=5)
for _ in range(num_teachers):
    teacher_name = fake.name()
    subject_id = fake.random_int(min=1, max=num_subjects)  # случайный выбор предмета
    teacher = Teacher(name=teacher_name, subject_id=subject_id)
    session.add(teacher)

# Додавання оцінок
for student in session.query(Student).all():
    for subject in session.query(Subject).all():
        num_grades = fake.random_int(min=1, max=20)  # Випадковий вибір кількості оцінок (від 1 до 20)
        for _ in range(num_grades):
            date_of = fake.date_between(start_date='-1y', end_date='today')
            grade = fake.random_int(min=1, max=10)
            grade_entry = Grade(student=student, subject=subject, date_of=date_of, grade=grade)
            session.add(grade_entry)

session.commit()
