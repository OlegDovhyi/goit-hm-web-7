from sqlalchemy import Column, Integer, SmallInteger, String,Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_number = Column(SmallInteger, unique=True, nullable=False)


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship(Group, backref="students")


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    subject = relationship(Subject, backref= "teachers")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship(Student, backref='students')
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    subject = relationship(Subject, backref='students')
    date_of = Column(Date, nullable=False)
    grade = Column(Integer, nullable=False)
