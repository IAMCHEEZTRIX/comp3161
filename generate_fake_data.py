from faker import Faker
import random

NUM_STUDENTS = 100000
NUM_LECTURERS = 60
NUM_COURSES = 200


    # studentID INT PRIMARY KEY NOT NULL,
    # userName VARCHAR(255),
    # s_fname VARCHAR(255) NOT NULL,
    # s_lname VARCHAR(255) NOT NULL,
    
    # INSERT INTO student (studentID, userName, s_fname, s_lname) VALUES (6200160000, "Damion_Henry", "Damion", "Henry")
    
faker = Faker()

department_prefixes = {
    "Biology": "BIO",
    "Chemistry": "CHEM",
    "Computer": "COMP",
    "Mathematics": "MATH",
    "Physics": "PHYS"
    # "English and Linguistics": "ENG",
    # "Art": "ART",
}
    # "ENG": ["Literary Criticism","Syntax and Semantics","Creative Writing","Language Acquisition","English Literature","Phonetics","Sociolinguistics","Discourse Analysis","World Literature","Historical Linguistics"],
    # "ART": ["Painting Techniques","Art History","Digital Illustration","Sculpture","Modern Art","Drawing Fundamentals","Graphic Design","Photography","Textile Arts","Printmaking"]

department_topics = {
    "BIO": [{"name": "Cell Structure", "code": "01"},{"name": "Genetics", "code": "02"},{"name": "Microbiology", "code": "03"},{"name": "Botany", "code": "04"},{"name": "Zoology", "code": "05"},{"name": "Ecology", "code": "06"},{"name": "Human Anatomy", "code": "07"},{"name": "Neuroscience", "code": "08"},{"name": "Evolutionary Biology", "code": "09"},{"name": "Immunology", "code": "10"}],
    "CHEM": [{"name": "Organic Chemistry", "code": "11"},{"name": "Inorganic Chemistry", "code": "12"},{"name": "Thermodynamics", "code": "13"},{"name": "Chemical Bonding", "code": "14"},{"name": "Analytical Chemistry", "code": "15"},{"name": "Biochemistry", "code": "16"},{"name": "Physical Chemistry", "code": "17"},{"name": "Environmental Chemistry", "code": "18"},{"name": "Polymer Chemistry", "code": "19"},{"name": "Quantum Chemistry", "code": "20"}],
    "COMP": [{"name": "Data Structures", "code": "21"},{"name": "Algorithms", "code": "22"},{"name": "Operating Systems", "code": "23"},{"name": "Databases", "code": "24"},{"name": "Computer Networks", "code": "25"},{"name": "Artificial Intelligence", "code": "26"},{"name": "Machine Learning", "code": "27"},{"name": "Software Engineering", "code": "28"},{"name": "Cybersecurity", "code": "29"},{"name": "Web Development", "code": "30"}],
    "MATH": [{"name": "Calculus", "code": "31"},{"name": "Linear Algebra", "code": "32"},{"name": "Probability", "code": "33"},{"name": "Statistics", "code": "34"},{"name": "Number Theory", "code": "35"},{"name": "Discrete Mathematics", "code": "36"},{"name": "Differential Equations", "code": "37"},{"name": "Topology", "code": "38"},{"name": "Complex Analysis", "code": "39"},{"name": "Real Analysis", "code": "40"}],
    "PHYS": [{"name": "Classical Mechanics", "code": "41"},{"name": "Quantum Physics", "code": "42"},{"name": "Electromagnetism", "code": "43"},{"name": "Thermodynamics", "code": "44"},{"name": "Nuclear Physics", "code": "45"},{"name": "Optics", "code": "46"},{"name": "Relativity", "code": "47"},{"name": "Astrophysics", "code": "48"},{"name": "Particle Physics", "code": "49"},{"name": "Fluid Mechanics", "code": "50"}]
}


course_prefixes = {
    "intro": ["Introduction to", "10"],
    "appl": ["Applications of", "22"],
    "adv": ["Advanced Topics in", "32"],
    "cap": ["Capstone in", "33"]   
}

def generate_course(dprefix, cprefix, ccode, topic, ctopic):
    return (f"{dprefix}{ccode}{ctopic}", f"{cprefix} {topic}")


