"""Student Grade Management

1. Add Student
2. Display All Students
3. Calculate Class Average Grade
4. Exit

Enter your choice: 1

Enter student name: Alice
Enter student grade: 85

Student record added successfully.

Enter your choice: 2

List of All Students:
1. Alice - Grade: 85

Enter your choice: 3

Class Average Grade: 85.0

Enter your choice: 4

Exiting program..."""

import json
import os

FILE_NAME = 'students.json'

class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def to_dict(self):
        return {'name': self.name, 'grade': self.grade}

def add_student(students, name, grade):
    students.append(Student(name, grade))
    save_students(students)
    print("Student record added successfully.")

def display_all_students(students):
    if not students:
        print("No student records found.")
    else:
        for i, student in enumerate(students, 1):
            print(f"{i}. {student.name} - Grade: {student.grade}")

def calculate_class_average_grade(students):
    if not students:
        return 0
    total_grade = sum(student.grade for student in students)
    avg_grade = total_grade / len(students)
    return avg_grade

def load_students():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as file:
            students_data = json.load(file)
            return [Student(**data) for data in students_data]
    return []

def save_students(students):
    with open(FILE_NAME, 'w') as file:
        students_data = [student.to_dict() for student in students]
        json.dump(students_data, file, indent=4)

def main():
    students = load_students()
    while True:
        print("\nStudent Grade Management")
        print("1. Add Student")
        print("2. Display All Students")
        print("3. Calculate Class Average Grade")
        print("4. Exit")
        print("Enter your choice:")
        choice = int(input())
        if choice == 1:
            print("Enter student name:")
            name = input("")
            print("Enter student grade:")
            grade = int(input(""))
            add_student(students, name, grade)
        elif choice == 2:
            display_all_students(students)
        elif choice == 3:
            avg_grade = calculate_class_average_grade(students)
            print(f"Class Average Grade: {avg_grade:.2f}")
        elif choice == 4:
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
