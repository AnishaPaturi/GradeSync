DROP DATABASE student_management;
CREATE DATABASE student_management;
USE student_management;
CREATE TABLE students(
	id INT NOT NULL auto_increment,
	 name VARCHAR (50),
     grade INT,
     primary key(id)
     );

INSERT INTO students(name,grade)
VALUES
("BBB",91),
("CCC",92),
("DDD",93)
;

SELECT * FROM students;


