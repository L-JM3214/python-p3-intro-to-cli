#!/usr/bin/env python3

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///my_database.db')
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    grades = relationship('Grade', back_populates='student')

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    grades = relationship('Grade', back_populates='course')

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    grade = Column(String, nullable=False)
    student = relationship('Student', back_populates='grades')
    course = relationship('Course', back_populates='grades')

Base.metadata.create_all(engine)

def add_student(session, name):
    student = Student(name=name)
    session.add(student)
    session.commit()
    print(f"Student '{name}' added successfully!")

def add_course(session, name):
    course = Course(name=name)
    session.add(course)
    session.commit()
    print(f"Course '{name}' added successfully!")

def add_grade(session, student_name, course_name, grade):
    student = session.query(Student).filter_by(name=student_name).first()
    course = session.query(Course).filter_by(name=course_name).first()
    if student and course:
        new_grade = Grade(student=student, course=course, grade=grade)
        session.add(new_grade)
        session.commit()
        print(f"Grade '{grade}' added for {student_name} in {course_name} successfully!")
    else:
        print("Student or course not found. Please check the names.")

def main():
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("1. Add Student")
        print("2. Add Course")
        print("3. Add Grade")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter student name: ")
            add_student(session, name)
        elif choice == "2":
            name = input("Enter course name: ")
            add_course(session, name)
        elif choice == "3":
            student_name = input("Enter student name: ")
            course_name = input("Enter course name: ")
            grade = input("Enter grade: ")
            add_grade(session, student_name, course_name, grade)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

    session.close()

if __name__ == '__main__':
    main()