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

import os
while True:
    print("Student Grade Management\n")
    print("1. Add Student\n2. Display All Students\n3. Calculate Class Average Grade\n4. Exit\n")
    print("Enter your choice")
    choice = int(input())
    if choice == 1:
        name = input("Enter the name of the student: ")
        grade = int(input("Enter the grade of the students: "))
        with open("studentmanagement.txt","a") as f:
            f.write(f"{name}:{grade}\n")
        print("Student record added successfully.")
        
    elif choice == 2:
        print("\nHere is a list of the students:\n")
        with open("studentmanagement.txt","r") as f:
            for row in f:
                print(row)
                
    elif choice == 3:
        total_grades = 0
        count = 0
        with open("studentmanagement.txt", 'r') as file:
            for line in file:
                name, grade = line.strip().split(":")
                total_grades += int(grade)
                count += 1
        average_grade = total_grades / count
        print(f"The class average grade is: {average_grade:.2f}")

        
            
    elif choice == 4:
        exit()
        
    else:
        print("Invalid choice")
    
    
