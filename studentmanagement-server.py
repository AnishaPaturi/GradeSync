import mysql.connector
from mysql.connector import Error
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import simplejson as json
import datetime

#log
def log(str1):
    current_date = datetime.date.today()
    current_time = datetime.datetime.now().time()
    with open("Log-server.txt","a") as f:
        f.write(f"{str1} at {current_time} on {current_date}\n")

# Database credentials
import os
host = os.environ.get("DB_HOST", "localhost")
user = os.environ.get("DB_USER", "root")
password = os.environ.get("DB_PASSWORD", "Arush_09")
database = os.environ.get("DB_NAME", "student_management")
db_port = int(os.environ.get("DB_PORT", 3306))

# Establish database connection
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=db_port
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            log("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None


# Define the request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        print(f"Query_params:{query_params}")

        # Serve static files
        if path in ["/", "/studentmanagement.html"]:
            try:
                with open("studentmanagement.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
            return
        elif path == "/studentmanagement.css":
            try:
                with open("studentmanagement.css", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
            return
        elif path == "/studentmanagement.js":
            try:
                with open("studentmanagement.js", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
            return

        connection = connect_to_db()
        log("Connection of server to database was sucessful.")
        if not connection:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Database connection failed'}).encode('utf-8'))
            log("Connection of server to database failed.")
            return
            
        cursor = connection.cursor()

        if path == "/display_students":
            try:
                student_id = query_params.get("id", [None])[0]
                print(student_id)
                
                if student_id:
                    student_indi_display = "SELECT * FROM students WHERE id=%s"
                    cursor.execute(student_indi_display,[student_id])
                else:
                    cursor.execute("SELECT * FROM students")
                students = cursor.fetchall()
                for stu in students:
                    print(stu)
                students_list = [{'id': stu[0], 'name': stu[1], 'grade': stu[2]} for stu in students]
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(students_list).encode('utf-8'))
            except Error as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

        elif path == "/class_average":
            try:
                cursor.execute("SELECT AVG(grade) FROM students")
                average_grade = cursor.fetchone()[0]
                if average_grade is None:
                    average_grade = 0
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'average_grade': float(average_grade)}).encode('utf-8'))
            except Error as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not Found'}).encode('utf-8'))

        cursor.close()
        connection.close()

    def do_POST(self):
        connection = connect_to_db()
        if not connection:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Database connection failed'}).encode('utf-8'))
            return

        cursor = connection.cursor()

        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/add_student":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_json_data = json.loads(post_data.decode('utf-8'))
            print(post_json_data)

            name = post_json_data["name"]
            grade = post_json_data["grade"]

            if name and grade:
                try:
                    insertStudentRecord = "INSERT INTO students(name, grade) VALUES (%s, %s)"
                    cursor.execute(insertStudentRecord, (name, int(grade)))
                    connection.commit()
                    self.send_response(201)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'message': 'Student record added successfully'}).encode('utf-8'))
                except Error as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid input'}).encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not Found'}).encode('utf-8'))

        cursor.close()
        connection.close()

# Set up and start the server
def run_server():
    host = '0.0.0.0'
    port = int(os.environ.get("PORT", 8080))
    # Create an instance of HTTPServer with our handler class
    server = HTTPServer((host, port), RequestHandler)
    print(f"Server started at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
