<?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $name = $_POST['name'] ?? '';
        $grade = $_POST['grade'] ?? '';
        
        if (empty($name) || empty($grade)) {
            die("Error: Name and grade are required.");
        }

        $conn = new mysqli('localhost', 'root', 'Arush_09', 'student_management');
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        
        $stmt = $conn->prepare("INSERT INTO students (name, grade) VALUES (?,?)");
        $stmt->bind_param("si", $name, $grade);
        
        if ($stmt->execute()) {
            echo "Student record added successfully.";
        } else {
            echo "Error adding student: " . $stmt->error;
        }
        
        $stmt->close();
        $conn->close();
    }
?>