def generate_sql():
    sql_statements = []
    
    #  Insert Students
    sql_statements.append("\n-- Insert Students")
    students = []
    for i in range(1, NUM_STUDENTS + 1):
        studentID = 6200160000 + i  
        first_name = faker.first_name().replace("'", "''")
        last_name = faker.last_name().replace("'", "''")
        user_name = f"{first_name}_{last_name}"
        students.append(studentID)
        sql_statements.append(f"INSERT INTO student (studentID, userName, s_fname, s_lname) VALUES ({studentID}, {user_name}, {first_name}, {last_name})")
    
    
        
    #  Insert Lecturers
    sql_statements.append("\n-- Insert Lecturers")
    lecturers = []
    for i in range(1, NUM_LECTURERS + 1):
        lectureID = 100010000 + i
        lec_first_name = faker.first_name().replace("'", "''")
        lec_last_name = faker.last_name().replace("'", "''")
        lec_user_name = f"{lec_first_name}_{lec_last_name}"
        lecturers.append(lectureID)
        sql_statements.append(f"INSERT INTO lecturer (lectureID, userName, lec_fname, lec_lname) VALUES ({lectureID}, {lec_user_name}, {lec_first_name}, {lec_last_name})")
        
        
    
        
    
    #  Insert Courses
    sql_statements.append("\n-- Insert Courses")
    courses = []

    # Store unique course codes
    courses = []
    for i in range(1, NUM_COURSES + 1):
        for dcode in department_prefixes.values():
            topics = department_topics[dcode]
            for topic in topics:
                for courseNamePrefixes, courseCode in course_prefixes.values():
                    courses.append(generate_course(dcode, courseNamePrefixes, courseCode, topic['name'],topic['code']))
              
                
    # Assign Lecturer to courses
    sql_statements.append("\n-- Assign Lecturer to courses")
    j = 0    
    for i in range(200):
        # 20 lecturers teach 5 courses, total courses 100
        if i < 100:
            if i == 0:
                sql_statements.append("\n-- 20 lecturers each teaches 5 courses")
                     
            sql_statements.append(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ({courses[i][0]}, {courses[i][1]}, {lecturers[j]})")
            print(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ({courses[i][0]}, {courses[i][1]}, {lecturers[j]})")
            
            # Move to the next Lecture if five course is assign to the current lecture
            if (i+1)%5 == 0:
                j = j+1
        
        # 10 lecturers teach 4 courses, total courses 140
        if 100 <= i < 140:
            if i == 100:
                sql_statements.append("\n-- 10 lecturers each teaches 4 courses")
            
            sql_statements.append(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ({courses[i][0]}, {courses[i][1]}, {lecturers[j]})")
            print(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ({courses[i][0]}, {courses[i][1]}, {lecturers[j]})")
            
            # Move to the next Lecture if five course is assign to the current lecture
            if (i+1)%4 == 0:
                j = j+1
        
        # 10 lecturers teach 3 courses, total courses 170
        if 140 <= i < 170:
            if i == 140:
                sql_statements.append("\n-- 10 lecturers each teaches 3 courses")
            
            sql_statements.append(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ({courses[i][0]}, {courses[i][1]}, {lecturers[j]})")
            print(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ({courses[i][0]}, {courses[i][1]}, {lecturers[j]})")
            
            # Move to the next Lecture if five course is assign to the current lecture
            # if i in [143, 146, 149, 152, 155, 158, 161, 164, 167]:
            if ((i+1) - 140) % 3 == 0:
                j = j+1
        
        # 10 lecturers teach 2 courses, total courses 190
        if 170 <= i < 190:
            if i == 170:
                sql_statements.append("\n-- 10 lecturers each teaches 2 courses")
                
            sql_statements.append(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ({courses[i][0]}, {courses[i][1]}, {lecturers[j]})")
            print(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ({courses[i][0]}, {courses[i][1]}, {lecturers[j]})")
            
            # Move to the next Lecture if five course is assign to the current lecture
            if ((i+1) - 170) % 2 == 0:
                j = j+1
        
        # 10 lecturers teach 1 courses, total courses 200
        if (i+1) > 190:
            if i == 190:
                sql_statements.append("\n-- 10 lecturers each teaches 1 course")
                
            sql_statements.append(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ({courses[i][0]}, {courses[i][1]}, {lecturers[j]})")
            print(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ({courses[i][0]}, {courses[i][1]}, {lecturers[j]})")
            
            # Move to the next Lecture if five course is assign to the current lecture
            j = j+1
            
            
            
            
    # CREATE TABLE registers (
    #     studentID INT KEY NOT NULL,
    #     courseID VARCHAR(15) NOT NULL,
    #     academic_year YEAR NOT NULL,
    #     academic_term VARCHAR(10),
    #     final_avg DECIMAL(5,2)

    # );
    
    # Register students to courses
    
       
generate_sql()

    
    