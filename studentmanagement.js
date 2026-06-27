const displayStudentsBtn = document.getElementById('display-students-btn');
const classAverageBtn = document.getElementById('class-average-btn');
const addStudentBtn = document.getElementById('add-student-btn');
const studentsList = document.getElementById('students-list');
const classAverageResult = document.getElementById('class-average-result');
const addStudentResult = document.getElementById('add-student-result');

displayStudentsBtn.addEventListener('click', async () => {
  try {
    const response = await fetch('/display_students');
    const students = await response.json();
    studentsList.innerHTML = '';
    students.forEach((student) => {
      const listItem = document.createElement('li');
      listItem.innerHTML = `<span class="student-name">${student.name}</span><span class="student-grade">${student.grade}</span>`;
      studentsList.appendChild(listItem);
    });
  } catch (error) {
    console.error(error);
  }
});

classAverageBtn.addEventListener('click', async () => {
  try {
    const response = await fetch('/class_average');
    const averageGrade = await response.json();
    classAverageResult.textContent = `Class Average: ${averageGrade.average_grade}`;
  } catch (error) {
    console.error(error);
  }
});

addStudentBtn.addEventListener('click', async (event) => {
  event.preventDefault();
  try {
    const name = document.getElementById('name').value.trim();
    const grade = document.getElementById('grade').value.trim();
    
    if (!name || !grade) {
      addStudentResult.textContent = "Error: Name and grade cannot be empty.";
      addStudentResult.className = "error-text";
      return;
    }
    
    const response = await fetch('/add_student', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name: name, grade: parseInt(grade, 10) })
    });
    
    const result = await response.json();
    if (response.ok) {
      addStudentResult.textContent = result.message || "Student added successfully.";
      addStudentResult.className = "success-text";
      document.getElementById('add-student-form').reset();
    } else {
      addStudentResult.textContent = `Error: ${result.error || 'Failed to add student'}`;
      addStudentResult.className = "error-text";
    }
  } catch (error) {
    console.error(error);
    addStudentResult.textContent = "Error: Failed to connect to server.";
    addStudentResult.className = "error-text";
  }
});
